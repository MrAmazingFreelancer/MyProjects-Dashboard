from dataclasses import FrozenInstanceError

import pytest

from safe_web_access import DomainPolicy, SafeWebSettings
from safe_web_access.exceptions import (
    BlockedDomainError,
    DomainNotAllowedError,
    InvalidPolicyError,
    PortNotAllowedError,
)
from safe_web_access.urls import validate_and_normalize_url


def test_default_policy_permits_public_domains_on_standard_ports():
    pol = DomainPolicy()
    url = validate_and_normalize_url("https://example.com/path")
    pol.evaluate_url(url)


def test_exact_allowlisted_domain():
    pol = DomainPolicy(allowed_domains=("example.com",))
    url_valid = validate_and_normalize_url("https://example.com/path")
    url_invalid = validate_and_normalize_url("https://other.com/path")

    pol.evaluate_url(url_valid)
    with pytest.raises(DomainNotAllowedError):
        pol.evaluate_url(url_invalid)


def test_exact_blocked_domain():
    pol = DomainPolicy(blocked_domains=("blocked.com",))
    url_valid = validate_and_normalize_url("https://example.com/path")
    url_blocked = validate_and_normalize_url("https://blocked.com/path")

    pol.evaluate_url(url_valid)
    with pytest.raises(BlockedDomainError):
        pol.evaluate_url(url_blocked)


def test_blocked_domain_wins_over_allowlist():
    pol = DomainPolicy(
        allowed_domains=("example.com", "*.example.com"),
        blocked_domains=("bad.example.com",),
    )
    url_good = validate_and_normalize_url("https://good.example.com")
    url_bad = validate_and_normalize_url("https://bad.example.com")

    pol.evaluate_url(url_good)
    with pytest.raises(BlockedDomainError):
        pol.evaluate_url(url_bad)


def test_wildcard_subdomain_matching():
    pol = DomainPolicy(allowed_domains=("*.example.com",))
    url_sub = validate_and_normalize_url("https://api.example.com/path")
    url_exact = validate_and_normalize_url("https://example.com/path")

    pol.evaluate_url(url_sub)
    with pytest.raises(DomainNotAllowedError):
        pol.evaluate_url(url_exact)


def test_uppercase_and_trailing_dot_normalization():
    pol = DomainPolicy(allowed_domains=("EXAMPLE.COM.",))
    url = validate_and_normalize_url("https://example.com/path")
    pol.evaluate_url(url)


def test_ip_address_destination_behavior():
    pol = DomainPolicy(allowed_domains=("93.184.216.34",))
    url_ip = validate_and_normalize_url("https://93.184.216.34/path")
    pol.evaluate_url(url_ip)


def test_allowed_ports():
    pol = DomainPolicy(allowed_ports=(80, 443, 8080))
    url_8080 = validate_and_normalize_url("https://example.com:8080/path")
    url_9000 = validate_and_normalize_url("https://example.com:9000/path")

    pol.evaluate_url(url_8080)
    with pytest.raises(PortNotAllowedError):
        pol.evaluate_url(url_9000)


@pytest.mark.parametrize(
    "invalid_entry",
    [
        "",
        "   ",
        "https://example.com",
        "user:pass@example.com",
        "example.com/path",
        "example.com?q=1",
        "example.com#frag",
        "*example.com",
        "foo.*.com",
        "*",
        "**",
        "*.",
        "example.com:8080",
    ],
)
def test_invalid_domain_entries_rejected(invalid_entry):
    with pytest.raises((ValueError, InvalidPolicyError)):
        DomainPolicy(allowed_domains=(invalid_entry,))


def test_duplicate_normalized_domain_rejection():
    with pytest.raises(ValueError, match="Duplicate"):
        DomainPolicy(allowed_domains=("example.com", "EXAMPLE.COM."))

    with pytest.raises(ValueError, match="Duplicate"):
        DomainPolicy(blocked_domains=("example.com", "example.com"))


@pytest.mark.parametrize(
    "invalid_port",
    [
        True,
        False,
        0,
        65536,
        -80,
        "8080",
    ],
)
def test_invalid_port_rejection(invalid_port):
    with pytest.raises((ValueError, TypeError, InvalidPolicyError)):
        DomainPolicy(allowed_ports=(invalid_port,))  # type: ignore


def test_policy_immutability():
    pol = DomainPolicy()
    with pytest.raises(FrozenInstanceError):
        pol.allowed_ports = (80,)  # type: ignore


def test_redirect_destination_policy_validation():
    pol = DomainPolicy(blocked_domains=("evil.com",))
    settings = SafeWebSettings(domain_policy=pol)
    url = validate_and_normalize_url("https://evil.com/redirect")
    with pytest.raises(BlockedDomainError):
        settings.domain_policy.evaluate_url(url)  # type: ignore


def test_domain_policy_non_tuple_and_non_str_inputs():
    with pytest.raises(TypeError, match="must be a tuple"):
        DomainPolicy(allowed_domains="example.com")  # type: ignore

    with pytest.raises(TypeError, match="must be a tuple"):
        DomainPolicy(blocked_domains="example.com")  # type: ignore

    with pytest.raises(TypeError, match="must be a tuple"):
        DomainPolicy(allowed_ports=[80, 443])  # type: ignore

    with pytest.raises(TypeError, match="Domain policy entries must be strings"):
        DomainPolicy(allowed_domains=(123,))  # type: ignore

    with pytest.raises(ValueError, match="Duplicate"):
        DomainPolicy(allowed_ports=(80, 80))
