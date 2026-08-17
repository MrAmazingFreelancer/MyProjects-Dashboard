"""
This module defines the standard result returned after a safe web request.
Successful and failed requests use the same structured SafeWebResult class.
Its main public class is SafeWebResult which is immutable and slotted.
It works with budgets, client, and result_builders to describe outcomes.
It validates field types, HTTP status ranges, and error metadata consistency.
It does not raise exceptions directly; it returns structured failure reports.
"""

from dataclasses import dataclass

from .budgets import CrawlBudget


@dataclass(frozen=True, slots=True)
class SafeWebResult:
    """Stores the final result of one safe web request."""

    success: bool
    requested_url: str
    final_url: str | None = None
    status_code: int | None = None
    content_type: str | None = None
    method: str = "GET"
    elapsed_ms: int | None = None
    size_bytes: int = 0
    body: bytes | None = None
    cleaned_text: str | None = None
    robots_status: str | None = None
    budget: CrawlBudget | None = None
    error_code: str | None = None
    error_message: str | None = None
    redirect_count: int = 0
    attempt_count: int = 1

    def __post_init__(self) -> None:
        """Checks that the result contains valid and consistent values."""
        if not isinstance(self.requested_url, str):
            raise TypeError("requested_url must be a string.")
        if not self.requested_url.strip():
            raise ValueError("requested_url cannot be empty or whitespace-only.")

        if not isinstance(self.method, str):
            raise TypeError("method must be a string.")
        if not self.method.strip():
            raise ValueError("method cannot be empty or whitespace-only.")
        if self.method.upper() not in {"GET", "HEAD"}:
            raise ValueError("method must be GET or HEAD.")

        if isinstance(self.attempt_count, bool) or not isinstance(
            self.attempt_count, int
        ):
            raise TypeError("attempt_count must be an integer.")
        if self.attempt_count < 1:
            raise ValueError("attempt_count must be at least 1.")

        if self.final_url is not None:
            if not isinstance(self.final_url, str):
                raise TypeError("final_url must be a string.")
            if not self.final_url.strip():
                raise ValueError("final_url cannot be empty or whitespace-only.")

        if self.content_type is not None:
            if not isinstance(self.content_type, str):
                raise TypeError("content_type must be a string.")
            if not self.content_type.strip():
                raise ValueError("content_type cannot be empty or whitespace-only.")

        if self.cleaned_text is not None and not isinstance(self.cleaned_text, str):
            raise TypeError("cleaned_text must be a string.")

        if self.elapsed_ms is not None and self.elapsed_ms < 0:
            raise ValueError("elapsed_ms cannot be negative.")
        if self.size_bytes < 0:
            raise ValueError("size_bytes cannot be negative.")
        if self.redirect_count < 0:
            raise ValueError("redirect_count cannot be negative.")
        if self.status_code is not None and not (100 <= self.status_code <= 599):
            raise ValueError("status_code must be between 100 and 599.")

        if self.budget is not None and not isinstance(self.budget, CrawlBudget):
            raise TypeError("budget must be a CrawlBudget instance or None.")

        if self.robots_status is not None:
            if not isinstance(self.robots_status, str):
                raise TypeError("robots_status must be a string.")
            if self.robots_status not in {
                "allowed",
                "disallowed",
                "missing",
                "unreachable",
                "invalid",
            }:
                raise ValueError(
                    "robots_status must be one of: allowed, disallowed, missing, unreachable, invalid, or None."
                )

        if self.success:
            if not isinstance(self.final_url, str) or not self.final_url.strip():
                raise ValueError(
                    "final_url must be a non-empty string when success is True."
                )
            if self.status_code is None or not (200 <= self.status_code <= 299):
                raise ValueError(
                    "status_code must be between 200 and 299 when success is True."
                )
            if not isinstance(self.content_type, str) or not self.content_type.strip():
                raise ValueError(
                    "content_type must be a non-empty string when success is True."
                )
            if self.body is None or not isinstance(self.body, bytes):
                raise ValueError("body must be bytes when success is True.")
            if self.size_bytes != len(self.body):
                raise ValueError(
                    "size_bytes must equal len(body) when success is True."
                )
            if self.error_code is not None:
                raise ValueError("error_code must be None when success is True.")
            if self.error_message is not None:
                raise ValueError("error_message must be None when success is True.")
        else:
            if self.body is not None:
                raise ValueError("body must be None when success is False.")
            if not isinstance(self.error_code, str) or not self.error_code.strip():
                raise ValueError(
                    "error_code must be a non-empty string when success is False."
                )
            if (
                not isinstance(self.error_message, str)
                or not self.error_message.strip()
            ):
                raise ValueError(
                    "error_message must be a non-empty string when success is False."
                )
