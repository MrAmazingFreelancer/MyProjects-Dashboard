from ipaddress import ip_address
from pathlib import Path

import httpx
import pytest

from safe_web_access.budgets import CrawlBudget
from safe_web_access.networks import NetworkCheckResult
from safe_web_access.settings import SafeWebSettings

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def default_settings() -> SafeWebSettings:
    """Returns standard default settings."""
    return SafeWebSettings()


@pytest.fixture
def tiny_settings() -> SafeWebSettings:
    """Returns strict small settings for testing limits."""
    return SafeWebSettings(
        connect_timeout_seconds=2,
        read_timeout_seconds=2,
        max_redirects=2,
        max_response_bytes=50,
        max_pages=2,
        max_total_bytes=100,
    )


@pytest.fixture
def initial_budget() -> CrawlBudget:
    """Returns an initial fresh crawl budget."""
    return CrawlBudget(max_pages=5, max_total_bytes=1000)


@pytest.fixture
def mock_public_ip_result() -> NetworkCheckResult:
    """Returns a valid public IPv4 resolution result."""
    return NetworkCheckResult(
        hostname="example.com",
        addresses=(ip_address("93.184.216.34"),),
    )


@pytest.fixture
def mock_public_ipv6_result() -> NetworkCheckResult:
    """Returns a valid public IPv6 resolution result."""
    return NetworkCheckResult(
        hostname="example.com",
        addresses=(ip_address("2606:2800:220:1:248:1893:25c8:1946"),),
    )


@pytest.fixture
def html_headers() -> dict[str, str]:
    """Returns HTML response headers."""
    return {"Content-Type": "text/html; charset=utf-8"}


@pytest.fixture
def text_headers() -> dict[str, str]:
    """Returns plain text response headers."""
    return {"Content-Type": "text/plain"}


@pytest.fixture
def xhtml_headers() -> dict[str, str]:
    """Returns XHTML response headers."""
    return {"Content-Type": "application/xhtml+xml"}


@pytest.fixture
def pdf_headers() -> dict[str, str]:
    """Returns PDF response headers."""
    return {"Content-Type": "application/pdf"}


@pytest.fixture
def valid_html_bytes() -> bytes:
    """Returns valid HTML bytes from fixture file."""
    fixture_path = FIXTURES_DIR / "normal.html"
    if fixture_path.exists():
        return fixture_path.read_bytes()
    return b"<html><body><h1>Test Page</h1></body></html>"


@pytest.fixture
def valid_text_bytes() -> bytes:
    """Returns valid text bytes."""
    return b"Hello Plain Text"


@pytest.fixture
def valid_pdf_bytes() -> bytes:
    """Returns valid PDF bytes."""
    return b"%PDF-1.4 Fake PDF Content"


@pytest.fixture
def default_timeout() -> httpx.Timeout:
    """Returns standard httpx Timeout."""
    return httpx.Timeout(5.0)


@pytest.fixture
def mock_dns_resolver(monkeypatch, mock_public_ip_result):
    """Patches resolve_public_addresses across client, transport, redirects, and robots_fetcher."""

    def dummy_resolve(hostname):
        return mock_public_ip_result

    monkeypatch.setattr(
        "safe_web_access.client.resolve_public_addresses",
        dummy_resolve,
    )
    monkeypatch.setattr(
        "safe_web_access.transport.resolve_public_addresses",
        dummy_resolve,
    )
    monkeypatch.setattr(
        "safe_web_access.redirects.resolve_public_addresses",
        dummy_resolve,
    )
    monkeypatch.setattr(
        "safe_web_access.robots_fetcher.resolve_public_addresses",
        dummy_resolve,
    )
    return dummy_resolve
