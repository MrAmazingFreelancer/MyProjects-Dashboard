from ipaddress import IPv4Address, ip_address

import pytest

from safe_web_access.exceptions import (
    DnsResolutionError,
    InvalidUrlError,
    UnsafeNetworkError,
)
from safe_web_access.networks import (
    NetworkCheckResult,
    _is_public_address,
    resolve_public_addresses,
)


def test_networks_public_ipv4():
    res = resolve_public_addresses("93.184.216.34")
    assert res.hostname == "93.184.216.34"
    assert len(res.addresses) == 1
    assert res.addresses[0] == IPv4Address("93.184.216.34")


def test_networks_public_ipv6():
    res = resolve_public_addresses("[2606:2800:220:1:248:1893:25c8:1946]")
    assert len(res.addresses) == 1
    assert str(res.addresses[0]) == "2606:2800:220:1:248:1893:25c8:1946"


def test_networks_dns_resolution(monkeypatch):
    def dummy_getaddrinfo(host, port, type):
        return [(None, None, None, None, ("93.184.216.34", 0))]

    monkeypatch.setattr("socket.getaddrinfo", dummy_getaddrinfo)
    res = resolve_public_addresses("example.com")
    assert res.hostname == "example.com"
    assert len(res.addresses) == 1
    assert str(res.addresses[0]) == "93.184.216.34"


@pytest.mark.parametrize(
    "unsafe_ip",
    [
        "127.0.0.1",
        "10.0.0.1",
        "172.16.0.1",
        "192.168.1.1",
        "169.254.169.254",
        "0.0.0.0",
        "::1",
        "224.0.0.1",
        "localhost",
        "app.localhost",
    ],
)
def test_networks_unsafe_ip_rejection(unsafe_ip):
    with pytest.raises(UnsafeNetworkError):
        resolve_public_addresses(unsafe_ip)


def test_networks_mixed_dns_answer_rejection(monkeypatch):
    def dummy_resolve_mixed(host, port, type):
        return [
            (None, None, None, None, ("93.184.216.34", 0)),
            (None, None, None, None, ("127.0.0.1", 0)),
        ]

    monkeypatch.setattr("socket.getaddrinfo", dummy_resolve_mixed)
    with pytest.raises(UnsafeNetworkError):
        resolve_public_addresses("example.com")


def test_networks_dns_resolution_failure(monkeypatch):
    def dummy_resolve_fail(host, port, type):
        import socket

        raise socket.gaierror("Name or service not known")

    monkeypatch.setattr("socket.getaddrinfo", dummy_resolve_fail)
    with pytest.raises(DnsResolutionError):
        resolve_public_addresses("nonexistent.invalid")


@pytest.mark.parametrize(
    "invalid_input",
    [
        "",
        "   ",
        ".",
        12345,
        True,
        None,
    ],
)
def test_networks_invalid_hostname_inputs(invalid_input):
    with pytest.raises(InvalidUrlError):
        resolve_public_addresses(invalid_input)  # type: ignore


def test_networks_malformed_ip_from_resolver(monkeypatch):
    def dummy_resolve_malformed(host, port, type):
        return [(None, None, None, None, ("invalid-ip-string", 0))]

    monkeypatch.setattr("socket.getaddrinfo", dummy_resolve_malformed)
    with pytest.raises(DnsResolutionError, match="did not resolve to any IP"):
        resolve_public_addresses("example.com")


def test_is_public_address_special_ranges():
    assert _is_public_address(ip_address("8.8.8.8")) is True
    assert _is_public_address(ip_address("127.0.0.1")) is False
    assert _is_public_address(ip_address("10.0.0.1")) is False
    assert _is_public_address(ip_address("172.16.0.1")) is False
    assert _is_public_address(ip_address("192.168.1.1")) is False
    assert _is_public_address(ip_address("169.254.1.1")) is False
    assert _is_public_address(ip_address("224.0.0.1")) is False
    assert _is_public_address(ip_address("240.0.0.1")) is False
    assert _is_public_address(ip_address("0.0.0.0")) is False
    assert _is_public_address(ip_address("::")) is False
    assert _is_public_address(ip_address("::1")) is False
    assert _is_public_address(ip_address("fe80::1")) is False
    assert _is_public_address(ip_address("ff02::1")) is False
    assert _is_public_address(ip_address("100::1")) is False


def test_network_check_result_post_init_validation():
    with pytest.raises(ValueError, match="hostname"):
        NetworkCheckResult(hostname="", addresses=(ip_address("93.184.216.34"),))

    with pytest.raises(ValueError, match="addresses cannot be empty"):
        NetworkCheckResult(hostname="example.com", addresses=())

    with pytest.raises(ValueError, match="duplicate addresses"):
        NetworkCheckResult(
            hostname="example.com",
            addresses=(ip_address("93.184.216.34"), ip_address("93.184.216.34")),
        )

    with pytest.raises(ValueError, match="unsafe address"):
        NetworkCheckResult(
            hostname="example.com",
            addresses=(ip_address("127.0.0.1"),),
        )
