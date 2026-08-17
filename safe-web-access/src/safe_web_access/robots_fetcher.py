"""
This module handles fetching and evaluating robots.txt files in an advisory mode.
It resolves DNS hostnames, follows manual redirects safely, and limits download sizes.
Its main public function is fetch_robots_advisory returning a RobotsCheckResult.
It works with robots, networks, redirects, policies, and settings modules.
It streams raw robots.txt rules and falls back to advisory results on timeouts.
It does not parse HTML webpages or execute custom scraping policies.
"""

import httpx

from .exceptions import SafeWebError
from .networks import resolve_public_addresses
from .redirects import validate_redirect_target
from .robots import (
    RobotsCheckResult,
    build_robots_url,
    create_robots_unreachable_result,
    evaluate_robots_rules,
)
from .settings import SafeWebSettings
from .urls import validate_and_normalize_url


async def fetch_robots_advisory(
    client: httpx.AsyncClient,
    target_url: str,
    settings: SafeWebSettings,
    timeout: httpx.Timeout,
) -> RobotsCheckResult:
    """Fetches and evaluates the advisory robots.txt policy for a target URL."""
    current_robots_url = build_robots_url(target_url)
    visited_robots_urls: set[str] = {current_robots_url}
    robots_redirect_count = 0
    max_robots_redirects = min(settings.max_redirects, 3)
    default_headers = {
        "User-Agent": settings.user_agent,
        "Accept": "text/plain, text/html",
    }

    # Dedicated loop for safely fetching and following robots.txt redirects
    while True:
        try:
            parsed_robots = validate_and_normalize_url(current_robots_url)
            if settings.domain_policy is not None:
                settings.domain_policy.evaluate_url(parsed_robots)
            resolve_public_addresses(parsed_robots.hostname)
        except (ValueError, TypeError, SafeWebError):
            return create_robots_unreachable_result(target_url, settings.user_agent)

        try:
            async with client.stream(
                "GET",
                current_robots_url,
                headers=default_headers,
                timeout=timeout,
                follow_redirects=False,
            ) as response:
                status_code = response.status_code

                # Handle robots.txt manual redirects (301, 302, 303, 307, 308)
                if status_code in {301, 302, 303, 307, 308}:
                    location_header = response.headers.get("Location")
                    if not location_header:
                        return create_robots_unreachable_result(
                            target_url, settings.user_agent
                        )

                    try:
                        redirect_res = validate_redirect_target(
                            source_url=current_robots_url,
                            location=location_header,
                            visited_urls=visited_robots_urls,
                            current_redirect_count=robots_redirect_count,
                            max_redirects=max_robots_redirects,
                            domain_policy=settings.domain_policy,
                        )
                    except (ValueError, TypeError, SafeWebError):
                        return create_robots_unreachable_result(
                            target_url, settings.user_agent
                        )

                    visited_robots_urls.add(current_robots_url)
                    current_robots_url = redirect_res.target.normalized
                    robots_redirect_count = redirect_res.redirect_count
                    continue

                if status_code in (404, 410):
                    return evaluate_robots_rules(target_url, "", settings.user_agent)
                if status_code < 200 or status_code >= 300:
                    return create_robots_unreachable_result(
                        target_url, settings.user_agent
                    )

                max_robots_bytes = min(262_144, settings.max_response_bytes)
                chunks: list[bytes] = []
                size = 0

                # Stream robots.txt content with strict byte limits
                async for chunk in response.aiter_bytes():
                    if chunk:
                        size += len(chunk)
                        if size > max_robots_bytes:
                            return create_robots_unreachable_result(
                                target_url, settings.user_agent
                            )
                        chunks.append(chunk)

                robots_text = b"".join(chunks).decode("utf-8", errors="replace")
                return evaluate_robots_rules(
                    target_url, robots_text, settings.user_agent
                )
        except (
            httpx.HTTPError,
            ValueError,
            TypeError,
            SafeWebError,
        ):
            return create_robots_unreachable_result(target_url, settings.user_agent)
