import asyncio
from pathlib import Path

import safe_web_access
from safe_web_access import (
    CrawlBudget,
    DomainPolicy,
    EventHook,
    RetryPolicy,
    SafeWebClient,
    SafeWebEvent,
    SafeWebEventType,
    SafeWebResult,
    SafeWebSettings,
    SyncSafeWebClient,
    __all__,
    __version__,
)


def test_public_imports():
    assert CrawlBudget is not None
    assert DomainPolicy is not None
    assert RetryPolicy is not None
    assert SafeWebClient is not None
    assert SafeWebResult is not None
    assert SafeWebSettings is not None
    assert SyncSafeWebClient is not None
    assert SafeWebEvent is not None
    assert SafeWebEventType is not None
    assert EventHook is not None
    assert isinstance(__version__, str)


def test_all_exports():
    expected = [
        "CrawlBudget",
        "DomainPolicy",
        "EventHook",
        "RetryPolicy",
        "SafeWebClient",
        "SafeWebEvent",
        "SafeWebEventType",
        "SafeWebResult",
        "SafeWebSettings",
        "SyncSafeWebClient",
        "__version__",
    ]
    for item in expected:
        assert item in __all__


def test_py_typed_exists():
    pkg_dir = Path(safe_web_access.__file__).parent
    py_typed = pkg_dir / "py.typed"
    assert py_typed.exists()


def test_import_side_effects():
    # Verify importing does not create event loops or network activity
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    assert loop is None


def test_lifecycle_methods_are_public_on_both_clients():
    """start/close/aclose must be part of the documented surface, not private helpers."""
    for name in ("start", "close", "aclose", "fetch"):
        assert callable(getattr(SafeWebClient, name, None)), f"SafeWebClient.{name}"

    for name in ("start", "close", "fetch"):
        assert callable(
            getattr(SyncSafeWebClient, name, None)
        ), f"SyncSafeWebClient.{name}"


def test_long_lived_service_wrapper_pattern(mock_dns_resolver):
    """Regression test for the integration pattern that motivated 0.1.2.

    A service object that builds the client lazily, keeps it for the process
    lifetime and closes it on shutdown must work without an ``async with`` block.
    Before 0.1.2 this raised ``AttributeError: 'SafeWebClient' object has no
    attribute 'start'`` on the very first call.

    Uses the mocked resolver so the suite stays offline.
    """

    import httpx

    class WebAccessService:
        def __init__(self) -> None:
            self._client: SafeWebClient | None = None

        async def start(self) -> None:
            if self._client is not None:
                return
            transport = httpx.MockTransport(
                lambda request: httpx.Response(
                    200,
                    text="<html>service ok</html>",
                    headers={"Content-Type": "text/html"},
                )
            )
            self._client = SafeWebClient(client=httpx.AsyncClient(transport=transport))
            await self._client.start()

        async def close(self) -> None:
            if self._client is None:
                return
            await self._client.close()
            self._client = None

        async def fetch(self, url: str) -> SafeWebResult:
            if self._client is None:
                await self.start()
            assert self._client is not None
            return await self._client.fetch(url, check_robots=False)

    async def run() -> SafeWebResult:
        service = WebAccessService()
        try:
            return await service.fetch("https://example.com")
        finally:
            await service.close()

    result = asyncio.run(run())
    assert result.success is True
    assert result.body == b"<html>service ok</html>"
