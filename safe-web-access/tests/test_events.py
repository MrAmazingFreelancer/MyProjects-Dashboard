import httpx
import pytest

from safe_web_access import (
    RetryPolicy,
    SafeWebClient,
    SafeWebEvent,
    SafeWebEventType,
    SafeWebSettings,
    SyncSafeWebClient,
)
from safe_web_access.exceptions import SafeWebError


def test_events_post_init_validation():
    with pytest.raises(TypeError, match="attempt_number"):
        SafeWebEvent(event_type=SafeWebEventType.REQUEST_STARTED, requested_url="u", attempt_number=True)  # type: ignore

    with pytest.raises(ValueError, match="attempt_number"):
        SafeWebEvent(
            event_type=SafeWebEventType.REQUEST_STARTED,
            requested_url="u",
            attempt_number=0,
        )

    with pytest.raises(TypeError, match="redirect_count"):
        SafeWebEvent(event_type=SafeWebEventType.REQUEST_STARTED, requested_url="u", redirect_count=True)  # type: ignore

    with pytest.raises(ValueError, match="redirect_count"):
        SafeWebEvent(
            event_type=SafeWebEventType.REQUEST_STARTED,
            requested_url="u",
            redirect_count=-1,
        )

    with pytest.raises(TypeError, match="elapsed_ms"):
        SafeWebEvent(event_type=SafeWebEventType.REQUEST_STARTED, requested_url="u", elapsed_ms=True)  # type: ignore

    with pytest.raises(ValueError, match="elapsed_ms"):
        SafeWebEvent(
            event_type=SafeWebEventType.REQUEST_STARTED,
            requested_url="u",
            elapsed_ms=-1,
        )

    with pytest.raises(TypeError, match="size_bytes"):
        SafeWebEvent(event_type=SafeWebEventType.REQUEST_STARTED, requested_url="u", size_bytes=True)  # type: ignore

    with pytest.raises(ValueError, match="size_bytes"):
        SafeWebEvent(
            event_type=SafeWebEventType.REQUEST_STARTED,
            requested_url="u",
            size_bytes=-1,
        )


@pytest.mark.asyncio
async def test_events_sync_and_async_hooks_and_order(monkeypatch, mock_dns_resolver):
    events_log: list[str] = []

    def sync_hook(event: SafeWebEvent) -> None:
        events_log.append(f"sync:{event.event_type}:{event.attempt_number}")

    async def async_hook(event: SafeWebEvent) -> None:
        events_log.append(f"async:{event.event_type}:{event.attempt_number}")

    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return httpx.Response(
                200, text="Content", headers={"Content-Type": "text/html"}
            )

    raw_client = httpx.AsyncClient(transport=MockTransport())
    async with SafeWebClient(
        client=raw_client, event_hooks=(sync_hook, async_hook)
    ) as client:
        res = await client.fetch("https://example.com", check_robots=False)
        assert res.success is True
        assert len(events_log) > 0
        assert events_log[0] == "sync:request_started:1"
        assert events_log[1] == "async:request_started:1"


@pytest.mark.asyncio
async def test_events_full_successful_and_failure_sequence(
    monkeypatch, mock_dns_resolver
):
    captured_types: list[str] = []

    def event_collector(event: SafeWebEvent) -> None:
        captured_types.append(event.event_type)

    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return httpx.Response(
                200, text="HTML", headers={"Content-Type": "text/html"}
            )

    raw_client = httpx.AsyncClient(transport=MockTransport())
    async with SafeWebClient(
        client=raw_client, event_hooks=(event_collector,)
    ) as client:
        res = await client.fetch("https://example.com", check_robots=False)
        assert res.success is True
        assert SafeWebEventType.REQUEST_STARTED in captured_types
        assert SafeWebEventType.ATTEMPT_STARTED in captured_types
        assert SafeWebEventType.URL_VALIDATED in captured_types
        assert SafeWebEventType.POLICY_VALIDATED in captured_types
        assert SafeWebEventType.NETWORK_VALIDATED in captured_types
        assert SafeWebEventType.BUDGET_VALIDATED in captured_types
        assert SafeWebEventType.RESPONSE_HEADERS_VALIDATED in captured_types
        assert SafeWebEventType.RESPONSE_BODY_READ in captured_types
        assert SafeWebEventType.REQUEST_SUCCEEDED in captured_types


@pytest.mark.asyncio
async def test_events_redirect_retry_and_robots(monkeypatch, mock_dns_resolver):
    captured_types: list[str] = []

    def event_collector(event: SafeWebEvent) -> None:
        captured_types.append(event.event_type)

    attempts = 0

    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            nonlocal attempts
            attempts += 1
            if request.url.path == "/robots.txt":
                return httpx.Response(200, text="User-agent: *\nAllow: /\n")
            if request.url.path == "/page1":
                return httpx.Response(
                    301, headers={"Location": "https://example.com/page2"}
                )
            if request.url.path == "/page2" and attempts <= 3:
                return httpx.Response(503, text="Service Unavailable")
            return httpx.Response(
                200, text="OK", headers={"Content-Type": "text/plain"}
            )

    retry_pol = RetryPolicy(max_attempts=3, backoff_base_seconds=0.0)
    settings = SafeWebSettings(retry_policy=retry_pol)

    async with httpx.AsyncClient(transport=MockTransport()) as raw_client:
        async with SafeWebClient(
            settings=settings, client=raw_client, event_hooks=(event_collector,)
        ) as client:
            res = await client.fetch("https://example.com/page1", check_robots=True)
            assert res.success is True
            assert SafeWebEventType.ROBOTS_CHECKED in captured_types
            assert SafeWebEventType.REDIRECT_FOLLOWED in captured_types
            assert SafeWebEventType.RETRY_SCHEDULED in captured_types


@pytest.mark.asyncio
async def test_events_safe_metadata_privacy(monkeypatch, mock_dns_resolver):
    captured_events: list[SafeWebEvent] = []

    def sync_hook(event: SafeWebEvent) -> None:
        captured_events.append(event)

    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return httpx.Response(
                200, text="Secret Content", headers={"Authorization": "Bearer secret"}
            )

    raw_client = httpx.AsyncClient(transport=MockTransport())
    async with SafeWebClient(client=raw_client, event_hooks=(sync_hook,)) as client:
        res = await client.fetch("https://example.com", check_robots=False)
        assert res.success is True

    for evt in captured_events:
        event_str = f"{evt.event_type} {evt.requested_url} {evt.current_url} {evt.message} {evt.error_code}"
        assert "Secret Content" not in event_str
        assert "Bearer secret" not in event_str


@pytest.mark.asyncio
async def test_events_isolated_hook_failure(monkeypatch, mock_dns_resolver):
    captured: list[str] = []

    def broken_hook(event: SafeWebEvent) -> None:
        raise RuntimeError("Hook crashed!")

    def working_hook(event: SafeWebEvent) -> None:
        captured.append(event.event_type)

    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return httpx.Response(
                200, text="OK", headers={"Content-Type": "text/plain"}
            )

    raw_client = httpx.AsyncClient(transport=MockTransport())
    async with SafeWebClient(
        client=raw_client, event_hooks=(broken_hook, working_hook)
    ) as client:
        res = await client.fetch("https://example.com", check_robots=False)
        assert res.success is True
        assert len(captured) > 0


@pytest.mark.asyncio
async def test_events_strict_event_hooks_failure(monkeypatch, mock_dns_resolver):
    def broken_hook(event: SafeWebEvent) -> None:
        if event.event_type == SafeWebEventType.REQUEST_STARTED:
            raise RuntimeError("Hook failure in strict mode!")

    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return httpx.Response(
                200, text="OK", headers={"Content-Type": "text/plain"}
            )

    raw_client = httpx.AsyncClient(transport=MockTransport())
    settings = SafeWebSettings(strict_event_hooks=True)
    async with SafeWebClient(
        settings=settings, client=raw_client, event_hooks=(broken_hook,)
    ) as client:
        with pytest.raises(SafeWebError, match="Event hook failed"):
            await client.fetch("https://example.com", check_robots=False)


@pytest.mark.asyncio
async def test_events_async_hook_failure_strict(monkeypatch, mock_dns_resolver):
    async def broken_async_hook(event: SafeWebEvent) -> None:
        if event.event_type == SafeWebEventType.REQUEST_STARTED:
            raise RuntimeError("Async hook failure!")

    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return httpx.Response(
                200, text="OK", headers={"Content-Type": "text/plain"}
            )

    raw_client = httpx.AsyncClient(transport=MockTransport())
    settings = SafeWebSettings(strict_event_hooks=True)
    async with SafeWebClient(
        settings=settings, client=raw_client, event_hooks=(broken_async_hook,)
    ) as client:
        with pytest.raises(SafeWebError, match="Event hook failed"):
            await client.fetch("https://example.com", check_robots=False)


def test_sync_client_event_hooks(monkeypatch, mock_dns_resolver):
    events: list[str] = []

    def hook(evt: SafeWebEvent) -> None:
        events.append(evt.event_type)

    class MockTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request):
            return httpx.Response(
                200, text="OK", headers={"Content-Type": "text/plain"}
            )

    raw_client = httpx.AsyncClient(transport=MockTransport())
    with SyncSafeWebClient(client=raw_client, event_hooks=(hook,)) as client:
        res = client.fetch("https://example.com", check_robots=False)
        assert res.success is True
        assert len(events) > 0
        assert SafeWebEventType.REQUEST_STARTED in events
