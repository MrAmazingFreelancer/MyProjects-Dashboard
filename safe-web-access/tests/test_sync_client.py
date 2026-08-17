import threading

import httpx
import pytest

from safe_web_access import (
    CrawlBudget,
    DomainPolicy,
    RetryPolicy,
    SafeWebClient,
    SafeWebSettings,
    SyncSafeWebClient,
)
from safe_web_access.errors import SafeWebErrorCode


def test_sync_client_basic_successful_fetch(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return httpx.Response(
                200,
                text="<html>Sync Content</html>",
                headers={"Content-Type": "text/html"},
            )

    raw_client = httpx.AsyncClient(transport=MockTransport())
    with SyncSafeWebClient(client=raw_client) as client:
        res = client.fetch("https://example.com", check_robots=False)
        assert res.success is True
        assert res.status_code == 200
        assert res.body == b"<html>Sync Content</html>"


def test_sync_client_loop_reused_and_thread_terminates(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return httpx.Response(
                200, text="OK", headers={"Content-Type": "text/plain"}
            )

    raw_client = httpx.AsyncClient(transport=MockTransport())
    client = SyncSafeWebClient(client=raw_client)

    initial_loop = client._loop
    thread = client._thread
    assert thread.is_alive() is True

    # Multi-fetch reuse test
    r1 = client.fetch("https://example.com", check_robots=False)
    r2 = client.fetch("https://example.com", check_robots=False)
    r3 = client.fetch("https://example.com", check_robots=False)

    assert r1.success and r2.success and r3.success
    assert client._loop is initial_loop

    # Idempotent close
    client.close()
    client.close()

    assert thread.is_alive() is False

    # Fetch after close returns structured failure
    r_after = client.fetch("https://example.com")
    assert r_after.success is False
    assert r_after.error_message == "Client is closed."

    # Context manager enter when already closed raises RuntimeError
    with pytest.raises(RuntimeError, match="Client is already closed"):
        with client:
            pass


def test_sync_client_no_leaked_threads_on_repeated_cycles(
    monkeypatch, mock_dns_resolver
):
    initial_thread_count = threading.active_count()

    for _ in range(5):
        with SyncSafeWebClient():
            pass

    assert threading.active_count() <= initial_thread_count + 1


def test_sync_client_structured_failure(monkeypatch, mock_dns_resolver):
    policy = DomainPolicy(blocked_domains=("example.com",))
    settings = SafeWebSettings(domain_policy=policy)
    with SyncSafeWebClient(settings=settings) as client:
        res = client.fetch("https://example.com", check_robots=False)
        assert res.success is False
        assert res.error_code == SafeWebErrorCode.BLOCKED_DOMAIN.value


def test_sync_client_domain_policy_support(monkeypatch, mock_dns_resolver):
    policy = DomainPolicy(allowed_domains=("allowed.com",))
    settings = SafeWebSettings(domain_policy=policy)
    with SyncSafeWebClient(settings=settings) as client:
        res_allowed = client.fetch("https://allowed.com", check_robots=False)
        res_blocked = client.fetch("https://forbidden.com", check_robots=False)
        assert res_allowed.error_code != SafeWebErrorCode.DOMAIN_NOT_ALLOWED.value
        assert res_blocked.error_code == SafeWebErrorCode.DOMAIN_NOT_ALLOWED.value


def test_sync_client_retry_support(monkeypatch, mock_dns_resolver):
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
    raw_client = httpx.AsyncClient(transport=MockTransport())

    with SyncSafeWebClient(settings=settings, client=raw_client) as client:
        res = client.fetch("https://example.com", check_robots=False)
        assert res.success is True
        assert res.attempt_count == 2


def test_sync_client_budget_tracking(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return httpx.Response(
                200, text="1234567890", headers={"Content-Type": "text/plain"}
            )

    raw_client = httpx.AsyncClient(transport=MockTransport())
    budget = CrawlBudget(max_pages=2, max_total_bytes=100)

    with SyncSafeWebClient(client=raw_client) as client:
        res1 = client.fetch("https://example.com", budget=budget, check_robots=False)
        assert res1.success is True
        assert res1.budget is not None
        assert res1.budget.pages_used == 1

        res2 = client.fetch(
            "https://example.com", budget=res1.budget, check_robots=False
        )
        assert res2.success is True
        assert res2.budget is not None
        assert res2.budget.pages_used == 2


@pytest.mark.asyncio
async def test_async_and_sync_result_parity(monkeypatch, mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return httpx.Response(
                200, text="Content Parity", headers={"Content-Type": "text/html"}
            )

    raw_client1 = httpx.AsyncClient(transport=MockTransport())
    async with SafeWebClient(client=raw_client1) as async_client:
        async_res = await async_client.fetch("https://example.com", check_robots=False)

    raw_client2 = httpx.AsyncClient(transport=MockTransport())
    with SyncSafeWebClient(client=raw_client2) as sync_client:
        sync_res = sync_client.fetch("https://example.com", check_robots=False)

    assert async_res.success == sync_res.success
    assert async_res.status_code == sync_res.status_code
    assert async_res.content_type == sync_res.content_type
    assert async_res.body == sync_res.body
    assert async_res.attempt_count == sync_res.attempt_count
    assert async_res.redirect_count == sync_res.redirect_count


# ---------------------------------------------------------------------------
# Manual lifecycle: start() / close()
#
# Mirrors the asynchronous client so both surfaces read the same way.
# ---------------------------------------------------------------------------


def test_sync_client_start_returns_same_instance():
    client = SyncSafeWebClient()
    started = client.start()
    assert started is client
    client.close()


def test_sync_client_start_is_idempotent():
    client = SyncSafeWebClient()
    client.start()
    client.start()
    assert client._closed is False
    client.close()


def test_sync_client_start_after_close_raises():
    client = SyncSafeWebClient()
    client.close()
    with pytest.raises(RuntimeError):
        client.start()


def test_sync_client_fetch_works_after_manual_start(mock_dns_resolver):
    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return httpx.Response(
                200,
                text="<html>Sync manual lifecycle</html>",
                headers={"Content-Type": "text/html"},
            )

    raw_client = httpx.AsyncClient(transport=MockTransport())
    client = SyncSafeWebClient(client=raw_client).start()
    try:
        res = client.fetch("https://example.com", check_robots=False)
        assert res.success is True
        assert res.body == b"<html>Sync manual lifecycle</html>"
    finally:
        client.close()
