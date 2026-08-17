"""
This module provides a synchronous client wrapper around SafeWebClient.
It manages a dedicated background event loop and thread for safe HTTP fetches.
Its main public class is SyncSafeWebClient supporting context managers.
It works with SafeWebClient, settings, budgets, policies, and event hooks.
It guarantees thread isolation, resource cleanup, and idempotent closing.
It does not use asyncio.run per request or expose async methods directly.
"""

import asyncio
import threading
from types import TracebackType
from typing import Awaitable, Callable

import httpx

from .budgets import CrawlBudget
from .client import SafeWebClient
from .errors import SafeWebErrorCode
from .events import EventHook
from .result_builders import make_failure_result
from .results import SafeWebResult
from .settings import SafeWebSettings


class SyncSafeWebClient:
    """Synchronous HTTP client wrapping SafeWebClient using a background event loop."""

    def __init__(
        self,
        settings: SafeWebSettings | None = None,
        client: httpx.AsyncClient | None = None,
        event_hooks: tuple[EventHook, ...] | list[EventHook] | None = None,
        sleeper: Callable[[float], Awaitable[None]] | None = None,
    ) -> None:
        """Initializes SyncSafeWebClient and starts an internal background thread."""
        self._settings = settings if settings is not None else SafeWebSettings()
        self._closed = False
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(
            target=self._run_loop,
            name="SyncSafeWebClientLoop",
            daemon=True,
        )
        self._thread.start()

        fut = asyncio.run_coroutine_threadsafe(
            self._create_async_client(client, event_hooks, sleeper),
            self._loop,
        )
        self._async_client = fut.result()

    async def _create_async_client(
        self,
        client: httpx.AsyncClient | None,
        event_hooks: tuple[EventHook, ...] | list[EventHook] | None,
        sleeper: Callable[[float], Awaitable[None]] | None,
    ) -> SafeWebClient:
        return SafeWebClient(
            settings=self._settings,
            client=client,
            event_hooks=event_hooks,
            sleeper=sleeper,
        )

    def _run_loop(self) -> None:
        """Runs the background asyncio event loop."""
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def start(self) -> "SyncSafeWebClient":
        """Prepares the client for use and returns it, for callers not using ``with``.

        The constructor already starts the background loop, so this performs no setup
        work. It exists so a caller managing the lifecycle by hand can write
        ``client = SyncSafeWebClient().start()`` and later ``client.close()``,
        matching the asynchronous client. Calling it more than once is safe.
        """
        if self._closed:
            raise RuntimeError("Client is already closed.")
        return self

    def __enter__(self) -> "SyncSafeWebClient":
        """Enters context manager after ensuring client is open."""
        if self._closed:
            raise RuntimeError("Client is already closed.")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exits context manager and closes resources."""
        self.close()

    def close(self) -> None:
        """Closes internal resources and stops the background thread idempotently."""
        if self._closed:
            return
        self._closed = True
        if self._loop.is_running():
            fut = asyncio.run_coroutine_threadsafe(
                self._async_client.aclose(),
                self._loop,
            )
            try:
                fut.result(timeout=5.0)
            except Exception:
                pass
            self._loop.call_soon_threadsafe(self._loop.stop)
        if self._thread.is_alive():
            self._thread.join(timeout=5.0)
        if not self._loop.is_closed():
            self._loop.close()

    def fetch(
        self,
        url: str,
        *,
        budget: CrawlBudget | None = None,
        check_robots: bool = True,
    ) -> SafeWebResult:
        """Executes a synchronous safe fetch request."""
        if self._closed:
            req_url = url if isinstance(url, str) and url.strip() else "invalid_url"
            return make_failure_result(
                requested_url=req_url,
                error_code=SafeWebErrorCode.REQUEST_FAILED,
                error_message="Client is closed.",
            )

        fut = asyncio.run_coroutine_threadsafe(
            self._async_client.fetch(url, budget=budget, check_robots=check_robots),
            self._loop,
        )
        return fut.result()
