"""
This module contains helper functions for creating standard SafeWebResult objects.
It builds standardized outcomes for both successful fetches and custom exceptions.
Its main functions include make_success_result, make_failure_result, and make_failure_from_exception.
It works with results, budgets, errors, and exceptions to construct data wrappers.
It maps typed exceptions to correct error codes and preserves crawl budgets.
It does not perform any HTTP operations, socket resolution, or robots validation.
"""

from .budgets import CrawlBudget
from .errors import SafeWebErrorCode
from .exceptions import SafeWebError
from .results import SafeWebResult


def make_failure_result(
    requested_url: str,
    error_code: SafeWebErrorCode | str,
    error_message: str,
    *,
    final_url: str | None = None,
    status_code: int | None = None,
    elapsed_ms: int | None = None,
    size_bytes: int = 0,
    redirect_count: int = 0,
    attempt_count: int = 1,
    robots_status: str | None = None,
    budget: CrawlBudget | None = None,
) -> SafeWebResult:
    """Constructs a failed SafeWebResult object with structured error details."""
    code_str = (
        error_code.value
        if isinstance(error_code, SafeWebErrorCode)
        else str(error_code)
    )
    return SafeWebResult(
        success=False,
        requested_url=requested_url,
        final_url=final_url,
        status_code=status_code,
        content_type=None,
        method="GET",
        elapsed_ms=elapsed_ms,
        size_bytes=size_bytes,
        body=None,
        cleaned_text=None,
        robots_status=robots_status,
        budget=budget,
        error_code=code_str,
        error_message=error_message,
        redirect_count=redirect_count,
        attempt_count=attempt_count,
    )


def make_failure_from_exception(
    exc: SafeWebError,
    requested_url: str,
    *,
    elapsed_ms: int | None = None,
    attempt_count: int = 1,
    robots_status: str | None = None,
    budget: CrawlBudget | None = None,
) -> SafeWebResult:
    """Constructs a failed SafeWebResult directly from a typed SafeWebError exception."""
    return make_failure_result(
        requested_url=requested_url,
        final_url=exc.current_url,
        status_code=exc.status_code,
        elapsed_ms=elapsed_ms,
        size_bytes=exc.size_bytes,
        redirect_count=exc.redirect_count,
        attempt_count=attempt_count,
        robots_status=robots_status,
        budget=budget,
        error_code=exc.error_code,
        error_message=exc.message,
    )


def make_success_result(
    requested_url: str,
    final_url: str,
    status_code: int,
    content_type: str,
    elapsed_ms: int,
    size_bytes: int,
    body: bytes,
    redirect_count: int = 0,
    attempt_count: int = 1,
    robots_status: str | None = None,
    budget: CrawlBudget | None = None,
) -> SafeWebResult:
    """Constructs a successful SafeWebResult object containing response body bytes and metadata."""
    return SafeWebResult(
        success=True,
        requested_url=requested_url,
        final_url=final_url,
        status_code=status_code,
        content_type=content_type,
        method="GET",
        elapsed_ms=elapsed_ms,
        size_bytes=size_bytes,
        body=body,
        cleaned_text=None,
        robots_status=robots_status,
        budget=budget,
        error_code=None,
        error_message=None,
        redirect_count=redirect_count,
        attempt_count=attempt_count,
    )
