from safe_web_access.budgets import CrawlBudget
from safe_web_access.errors import SafeWebErrorCode
from safe_web_access.exceptions import UnsafeNetworkError
from safe_web_access.result_builders import (
    make_failure_from_exception,
    make_failure_result,
    make_success_result,
)


def test_make_success_result():
    budget = CrawlBudget(max_pages=5, max_total_bytes=1000, pages_used=1, bytes_used=10)
    res = make_success_result(
        requested_url="https://example.com",
        final_url="https://example.com/final",
        status_code=200,
        content_type="text/html",
        elapsed_ms=100,
        size_bytes=10,
        body=b"0123456789",
        redirect_count=1,
        robots_status="allowed",
        budget=budget,
    )
    assert res.success is True
    assert res.requested_url == "https://example.com"
    assert res.final_url == "https://example.com/final"
    assert res.status_code == 200
    assert res.body == b"0123456789"
    assert res.size_bytes == 10
    assert res.error_code is None
    assert res.error_message is None
    assert res.budget == budget


def test_make_failure_result():
    budget = CrawlBudget(max_pages=5, max_total_bytes=1000)
    res = make_failure_result(
        requested_url="https://example.com",
        error_code=SafeWebErrorCode.PRIVATE_NETWORK,
        error_message="Host resolves to private IP",
        final_url="https://example.com/private",
        elapsed_ms=50,
        redirect_count=1,
        robots_status="missing",
        budget=budget,
    )
    assert res.success is False
    assert res.body is None
    assert res.error_code == "private_network"
    assert res.error_message == "Host resolves to private IP"
    assert res.final_url == "https://example.com/private"
    assert res.budget == budget


def test_make_failure_from_exception():
    exc = UnsafeNetworkError(
        "Host resolves to loopback IP", current_url="http://127.0.0.1"
    )
    res = make_failure_from_exception(
        exc, requested_url="http://127.0.0.1", elapsed_ms=12
    )

    assert res.success is False
    assert res.requested_url == "http://127.0.0.1"
    assert res.final_url == "http://127.0.0.1"
    assert res.error_code == "private_network"
    assert res.error_message == "Host resolves to loopback IP"
    assert res.elapsed_ms == 12
