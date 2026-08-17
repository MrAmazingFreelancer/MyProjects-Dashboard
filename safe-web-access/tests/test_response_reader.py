import httpx
import pytest

from safe_web_access.budgets import CrawlBudget
from safe_web_access.exceptions import (
    ByteBudgetExceededError,
    ResponseTooLargeError,
    UnsupportedContentTypeError,
)
from safe_web_access.response_reader import ReadResponseResult, read_response_body
from safe_web_access.settings import SafeWebSettings


class DummyStream(httpx.AsyncByteStream):
    def __init__(self, chunks):
        self._chunks = chunks

    async def __aiter__(self):
        for chunk in self._chunks:
            yield chunk


@pytest.mark.asyncio
async def test_response_reader_success_html():
    settings = SafeWebSettings(max_response_bytes=100)
    budget = CrawlBudget(max_pages=5, max_total_bytes=1000)
    response = httpx.Response(
        200, headers={"Content-Type": "text/html"}, content=b"<html>Hello</html>"
    )

    res = await read_response_body(response, settings, budget)
    assert res.content_type == "text/html"
    assert res.body == b"<html>Hello</html>"
    assert res.size_bytes == 18


@pytest.mark.asyncio
async def test_response_reader_unsupported_content_type():
    settings = SafeWebSettings(allowed_content_types=("text/html",))
    budget = CrawlBudget(max_pages=5, max_total_bytes=1000)
    response = httpx.Response(
        200, headers={"Content-Type": "image/png"}, content=b"fake png"
    )

    with pytest.raises(UnsupportedContentTypeError):
        await read_response_body(response, settings, budget)


@pytest.mark.asyncio
async def test_response_reader_no_content_length_header():
    settings = SafeWebSettings(max_response_bytes=100)
    budget = CrawlBudget(max_pages=5, max_total_bytes=1000)
    response = httpx.Response(
        200, headers={"Content-Type": "text/html"}, content=b"No content length header"
    )

    res = await read_response_body(response, settings, budget)
    assert res.body == b"No content length header"
    assert res.size_bytes == 24


@pytest.mark.asyncio
async def test_response_reader_duplicate_identical_content_length_headers():
    settings = SafeWebSettings(max_response_bytes=100)
    budget = CrawlBudget(max_pages=5, max_total_bytes=1000)
    response = httpx.Response(
        200,
        headers={"Content-Type": "text/html", "Content-Length": "18, 18"},
        content=b"<html>Hello</html>",
    )

    res = await read_response_body(response, settings, budget)
    assert res.size_bytes == 18


@pytest.mark.asyncio
async def test_response_reader_malformed_content_length_header():
    settings = SafeWebSettings(max_response_bytes=100)
    budget = CrawlBudget(max_pages=5, max_total_bytes=1000)
    response = httpx.Response(
        200,
        headers={"Content-Type": "text/html", "Content-Length": "invalid_number"},
        content=b"Hello",
    )

    res = await read_response_body(response, settings, budget)
    assert res.body == b"Hello"
    assert res.size_bytes == 5


@pytest.mark.asyncio
async def test_response_reader_stream_with_empty_chunks():
    settings = SafeWebSettings(max_response_bytes=100)
    budget = CrawlBudget(max_pages=5, max_total_bytes=1000)
    response = httpx.Response(
        200,
        headers={"Content-Type": "text/html"},
        stream=DummyStream([b"", b"Hello", b"", b" World", b""]),
    )

    res = await read_response_body(response, settings, budget)
    assert res.body == b"Hello World"
    assert res.size_bytes == 11


@pytest.mark.asyncio
async def test_response_reader_declared_content_length_too_large():
    settings = SafeWebSettings(max_response_bytes=50)
    budget = CrawlBudget(max_pages=5, max_total_bytes=1000)
    response = httpx.Response(
        200,
        headers={"Content-Type": "text/html", "Content-Length": "100"},
        content=b"",
    )

    with pytest.raises(ResponseTooLargeError, match="Declared Content-Length exceeds"):
        await read_response_body(response, settings, budget)


@pytest.mark.asyncio
async def test_response_reader_streamed_body_too_large():
    settings = SafeWebSettings(max_response_bytes=10)
    budget = CrawlBudget(max_pages=5, max_total_bytes=1000)
    response = httpx.Response(
        200, headers={"Content-Type": "text/html"}, content=b"123456789012345"
    )

    with pytest.raises(ResponseTooLargeError):
        await read_response_body(response, settings, budget)


@pytest.mark.asyncio
async def test_response_reader_streamed_body_too_large_no_content_length():
    settings = SafeWebSettings(max_response_bytes=10)
    budget = CrawlBudget(max_pages=5, max_total_bytes=1000)
    response = httpx.Response(
        200,
        headers={"Content-Type": "text/html"},
        stream=DummyStream([b"123456789012345"]),
    )

    with pytest.raises(ResponseTooLargeError):
        await read_response_body(response, settings, budget)


@pytest.mark.asyncio
async def test_response_reader_streamed_body_exceeds_budget():
    settings = SafeWebSettings(max_response_bytes=100)
    budget = CrawlBudget(max_pages=5, max_total_bytes=15)
    response = httpx.Response(
        200, headers={"Content-Type": "text/html"}, content=b"12345678901234567890"
    )

    with pytest.raises(ByteBudgetExceededError):
        await read_response_body(response, settings, budget)


@pytest.mark.asyncio
async def test_response_reader_streamed_body_exceeds_budget_no_content_length():
    settings = SafeWebSettings(max_response_bytes=100)
    budget = CrawlBudget(max_pages=5, max_total_bytes=15)
    response = httpx.Response(
        200,
        headers={"Content-Type": "text/html"},
        stream=DummyStream([b"12345678901234567890"]),
    )

    with pytest.raises(ByteBudgetExceededError):
        await read_response_body(response, settings, budget)


@pytest.mark.asyncio
async def test_response_reader_conflicting_content_length_headers():
    settings = SafeWebSettings()
    budget = CrawlBudget(max_pages=5, max_total_bytes=1000)
    response = httpx.Response(
        200,
        headers={"Content-Type": "text/html", "Content-Length": "100, 200"},
        content=b"",
    )

    with pytest.raises(
        ResponseTooLargeError, match="Conflicting duplicate Content-Length headers"
    ):
        await read_response_body(response, settings, budget)


@pytest.mark.asyncio
async def test_response_reader_negative_content_length_header():
    settings = SafeWebSettings()
    budget = CrawlBudget(max_pages=5, max_total_bytes=1000)
    response = httpx.Response(
        200,
        headers={"Content-Type": "text/html", "Content-Length": "-50"},
        content=b"",
    )

    with pytest.raises(ResponseTooLargeError, match="Negative Content-Length header"):
        await read_response_body(response, settings, budget)


@pytest.mark.asyncio
async def test_response_reader_declared_content_length_exceeds_budget():
    settings = SafeWebSettings(max_response_bytes=100)
    budget = CrawlBudget(max_pages=5, max_total_bytes=30)
    response = httpx.Response(
        200,
        headers={"Content-Type": "text/html", "Content-Length": "50"},
        content=b"",
    )

    with pytest.raises(
        ByteBudgetExceededError, match="exceeds remaining crawl byte budget"
    ):
        await read_response_body(response, settings, budget)


def test_read_response_result_post_init_validation():
    with pytest.raises(ValueError, match=r"len\(body\) must equal size_bytes"):
        ReadResponseResult(content_type="text/html", body=b"12345", size_bytes=10)
