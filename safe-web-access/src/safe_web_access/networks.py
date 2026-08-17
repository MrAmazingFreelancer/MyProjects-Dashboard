"""
This module validates destination networks to prevent Server-Side Request Forgery.
It resolves hostnames to IP addresses and filters out private/loopback destinations.
Its main public function is resolve_public_addresses returning a NetworkCheckResult.
It works with redirects, transport, and client modules during requests.
It rejects private, loopback, link-local, multicast, or reserved ranges.
It does not implement DNS pinning or protect against DNS rebinding attacks.
"""

import socket
from dataclasses import dataclass
from ipaddress import IPv4Address, IPv6Address, ip_address

from .exceptions import DnsResolutionError, InvalidUrlError, UnsafeNetworkError

IPAddress = IPv4Address | IPv6Address


def _is_public_address(address: IPAddress) -> bool:
    """Returns True only when an IP address is safe for public web access."""
    if address.is_private:
        return False
    if address.is_loopback:
        return False
    if address.is_link_local:
        return False
    if address.is_multicast:
        return False
    if address.is_reserved:
        return False
    if address.is_unspecified:
        return False
    return address.is_global


@dataclass(frozen=True, slots=True)
class NetworkCheckResult:
    """Stores the safe public IP addresses found for one hostname."""

    hostname: str
    addresses: tuple[IPAddress, ...]

    def __post_init__(self) -> None:
        """Checks that the network result contains valid public addresses."""
        if not self.hostname or not self.hostname.strip():
            raise ValueError("hostname cannot be empty or whitespace-only.")
        if not self.addresses:
            raise ValueError("addresses cannot be empty.")
        if len(self.addresses) != len(set(self.addresses)):
            raise ValueError("duplicate addresses are not allowed.")
        for addr in self.addresses:
            if not _is_public_address(addr):
                raise ValueError("addresses contains an unsafe address.")


def resolve_public_addresses(hostname: str) -> NetworkCheckResult:
    """Resolves a hostname and returns only verified public IP addresses."""
    if not isinstance(hostname, str):
        raise InvalidUrlError("hostname must be a string.")

    if not hostname or not hostname.strip():
        raise InvalidUrlError("hostname cannot be empty or whitespace-only.")

    cleaned_host = hostname.strip().lower().removesuffix(".")
    if not cleaned_host:
        raise InvalidUrlError("hostname cannot be empty or whitespace-only.")

    if cleaned_host == "localhost" or cleaned_host.endswith(".localhost"):
        raise UnsafeNetworkError("Hostname resolves to an unsafe network address.")

    # Strip brackets if it is a bracketed IPv6 address literal
    host_to_parse = cleaned_host
    if host_to_parse.startswith("[") and host_to_parse.endswith("]"):
        host_to_parse = host_to_parse[1:-1]

    # Check if the hostname itself is an IP address literal
    try:
        ip = ip_address(host_to_parse)
        is_ip = True
    except ValueError:
        is_ip = False

    if is_ip:
        if not _is_public_address(ip):
            raise UnsafeNetworkError("Hostname resolves to an unsafe network address.")
        return NetworkCheckResult(hostname=cleaned_host, addresses=(ip,))

    # Resolve hostname via DNS
    try:
        addr_info = socket.getaddrinfo(cleaned_host, None, type=socket.SOCK_STREAM)
    except (socket.gaierror, socket.herror) as exc:
        raise DnsResolutionError("Hostname could not be resolved.") from exc

    resolved_ips: set[IPAddress] = set()
    for item in addr_info:
        ip_text = item[4][0]
        try:
            resolved_ips.add(ip_address(ip_text))
        except ValueError:
            # Ignore an unexpected malformed address returned by the resolver.
            continue

    if not resolved_ips:
        raise DnsResolutionError("Hostname did not resolve to any IP address.")

    for ip in resolved_ips:
        if not _is_public_address(ip):
            raise UnsafeNetworkError("Hostname resolves to an unsafe network address.")

    sorted_ips = sorted(resolved_ips, key=lambda ip: (ip.version, int(ip)))

    return NetworkCheckResult(hostname=cleaned_host, addresses=tuple(sorted_ips))
