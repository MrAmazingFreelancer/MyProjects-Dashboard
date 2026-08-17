"""
This module stores the standard error codes used by safe web access.
It groups all possible failure categories into a unified string enumeration.
Its main public class is SafeWebErrorCode which extends standard StrEnum.
It works with exceptions, result_builders, and results to classify failures.
It provides clear codes for private networks, policies, redirect loops, and timeouts.
It does not raise exceptions or write to log destinations itself.
"""

from enum import StrEnum


class SafeWebErrorCode(StrEnum):
    """Lists the standard failure codes used by safe web requests."""

    INVALID_URL = "invalid_url"
    UNSUPPORTED_SCHEME = "unsupported_scheme"
    BLOCKED_HOST = "blocked_host"
    PRIVATE_NETWORK = "private_network"
    DNS_RESOLUTION_FAILED = "dns_resolution_failed"
    ROBOTS_DENIED = "robots_denied"
    CONNECTION_TIMEOUT = "connection_timeout"
    READ_TIMEOUT = "read_timeout"
    TOO_MANY_REDIRECTS = "too_many_redirects"
    UNSAFE_REDIRECT = "unsafe_redirect"
    UNSUPPORTED_CONTENT_TYPE = "unsupported_content_type"
    RESPONSE_TOO_LARGE = "response_too_large"
    PAGE_BUDGET_EXCEEDED = "page_budget_exceeded"
    BYTE_BUDGET_EXCEEDED = "byte_budget_exceeded"
    HTTP_ERROR = "http_error"
    REQUEST_FAILED = "request_failed"
    DOMAIN_NOT_ALLOWED = "domain_not_allowed"
    BLOCKED_DOMAIN = "blocked_domain"
    PORT_NOT_ALLOWED = "port_not_allowed"
    INVALID_POLICY = "invalid_policy"
