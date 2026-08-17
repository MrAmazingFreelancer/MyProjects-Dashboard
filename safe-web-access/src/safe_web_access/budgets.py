"""
This module tracks crawl limits across one or more safe web fetches.
It counts successfully fetched pages and tracks total downloaded byte sizes.
Its main public class is CrawlBudget which uses immutable properties.
It works with settings, results, and client modules during fetches.
It guarantees that page and total byte budget boundaries are not exceeded.
It does not make HTTP requests or parse HTML page elements directly.
"""

from dataclasses import dataclass

from .exceptions import ByteBudgetExceededError, PageBudgetExceededError


def _require_integer(value: object, name: str) -> None:
    """Checks that a value is an integer but not a boolean."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer.")


@dataclass(frozen=True, slots=True)
class CrawlBudget:
    """Tracks page and byte usage for one website crawl."""

    max_pages: int
    max_total_bytes: int
    pages_used: int = 0
    bytes_used: int = 0

    def __post_init__(self) -> None:
        """Checks that the crawl limits and current usage are valid."""
        _require_integer(self.max_pages, "max_pages")
        _require_integer(self.max_total_bytes, "max_total_bytes")
        _require_integer(self.pages_used, "pages_used")
        _require_integer(self.bytes_used, "bytes_used")

        if self.max_pages <= 0:
            raise ValueError("max_pages must be greater than zero.")
        if self.max_total_bytes <= 0:
            raise ValueError("max_total_bytes must be greater than zero.")
        if self.pages_used < 0:
            raise ValueError("pages_used cannot be negative.")
        if self.bytes_used < 0:
            raise ValueError("bytes_used cannot be negative.")
        if self.pages_used > self.max_pages:
            raise ValueError("pages_used cannot be greater than max_pages.")
        if self.bytes_used > self.max_total_bytes:
            raise ValueError("bytes_used cannot be greater than max_total_bytes.")

    @property
    def remaining_pages(self) -> int:
        """Returns how many more pages may be accepted."""
        return self.max_pages - self.pages_used

    @property
    def remaining_bytes(self) -> int:
        """Returns how many more bytes may be accepted."""
        return self.max_total_bytes - self.bytes_used

    @property
    def is_exhausted(self) -> bool:
        """Returns True when no more crawl data can be accepted."""
        return self.remaining_pages <= 0 or self.remaining_bytes <= 0

    def ensure_request_allowed(self) -> None:
        """Raises an error when another page request is not allowed."""
        if self.pages_used >= self.max_pages:
            raise PageBudgetExceededError("Page budget exceeded.")
        if self.bytes_used >= self.max_total_bytes:
            raise ByteBudgetExceededError("Byte budget exceeded.")

    def record_response(self, size_bytes: int) -> "CrawlBudget":
        """Returns a new budget after accepting one response."""
        _require_integer(size_bytes, "size_bytes")
        if size_bytes < 0:
            raise ValueError("size_bytes cannot be negative.")

        self.ensure_request_allowed()

        new_pages_used = self.pages_used + 1
        new_bytes_used = self.bytes_used + size_bytes

        if new_pages_used > self.max_pages:
            raise PageBudgetExceededError("Page budget exceeded.")
        if new_bytes_used > self.max_total_bytes:
            raise ByteBudgetExceededError("Byte budget exceeded.")

        return CrawlBudget(
            max_pages=self.max_pages,
            max_total_bytes=self.max_total_bytes,
            pages_used=new_pages_used,
            bytes_used=new_bytes_used,
        )
