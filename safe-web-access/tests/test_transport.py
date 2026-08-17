import httpx
import pytest

from safe_web_access.exceptions import (
    MissingRedirectLocationError,
    SafeWebConnectionError,
    SafeWebConnectTimeout,
    SafeWebReadTimeout,
    SafeWebRequestTimeout,
)
from safe_web_access.settings import SafeWebSettings
from safe_web_access.transport import stream_safe_page


@pytest.mark.asyncio
async def test_transport_direct_200(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return httpx.Response(200, text="OK")

    settings = SafeWebSettings()
    timeout = httpx.Timeout(5.0)
    async with httpx.AsyncClient(transport=MockTransport()) as raw_client:
        async with stream_safe_page(
            raw_client, "https://example.com", settings, timeout
        ) as stream:
            assert stream.response.status_code == 200
            assert stream.final_url == "https://example.com"
            assert stream.redirect_count == 0


@pytest.mark.asyncio
async def test_transport_single_redirect(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            if request.url.path == "/":
                return httpx.Response(
                    301, headers={"Location": "https://example.com/target"}
                )
            return httpx.Response(200, text="Target OK")

    settings = SafeWebSettings()
    timeout = httpx.Timeout(5.0)
    async with httpx.AsyncClient(transport=MockTransport()) as raw_client:
        async with stream_safe_page(
            raw_client, "https://example.com/", settings, timeout
        ) as stream:
            assert stream.response.status_code == 200
            assert stream.final_url == "https://example.com/target"
            assert stream.redirect_count == 1


@pytest.mark.asyncio
async def test_transport_missing_location(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return httpx.Response(301, headers={})

    settings = SafeWebSettings()
    timeout = httpx.Timeout(5.0)
    async with httpx.AsyncClient(transport=MockTransport()) as raw_client:
        with pytest.raises(MissingRedirectLocationError):
            async with stream_safe_page(
                raw_client, "https://example.com", settings, timeout
            ):
                pass


@pytest.mark.asyncio
async def test_transport_connect_timeout(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            raise httpx.ConnectTimeout("Connect timeout error")

    settings = SafeWebSettings()
    timeout = httpx.Timeout(5.0)
    async with httpx.AsyncClient(transport=MockTransport()) as raw_client:
        with pytest.raises(SafeWebConnectTimeout):
            async with stream_safe_page(
                raw_client, "https://example.com", settings, timeout
            ):
                pass


@pytest.mark.asyncio
async def test_transport_read_timeout(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            raise httpx.ReadTimeout("Read timeout error")

    settings = SafeWebSettings()
    timeout = httpx.Timeout(5.0)
    async with httpx.AsyncClient(transport=MockTransport()) as raw_client:
        with pytest.raises(SafeWebReadTimeout):
            async with stream_safe_page(
                raw_client, "https://example.com", settings, timeout
            ):
                pass


@pytest.mark.asyncio
async def test_transport_request_timeout(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            raise httpx.TimeoutException("Request timeout error")

    settings = SafeWebSettings()
    timeout = httpx.Timeout(5.0)
    async with httpx.AsyncClient(transport=MockTransport()) as raw_client:
        with pytest.raises(SafeWebRequestTimeout):
            async with stream_safe_page(
                raw_client, "https://example.com", settings, timeout
            ):
                pass


@pytest.mark.asyncio
async def test_transport_connection_error(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            raise httpx.TransportError("Transport error")

    settings = SafeWebSettings()
    timeout = httpx.Timeout(5.0)
    async with httpx.AsyncClient(transport=MockTransport()) as raw_client:
        with pytest.raises(SafeWebConnectionError):
            async with stream_safe_page(
                raw_client, "https://example.com", settings, timeout
            ):
                pass
