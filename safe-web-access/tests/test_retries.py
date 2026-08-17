from dataclasses import FrozenInstanceError

import httpx
import pytest

from safe_web_access import (
    CrawlBudget,
    DomainPolicy,
    RetryPolicy,
    SafeWebClient,
    SafeWebSettings,
)
from safe_web_access.errors import SafeWebErrorCode


def test_retry_policy_defaults_and_validation():
    pol = RetryPolicy()
    assert pol.max_attempts == 1
    assert pol.backoff_base_seconds == 0.5
    assert pol.backoff_max_seconds == 10.0
    assert pol.retry_status_codes == (408, 429, 502, 503, 504)

    with pytest.raises(ValueError):
        RetryPolicy(max_attempts=0)

    with pytest.raises(TypeError):
        RetryPolicy(max_attempts=True)  # type: ignore

    with pytest.raises(ValueError):
        RetryPolicy(backoff_base_seconds=-1)

    with pytest.raises(ValueError):
        RetryPolicy(backoff_multiplier=0.5)

    with pytest.raises(ValueError):
        RetryPolicy(retry_status_codes=(408, 408))

    with pytest.raises(TypeError):
        RetryPolicy(retry_status_codes="408")  # type: ignore

    with pytest.raises(TypeError):
        RetryPolicy(retry_status_codes=(True,))  # type: ignore

    with pytest.raises(ValueError):
        RetryPolicy(retry_status_codes=(99,))

    with pytest.raises(TypeError):
        RetryPolicy(respect_retry_after="yes")  # type: ignore

    with pytest.raises(ValueError):
        RetryPolicy(jitter_seconds=-1.0)

    with pytest.raises(FrozenInstanceError):
        pol.max_attempts = 3  # type: ignore


def test_calculate_delay_exponential_and_retry_after():
    pol = RetryPolicy(
        backoff_base_seconds=1.0,
        backoff_multiplier=2.0,
        backoff_max_seconds=10.0,
        respect_retry_after=True,
    )
    assert pol.calculate_delay(1) == 1.0
    assert pol.calculate_delay(2) == 2.0
    assert pol.calculate_delay(3) == 4.0
    assert pol.calculate_delay(5) == 10.0

    # Retry-After integer header
    headers = {"Retry-After": "5"}
    assert pol.calculate_delay(1, headers) == 5.0

    # Retry-After HTTP date header
    date_headers = {"Retry-After": "Wed, 21 Oct 2035 07:28:00 GMT"}
    assert pol.calculate_delay(1, date_headers) > 0.0

    # Malformed Retry-After falls back safely
    malformed_headers = {"Retry-After": "invalid"}
    assert pol.calculate_delay(1, malformed_headers) == 1.0


def test_retry_policy_jitter():
    pol = RetryPolicy(backoff_base_seconds=1.0, jitter_seconds=0.5)
    delay = pol.calculate_delay(1)
    assert 0.5 <= delay <= 1.5


@pytest.mark.asyncio
async def test_no_retry_by_default(monkeypatch, mock_dns_resolver):
    attempts_count = 0

    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            nonlocal attempts_count
            attempts_count += 1
            return httpx.Response(503, text="Service Unavailable")

    async with httpx.AsyncClient(transport=MockTransport()) as raw_client:
        async with SafeWebClient(client=raw_client) as client:
            res = await client.fetch("https://example.com", check_robots=False)
            assert res.success is False
            assert res.attempt_count == 1
            assert attempts_count == 1


@pytest.mark.asyncio
async def test_retry_success_after_failure(monkeypatch, mock_dns_resolver):
    delays: list[float] = []

    async def fake_sleeper(sec: float) -> None:
        delays.append(sec)

    attempts_count = 0

    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            nonlocal attempts_count
            attempts_count += 1
            if attempts_count == 1:
                return httpx.Response(503, text="Service Unavailable")
            return httpx.Response(
                200, text="<html>Success</html>", headers={"Content-Type": "text/html"}
            )

    retry_pol = RetryPolicy(max_attempts=3, backoff_base_seconds=0.5)
    settings = SafeWebSettings(retry_policy=retry_pol)

    async with httpx.AsyncClient(transport=MockTransport()) as raw_client:
        async with SafeWebClient(
            settings=settings, client=raw_client, sleeper=fake_sleeper
        ) as client:
            res = await client.fetch("https://example.com", check_robots=False)
            assert res.success is True
            assert res.status_code == 200
            assert res.attempt_count == 2
            assert len(delays) == 1
            assert delays[0] == 0.5


@pytest.mark.asyncio
async def test_retry_all_attempts_exhausted(monkeypatch, mock_dns_resolver):
    delays: list[float] = []

    async def fake_sleeper(sec: float) -> None:
        delays.append(sec)

    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return httpx.Response(502, text="Bad Gateway")

    retry_pol = RetryPolicy(
        max_attempts=3, backoff_base_seconds=0.5, backoff_multiplier=2.0
    )
    settings = SafeWebSettings(retry_policy=retry_pol)

    async with httpx.AsyncClient(transport=MockTransport()) as raw_client:
        async with SafeWebClient(
            settings=settings, client=raw_client, sleeper=fake_sleeper
        ) as client:
            res = await client.fetch("https://example.com", check_robots=False)
            assert res.success is False
            assert res.error_code == SafeWebErrorCode.HTTP_ERROR
            assert res.attempt_count == 3
            assert delays == [0.5, 1.0]


@pytest.mark.asyncio
async def test_retry_transport_timeouts_and_connection_errors(
    monkeypatch, mock_dns_resolver
):
    delays: list[float] = []

    async def fake_sleeper(sec: float) -> None:
        delays.append(sec)

    attempts_count = 0

    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            nonlocal attempts_count
            attempts_count += 1
            if attempts_count == 1:
                raise httpx.ConnectTimeout("Connect fail")
            if attempts_count == 2:
                raise httpx.ReadTimeout("Read fail")
            if attempts_count == 3:
                raise httpx.TransportError("Transport fail")
            return httpx.Response(
                200, text="OK", headers={"Content-Type": "text/plain"}
            )

    retry_pol = RetryPolicy(max_attempts=4, backoff_base_seconds=0.1)
    settings = SafeWebSettings(retry_policy=retry_pol)

    async with httpx.AsyncClient(transport=MockTransport()) as raw_client:
        async with SafeWebClient(
            settings=settings, client=raw_client, sleeper=fake_sleeper
        ) as client:
            res = await client.fetch("https://example.com", check_robots=False)
            assert res.success is True
            assert res.attempt_count == 4
            assert len(delays) == 3


@pytest.mark.asyncio
async def test_non_retryable_errors_never_retried(monkeypatch, mock_dns_resolver):
    delays: list[float] = []

    async def fake_sleeper(sec: float) -> None:
        delays.append(sec)

    policy = DomainPolicy(blocked_domains=("example.com",))
    retry_pol = RetryPolicy(max_attempts=3)
    settings = SafeWebSettings(domain_policy=policy, retry_policy=retry_pol)

    async with SafeWebClient(settings=settings, sleeper=fake_sleeper) as client:
        res = await client.fetch("https://example.com", check_robots=False)
        assert res.success is False
        assert res.error_code == SafeWebErrorCode.BLOCKED_DOMAIN
        assert res.attempt_count == 1
        assert len(delays) == 0


@pytest.mark.asyncio
async def test_dns_and_redirects_revalidated_on_every_attempt(monkeypatch):
    dns_check_count = 0

    def mock_resolve(hostname):
        nonlocal dns_check_count
        dns_check_count += 1
        from safe_web_access.networks import NetworkCheckResult, ip_address

        return NetworkCheckResult(hostname, (ip_address("93.184.216.34"),))

    monkeypatch.setattr("safe_web_access.client.resolve_public_addresses", mock_resolve)
    monkeypatch.setattr(
        "safe_web_access.transport.resolve_public_addresses", mock_resolve
    )

    attempts = 0

    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            nonlocal attempts
            attempts += 1
            if attempts == 1:
                return httpx.Response(503, text="Service Unavailable")
            return httpx.Response(
                200, text="OK", headers={"Content-Type": "text/plain"}
            )

    retry_pol = RetryPolicy(max_attempts=2, backoff_base_seconds=0.0)
    settings = SafeWebSettings(retry_policy=retry_pol)

    async with httpx.AsyncClient(transport=MockTransport()) as raw_client:
        async with SafeWebClient(settings=settings, client=raw_client) as client:
            res = await client.fetch("https://example.com", check_robots=False)
            assert res.success is True
            assert res.attempt_count == 2
            assert dns_check_count >= 2


@pytest.mark.asyncio
async def test_budget_only_records_final_accepted_response(
    monkeypatch, mock_dns_resolver
):
    attempts_count = 0

    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            nonlocal attempts_count
            attempts_count += 1
            if attempts_count == 1:
                return httpx.Response(503, text="Service Unavailable")
            return httpx.Response(
                200, text="HTML Data", headers={"Content-Type": "text/html"}
            )

    retry_pol = RetryPolicy(max_attempts=2, retry_status_codes=(503,))
    settings = SafeWebSettings(retry_policy=retry_pol)
    budget = CrawlBudget(max_pages=5, max_total_bytes=1000)

    async with httpx.AsyncClient(transport=MockTransport()) as raw_client:
        async with SafeWebClient(settings=settings, client=raw_client) as client:
            res = await client.fetch(
                "https://example.com", budget=budget, check_robots=False
            )
            assert res.success is True
            assert res.budget is not None
            assert res.budget.pages_used == 1
            assert res.budget.bytes_used == len(b"HTML Data")
