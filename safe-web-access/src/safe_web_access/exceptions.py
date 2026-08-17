"""
This module defines the custom exceptions hierarchy for safe web access.
It uses typed exceptions to avoid brittle string-matching error classification.
Its main classes include SafeWebError, UnsafeNetworkError, and DomainNotAllowedError.
It works with errors, result_builders, and client to signal exact faults.
It maps each exception directly to a standard error code with metadata.
It does not define exceptions for HTML parser issues or business rules.
"""

from .errors import SafeWebErrorCode


class SafeWebError(Exception):
    """Base exception for all safe web access errors."""

    def __init__(
        self,
        message: str,
        error_code: SafeWebErrorCode,
        *,
        current_url: str | None = None,
        redirect_count: int = 0,
        status_code: int | None = None,
        size_bytes: int = 0,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.current_url = current_url
        self.redirect_count = redirect_count
        self.status_code = status_code
        self.size_bytes = size_bytes


class InvalidUrlError(SafeWebError):
    """Raised when a URL is malformed or invalid."""

    def __init__(self, message: str, current_url: str | None = None) -> None:
        super().__init__(
            message,
            SafeWebErrorCode.INVALID_URL,
            current_url=current_url,
        )


class UnsupportedSchemeError(SafeWebError):
    """Raised when a URL scheme is not HTTP or HTTPS."""

    def __init__(self, message: str, current_url: str | None = None) -> None:
        super().__init__(
            message,
            SafeWebErrorCode.UNSUPPORTED_SCHEME,
            current_url=current_url,
        )


class DnsResolutionError(SafeWebError):
    """Raised when hostname resolution fails via socket DNS lookups."""

    def __init__(self, message: str, current_url: str | None = None) -> None:
        super().__init__(
            message,
            SafeWebErrorCode.DNS_RESOLUTION_FAILED,
            current_url=current_url,
        )


class UnsafeNetworkError(SafeWebError):
    """Raised when a target IP address resolves to a private, loopback, or reserved network range."""

    def __init__(self, message: str, current_url: str | None = None) -> None:
        super().__init__(
            message,
            SafeWebErrorCode.PRIVATE_NETWORK,
            current_url=current_url,
        )


class RedirectLoopError(SafeWebError):
    """Raised when an HTTP redirect loop is detected."""

    def __init__(
        self,
        message: str,
        current_url: str | None = None,
        redirect_count: int = 0,
    ) -> None:
        super().__init__(
            message,
            SafeWebErrorCode.TOO_MANY_REDIRECTS,
            current_url=current_url,
            redirect_count=redirect_count,
        )


class RedirectLimitError(SafeWebError):
    """Raised when maximum allowed redirect count is exceeded."""

    def __init__(
        self,
        message: str,
        current_url: str | None = None,
        redirect_count: int = 0,
    ) -> None:
        super().__init__(
            message,
            SafeWebErrorCode.TOO_MANY_REDIRECTS,
            current_url=current_url,
            redirect_count=redirect_count,
        )


class UnsafeRedirectError(SafeWebError):
    """Raised when a redirect target URL or network is unsafe."""

    def __init__(
        self,
        message: str,
        current_url: str | None = None,
        redirect_count: int = 0,
    ) -> None:
        super().__init__(
            message,
            SafeWebErrorCode.UNSAFE_REDIRECT,
            current_url=current_url,
            redirect_count=redirect_count,
        )


class MissingRedirectLocationError(SafeWebError):
    """Raised when a 3xx redirect response lacks a Location header."""

    def __init__(
        self,
        message: str,
        current_url: str | None = None,
        redirect_count: int = 0,
    ) -> None:
        super().__init__(
            message,
            SafeWebErrorCode.UNSAFE_REDIRECT,
            current_url=current_url,
            redirect_count=redirect_count,
        )


class UnsupportedContentTypeError(SafeWebError):
    """Raised when a response Content-Type header is not in the allowed list."""

    def __init__(
        self,
        message: str,
        current_url: str | None = None,
        redirect_count: int = 0,
        status_code: int | None = None,
    ) -> None:
        super().__init__(
            message,
            SafeWebErrorCode.UNSUPPORTED_CONTENT_TYPE,
            current_url=current_url,
            redirect_count=redirect_count,
            status_code=status_code,
        )


class ResponseTooLargeError(SafeWebError):
    """Raised when response body size exceeds maximum response byte limits."""

    def __init__(
        self,
        message: str,
        current_url: str | None = None,
        redirect_count: int = 0,
        status_code: int | None = None,
        size_bytes: int = 0,
    ) -> None:
        super().__init__(
            message,
            SafeWebErrorCode.RESPONSE_TOO_LARGE,
            current_url=current_url,
            redirect_count=redirect_count,
            status_code=status_code,
            size_bytes=size_bytes,
        )


class PageBudgetExceededError(SafeWebError):
    """Raised when crawl page budget limits are exhausted."""

    def __init__(
        self,
        message: str,
        current_url: str | None = None,
        redirect_count: int = 0,
    ) -> None:
        super().__init__(
            message,
            SafeWebErrorCode.PAGE_BUDGET_EXCEEDED,
            current_url=current_url,
            redirect_count=redirect_count,
        )


class ByteBudgetExceededError(SafeWebError):
    """Raised when crawl total byte budget limits are exhausted."""

    def __init__(
        self,
        message: str,
        current_url: str | None = None,
        redirect_count: int = 0,
        status_code: int | None = None,
        size_bytes: int = 0,
    ) -> None:
        super().__init__(
            message,
            SafeWebErrorCode.BYTE_BUDGET_EXCEEDED,
            current_url=current_url,
            redirect_count=redirect_count,
            status_code=status_code,
            size_bytes=size_bytes,
        )


class DomainNotAllowedError(SafeWebError):
    """Raised when target domain is not present in the allowed domains policy."""

    def __init__(self, message: str, current_url: str | None = None) -> None:
        super().__init__(
            message,
            SafeWebErrorCode.DOMAIN_NOT_ALLOWED,
            current_url=current_url,
        )


class BlockedDomainError(SafeWebError):
    """Raised when target domain is explicitly present in the blocked domains policy."""

    def __init__(self, message: str, current_url: str | None = None) -> None:
        super().__init__(
            message,
            SafeWebErrorCode.BLOCKED_DOMAIN,
            current_url=current_url,
        )


class PortNotAllowedError(SafeWebError):
    """Raised when target URL port is not present in the allowed ports policy."""

    def __init__(self, message: str, current_url: str | None = None) -> None:
        super().__init__(
            message,
            SafeWebErrorCode.PORT_NOT_ALLOWED,
            current_url=current_url,
        )


class InvalidPolicyError(SafeWebError):
    """Raised when a domain or port policy configuration is malformed."""

    def __init__(self, message: str, current_url: str | None = None) -> None:
        super().__init__(
            message,
            SafeWebErrorCode.INVALID_POLICY,
            current_url=current_url,
        )


class SafeWebTransportError(SafeWebError):
    """Base exception for transport errors carrying target URL and redirect count metadata."""

    def __init__(
        self,
        message: str,
        current_url: str,
        redirect_count: int,
        error_code: SafeWebErrorCode = SafeWebErrorCode.REQUEST_FAILED,
    ) -> None:
        super().__init__(
            message,
            error_code,
            current_url=current_url,
            redirect_count=redirect_count,
        )


class SafeWebConnectTimeout(SafeWebTransportError):
    """Raised when establishing a socket connection times out."""

    def __init__(self, message: str, current_url: str, redirect_count: int) -> None:
        super().__init__(
            message,
            current_url,
            redirect_count,
            error_code=SafeWebErrorCode.CONNECTION_TIMEOUT,
        )


class SafeWebReadTimeout(SafeWebTransportError):
    """Raised when reading response bytes times out."""

    def __init__(self, message: str, current_url: str, redirect_count: int) -> None:
        super().__init__(
            message,
            current_url,
            redirect_count,
            error_code=SafeWebErrorCode.READ_TIMEOUT,
        )


class SafeWebRequestTimeout(SafeWebTransportError):
    """Raised when a general request timeout occurs."""

    def __init__(self, message: str, current_url: str, redirect_count: int) -> None:
        super().__init__(
            message,
            current_url,
            redirect_count,
            error_code=SafeWebErrorCode.CONNECTION_TIMEOUT,
        )


class SafeWebConnectionError(SafeWebTransportError):
    """Raised when low-level network or transport connection fails."""

    def __init__(self, message: str, current_url: str, redirect_count: int) -> None:
        super().__init__(
            message,
            current_url,
            redirect_count,
            error_code=SafeWebErrorCode.REQUEST_FAILED,
        )
