import httpx
import pytest

from safe_web_access import CrawlBudget, DomainPolicy, SafeWebClient, SafeWebSettings
from safe_web_access.errors import SafeWebErrorCode
from safe_web_access.robots import RobotsStatus


@pytest.mark.asyncio
async def test_client_basic_fetch_success(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return httpx.Response(
                200,
                text="<html>Content</html>",
                headers={"Content-Type": "text/html"},
            )

    raw_client = httpx.AsyncClient(transport=MockTransport())
    async with SafeWebClient(client=raw_client) as client:
        res = await client.fetch("https://example.com", check_robots=False)
        assert res.success is True
        assert res.status_code == 200
        assert res.body == b"<html>Content</html>"


@pytest.mark.asyncio
async def test_client_default_settings_and_owned_transport():
    async with SafeWebClient() as client:
        assert isinstance(client._settings, SafeWebSettings)


@pytest.mark.asyncio
async def test_client_network_resolution_failure(monkeypatch):
    def dummy_resolve_fail(host):
        from safe_web_access.exceptions import DnsResolutionError

        raise DnsResolutionError("DNS resolution failed")

    monkeypatch.setattr(
        "safe_web_access.client.resolve_public_addresses", dummy_resolve_fail
    )
    async with SafeWebClient() as client:
        res = await client.fetch("https://example.com", check_robots=False)
        assert res.success is False
        assert res.error_code == SafeWebErrorCode.DNS_RESOLUTION_FAILED.value


@pytest.mark.asyncio
async def test_client_domain_policy_rejection():
    pol = DomainPolicy(blocked_domains=("example.com",))
    settings = SafeWebSettings(domain_policy=pol)
    async with SafeWebClient(settings=settings) as client:
        res = await client.fetch("https://example.com", check_robots=False)
        assert res.success is False
        assert res.error_code == SafeWebErrorCode.BLOCKED_DOMAIN.value


@pytest.mark.asyncio
async def test_client_budget_exhausted(monkeypatch):
    budget = CrawlBudget(max_pages=1, max_total_bytes=1000)
    budget = budget.record_response(10)

    call_count = 0

    def dummy_resolve(hostname):
        nonlocal call_count
        call_count += 1
        from ipaddress import ip_address

        from safe_web_access.networks import NetworkCheckResult

        return NetworkCheckResult(
            hostname=hostname, addresses=(ip_address("93.184.216.34"),)
        )

    monkeypatch.setattr(
        "safe_web_access.client.resolve_public_addresses", dummy_resolve
    )

    async with SafeWebClient() as client:
        res = await client.fetch(
            "https://example.com", budget=budget, check_robots=False
        )
        assert res.success is False
        assert res.error_code == SafeWebErrorCode.PAGE_BUDGET_EXCEEDED.value
        assert call_count == 1


@pytest.mark.asyncio
async def test_client_robots_disallowed(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            if "robots.txt" in str(request.url):
                return httpx.Response(
                    200,
                    text="User-agent: *\nDisallow: /page\n",
                    headers={"Content-Type": "text/plain"},
                )
            return httpx.Response(
                200, text="Content", headers={"Content-Type": "text/html"}
            )

    raw_client = httpx.AsyncClient(transport=MockTransport())
    settings = SafeWebSettings(user_agent="MyBot/1.0")
    async with SafeWebClient(settings=settings, client=raw_client) as client:
        res = await client.fetch("https://example.com/page", check_robots=True)
        assert res.success is True
        assert res.robots_status == RobotsStatus.DISALLOWED.value


@pytest.mark.asyncio
async def test_client_status_408_read_timeout_mapping(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return httpx.Response(408, text="Request Timeout")

    raw_client = httpx.AsyncClient(transport=MockTransport())
    async with SafeWebClient(client=raw_client) as client:
        res = await client.fetch("https://example.com", check_robots=False)
        assert res.success is False
        assert res.error_code == SafeWebErrorCode.READ_TIMEOUT.value


@pytest.mark.asyncio
async def test_client_status_413_response_too_large_mapping(
    monkeypatch, mock_dns_resolver
):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return httpx.Response(413, text="Payload Too Large")

    raw_client = httpx.AsyncClient(transport=MockTransport())
    async with SafeWebClient(client=raw_client) as client:
        res = await client.fetch("https://example.com", check_robots=False)
        assert res.success is False
        assert res.error_code == SafeWebErrorCode.RESPONSE_TOO_LARGE.value


@pytest.mark.asyncio
async def test_client_connect_timeout_handling(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            raise httpx.ConnectTimeout("Connect timeout error")

    raw_client = httpx.AsyncClient(transport=MockTransport())
    async with SafeWebClient(client=raw_client) as client:
        res = await client.fetch("https://example.com", check_robots=False)
        assert res.success is False
        assert res.error_code == SafeWebErrorCode.CONNECTION_TIMEOUT.value


@pytest.mark.asyncio
async def test_client_read_timeout_handling(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            raise httpx.ReadTimeout("Read timeout error")

    raw_client = httpx.AsyncClient(transport=MockTransport())
    async with SafeWebClient(client=raw_client) as client:
        res = await client.fetch("https://example.com", check_robots=False)
        assert res.success is False
        assert res.error_code == SafeWebErrorCode.READ_TIMEOUT.value


@pytest.mark.asyncio
async def test_client_request_timeout_handling(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            raise httpx.TimeoutException("Generic timeout error")

    raw_client = httpx.AsyncClient(transport=MockTransport())
    async with SafeWebClient(client=raw_client) as client:
        res = await client.fetch("https://example.com", check_robots=False)
        assert res.success is False
        assert res.error_code == SafeWebErrorCode.CONNECTION_TIMEOUT.value


@pytest.mark.asyncio
async def test_client_connection_error_handling(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            raise httpx.TransportError("Transport connection error")

    raw_client = httpx.AsyncClient(transport=MockTransport())
    async with SafeWebClient(client=raw_client) as client:
        res = await client.fetch("https://example.com", check_robots=False)
        assert res.success is False
        assert res.error_code == SafeWebErrorCode.REQUEST_FAILED.value


@pytest.mark.asyncio
async def test_client_invalid_url(monkeypatch):
    async with SafeWebClient() as client:
        res = await client.fetch("ftp://example.com", check_robots=False)
        assert res.success is False
        assert res.error_code == SafeWebErrorCode.UNSUPPORTED_SCHEME.value


@pytest.mark.asyncio
async def test_client_aclose():
    client = SafeWebClient()
    await client.aclose()
    await client.aclose()


# ---------------------------------------------------------------------------
# Manual lifecycle: start() / close()
#
# These cover the pattern used by callers that hold a long-lived client instead
# of an "async with" block, e.g. a service object that builds the client once and
# closes it on shutdown.
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_client_start_returns_same_instance():
    client = SafeWebClient()
    started = await client.start()
    assert started is client
    await client.close()


@pytest.mark.asyncio
async def test_client_start_is_idempotent():
    client = SafeWebClient()
    await client.start()
    await client.start()
    assert client._closed is False
    await client.close()


@pytest.mark.asyncio
async def test_client_start_after_close_raises():
    client = SafeWebClient()
    await client.close()
    with pytest.raises(RuntimeError):
        await client.start()


@pytest.mark.asyncio
async def test_client_close_is_idempotent_and_matches_aclose():
    client = SafeWebClient()
    await client.close()
    await client.close()
    await client.aclose()
    assert client._closed is True


@pytest.mark.asyncio
async def test_client_fetch_works_after_manual_start(mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return httpx.Response(
                200,
                text="<html>Manual lifecycle</html>",
                headers={"Content-Type": "text/html"},
            )

    raw_client = httpx.AsyncClient(transport=MockTransport())
    client = await SafeWebClient(client=raw_client).start()
    try:
        res = await client.fetch("https://example.com", check_robots=False)
        assert res.success is True
        assert res.body == b"<html>Manual lifecycle</html>"
    finally:
        await client.close()


@pytest.mark.asyncio
async def test_client_close_does_not_close_injected_transport():
    raw_client = httpx.AsyncClient(
        transport=httpx.MockTransport(lambda r: httpx.Response(200))
    )
    client = await SafeWebClient(client=raw_client).start()
    await client.close()

    assert client._owned_client is False
    assert raw_client.is_closed is False
    await raw_client.aclose()


@pytest.mark.asyncio
async def test_client_close_closes_owned_transport():
    client = SafeWebClient()
    internal = client._client
    await client.close()

    assert client._owned_client is True
    assert internal.is_closed is True


@pytest.mark.asyncio
async def test_client_fetch_after_close_returns_failure_not_raise():
    client = SafeWebClient()
    await client.close()
    res = await client.fetch("https://example.com", check_robots=False)
    assert res.success is False
    assert res.error_code == SafeWebErrorCode.REQUEST_FAILED.value
