from dataclasses import FrozenInstanceError

import pytest

from safe_web_access.budgets import CrawlBudget
from safe_web_access.errors import SafeWebErrorCode
from safe_web_access.results import SafeWebResult


def test_results_valid_success():
    budget = CrawlBudget(max_pages=5, max_total_bytes=1000)
    res = SafeWebResult(
        success=True,
        requested_url="https://example.com",
        final_url="https://example.com/home",
        status_code=200,
        content_type="text/html",
        elapsed_ms=150,
        size_bytes=12,
        body=b"Hello World!",
        robots_status="allowed",
        budget=budget,
    )
    assert res.success is True
    assert res.body == b"Hello World!"
    assert res.status_code == 200
    assert res.content_type == "text/html"
    assert res.error_code is None


def test_results_valid_failure():
    res = SafeWebResult(
        success=False,
        requested_url="https://example.com",
        error_code=SafeWebErrorCode.PRIVATE_NETWORK.value,
        error_message="Host resolves to private IP.",
        status_code=None,
    )
    assert res.success is False
    assert res.body is None
    assert res.error_code == "private_network"
    assert res.error_message == "Host resolves to private IP."


def test_results_frozen():
    res = SafeWebResult(
        success=False,
        requested_url="https://example.com",
        error_code="test_code",
        error_message="test_msg",
    )
    with pytest.raises(FrozenInstanceError):
        res.success = True  # type: ignore


def test_results_success_invalid_cases():
    with pytest.raises(ValueError, match="final_url"):
        SafeWebResult(
            success=True,
            requested_url="https://example.com",
            final_url="",
            status_code=200,
            content_type="text/html",
            body=b"test",
            size_bytes=4,
        )

    with pytest.raises(ValueError, match="status_code"):
        SafeWebResult(
            success=True,
            requested_url="https://example.com",
            final_url="https://example.com",
            status_code=404,
            content_type="text/html",
            body=b"test",
            size_bytes=4,
        )

    with pytest.raises(ValueError, match="content_type"):
        SafeWebResult(
            success=True,
            requested_url="https://example.com",
            final_url="https://example.com",
            status_code=200,
            content_type="",
            body=b"test",
            size_bytes=4,
        )

    with pytest.raises(ValueError, match="body"):
        SafeWebResult(
            success=True,
            requested_url="https://example.com",
            final_url="https://example.com",
            status_code=200,
            content_type="text/html",
            body=None,
            size_bytes=0,
        )

    with pytest.raises(ValueError, match="size_bytes"):
        SafeWebResult(
            success=True,
            requested_url="https://example.com",
            final_url="https://example.com",
            status_code=200,
            content_type="text/html",
            body=b"test",
            size_bytes=100,
        )

    with pytest.raises(ValueError, match="error_code"):
        SafeWebResult(
            success=True,
            requested_url="https://example.com",
            final_url="https://example.com",
            status_code=200,
            content_type="text/html",
            body=b"test",
            size_bytes=4,
            error_code="err",
        )

    with pytest.raises(ValueError, match="error_message"):
        SafeWebResult(
            success=True,
            requested_url="https://example.com",
            final_url="https://example.com",
            status_code=200,
            content_type="text/html",
            body=b"test",
            size_bytes=4,
            error_message="msg",
        )


def test_results_failure_invalid_cases():
    with pytest.raises(ValueError, match="body"):
        SafeWebResult(
            success=False,
            requested_url="https://example.com",
            body=b"should be None",
            error_code="code",
            error_message="msg",
        )

    with pytest.raises(ValueError, match="error_code"):
        SafeWebResult(
            success=False,
            requested_url="https://example.com",
            error_code="",
            error_message="msg",
        )

    with pytest.raises(ValueError, match="error_message"):
        SafeWebResult(
            success=False,
            requested_url="https://example.com",
            error_code="code",
            error_message="",
        )


def test_results_general_validations():
    with pytest.raises(TypeError, match="requested_url"):
        SafeWebResult(success=False, requested_url=123, error_code="err", error_message="msg")  # type: ignore

    with pytest.raises(ValueError, match="requested_url"):
        SafeWebResult(
            success=False, requested_url="  ", error_code="err", error_message="msg"
        )

    with pytest.raises(TypeError, match="method"):
        SafeWebResult(success=False, requested_url="https://example.com", method=123, error_code="err", error_message="msg")  # type: ignore

    with pytest.raises(ValueError, match="method"):
        SafeWebResult(
            success=False,
            requested_url="https://example.com",
            method="POST",
            error_code="err",
            error_message="msg",
        )

    with pytest.raises(TypeError, match="attempt_count"):
        SafeWebResult(success=False, requested_url="https://example.com", attempt_count=True, error_code="err", error_message="msg")  # type: ignore

    with pytest.raises(ValueError, match="attempt_count"):
        SafeWebResult(
            success=False,
            requested_url="https://example.com",
            attempt_count=0,
            error_code="err",
            error_message="msg",
        )

    with pytest.raises(TypeError, match="final_url"):
        SafeWebResult(success=False, requested_url="https://example.com", final_url=123, error_code="err", error_message="msg")  # type: ignore

    with pytest.raises(ValueError, match="final_url"):
        SafeWebResult(
            success=False,
            requested_url="https://example.com",
            final_url="  ",
            error_code="err",
            error_message="msg",
        )

    with pytest.raises(TypeError, match="content_type"):
        SafeWebResult(success=False, requested_url="https://example.com", content_type=123, error_code="err", error_message="msg")  # type: ignore

    with pytest.raises(ValueError, match="content_type"):
        SafeWebResult(
            success=False,
            requested_url="https://example.com",
            content_type="  ",
            error_code="err",
            error_message="msg",
        )

    with pytest.raises(TypeError, match="cleaned_text"):
        SafeWebResult(success=False, requested_url="https://example.com", cleaned_text=123, error_code="err", error_message="msg")  # type: ignore

    with pytest.raises(ValueError, match="elapsed_ms"):
        SafeWebResult(
            success=False,
            requested_url="https://example.com",
            elapsed_ms=-1,
            error_code="err",
            error_message="msg",
        )

    with pytest.raises(ValueError, match="size_bytes"):
        SafeWebResult(
            success=False,
            requested_url="https://example.com",
            size_bytes=-1,
            error_code="err",
            error_message="msg",
        )

    with pytest.raises(ValueError, match="redirect_count"):
        SafeWebResult(
            success=False,
            requested_url="https://example.com",
            redirect_count=-1,
            error_code="err",
            error_message="msg",
        )

    with pytest.raises(ValueError, match="status_code"):
        SafeWebResult(
            success=False,
            requested_url="https://example.com",
            status_code=700,
            error_code="err",
            error_message="msg",
        )

    with pytest.raises(TypeError, match="budget"):
        SafeWebResult(success=False, requested_url="https://example.com", budget="invalid", error_code="err", error_message="msg")  # type: ignore

    with pytest.raises(TypeError, match="robots_status"):
        SafeWebResult(success=False, requested_url="https://example.com", robots_status=123, error_code="err", error_message="msg")  # type: ignore

    with pytest.raises(ValueError, match="robots_status"):
        SafeWebResult(
            success=False,
            requested_url="https://example.com",
            robots_status="invalid_status",
            error_code="err",
            error_message="msg",
        )
