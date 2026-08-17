"""
This module prepares and validates website links before they are fetched.
It parses schemes, handles missing protocols, and strips default ports.
Its main public function is validate_and_normalize_url returning a ValidatedUrl.
It works with redirects, networks, and client modules to ensure URL sanity.
It rejects fragments, user credentials, unsupported schemes, and control characters.
It does not perform DNS resolution or check IP address privacy.
"""

from dataclasses import dataclass
from urllib.parse import urlsplit, urlunsplit

from .exceptions import InvalidUrlError, UnsupportedSchemeError


@dataclass(frozen=True, slots=True)
class ValidatedUrl:
    """Stores a validated and normalized website URL."""

    original: str
    normalized: str
    scheme: str
    hostname: str
    port: int | None
    path: str
    query: str

    def __post_init__(self) -> None:
        """Checks that the validated URL data is complete and consistent."""
        if not self.original.strip():
            raise ValueError("original cannot be empty or whitespace-only.")
        if not self.normalized.strip():
            raise ValueError("normalized cannot be empty or whitespace-only.")
        if self.scheme not in {"http", "https"}:
            raise ValueError("scheme must be http or https.")
        if not self.hostname.strip():
            raise ValueError("hostname cannot be empty or whitespace-only.")
        if self.port is not None and not (1 <= self.port <= 65535):
            raise ValueError("port must be between 1 and 65535.")
        if self.path and not self.path.startswith("/"):
            raise ValueError("path must start with '/' when it is not empty.")


def validate_and_normalize_url(url: str) -> ValidatedUrl:
    """Validates a basic HTTP URL and returns its normalized parts."""
    if not isinstance(url, str):
        raise InvalidUrlError("URL must be a string.")

    if not url or not url.strip():
        raise InvalidUrlError("URL cannot be empty or whitespace-only.")

    original_url = url.strip()
    working_url = original_url

    if "://" in working_url:
        scheme = working_url.split("://", 1)[0].lower()
        if scheme not in {"http", "https"}:
            raise UnsupportedSchemeError("Scheme must be http or https.")
    else:
        working_url = f"https://{working_url}"

    parsed = urlsplit(working_url)

    try:
        hostname = parsed.hostname
        username = parsed.username
        password = parsed.password
        port = parsed.port
    except ValueError as exc:
        raise InvalidUrlError("Malformed URL.") from exc

    scheme_lower = parsed.scheme.lower() if parsed.scheme else ""
    if scheme_lower not in {"http", "https"}:
        raise UnsupportedSchemeError("Scheme must be http or https.")

    if not hostname:
        raise InvalidUrlError("URL must contain a hostname.")

    if username is not None or password is not None:
        raise InvalidUrlError("User credentials are not allowed in the URL.")

    if parsed.fragment:
        raise InvalidUrlError("URL fragments are not allowed.")

    if port is not None and not (1 <= port <= 65535):
        raise InvalidUrlError("Port must be between 1 and 65535.")

    hostname_lower = hostname.lower()

    # Filter out default ports (80 for HTTP, 443 for HTTPS) to normalize the URL
    normalized_port = None
    if port is not None:
        is_default_http = scheme_lower == "http" and port == 80
        is_default_https = scheme_lower == "https" and port == 443
        if not (is_default_http or is_default_https):
            normalized_port = port

    # Wrap IPv6 addresses in square brackets when forming the netloc
    if ":" in hostname_lower:
        netloc = f"[{hostname_lower}]"
    else:
        netloc = hostname_lower

    if normalized_port is not None:
        netloc = f"{netloc}:{normalized_port}"

    normalized_path = parsed.path if parsed.path else "/"
    normalized_query = parsed.query

    normalized_url = urlunsplit(
        (
            scheme_lower,
            netloc,
            normalized_path,
            normalized_query,
            "",
        )
    )

    return ValidatedUrl(
        original=original_url,
        normalized=normalized_url,
        scheme=scheme_lower,
        hostname=hostname_lower,
        port=port,
        path=normalized_path,
        query=normalized_query,
    )
