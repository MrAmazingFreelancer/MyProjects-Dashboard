"""
This module defines domain and port filtering policies for safe web access.
It restricts outbound HTTP requests to authorized hostnames and port numbers.
Its main public class is DomainPolicy supporting allowlists and blocklists.
It works with urls, settings, client, and transport to evaluate targets.
It enforces case-insensitive domain matching, wildcards, and port safety.
It does not perform DNS address resolution or IP range verification.
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .exceptions import (
    BlockedDomainError,
    DomainNotAllowedError,
    PortNotAllowedError,
)

if TYPE_CHECKING:
    from .urls import ValidatedUrl


def _normalize_domain_entry(entry: str) -> str:
    """Validates and normalizes one domain policy string."""
    if isinstance(entry, bool) or not isinstance(entry, str):
        raise TypeError("Domain policy entries must be strings.")

    cleaned = entry.strip()
    if not cleaned:
        raise ValueError("Domain policy entries cannot be empty or whitespace-only.")

    if any(char in cleaned for char in ("://", "@", "/", "?", "#", " ", "\t")):
        raise ValueError(f"Invalid domain policy entry: '{entry}'.")

    if ":" in cleaned:
        raise ValueError(
            f"Domain policy entry must not contain port numbers: '{entry}'."
        )

    if "*" in cleaned:
        if not cleaned.startswith("*."):
            raise ValueError(f"Invalid wildcard pattern: '{entry}'.")
        remainder = cleaned[2:]
        if not remainder or "*" in remainder or "." not in remainder:
            raise ValueError(f"Invalid wildcard pattern: '{entry}'.")
        return f"*.{remainder.lower().removesuffix('.')}"

    normalized = cleaned.lower().removesuffix(".")
    if not normalized:
        raise ValueError(f"Invalid domain policy entry: '{entry}'.")
    return normalized


@dataclass(frozen=True, slots=True)
class DomainPolicy:
    """Defines domain allowlist, blocklist, and allowed port rules."""

    allowed_domains: tuple[str, ...] | None = None
    blocked_domains: tuple[str, ...] = ()
    allowed_ports: tuple[int, ...] = (80, 443)
    allow_subdomains: bool = True

    def __post_init__(self) -> None:
        """Validates domain policy entries and allowed ports."""
        if not isinstance(self.allow_subdomains, bool):
            raise TypeError("allow_subdomains must be a boolean.")

        if self.allowed_domains is not None:
            if isinstance(self.allowed_domains, bool) or not isinstance(
                self.allowed_domains, tuple
            ):
                raise TypeError("allowed_domains must be a tuple or None.")
            norm_allowed: list[str] = []
            for item in self.allowed_domains:
                norm = _normalize_domain_entry(item)
                if norm in norm_allowed:
                    raise ValueError(f"Duplicate entry in allowed_domains: '{item}'.")
                norm_allowed.append(norm)

        if isinstance(self.blocked_domains, bool) or not isinstance(
            self.blocked_domains, tuple
        ):
            raise TypeError("blocked_domains must be a tuple.")
        norm_blocked: list[str] = []
        for item in self.blocked_domains:
            norm = _normalize_domain_entry(item)
            if norm in norm_blocked:
                raise ValueError(f"Duplicate entry in blocked_domains: '{item}'.")
            norm_blocked.append(norm)

        if isinstance(self.allowed_ports, bool) or not isinstance(
            self.allowed_ports, tuple
        ):
            raise TypeError("allowed_ports must be a tuple.")

        norm_ports: list[int] = []
        for port in self.allowed_ports:
            if isinstance(port, bool) or not isinstance(port, int):
                raise TypeError("allowed_ports items must be integers.")
            if not (1 <= port <= 65535):
                raise ValueError("Port must be between 1 and 65535.")
            if port in norm_ports:
                raise ValueError(f"Duplicate port in allowed_ports: {port}.")
            norm_ports.append(port)

    def _matches_pattern(self, hostname: str, pattern: str) -> bool:
        """Returns True if normalized hostname matches a policy domain pattern."""
        norm_host = hostname.lower().removesuffix(".")
        if pattern.startswith("*."):
            base = pattern[2:]
            return norm_host.endswith(f".{base}")
        if norm_host == pattern:
            return True
        if self.allow_subdomains and norm_host.endswith(f".{pattern}"):
            return True
        return False

    def evaluate_url(self, validated_url: "ValidatedUrl") -> None:
        """Evaluates a validated URL against port and domain policies."""
        port = (
            validated_url.port
            if validated_url.port is not None
            else (80 if validated_url.scheme == "http" else 443)
        )

        if port not in self.allowed_ports:
            raise PortNotAllowedError(
                f"Port {port} is not permitted by domain policy.",
                current_url=validated_url.normalized,
            )

        norm_host = validated_url.hostname.lower().removesuffix(".")

        # Blocklist always takes precedence over allowlist
        for blocked_pat in self.blocked_domains:
            norm_pat = _normalize_domain_entry(blocked_pat)
            if self._matches_pattern(norm_host, norm_pat):
                raise BlockedDomainError(
                    f"Domain '{norm_host}' is blocked by domain policy.",
                    current_url=validated_url.normalized,
                )

        if self.allowed_domains is not None:
            matched = False
            for allowed_pat in self.allowed_domains:
                norm_pat = _normalize_domain_entry(allowed_pat)
                if self._matches_pattern(norm_host, norm_pat):
                    matched = True
                    break
            if not matched:
                raise DomainNotAllowedError(
                    f"Domain '{norm_host}' is not permitted by domain policy.",
                    current_url=validated_url.normalized,
                )
