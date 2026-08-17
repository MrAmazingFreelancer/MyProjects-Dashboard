"""
This module provides configurable retry and exponential backoff policies.
It determines whether failed requests are temporary and should be retried.
Its main public class is RetryPolicy supporting status codes and delays.
It works with transport, client, and response_reader to retry safely.
It enforces maximum attempt bounds, Retry-After header parsing, and jitter.
It does not retry security violations, budget exhaustion, or invalid URLs.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Mapping

from .exceptions import (
    SafeWebConnectionError,
    SafeWebConnectTimeout,
    SafeWebReadTimeout,
    SafeWebRequestTimeout,
)


def _require_int_not_bool(value: object, name: str) -> int:
    """Ensures value is an integer and not a boolean."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer.")
    return value


def _require_num_not_bool(value: object, name: str) -> float:
    """Ensures value is a float or int and not a boolean."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number.")
    return float(value)


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    """Stores retry configuration limits, eligible status codes, and backoff timing."""

    max_attempts: int = 1
    backoff_base_seconds: float = 0.5
    backoff_max_seconds: float = 10.0
    backoff_multiplier: float = 2.0
    retry_status_codes: tuple[int, ...] = (408, 429, 502, 503, 504)
    respect_retry_after: bool = True
    jitter_seconds: float = 0.0

    def __post_init__(self) -> None:
        """Validates retry policy settings."""
        max_att = _require_int_not_bool(self.max_attempts, "max_attempts")
        if max_att < 1:
            raise ValueError("max_attempts must be at least 1.")

        base_sec = _require_num_not_bool(
            self.backoff_base_seconds, "backoff_base_seconds"
        )
        if base_sec < 0:
            raise ValueError("backoff_base_seconds cannot be negative.")

        max_sec = _require_num_not_bool(self.backoff_max_seconds, "backoff_max_seconds")
        if max_sec < 0:
            raise ValueError("backoff_max_seconds cannot be negative.")

        mult = _require_num_not_bool(self.backoff_multiplier, "backoff_multiplier")
        if mult < 1.0:
            raise ValueError("backoff_multiplier must be at least 1.0.")

        if isinstance(self.retry_status_codes, bool) or not isinstance(
            self.retry_status_codes, tuple
        ):
            raise TypeError("retry_status_codes must be a tuple.")

        seen_codes: set[int] = set()
        for code in self.retry_status_codes:
            code_int = _require_int_not_bool(code, "retry_status_codes item")
            if not (100 <= code_int <= 599):
                raise ValueError("retry status code must be between 100 and 599.")
            if code_int in seen_codes:
                raise ValueError(
                    f"Duplicate status code in retry_status_codes: {code_int}."
                )
            seen_codes.add(code_int)

        if not isinstance(self.respect_retry_after, bool):
            raise TypeError("respect_retry_after must be a boolean.")

        jit = _require_num_not_bool(self.jitter_seconds, "jitter_seconds")
        if jit < 0:
            raise ValueError("jitter_seconds cannot be negative.")

    def is_retryable_status(self, status_code: int) -> bool:
        """Returns True if the HTTP status code is eligible for retry."""
        return status_code in self.retry_status_codes

    def is_retryable_exception(self, exc: BaseException) -> bool:
        """Returns True if the exception represents a temporary transport failure."""
        return isinstance(
            exc,
            (
                SafeWebConnectTimeout,
                SafeWebReadTimeout,
                SafeWebRequestTimeout,
                SafeWebConnectionError,
            ),
        )

    def calculate_delay(
        self,
        attempt: int,
        response_headers: Mapping[str, str] | None = None,
    ) -> float:
        """Calculates backoff delay in seconds before the next retry attempt."""
        if attempt < 1:
            return 0.0

        header_delay: float | None = None
        if self.respect_retry_after and response_headers:
            header_val = None
            for key, val in response_headers.items():
                if key.lower() == "retry-after":
                    header_val = val
                    break

            if header_val:
                header_val_str = header_val.strip()
                if header_val_str.isdigit():
                    header_delay = float(header_val_str)
                else:
                    try:
                        dt = parsedate_to_datetime(header_val_str)
                        if dt.tzinfo is None:
                            dt = dt.replace(tzinfo=timezone.utc)
                        now = datetime.now(timezone.utc)
                        header_delay = (dt - now).total_seconds()
                    except (TypeError, ValueError):
                        header_delay = None

        if header_delay is not None and header_delay >= 0:
            delay = header_delay
        else:
            delay = self.backoff_base_seconds * (
                self.backoff_multiplier ** (attempt - 1)
            )

        if self.jitter_seconds > 0:
            delay += self.jitter_seconds

        return max(0.0, min(delay, self.backoff_max_seconds))
