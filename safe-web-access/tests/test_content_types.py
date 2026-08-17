import pytest

from safe_web_access.content_types import ContentTypeResult, validate_content_type
from safe_web_access.exceptions import UnsupportedContentTypeError


def test_content_types_html():
    res = validate_content_type("text/html; charset=utf-8", ("text/html", "text/plain"))
    assert res.normalized == "text/html"
    assert res.charset == "utf-8"
    assert res.is_text is True
    assert res.is_pdf is False


def test_content_types_pdf():
    res = validate_content_type("application/pdf", ("text/html", "application/pdf"))
    assert res.normalized == "application/pdf"
    assert res.charset is None
    assert res.is_text is False
    assert res.is_pdf is True


def test_content_types_unsupported_media_type():
    with pytest.raises(UnsupportedContentTypeError):
        validate_content_type("image/png", ("text/html",))


def test_content_types_invalid_header_inputs():
    with pytest.raises(TypeError):
        validate_content_type(123, ("text/html",))  # type: ignore

    with pytest.raises(UnsupportedContentTypeError):
        validate_content_type("", ("text/html",))

    with pytest.raises(UnsupportedContentTypeError):
        validate_content_type("   ", ("text/html",))


def test_content_types_invalid_allowed_types_inputs():
    with pytest.raises(TypeError):
        validate_content_type("text/html", "text/html")  # type: ignore

    with pytest.raises(ValueError, match="empty"):
        validate_content_type("text/html", ())

    with pytest.raises(TypeError, match="strings"):
        validate_content_type("text/html", (123,))  # type: ignore

    with pytest.raises(ValueError, match="empty"):
        validate_content_type("text/html", ("",))

    with pytest.raises(ValueError, match="Duplicate"):
        validate_content_type("text/html", ("text/html", "TEXT/HTML"))

    with pytest.raises(ValueError, match=";"):
        validate_content_type("text/html", ("text/html; charset=utf-8",))


def test_content_types_multiple_charsets():
    with pytest.raises(UnsupportedContentTypeError, match="more than one charset"):
        validate_content_type(
            "text/html; charset=utf-8; charset=iso-8859-1", ("text/html",)
        )


def test_content_types_empty_charset_value():
    with pytest.raises(UnsupportedContentTypeError, match="charset cannot be empty"):
        validate_content_type("text/html; charset=", ("text/html",))


def test_content_types_invalid_media_structure():
    with pytest.raises(
        UnsupportedContentTypeError, match="Invalid media type structure"
    ):
        validate_content_type("invalid_media_type", ("text/html",))

    with pytest.raises(
        UnsupportedContentTypeError, match="Invalid media type structure"
    ):
        validate_content_type("text/", ("text/html",))


def test_content_type_result_post_init_validation():
    with pytest.raises(ValueError, match="original"):
        ContentTypeResult(
            original="",
            normalized="text/html",
            charset=None,
            is_text=True,
            is_pdf=False,
        )

    with pytest.raises(ValueError, match="normalized"):
        ContentTypeResult(
            original="text/html",
            normalized="",
            charset=None,
            is_text=True,
            is_pdf=False,
        )

    with pytest.raises(ValueError, match="whitespace"):
        ContentTypeResult(
            original="text/html",
            normalized=" text/html ",
            charset=None,
            is_text=True,
            is_pdf=False,
        )

    with pytest.raises(ValueError, match="lowercase"):
        ContentTypeResult(
            original="text/html",
            normalized="TEXT/HTML",
            charset=None,
            is_text=True,
            is_pdf=False,
        )

    with pytest.raises(ValueError, match=";"):
        ContentTypeResult(
            original="text/html",
            normalized="text/html;charset=utf-8",
            charset=None,
            is_text=True,
            is_pdf=False,
        )

    with pytest.raises(TypeError, match="is_text"):
        ContentTypeResult(original="text/html", normalized="text/html", charset=None, is_text="yes", is_pdf=False)  # type: ignore

    with pytest.raises(TypeError, match="is_pdf"):
        ContentTypeResult(original="text/html", normalized="text/html", charset=None, is_text=True, is_pdf="no")  # type: ignore

    with pytest.raises(ValueError, match="cannot both be True"):
        ContentTypeResult(
            original="text/html",
            normalized="text/html",
            charset=None,
            is_text=True,
            is_pdf=True,
        )

    with pytest.raises(ValueError, match="charset"):
        ContentTypeResult(
            original="text/html",
            normalized="text/html",
            charset="",
            is_text=True,
            is_pdf=False,
        )

    with pytest.raises(ValueError, match="lowercase"):
        ContentTypeResult(
            original="text/html",
            normalized="text/html",
            charset="UTF-8",
            is_text=True,
            is_pdf=False,
        )
