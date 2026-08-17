"""
This module defines all default safety limits for safe web access.
It controls request timeouts, redirect limits, and download byte sizes.
Its main public class is SafeWebSettings with frozen dataclass constraints.
It works with budgets, policies, retries, and client to apply scraping limits.
It validates connect/read timeouts, user agent format, and allowed types.
It does not allow changing settings dynamically once they are instantiated.
"""

from dataclasses import dataclass, field

from .policies import DomainPolicy
from .retries import RetryPolicy


def _require_num_not_bool(value: object, name: str) -> float:
    """Ensures value is a float or int and not a boolean."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number.")
    return float(value)


def _require_int_not_bool(value: object, name: str) -> int:
    """Ensures value is an integer and not a boolean."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer.")
    return value


@dataclass(frozen=True)
class SafeWebSettings:
    """Stores shared limits and defaults for safe web requests."""

    connect_timeout_seconds: float = 10.0
    read_timeout_seconds: float = 20.0
    max_redirects: int = 5
    max_response_bytes: int = 3_000_000
    max_pages: int = 20
    max_total_bytes: int = 20_000_000
    user_agent: str = "SafeWebAccess/1.0"
    allowed_content_types: tuple[str, ...] = (
        "text/html",
        "text/plain",
        "application/xhtml+xml",
    )
    domain_policy: DomainPolicy = field(default_factory=DomainPolicy)
    retry_policy: RetryPolicy = field(default_factory=RetryPolicy)
    strict_event_hooks: bool = False

    def __post_init__(self) -> None:
        """Checks invalid settings when the settings object is created."""
        conn_to = _require_num_not_bool(
            self.connect_timeout_seconds, "connect_timeout_seconds"
        )
        if conn_to <= 0:
            raise ValueError("connect_timeout_seconds must be greater than zero.")

        read_to = _require_num_not_bool(
            self.read_timeout_seconds, "read_timeout_seconds"
        )
        if read_to <= 0:
            raise ValueError("read_timeout_seconds must be greater than zero.")

        max_red = _require_int_not_bool(self.max_redirects, "max_redirects")
        if max_red < 0:
            raise ValueError("max_redirects limit cannot be negative.")

        max_pg = _require_int_not_bool(self.max_pages, "max_pages")
        if max_pg <= 0:
            raise ValueError("max_pages must be greater than zero.")

        max_resp = _require_int_not_bool(self.max_response_bytes, "max_response_bytes")
        if max_resp <= 0:
            raise ValueError("max_response_bytes limit must be greater than zero.")

        max_tot = _require_int_not_bool(self.max_total_bytes, "max_total_bytes")
        if max_tot <= 0:
            raise ValueError("max_total_bytes limit must be greater than zero.")

        if max_tot < max_resp:
            raise ValueError(
                "max_total_bytes cannot be smaller than max_response_bytes."
            )

        if not isinstance(self.user_agent, str) or not self.user_agent.strip():
            raise ValueError("user_agent cannot be empty or whitespace-only.")

        if isinstance(self.allowed_content_types, bool) or not isinstance(
            self.allowed_content_types, tuple
        ):
            raise TypeError("allowed_content_types must be a tuple.")
        if not self.allowed_content_types:
            raise ValueError("allowed_content_types cannot be empty.")
        if any(
            isinstance(ct, bool) or not isinstance(ct, str) or not ct.strip()
            for ct in self.allowed_content_types
        ):
            raise ValueError("allowed_content_types cannot contain empty values.")

        if not isinstance(self.domain_policy, DomainPolicy):
            raise TypeError("domain_policy must be a DomainPolicy instance.")

        if not isinstance(self.retry_policy, RetryPolicy):
            raise TypeError("retry_policy must be a RetryPolicy instance.")

        if not isinstance(self.strict_event_hooks, bool):
            raise TypeError("strict_event_hooks must be a boolean.")
