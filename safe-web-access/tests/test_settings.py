from dataclasses import FrozenInstanceError

import pytest

from safe_web_access.policies import DomainPolicy
from safe_web_access.retries import RetryPolicy
from safe_web_access.settings import SafeWebSettings


def test_settings_valid_defaults():
    settings = SafeWebSettings()
    assert settings.connect_timeout_seconds == 10.0
    assert settings.read_timeout_seconds == 20.0
    assert settings.max_redirects == 5
    assert settings.max_response_bytes == 3_000_000
    assert settings.max_pages == 20
    assert settings.max_total_bytes == 20_000_000
    assert "SafeWebAccess" in settings.user_agent
    assert "text/html" in settings.allowed_content_types
    assert isinstance(settings.domain_policy, DomainPolicy)
    assert isinstance(settings.retry_policy, RetryPolicy)
    assert settings.strict_event_hooks is False


def test_settings_valid_custom():
    settings = SafeWebSettings(
        connect_timeout_seconds=10,
        read_timeout_seconds=30,
        max_redirects=3,
        max_response_bytes=1000,
        max_pages=5,
        max_total_bytes=5000,
        user_agent="CustomBot/1.0",
        allowed_content_types=("text/html", "application/pdf"),
        strict_event_hooks=True,
    )
    assert settings.connect_timeout_seconds == 10
    assert settings.user_agent == "CustomBot/1.0"
    assert len(settings.allowed_content_types) == 2
    assert settings.strict_event_hooks is True


def test_settings_immutable():
    settings = SafeWebSettings()
    with pytest.raises(FrozenInstanceError):
        settings.max_redirects = 10  # type: ignore


@pytest.mark.parametrize(
    "kwargs,exc_type,match",
    [
        ({"connect_timeout_seconds": 0}, ValueError, "must be greater than zero"),
        ({"connect_timeout_seconds": -5}, ValueError, "must be greater than zero"),
        ({"read_timeout_seconds": 0}, ValueError, "must be greater than zero"),
        ({"max_redirects": -1}, ValueError, "cannot be negative"),
        ({"max_response_bytes": 0}, ValueError, "must be greater than zero"),
        ({"max_pages": 0}, ValueError, "must be greater than zero"),
        ({"max_total_bytes": 0}, ValueError, "must be greater than zero"),
        (
            {"max_total_bytes": 100, "max_response_bytes": 1000},
            ValueError,
            "smaller than max_response_bytes",
        ),
        ({"user_agent": ""}, ValueError, "cannot be empty"),
        ({"user_agent": "   "}, ValueError, "cannot be empty"),
        ({"user_agent": 123}, ValueError, "cannot be empty"),
        ({"allowed_content_types": ()}, ValueError, "cannot be empty"),
        ({"allowed_content_types": ("  ",)}, ValueError, "cannot contain empty values"),
        ({"allowed_content_types": "text/html"}, TypeError, "must be a tuple"),
        ({"domain_policy": "invalid"}, TypeError, "must be a DomainPolicy"),
        ({"retry_policy": "invalid"}, TypeError, "must be a RetryPolicy"),
        ({"strict_event_hooks": "invalid"}, TypeError, "must be a boolean"),
    ],
)
def test_settings_invalid_inputs(kwargs, exc_type, match):
    with pytest.raises(exc_type, match=match):
        SafeWebSettings(**kwargs)  # type: ignore
