"""
This module checks what type of content a website has returned.
It extracts and cleans media types from the raw Content-Type headers.
Its main public function is validate_content_type returning a ContentTypeResult.
It works with settings, exceptions, and response_reader modules during fetches.
It blocks binary types like ZIP archives, videos, executables, and image files.
It does not parse any files, decode binary structures, or extract HTML data.
"""

from dataclasses import dataclass

from .exceptions import UnsupportedContentTypeError


@dataclass(frozen=True, slots=True)
class ContentTypeResult:
    """Stores one normalized and approved response content type."""

    original: str
    normalized: str
    charset: str | None
    is_text: bool
    is_pdf: bool

    def __post_init__(self) -> None:
        """Checks that the content type result is valid and consistent."""
        if not self.original or not self.original.strip():
            raise ValueError("original cannot be empty or whitespace-only.")
        if not self.normalized or not self.normalized.strip():
            raise ValueError("normalized cannot be empty or whitespace-only.")
        if self.normalized != self.normalized.strip():
            raise ValueError("normalized cannot contain surrounding whitespace.")
        if self.normalized != self.normalized.lower():
            raise ValueError("normalized must be lowercase.")
        if ";" in self.normalized:
            raise ValueError("normalized must not contain ';'.")
        if not isinstance(self.is_text, bool):
            raise TypeError("is_text must be a boolean value.")
        if not isinstance(self.is_pdf, bool):
            raise TypeError("is_pdf must be a boolean value.")
        if self.is_text and self.is_pdf:
            raise ValueError("is_text and is_pdf cannot both be True.")
        if self.charset is not None and (not self.charset or not self.charset.strip()):
            raise ValueError("charset cannot be empty or whitespace-only.")
        if self.charset is not None and self.charset != self.charset.lower():
            raise ValueError("charset must be lowercase.")


def validate_content_type(
    content_type_header: str,
    allowed_content_types: tuple[str, ...],
) -> ContentTypeResult:
    """Normalizes and validates a response Content-Type header."""
    if isinstance(content_type_header, bool) or not isinstance(
        content_type_header, str
    ):
        raise TypeError("content_type_header must be a string.")
    if isinstance(allowed_content_types, bool) or not isinstance(
        allowed_content_types, tuple
    ):
        raise TypeError("allowed_content_types must be a tuple.")

    if not content_type_header or not content_type_header.strip():
        raise UnsupportedContentTypeError(
            "content_type_header cannot be empty or whitespace-only."
        )
    if not allowed_content_types:
        raise ValueError("allowed_content_types cannot be empty.")

    normalized_allowed: set[str] = set()
    for item in allowed_content_types:
        if isinstance(item, bool) or not isinstance(item, str):
            raise TypeError("Allowed content types must be strings.")
        if not item or not item.strip():
            raise ValueError("Allowed content types cannot be empty.")

        norm = item.strip().lower()
        if norm in normalized_allowed:
            raise ValueError("Duplicate allowed content types are not allowed.")
        if ";" in norm:
            raise ValueError("Allowed content types cannot contain ';'.")

        normalized_allowed.add(norm)

    parts = content_type_header.split(";")
    media_type = parts[0].strip().lower()

    charset = None
    charset_count = 0

    # Parse and extract only the charset parameter from the remaining parts
    for param in parts[1:]:
        param = param.strip()
        if "=" in param:
            name, value = param.split("=", 1)
            name = name.strip().lower()
            if name == "charset":
                charset_count += 1
                if charset_count > 1:
                    raise UnsupportedContentTypeError(
                        "Content-Type contains more than one charset."
                    )
                charset_value = value.strip().strip("'\"").strip().lower()
                if not charset_value:
                    raise UnsupportedContentTypeError("charset cannot be empty.")
                charset = charset_value

    if media_type.count("/") != 1:
        raise UnsupportedContentTypeError("Invalid media type structure.")

    main_type, subtype = media_type.split("/", 1)
    if not main_type.strip() or not subtype.strip():
        raise UnsupportedContentTypeError("Invalid media type structure.")

    if media_type not in normalized_allowed:
        raise UnsupportedContentTypeError("Unsupported content type.")

    is_text = media_type in {
        "text/html",
        "text/plain",
        "application/xhtml+xml",
    }

    is_pdf = media_type == "application/pdf"

    return ContentTypeResult(
        original=content_type_header,
        normalized=media_type,
        charset=charset,
        is_text=is_text,
        is_pdf=is_pdf,
    )
