import pytest

from safe_web_access.exceptions import (
    BlockedDomainError,
    InvalidUrlError,
    RedirectLimitError,
    RedirectLoopError,
    UnsafeNetworkError,
    UnsafeRedirectError,
)
from safe_web_access.networks import NetworkCheckResult, ip_address
from safe_web_access.policies import DomainPolicy
from safe_web_access.redirects import RedirectResult, validate_redirect_target
from safe_web_access.urls import validate_and_normalize_url


def test_redirects_absolute(monkeypatch, mock_dns_resolver):
    res = validate_redirect_target(
        source_url="https://example.com/start",
        location="https://example.com/end",
        visited_urls={"https://example.com/start"},
        current_redirect_count=0,
        max_redirects=5,
    )
    assert res.source_url == "https://example.com/start"
    assert res.target.normalized == "https://example.com/end"
    assert res.redirect_count == 1


def test_redirects_relative(monkeypatch, mock_dns_resolver):
    res = validate_redirect_target(
        source_url="https://example.com/dir/page1",
        location="../page2",
        visited_urls={"https://example.com/dir/page1"},
        current_redirect_count=1,
        max_redirects=5,
    )
    assert res.target.normalized == "https://example.com/page2"
    assert res.redirect_count == 2


def test_redirects_self_loop_detection():
    with pytest.raises(RedirectLoopError):
        validate_redirect_target(
            source_url="https://example.com/same",
            location="https://example.com/same",
            visited_urls={"https://example.com/same"},
            current_redirect_count=0,
            max_redirects=5,
        )


def test_redirects_multi_step_loop_detection(monkeypatch, mock_dns_resolver):
    visited = {"https://example.com/step1", "https://example.com/step2"}
    with pytest.raises(RedirectLoopError):
        validate_redirect_target(
            source_url="https://example.com/step2",
            location="https://example.com/step1",
            visited_urls=visited,
            current_redirect_count=2,
            max_redirects=5,
        )


def test_redirects_limit_exceeded(monkeypatch, mock_dns_resolver):
    with pytest.raises(RedirectLimitError):
        validate_redirect_target(
            source_url="https://example.com/step5",
            location="https://example.com/step6",
            visited_urls=set(),
            current_redirect_count=5,
            max_redirects=5,
        )


def test_redirects_empty_location():
    with pytest.raises(UnsafeRedirectError):
        validate_redirect_target(
            source_url="https://example.com/start",
            location="",
            visited_urls=set(),
            current_redirect_count=0,
            max_redirects=5,
        )


def test_redirects_private_target():
    with pytest.raises((UnsafeRedirectError, UnsafeNetworkError)):
        validate_redirect_target(
            source_url="https://example.com/start",
            location="http://127.0.0.1/admin",
            visited_urls=set(),
            current_redirect_count=0,
            max_redirects=5,
        )


def test_redirects_domain_policy_rejection(monkeypatch, mock_dns_resolver):
    pol = DomainPolicy(blocked_domains=("evil.com",))
    with pytest.raises(BlockedDomainError):
        validate_redirect_target(
            source_url="https://example.com/start",
            location="https://evil.com/target",
            visited_urls=set(),
            current_redirect_count=0,
            max_redirects=5,
            domain_policy=pol,
        )

    with pytest.raises(TypeError, match="DomainPolicy"):
        validate_redirect_target(
            source_url="https://example.com/start",
            location="https://example.com/target",
            visited_urls=set(),
            current_redirect_count=0,
            max_redirects=5,
            domain_policy="invalid_policy",  # type: ignore
        )


def test_redirects_invalid_parameters():
    with pytest.raises(TypeError, match="source_url"):
        validate_redirect_target(123, "https://example.com", set(), 0, 5)  # type: ignore

    with pytest.raises(TypeError, match="location"):
        validate_redirect_target("https://example.com", 123, set(), 0, 5)  # type: ignore

    with pytest.raises(TypeError, match="visited_urls"):
        validate_redirect_target("https://example.com", "https://example.com/2", [], 0, 5)  # type: ignore

    with pytest.raises(TypeError, match="current_redirect_count"):
        validate_redirect_target("https://example.com", "https://example.com/2", set(), True, 5)  # type: ignore

    with pytest.raises(TypeError, match="max_redirects"):
        validate_redirect_target("https://example.com", "https://example.com/2", set(), 0, "5")  # type: ignore

    with pytest.raises(InvalidUrlError, match="source_url"):
        validate_redirect_target("", "https://example.com/2", set(), 0, 5)

    with pytest.raises(ValueError, match="current_redirect_count"):
        validate_redirect_target(
            "https://example.com", "https://example.com/2", set(), -1, 5
        )

    with pytest.raises(ValueError, match="max_redirects"):
        validate_redirect_target(
            "https://example.com", "https://example.com/2", set(), 0, -1
        )

    with pytest.raises(TypeError, match="visited_urls"):
        validate_redirect_target("https://example.com", "https://example.com/2", {123}, 0, 5)  # type: ignore


def test_redirect_result_post_init_validation():
    target = validate_and_normalize_url("https://example.com")
    net = NetworkCheckResult("example.com", (ip_address("93.184.216.34"),))

    with pytest.raises(AttributeError):
        RedirectResult(source_url=123, target=target, network=net, redirect_count=1)  # type: ignore

    with pytest.raises(ValueError, match="source_url"):
        RedirectResult(source_url="", target=target, network=net, redirect_count=1)

    with pytest.raises(ValueError, match="redirect_count"):
        RedirectResult(
            source_url="https://example.com",
            target=target,
            network=net,
            redirect_count=0,
        )

    other_net = NetworkCheckResult("other.com", (ip_address("93.184.216.34"),))
    with pytest.raises(ValueError, match="hostname"):
        RedirectResult(
            source_url="https://example.com",
            target=target,
            network=other_net,
            redirect_count=1,
        )
