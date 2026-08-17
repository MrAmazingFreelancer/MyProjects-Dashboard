"""
This module reads and validates streamed HTTP response headers and bodies.
It verifies Content-Type and Content-Length headers before downloading the payload.
Its main public function is read_response_body returning a ReaderResult.
It works with budgets, content_types, and exceptions to apply strict size limits.
It checks byte chunks during downloads and blocks compressed/uncompressed overruns.
It does not decode body bytes to strings, parse HTML, or inspect PDF text.
"""

from dataclasses import dataclass

import httpx

from .budgets import CrawlBudget
from .content_types import validate_content_type
from .exceptions import ByteBudgetExceededError, ResponseTooLargeError
from .settings import SafeWebSettings


@dataclass(frozen=True, slots=True)
class ReadResponseResult:
    """Stores validated response metadata and full body bytes."""

    content_type: str
    body: bytes
    size_bytes: int

    def __post_init__(self) -> None:
        """Validates that body size equals size_bytes."""
        if len(self.body) != self.size_bytes:
            raise ValueError("len(body) must equal size_bytes.")


async def read_response_body(
    response: httpx.Response,
    settings: SafeWebSettings,
    budget: CrawlBudget,
) -> ReadResponseResult:
    """Validates response headers and streams the body bytes safely within configured limits."""
    # Validate Content-Type header
    ct_header = response.headers.get("Content-Type", "")
    ct_result = validate_content_type(ct_header, settings.allowed_content_types)

    # Inspect Content-Length header early if available
    content_length_header = response.headers.get("Content-Length")
    if content_length_header:
        cleaned_length = content_length_header.strip()
        # Handle potential comma-separated values if proxies duplicated Content-Length
        if "," in cleaned_length:
            lengths = {part.strip() for part in cleaned_length.split(",")}
            if len(lengths) > 1:
                raise ResponseTooLargeError(
                    "Conflicting duplicate Content-Length headers."
                )
            cleaned_length = lengths.pop()

        if cleaned_length.isdigit() or (
            cleaned_length.startswith("-") and cleaned_length[1:].isdigit()
        ):
            declared_length = int(cleaned_length)
            if declared_length < 0:
                raise ResponseTooLargeError("Negative Content-Length header.")
            if declared_length > settings.max_response_bytes:
                raise ResponseTooLargeError(
                    "Declared Content-Length exceeds maximum response limit."
                )
            if declared_length > budget.remaining_bytes:
                raise ByteBudgetExceededError(
                    "Declared Content-Length exceeds remaining crawl byte budget."
                )

    # Stream response bytes with hard memory limits
    accumulated_bytes = 0
    chunks: list[bytes] = []

    async for chunk in response.aiter_bytes():
        if chunk:
            accumulated_bytes += len(chunk)
            if accumulated_bytes > settings.max_response_bytes:
                raise ResponseTooLargeError(
                    "Response body exceeded maximum response byte limit."
                )
            if accumulated_bytes > budget.remaining_bytes:
                raise ByteBudgetExceededError(
                    "Response body exceeded remaining crawl byte budget."
                )
            chunks.append(chunk)

    body_bytes = b"".join(chunks)
    return ReadResponseResult(
        content_type=ct_result.normalized,
        body=body_bytes,
        size_bytes=accumulated_bytes,
    )
