import pytest

from safe_web_access.budgets import CrawlBudget
from safe_web_access.exceptions import ByteBudgetExceededError, PageBudgetExceededError


def test_budgets_valid_initialization():
    budget = CrawlBudget(max_pages=10, max_total_bytes=1000)
    assert budget.max_pages == 10
    assert budget.max_total_bytes == 1000
    assert budget.pages_used == 0
    assert budget.bytes_used == 0
    assert budget.remaining_pages == 10
    assert budget.remaining_bytes == 1000
    assert budget.is_exhausted is False


def test_budgets_record_response_success():
    b1 = CrawlBudget(max_pages=5, max_total_bytes=100)
    b2 = b1.record_response(30)
    assert b2.pages_used == 1
    assert b2.bytes_used == 30
    assert b2.remaining_pages == 4
    assert b2.remaining_bytes == 70
    assert b2.is_exhausted is False


def test_budgets_page_limit_exceeded():
    b1 = CrawlBudget(max_pages=1, max_total_bytes=100)
    b2 = b1.record_response(10)
    assert b2.is_exhausted is True
    with pytest.raises(PageBudgetExceededError):
        b2.ensure_request_allowed()
    with pytest.raises(PageBudgetExceededError):
        b2.record_response(10)


def test_budgets_byte_limit_exceeded():
    b1 = CrawlBudget(max_pages=5, max_total_bytes=50)
    b2 = b1.record_response(50)
    assert b2.is_exhausted is True
    with pytest.raises(ByteBudgetExceededError):
        b2.ensure_request_allowed()
    with pytest.raises(ByteBudgetExceededError):
        b2.record_response(10)


def test_budgets_record_response_limit_exceeded_exceptions():
    b1 = CrawlBudget(max_pages=2, max_total_bytes=100)
    b2 = b1.record_response(10)  # pages_used=1, bytes_used=10
    b3 = b2.record_response(10)  # pages_used=2, bytes_used=20 (at page limit)

    # Next record_response exceeds page limit
    with pytest.raises(PageBudgetExceededError):
        b3.record_response(10)

    b4 = CrawlBudget(max_pages=5, max_total_bytes=30)
    b5 = b4.record_response(20)  # pages_used=1, bytes_used=20
    # Next record_response exceeds byte limit
    with pytest.raises(ByteBudgetExceededError):
        b5.record_response(20)


@pytest.mark.parametrize(
    "kwargs,exc_type",
    [
        ({"max_pages": 0, "max_total_bytes": 100}, ValueError),
        ({"max_pages": -1, "max_total_bytes": 100}, ValueError),
        ({"max_pages": 10, "max_total_bytes": 0}, ValueError),
        ({"max_pages": 10, "max_total_bytes": -50}, ValueError),
        ({"max_pages": "10", "max_total_bytes": 100}, TypeError),
        ({"max_pages": 10, "max_total_bytes": "100"}, TypeError),
        ({"max_pages": True, "max_total_bytes": 100}, TypeError),
        ({"max_pages": 10, "max_total_bytes": True}, TypeError),
        ({"max_pages": 5, "max_total_bytes": 100, "pages_used": -1}, ValueError),
        ({"max_pages": 5, "max_total_bytes": 100, "bytes_used": -1}, ValueError),
        ({"max_pages": 5, "max_total_bytes": 100, "pages_used": 6}, ValueError),
        ({"max_pages": 5, "max_total_bytes": 100, "bytes_used": 101}, ValueError),
    ],
)
def test_budgets_invalid_inputs(kwargs, exc_type):
    with pytest.raises(exc_type):
        CrawlBudget(**kwargs)  # type: ignore


def test_budgets_record_response_invalid_size():
    budget = CrawlBudget(max_pages=5, max_total_bytes=100)
    with pytest.raises(TypeError):
        budget.record_response("30")  # type: ignore
    with pytest.raises(TypeError):
        budget.record_response(True)  # type: ignore
    with pytest.raises(ValueError):
        budget.record_response(-10)
