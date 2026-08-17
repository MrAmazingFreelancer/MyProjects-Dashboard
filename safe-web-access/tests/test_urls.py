import pytest

from safe_web_access.exceptions import InvalidUrlError, UnsupportedSchemeError
from safe_web_access.urls import ValidatedUrl, validate_and_normalize_url


def test_urls_valid_https():
    url = "https://example.com/path?query=1"
    v = validate_and_normalize_url(url)
    assert v.original == "https://example.com/path?query=1"
    assert v.normalized == "https://example.com/path?query=1"
    assert v.scheme == "https"
    assert v.hostname == "example.com"
    assert v.port is None
    assert v.path == "/path"
    assert v.query == "query=1"


def test_urls_missing_scheme_defaults_to_https():
    v = validate_and_normalize_url("example.com/path")
    assert v.normalized == "https://example.com/path"
    assert v.scheme == "https"


def test_urls_http_scheme_and_www():
    v = validate_and_normalize_url("http://www.example.com")
    assert v.normalized == "http://www.example.com/"
    assert v.scheme == "http"


def test_urls_default_port_removal():
    v1 = validate_and_normalize_url("http://example.com:80/path")
    assert v1.normalized == "http://example.com/path"
    assert v1.port == 80

    v2 = validate_and_normalize_url("https://example.com:443/path")
    assert v2.normalized == "https://example.com/path"
    assert v2.port == 443


def test_urls_non_default_port_preserved():
    v = validate_and_normalize_url("https://example.com:8443/path")
    assert v.normalized == "https://example.com:8443/path"
    assert v.port == 8443


def test_urls_case_normalization():
    v = validate_and_normalize_url("HTTPS://EXAMPLE.COM/PATH")
    assert v.normalized == "https://example.com/PATH"
    assert v.hostname == "example.com"


def test_urls_ipv4():
    v = validate_and_normalize_url("https://93.184.216.34:8080/test")
    assert v.normalized == "https://93.184.216.34:8080/test"
    assert v.hostname == "93.184.216.34"
    assert v.port == 8080


def test_urls_ipv6():
    v = validate_and_normalize_url(
        "https://[2606:2800:220:1:248:1893:25c8:1946]:8443/test"
    )
    assert v.normalized == "https://[2606:2800:220:1:248:1893:25c8:1946]:8443/test"
    assert v.hostname == "2606:2800:220:1:248:1893:25c8:1946"
    assert v.port == 8443


@pytest.mark.parametrize(
    "invalid_input,exc_type",
    [
        ("", InvalidUrlError),
        ("   ", InvalidUrlError),
        (12345, InvalidUrlError),
        (True, InvalidUrlError),
        ("ftp://example.com/file", UnsupportedSchemeError),
        ("file:///etc/passwd", UnsupportedSchemeError),
        ("javascript:alert(1)", InvalidUrlError),
        ("data:text/html,test", InvalidUrlError),
        ("https://user:pass@example.com", InvalidUrlError),
        ("https://example.com/page#fragment", InvalidUrlError),
        ("https://:8080/page", InvalidUrlError),
        ("https://example.com:70000/page", InvalidUrlError),
    ],
)
def test_urls_invalid_inputs(invalid_input, exc_type):
    with pytest.raises(exc_type):
        validate_and_normalize_url(invalid_input)  # type: ignore


def test_validated_url_post_init_validation():
    with pytest.raises(ValueError, match="original"):
        ValidatedUrl(
            original="",
            normalized="https://example.com",
            scheme="https",
            hostname="example.com",
            port=None,
            path="/",
            query="",
        )

    with pytest.raises(ValueError, match="normalized"):
        ValidatedUrl(
            original="https://example.com",
            normalized="",
            scheme="https",
            hostname="example.com",
            port=None,
            path="/",
            query="",
        )

    with pytest.raises(ValueError, match="scheme"):
        ValidatedUrl(
            original="https://example.com",
            normalized="https://example.com",
            scheme="ftp",  # type: ignore
            hostname="example.com",
            port=None,
            path="/",
            query="",
        )

    with pytest.raises(ValueError, match="hostname"):
        ValidatedUrl(
            original="https://example.com",
            normalized="https://example.com",
            scheme="https",
            hostname="",
            port=None,
            path="/",
            query="",
        )

    with pytest.raises(ValueError, match="port"):
        ValidatedUrl(
            original="https://example.com",
            normalized="https://example.com",
            scheme="https",
            hostname="example.com",
            port=70000,
            path="/",
            query="",
        )

    with pytest.raises(ValueError, match="path"):
        ValidatedUrl(
            original="https://example.com",
            normalized="https://example.com",
            scheme="https",
            hostname="example.com",
            port=None,
            path="path_without_slash",
            query="",
        )
