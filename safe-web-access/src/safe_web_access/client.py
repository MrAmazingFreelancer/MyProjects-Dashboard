"""
This module provides the main SafeWebClient for safe asynchronous web access.
It coordinates URL checks, policies, network safety, robots, and retries.
Its main public class is SafeWebClient with asynchronous fetch operations.
It works with transport, response_reader, budgets, events, and policies.
It returns structured results instead of exposing raw request exceptions.
It does not parse HTML, PDF content, companies, emails, or business data.
"""

import asyncio
import inspect
import time
from types import TracebackType
from typing import Awaitable, Callable

import httpx

from .budgets import CrawlBudget
from .errors import SafeWebErrorCode
from .events import EventHook, SafeWebEvent, SafeWebEventType
from .exceptions import SafeWebError
from .networks import resolve_public_addresses
from .response_reader import read_response_body
from .result_builders import (
    make_failure_from_exception,
    make_failure_result,
    make_success_result,
)
from .results import SafeWebResult
from .robots_fetcher import fetch_robots_advisory
from .settings import SafeWebSettings
from .transport import stream_safe_page
from .urls import validate_and_normalize_url


def _elapsed_ms(start_time: float) -> int:
    """Calculates elapsed milliseconds since start_time."""
    return max(0, int((time.perf_counter() - start_time) * 1000))


def _map_http_status(status_code: int) -> SafeWebErrorCode:
    """Maps non-success HTTP status codes to standard SafeWebErrorCode members."""
    if status_code == 408:
        return SafeWebErrorCode.READ_TIMEOUT
    if status_code == 413:
        return SafeWebErrorCode.RESPONSE_TOO_LARGE
    return SafeWebErrorCode.HTTP_ERROR


class SafeWebClient:
    """Asynchronous HTTP client that orchestrates SSRF safety, budgets, policies, and retries."""

    def __init__(
        self,
        settings: SafeWebSettings | None = None,
        client: httpx.AsyncClient | None = None,
        event_hooks: tuple[EventHook, ...] | list[EventHook] | None = None,
        sleeper: Callable[[float], Awaitable[None]] | None = None,
    ) -> None:
        """Initializes SafeWebClient with configuration settings, optional client, and event hooks."""
        self._settings = settings if settings is not None else SafeWebSettings()
        self._owned_client = client is None
        self._closed = False
        self._event_hooks = tuple(event_hooks) if event_hooks else ()
        self._sleeper = sleeper or asyncio.sleep

        self._timeout = httpx.Timeout(
            connect=self._settings.connect_timeout_seconds,
            read=self._settings.read_timeout_seconds,
            write=self._settings.read_timeout_seconds,
            pool=self._settings.connect_timeout_seconds,
        )

        if client is not None:
            self._client = client
        else:
            headers = {
                "User-Agent": self._settings.user_agent,
                "Accept": "text/html,text/plain,application/xhtml+xml,application/pdf",
            }
            self._client = httpx.AsyncClient(
                follow_redirects=False,
                timeout=self._timeout,
                headers=headers,
            )

    async def _emit_event(self, event: SafeWebEvent) -> None:
        """Executes registered event hooks sequentially with error isolation."""
        for hook in self._event_hooks:
            try:
                if inspect.iscoroutinefunction(hook) or asyncio.iscoroutinefunction(
                    hook
                ):
                    await hook(event)
                else:
                    res = hook(event)
                    if inspect.isawaitable(res):
                        await res
            except Exception as exc:
                if self._settings.strict_event_hooks:
                    raise SafeWebError(
                        f"Event hook failed: {exc}",
                        SafeWebErrorCode.REQUEST_FAILED,
                    ) from exc

    async def start(self) -> "SafeWebClient":
        """Prepares the client for use and returns it, for callers not using ``async with``.

        The constructor already builds everything needed, so this performs no setup
        work. It exists so that a caller managing the lifecycle by hand can write
        ``client = await SafeWebClient().start()`` and later ``await client.close()``,
        mirroring the context-manager form. Calling it more than once is safe.
        """
        if self._closed:
            raise RuntimeError("Client is already closed.")
        return self

    async def __aenter__(self) -> "SafeWebClient":
        """Enters the async context manager after verifying the client is open."""
        if self._closed:
            raise RuntimeError("Client is already closed.")
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exits the async context manager and closes internally owned resources."""
        await self.aclose()

    async def aclose(self) -> None:
        """Closes internally created HTTP client resources idempotently."""
        if self._closed:
            return
        self._closed = True
        await self._emit_event(
            SafeWebEvent(
                event_type=SafeWebEventType.CLIENT_CLOSED,
                requested_url="client://closed",
                message="Client closed.",
            )
        )
        if self._owned_client:
            await self._client.aclose()

    async def close(self) -> None:
        """Closes the client. Awaitable alias of :meth:`aclose`, idempotent like it.

        ``aclose`` follows the async naming convention; ``close`` is provided so the
        manual lifecycle reads as ``start()`` / ``close()``. Both do the same thing,
        and neither closes an ``httpx.AsyncClient`` that was supplied by the caller.
        """
        await self.aclose()

    async def fetch(
        self,
        url: str,
        *,
        budget: CrawlBudget | None = None,
        check_robots: bool = True,
    ) -> SafeWebResult:
        """Safely fetches a webpage while enforcing policies, retries, and budgets."""
        if self._closed:
            req_url = url if isinstance(url, str) and url.strip() else "invalid_url"
            fail_res = make_failure_result(
                requested_url=req_url,
                error_code=SafeWebErrorCode.REQUEST_FAILED,
                error_message="Client is closed.",
            )
            await self._emit_event(
                SafeWebEvent(
                    event_type=SafeWebEventType.REQUEST_FAILED,
                    requested_url=req_url,
                    error_code=SafeWebErrorCode.REQUEST_FAILED.value,
                    message="Client is closed.",
                )
            )
            return fail_res

        start_time = time.perf_counter()
        req_url = url if isinstance(url, str) and url.strip() else "invalid_url"

        await self._emit_event(
            SafeWebEvent(
                event_type=SafeWebEventType.REQUEST_STARTED,
                requested_url=req_url,
            )
        )

        retry_pol = self._settings.retry_policy
        max_attempts = retry_pol.max_attempts
        robots_status_val: str | None = None

        for attempt in range(1, max_attempts + 1):
            await self._emit_event(
                SafeWebEvent(
                    event_type=SafeWebEventType.ATTEMPT_STARTED,
                    requested_url=req_url,
                    attempt_number=attempt,
                    elapsed_ms=_elapsed_ms(start_time),
                )
            )

            # validate and normalize input url
            try:
                validated = validate_and_normalize_url(url)
                await self._emit_event(
                    SafeWebEvent(
                        event_type=SafeWebEventType.URL_VALIDATED,
                        requested_url=req_url,
                        current_url=validated.normalized,
                        attempt_number=attempt,
                        elapsed_ms=_elapsed_ms(start_time),
                    )
                )
            except SafeWebError as exc:
                res = make_failure_from_exception(
                    exc,
                    requested_url=req_url,
                    elapsed_ms=_elapsed_ms(start_time),
                    attempt_count=attempt,
                )
                await self._emit_event(
                    SafeWebEvent(
                        event_type=SafeWebEventType.REQUEST_FAILED,
                        requested_url=req_url,
                        attempt_number=attempt,
                        elapsed_ms=_elapsed_ms(start_time),
                        error_code=exc.error_code.value,
                        message=exc.message,
                    )
                )
                return res

            # evaluate domain and port policies
            try:
                self._settings.domain_policy.evaluate_url(validated)
                await self._emit_event(
                    SafeWebEvent(
                        event_type=SafeWebEventType.POLICY_VALIDATED,
                        requested_url=validated.original,
                        current_url=validated.normalized,
                        attempt_number=attempt,
                        elapsed_ms=_elapsed_ms(start_time),
                    )
                )
            except SafeWebError as exc:
                res = make_failure_from_exception(
                    exc,
                    requested_url=validated.original,
                    elapsed_ms=_elapsed_ms(start_time),
                    attempt_count=attempt,
                )
                await self._emit_event(
                    SafeWebEvent(
                        event_type=SafeWebEventType.REQUEST_FAILED,
                        requested_url=validated.original,
                        current_url=validated.normalized,
                        attempt_number=attempt,
                        elapsed_ms=_elapsed_ms(start_time),
                        error_code=exc.error_code.value,
                        message=exc.message,
                    )
                )
                return res

            # validate network destination ip addresses (ssrf prevention)
            try:
                resolve_public_addresses(validated.hostname)
                await self._emit_event(
                    SafeWebEvent(
                        event_type=SafeWebEventType.NETWORK_VALIDATED,
                        requested_url=validated.original,
                        current_url=validated.normalized,
                        attempt_number=attempt,
                        elapsed_ms=_elapsed_ms(start_time),
                    )
                )
            except SafeWebError as exc:
                res = make_failure_from_exception(
                    exc,
                    requested_url=validated.original,
                    elapsed_ms=_elapsed_ms(start_time),
                    attempt_count=attempt,
                )
                await self._emit_event(
                    SafeWebEvent(
                        event_type=SafeWebEventType.REQUEST_FAILED,
                        requested_url=validated.original,
                        current_url=validated.normalized,
                        attempt_number=attempt,
                        elapsed_ms=_elapsed_ms(start_time),
                        error_code=exc.error_code.value,
                        message=exc.message,
                    )
                )
                return res

            # initialize or verify active crawl budget
            active_budget = budget
            if active_budget is None:
                try:
                    active_budget = CrawlBudget(
                        max_pages=self._settings.max_pages,
                        max_total_bytes=self._settings.max_total_bytes,
                    )
                except (TypeError, ValueError) as exc:
                    res = make_failure_result(
                        requested_url=validated.original,
                        final_url=validated.normalized,
                        elapsed_ms=_elapsed_ms(start_time),
                        attempt_count=attempt,
                        error_code=SafeWebErrorCode.REQUEST_FAILED,
                        error_message=str(exc),
                    )
                    await self._emit_event(
                        SafeWebEvent(
                            event_type=SafeWebEventType.REQUEST_FAILED,
                            requested_url=validated.original,
                            current_url=validated.normalized,
                            attempt_number=attempt,
                            elapsed_ms=_elapsed_ms(start_time),
                            error_code=SafeWebErrorCode.REQUEST_FAILED.value,
                            message=str(exc),
                        )
                    )
                    return res

            try:
                active_budget.ensure_request_allowed()
                await self._emit_event(
                    SafeWebEvent(
                        event_type=SafeWebEventType.BUDGET_VALIDATED,
                        requested_url=validated.original,
                        current_url=validated.normalized,
                        attempt_number=attempt,
                        elapsed_ms=_elapsed_ms(start_time),
                    )
                )
            except SafeWebError as exc:
                res = make_failure_from_exception(
                    exc,
                    requested_url=validated.original,
                    elapsed_ms=_elapsed_ms(start_time),
                    attempt_count=attempt,
                    budget=active_budget,
                )
                await self._emit_event(
                    SafeWebEvent(
                        event_type=SafeWebEventType.REQUEST_FAILED,
                        requested_url=validated.original,
                        current_url=validated.normalized,
                        attempt_number=attempt,
                        elapsed_ms=_elapsed_ms(start_time),
                        error_code=exc.error_code.value,
                        message=exc.message,
                    )
                )
                return res

            # optional advisory robots.txt check
            if check_robots and robots_status_val is None:
                robots_res = await fetch_robots_advisory(
                    self._client,
                    validated.normalized,
                    self._settings,
                    self._timeout,
                )
                robots_status_val = str(robots_res.status)
                await self._emit_event(
                    SafeWebEvent(
                        event_type=SafeWebEventType.ROBOTS_CHECKED,
                        requested_url=validated.original,
                        current_url=validated.normalized,
                        attempt_number=attempt,
                        elapsed_ms=_elapsed_ms(start_time),
                        message=f"Robots status: {robots_status_val}",
                    )
                )

            # execute safe transport streaming request & process response
            try:
                async with stream_safe_page(
                    self._client,
                    validated.normalized,
                    self._settings,
                    self._timeout,
                ) as stream_item:
                    status_code = stream_item.response.status_code

                    if stream_item.redirect_count > 0:
                        await self._emit_event(
                            SafeWebEvent(
                                event_type=SafeWebEventType.REDIRECT_FOLLOWED,
                                requested_url=validated.original,
                                current_url=validated.normalized,
                                final_url=stream_item.final_url,
                                attempt_number=attempt,
                                redirect_count=stream_item.redirect_count,
                                elapsed_ms=_elapsed_ms(start_time),
                            )
                        )

                    # handle non-success http status codes
                    if status_code < 200 or status_code >= 300:
                        if (
                            retry_pol.is_retryable_status(status_code)
                            and attempt < max_attempts
                        ):
                            delay = retry_pol.calculate_delay(
                                attempt, stream_item.response.headers
                            )
                            await self._emit_event(
                                SafeWebEvent(
                                    event_type=SafeWebEventType.RETRY_SCHEDULED,
                                    requested_url=validated.original,
                                    current_url=stream_item.final_url,
                                    attempt_number=attempt,
                                    status_code=status_code,
                                    elapsed_ms=_elapsed_ms(start_time),
                                    message=f"HTTP {status_code} retry in {delay:.2f}s",
                                )
                            )
                            if delay > 0:
                                await self._sleeper(delay)
                            continue

                        err_code = _map_http_status(status_code)
                        res = make_failure_result(
                            requested_url=validated.original,
                            final_url=stream_item.final_url,
                            status_code=status_code,
                            elapsed_ms=_elapsed_ms(start_time),
                            redirect_count=stream_item.redirect_count,
                            attempt_count=attempt,
                            robots_status=robots_status_val,
                            budget=active_budget,
                            error_code=err_code,
                            error_message=f"HTTP request failed with status code {status_code}.",
                        )
                        await self._emit_event(
                            SafeWebEvent(
                                event_type=SafeWebEventType.REQUEST_FAILED,
                                requested_url=validated.original,
                                current_url=validated.normalized,
                                final_url=stream_item.final_url,
                                attempt_number=attempt,
                                status_code=status_code,
                                redirect_count=stream_item.redirect_count,
                                elapsed_ms=_elapsed_ms(start_time),
                                error_code=err_code.value,
                                message=res.error_message,
                            )
                        )
                        return res

                    # validate headers and stream response body
                    await self._emit_event(
                        SafeWebEvent(
                            event_type=SafeWebEventType.RESPONSE_HEADERS_VALIDATED,
                            requested_url=validated.original,
                            current_url=validated.normalized,
                            final_url=stream_item.final_url,
                            attempt_number=attempt,
                            status_code=status_code,
                            elapsed_ms=_elapsed_ms(start_time),
                        )
                    )

                    read_res = await read_response_body(
                        stream_item.response,
                        self._settings,
                        active_budget,
                    )

                    await self._emit_event(
                        SafeWebEvent(
                            event_type=SafeWebEventType.RESPONSE_BODY_READ,
                            requested_url=validated.original,
                            current_url=validated.normalized,
                            final_url=stream_item.final_url,
                            attempt_number=attempt,
                            status_code=status_code,
                            size_bytes=read_res.size_bytes,
                            elapsed_ms=_elapsed_ms(start_time),
                        )
                    )

                    #  record consumed bytes in crawl budget
                    active_budget = active_budget.record_response(read_res.size_bytes)

                    success_res = make_success_result(
                        requested_url=validated.original,
                        final_url=stream_item.final_url,
                        status_code=status_code,
                        content_type=read_res.content_type,
                        elapsed_ms=_elapsed_ms(start_time),
                        size_bytes=read_res.size_bytes,
                        body=read_res.body,
                        redirect_count=stream_item.redirect_count,
                        attempt_count=attempt,
                        robots_status=robots_status_val,
                        budget=active_budget,
                    )

                    await self._emit_event(
                        SafeWebEvent(
                            event_type=SafeWebEventType.REQUEST_SUCCEEDED,
                            requested_url=validated.original,
                            current_url=validated.normalized,
                            final_url=stream_item.final_url,
                            attempt_number=attempt,
                            status_code=status_code,
                            size_bytes=read_res.size_bytes,
                            redirect_count=stream_item.redirect_count,
                            elapsed_ms=_elapsed_ms(start_time),
                        )
                    )

                    return success_res

            except SafeWebError as exc:
                if retry_pol.is_retryable_exception(exc) and attempt < max_attempts:
                    delay = retry_pol.calculate_delay(attempt, None)
                    await self._emit_event(
                        SafeWebEvent(
                            event_type=SafeWebEventType.RETRY_SCHEDULED,
                            requested_url=validated.original,
                            current_url=exc.current_url or validated.normalized,
                            attempt_number=attempt,
                            elapsed_ms=_elapsed_ms(start_time),
                            error_code=exc.error_code.value,
                            message=f"Transport error retry in {delay:.2f}s: {exc.message}",
                        )
                    )
                    if delay > 0:
                        await self._sleeper(delay)
                    continue

                res = make_failure_from_exception(
                    exc,
                    requested_url=validated.original,
                    elapsed_ms=_elapsed_ms(start_time),
                    attempt_count=attempt,
                    robots_status=robots_status_val,
                    budget=active_budget,
                )
                await self._emit_event(
                    SafeWebEvent(
                        event_type=SafeWebEventType.REQUEST_FAILED,
                        requested_url=validated.original,
                        current_url=validated.normalized,
                        final_url=exc.current_url,
                        attempt_number=attempt,
                        redirect_count=exc.redirect_count,
                        elapsed_ms=_elapsed_ms(start_time),
                        error_code=exc.error_code.value,
                        message=exc.message,
                    )
                )
                return res

        # fallback return if attempts loop ends without returning
        return make_failure_result(
            requested_url=req_url,
            error_code=SafeWebErrorCode.REQUEST_FAILED,
            error_message="Retries exhausted without resolution.",
            attempt_count=max_attempts,
            elapsed_ms=_elapsed_ms(start_time),
        )
