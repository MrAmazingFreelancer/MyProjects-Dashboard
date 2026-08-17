"""
This module checks every new link returned by a website redirect.
It manages redirect validation to prevent Server-Side Request Forgery.
Its main function is validate_redirect_target and the main class is RedirectResult.
It works with urls, networks, policies, and exceptions to ensure hops are safe.
It stops redirect loops, policy violations, and overly long redirect chains.
It does not send HTTP requests or read webpage content.
"""

from dataclasses import dataclass
from urllib.parse import urljoin

from .exceptions import (
    InvalidUrlError,
    RedirectLimitError,
    RedirectLoopError,
    UnsafeRedirectError,
    UnsupportedSchemeError,
)
from .networks import NetworkCheckResult, resolve_public_addresses
from .policies import DomainPolicy
from .urls import ValidatedUrl, validate_and_normalize_url


@dataclass(frozen=True, slots=True)
class RedirectResult:
    """Stores one validated step in a redirect chain."""

    source_url: str
    target: ValidatedUrl
    network: NetworkCheckResult
    redirect_count: int

    def __post_init__(self) -> None:
        """Checks that the redirect result contains valid data."""
        if not self.source_url or not self.source_url.strip():
            raise ValueError("source_url cannot be empty or whitespace-only.")
        if self.redirect_count <= 0:
            raise ValueError("redirect_count must be greater than zero.")
        if self.target.hostname.lower() != self.network.hostname.lower():
            raise ValueError("target.hostname and network.hostname do not match.")
        if not self.network.addresses:
            raise ValueError("network.addresses cannot be empty.")


def validate_redirect_target(
    source_url: str,
    location: str,
    visited_urls: set[str] | frozenset[str],
    current_redirect_count: int,
    max_redirects: int,
    domain_policy: DomainPolicy | None = None,
) -> RedirectResult:
    """Builds and validates the next safe URL in a redirect chain."""
    if not isinstance(source_url, str):
        raise TypeError("source_url must be a string.")
    if not isinstance(location, str):
        raise TypeError("location must be a string.")
    if not isinstance(visited_urls, (set, frozenset)):
        raise TypeError("visited_urls must be a set or frozenset.")
    if isinstance(current_redirect_count, bool) or not isinstance(
        current_redirect_count, int
    ):
        raise TypeError("current_redirect_count must be an integer.")
    if isinstance(max_redirects, bool) or not isinstance(max_redirects, int):
        raise TypeError("max_redirects must be an integer.")
    if domain_policy is not None and not isinstance(domain_policy, DomainPolicy):
        raise TypeError("domain_policy must be a DomainPolicy instance or None.")

    if not source_url or not source_url.strip():
        raise InvalidUrlError("source_url cannot be empty or whitespace-only.")
    if not location or not location.strip():
        raise UnsafeRedirectError("location cannot be empty or whitespace-only.")
    if current_redirect_count < 0:
        raise ValueError("current_redirect_count cannot be negative.")
    if max_redirects < 0:
        raise ValueError("max_redirects cannot be negative.")

    for item in visited_urls:
        if not isinstance(item, str):
            raise TypeError("All items in visited_urls must be strings.")

    source = validate_and_normalize_url(source_url)

    # Resolve the redirect target URL by joining it to the source URL
    joined_target = urljoin(source.normalized, location.strip())
    try:
        target = validate_and_normalize_url(joined_target)
    except (InvalidUrlError, UnsupportedSchemeError) as exc:
        raise UnsafeRedirectError(f"Invalid redirect target URL: {exc}") from exc

    if domain_policy is not None:
        domain_policy.evaluate_url(target)

    next_redirect_count = current_redirect_count + 1
    if next_redirect_count > max_redirects:
        raise RedirectLimitError(
            "Redirect limit exceeded.",
            current_url=target.normalized,
            redirect_count=next_redirect_count,
        )

    # Normalize visited URLs to check for potential redirect loops
    normalized_visited = {
        validate_and_normalize_url(visited).normalized for visited in visited_urls
    }
    normalized_visited.add(source.normalized)
    if target.normalized in normalized_visited:
        raise RedirectLoopError(
            "Redirect loop detected.",
            current_url=target.normalized,
            redirect_count=next_redirect_count,
        )

    network = resolve_public_addresses(target.hostname)

    return RedirectResult(
        source_url=source.normalized,
        target=target,
        network=network,
        redirect_count=next_redirect_count,
    )
