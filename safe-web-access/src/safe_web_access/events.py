"""
This module provides event definitions and telemetry hooks for safe web requests.
It defines structured event types and metadata emitted throughout execution.
Its main public classes are SafeWebEventType enum and SafeWebEvent dataclass.
It works with client and sync_client to notify registered observability hooks.
It guarantees metadata safety by excluding request headers, cookies, and bodies.
It does not handle logging, metrics storage, or network transmission itself.
"""

from dataclasses import dataclass
from enum import StrEnum
from typing import Awaitable, Callable, Union


class SafeWebEventType(StrEnum):
    """Lists standard event types emitted during safe web request execution."""

    REQUEST_STARTED = "request_started"
    URL_VALIDATED = "url_validated"
    POLICY_VALIDATED = "policy_validated"
    NETWORK_VALIDATED = "network_validated"
    BUDGET_VALIDATED = "budget_validated"
    ROBOTS_CHECKED = "robots_checked"
    ATTEMPT_STARTED = "attempt_started"
    REDIRECT_FOLLOWED = "redirect_followed"
    RETRY_SCHEDULED = "retry_scheduled"
    RESPONSE_HEADERS_VALIDATED = "response_headers_validated"
    RESPONSE_BODY_READ = "response_body_read"
    REQUEST_SUCCEEDED = "request_succeeded"
    REQUEST_FAILED = "request_failed"
    CLIENT_CLOSED = "client_closed"


@dataclass(frozen=True, slots=True)
class SafeWebEvent:
    """Stores safe telemetry metadata emitted during request execution."""

    event_type: SafeWebEventType
    requested_url: str
    current_url: str | None = None
    final_url: str | None = None
    attempt_number: int = 1
    status_code: int | None = None
    redirect_count: int = 0
    elapsed_ms: int = 0
    size_bytes: int = 0
    error_code: str | None = None
    message: str | None = None

    def __post_init__(self) -> None:
        """Validates event metadata fields."""
        if not isinstance(self.event_type, SafeWebEventType):
            raise TypeError("event_type must be a SafeWebEventType enum member.")
        if not isinstance(self.requested_url, str) or not self.requested_url.strip():
            raise ValueError("requested_url must be a non-empty string.")
        if isinstance(self.attempt_number, bool) or not isinstance(
            self.attempt_number, int
        ):
            raise TypeError("attempt_number must be an integer.")
        if self.attempt_number < 1:
            raise ValueError("attempt_number must be at least 1.")
        if isinstance(self.redirect_count, bool) or not isinstance(
            self.redirect_count, int
        ):
            raise TypeError("redirect_count must be an integer.")
        if self.redirect_count < 0:
            raise ValueError("redirect_count cannot be negative.")
        if isinstance(self.elapsed_ms, bool) or not isinstance(self.elapsed_ms, int):
            raise TypeError("elapsed_ms must be an integer.")
        if self.elapsed_ms < 0:
            raise ValueError("elapsed_ms cannot be negative.")
        if isinstance(self.size_bytes, bool) or not isinstance(self.size_bytes, int):
            raise TypeError("size_bytes must be an integer.")
        if self.size_bytes < 0:
            raise ValueError("size_bytes cannot be negative.")


EventHook = Union[
    Callable[[SafeWebEvent], None],
    Callable[[SafeWebEvent], Awaitable[None]],
]
