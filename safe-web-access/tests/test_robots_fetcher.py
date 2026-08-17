import httpx
import pytest

from safe_web_access.policies import DomainPolicy
from safe_web_access.robots import RobotsStatus
from safe_web_access.robots_fetcher import fetch_robots_advisory
from safe_web_access.settings import SafeWebSettings


@pytest.mark.asyncio
async def test_robots_fetcher_allow(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            assert request.url.path == "/robots.txt"
            return httpx.Response(200, text="User-agent: *\nAllow: /\n")

    settings = SafeWebSettings()
    timeout = httpx.Timeout(5.0)
    async with httpx.AsyncClient(transport=MockTransport()) as raw_client:
        res = await fetch_robots_advisory(
            raw_client, "https://example.com/page", settings, timeout
        )
        assert res.status == RobotsStatus.ALLOWED
        assert res.allowed is True


@pytest.mark.asyncio
async def test_robots_fetcher_disallow(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return httpx.Response(200, text="User-agent: *\nDisallow: /page\n")

    settings = SafeWebSettings()
    timeout = httpx.Timeout(5.0)
    async with httpx.AsyncClient(transport=MockTransport()) as raw_client:
        res = await fetch_robots_advisory(
            raw_client, "https://example.com/page", settings, timeout
        )
        assert res.status == RobotsStatus.DISALLOWED
        assert res.allowed is False


@pytest.mark.asyncio
async def test_robots_fetcher_404_returns_missing(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return httpx.Response(404, text="Not Found")

    settings = SafeWebSettings()
    timeout = httpx.Timeout(5.0)
    async with httpx.AsyncClient(transport=MockTransport()) as raw_client:
        res = await fetch_robots_advisory(
            raw_client, "https://example.com/page", settings, timeout
        )
        assert res.status == RobotsStatus.MISSING
        assert res.allowed is None


@pytest.mark.asyncio
async def test_robots_fetcher_500_returns_unreachable(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return httpx.Response(500, text="Server Error")

    settings = SafeWebSettings()
    timeout = httpx.Timeout(5.0)
    async with httpx.AsyncClient(transport=MockTransport()) as raw_client:
        res = await fetch_robots_advisory(
            raw_client, "https://example.com/page", settings, timeout
        )
        assert res.status == RobotsStatus.UNREACHABLE
        assert res.allowed is None


@pytest.mark.asyncio
async def test_robots_fetcher_dns_failure(monkeypatch):
    def dummy_resolve_fail(host):
        from safe_web_access.exceptions import DnsResolutionError

        raise DnsResolutionError("DNS fail")

    monkeypatch.setattr(
        "safe_web_access.robots_fetcher.resolve_public_addresses", dummy_resolve_fail
    )
    settings = SafeWebSettings()
    timeout = httpx.Timeout(5.0)
    async with httpx.AsyncClient() as raw_client:
        res = await fetch_robots_advisory(
            raw_client, "https://example.com/page", settings, timeout
        )
        assert res.status == RobotsStatus.UNREACHABLE


@pytest.mark.asyncio
async def test_robots_fetcher_redirect_missing_location(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return httpx.Response(301, headers={})

    settings = SafeWebSettings()
    timeout = httpx.Timeout(5.0)
    async with httpx.AsyncClient(transport=MockTransport()) as raw_client:
        res = await fetch_robots_advisory(
            raw_client, "https://example.com/page", settings, timeout
        )
        assert res.status == RobotsStatus.UNREACHABLE


@pytest.mark.asyncio
async def test_robots_fetcher_successful_redirect(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            if request.url.path == "/robots.txt":
                return httpx.Response(
                    301, headers={"Location": "https://example.com/alt-robots.txt"}
                )
            if request.url.path == "/alt-robots.txt":
                return httpx.Response(200, text="User-agent: *\nDisallow: /page\n")
            return httpx.Response(404)

    settings = SafeWebSettings()
    timeout = httpx.Timeout(5.0)
    async with httpx.AsyncClient(transport=MockTransport()) as raw_client:
        res = await fetch_robots_advisory(
            raw_client, "https://example.com/page", settings, timeout
        )
        assert res.status == RobotsStatus.DISALLOWED
        assert res.allowed is False


@pytest.mark.asyncio
async def test_robots_fetcher_unsafe_redirect(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return httpx.Response(
                301, headers={"Location": "http://127.0.0.1/robots.txt"}
            )

    settings = SafeWebSettings()
    timeout = httpx.Timeout(5.0)
    async with httpx.AsyncClient(transport=MockTransport()) as raw_client:
        res = await fetch_robots_advisory(
            raw_client, "https://example.com/page", settings, timeout
        )
        assert res.status == RobotsStatus.UNREACHABLE


@pytest.mark.asyncio
async def test_robots_fetcher_domain_policy_allowed(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return httpx.Response(200, text="User-agent: *\nAllow: /\n")

    policy = DomainPolicy(allowed_domains=("example.com",))
    settings = SafeWebSettings(domain_policy=policy)
    timeout = httpx.Timeout(5.0)
    async with httpx.AsyncClient(transport=MockTransport()) as raw_client:
        res = await fetch_robots_advisory(
            raw_client, "https://example.com/page", settings, timeout
        )
        assert res.status == RobotsStatus.ALLOWED


@pytest.mark.asyncio
async def test_robots_fetcher_policy_rejection(monkeypatch, mock_dns_resolver):
    policy = DomainPolicy(blocked_domains=("example.com",))
    settings = SafeWebSettings(domain_policy=policy)
    timeout = httpx.Timeout(5.0)
    async with httpx.AsyncClient() as raw_client:
        res = await fetch_robots_advisory(
            raw_client, "https://example.com/page", settings, timeout
        )
        assert res.status == RobotsStatus.UNREACHABLE


@pytest.mark.asyncio
async def test_robots_fetcher_too_large(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return httpx.Response(200, text="A" * 300_000)

    settings = SafeWebSettings()
    timeout = httpx.Timeout(5.0)
    async with httpx.AsyncClient(transport=MockTransport()) as raw_client:
        res = await fetch_robots_advisory(
            raw_client, "https://example.com/page", settings, timeout
        )
        assert res.status == RobotsStatus.UNREACHABLE


@pytest.mark.asyncio
async def test_robots_fetcher_transport_exception(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            raise httpx.ConnectTimeout("Connect timeout")

    settings = SafeWebSettings()
    timeout = httpx.Timeout(5.0)
    async with httpx.AsyncClient(transport=MockTransport()) as raw_client:
        res = await fetch_robots_advisory(
            raw_client, "https://example.com/page", settings, timeout
        )
        assert res.status == RobotsStatus.UNREACHABLE
