"""
This module handles low-level asynchronous HTTP requests and redirects.
It resolves network destinations before every fetch to prevent SSRF vulnerabilities.
Its main public function is stream_safe_page yielding a TransportStream.
It works with networks, redirects, policies, settings, and exceptions to fetch.
It checks redirect chains step-by-step, enforcing limits and loop prevention.
It does not read response bodies or parse page headers themselves.
"""

from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncGenerator

import httpx

from .exceptions import (
    MissingRedirectLocationError,
    SafeWebConnectionError,
    SafeWebConnectTimeout,
    SafeWebReadTimeout,
    SafeWebRequestTimeout,
)
from .networks import resolve_public_addresses
from .redirects import validate_redirect_target
from .settings import SafeWebSettings
from .urls import validate_and_normalize_url


@dataclass(frozen=True, slots=True)
class TransportStream:
    """Stores the active HTTP response stream along with final request metadata."""

    response: httpx.Response
    final_url: str
    redirect_count: int


@asynccontextmanager
async def stream_safe_page(
    client: httpx.AsyncClient,
    validated_url_str: str,
    settings: SafeWebSettings,
    timeout: httpx.Timeout,
) -> AsyncGenerator[TransportStream, None]:
    """Executes a safe streaming GET request, manually validating every redirect before following."""
    current_url = validated_url_str
    # Initialize visited_urls with the original normalized URL to catch immediate self-redirect loops
    visited_urls: set[str] = {validated_url_str}
    redirect_count = 0
    default_headers = {
        "User-Agent": settings.user_agent,
        "Accept": "text/html,text/plain,application/xhtml+xml,application/pdf",
    }

    # Redirect loop: manually validate every target host against SSRF and loop rules
    while True:
        parsed = validate_and_normalize_url(current_url)
        if settings.domain_policy is not None:
            settings.domain_policy.evaluate_url(parsed)

        # Validate destination IP addresses before connecting
        resolve_public_addresses(parsed.hostname)

        try:
            async with client.stream(
                "GET",
                current_url,
                headers=default_headers,
                timeout=timeout,
                follow_redirects=False,
            ) as response:
                status_code = response.status_code

                # Handle manual redirects (301, 302, 303, 307, 308)
                if status_code in {301, 302, 303, 307, 308}:
                    location_header = response.headers.get("Location")
                    if not location_header:
                        raise MissingRedirectLocationError(
                            "Location header is missing in redirect response.",
                            current_url=current_url,
                            redirect_count=redirect_count,
                        )

                    redirect_res = validate_redirect_target(
                        source_url=current_url,
                        location=location_header,
                        visited_urls=visited_urls,
                        current_redirect_count=redirect_count,
                        max_redirects=settings.max_redirects,
                        domain_policy=settings.domain_policy,
                    )

                    visited_urls.add(current_url)
                    current_url = redirect_res.target.normalized
                    redirect_count = redirect_res.redirect_count
                    continue

                yield TransportStream(
                    response=response,
                    final_url=current_url,
                    redirect_count=redirect_count,
                )
                return
        except httpx.ConnectTimeout as exc:
            raise SafeWebConnectTimeout(
                f"Connection timeout: {exc}", current_url, redirect_count
            ) from exc
        except httpx.ReadTimeout as exc:
            raise SafeWebReadTimeout(
                f"Read timeout: {exc}", current_url, redirect_count
            ) from exc
        except httpx.TimeoutException as exc:
            raise SafeWebRequestTimeout(
                f"Request timeout: {exc}", current_url, redirect_count
            ) from exc
        except (httpx.TransportError, httpx.HTTPError) as exc:
            raise SafeWebConnectionError(
                f"Transport/HTTP error: {exc}", current_url, redirect_count
            ) from exc
