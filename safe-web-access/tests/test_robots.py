import pytest

from safe_web_access.robots import (
    RobotsCheckResult,
    RobotsStatus,
    build_robots_url,
    create_robots_unreachable_result,
    evaluate_robots_rules,
)


def test_robots_build_robots_url():
    url = build_robots_url("https://example.com/path/to/page")
    assert url == "https://example.com/robots.txt"


def test_robots_evaluate_rules_allowed():
    text = "User-agent: *\nAllow: /path/\n"
    res = evaluate_robots_rules("https://example.com/path/page", text, "MyBot/1.0")
    assert res.status == RobotsStatus.ALLOWED
    assert res.allowed is True


def test_robots_evaluate_rules_disallowed():
    text = "User-agent: *\nDisallow: /private/\n"
    res = evaluate_robots_rules("https://example.com/private/page", text, "MyBot/1.0")
    assert res.status == RobotsStatus.DISALLOWED
    assert res.allowed is False


def test_robots_evaluate_rules_empty_returns_missing():
    res = evaluate_robots_rules("https://example.com/page", "", "MyBot/1.0")
    assert res.status == RobotsStatus.MISSING
    assert res.allowed is None


def test_robots_create_unreachable_result():
    res = create_robots_unreachable_result("https://example.com/page", "MyBot/1.0")
    assert res.status == RobotsStatus.UNREACHABLE
    assert res.allowed is None


def test_robots_invalid_input_parameters():
    with pytest.raises(TypeError):
        build_robots_url(123)  # type: ignore
    with pytest.raises(ValueError):
        build_robots_url("  ")

    with pytest.raises(TypeError):
        evaluate_robots_rules(123, "text", "agent")  # type: ignore
    with pytest.raises(TypeError):
        evaluate_robots_rules("url", 123, "agent")  # type: ignore
    with pytest.raises(TypeError):
        evaluate_robots_rules("url", "text", 123)  # type: ignore

    with pytest.raises(ValueError):
        evaluate_robots_rules("   ", "text", "agent")
    with pytest.raises(ValueError):
        evaluate_robots_rules("url", "text", "   ")

    with pytest.raises(TypeError):
        create_robots_unreachable_result(123, "agent")  # type: ignore
    with pytest.raises(ValueError):
        create_robots_unreachable_result("   ", "agent")
    with pytest.raises(TypeError):
        create_robots_unreachable_result("url", 123)  # type: ignore
    with pytest.raises(ValueError):
        create_robots_unreachable_result("url", "   ")


def test_robots_check_result_post_init_validation():
    with pytest.raises(TypeError, match="target_url"):
        RobotsCheckResult(target_url=123, robots_url="r", user_agent="u", status=RobotsStatus.ALLOWED, allowed=True, message="m")  # type: ignore

    with pytest.raises(ValueError, match="target_url"):
        RobotsCheckResult(
            target_url=" ",
            robots_url="r",
            user_agent="u",
            status=RobotsStatus.ALLOWED,
            allowed=True,
            message="m",
        )

    with pytest.raises(TypeError, match="robots_url"):
        RobotsCheckResult(target_url="t", robots_url=123, user_agent="u", status=RobotsStatus.ALLOWED, allowed=True, message="m")  # type: ignore

    with pytest.raises(ValueError, match="robots_url"):
        RobotsCheckResult(
            target_url="t",
            robots_url=" ",
            user_agent="u",
            status=RobotsStatus.ALLOWED,
            allowed=True,
            message="m",
        )

    with pytest.raises(TypeError, match="user_agent"):
        RobotsCheckResult(target_url="t", robots_url="r", user_agent=123, status=RobotsStatus.ALLOWED, allowed=True, message="m")  # type: ignore

    with pytest.raises(ValueError, match="user_agent"):
        RobotsCheckResult(
            target_url="t",
            robots_url="r",
            user_agent=" ",
            status=RobotsStatus.ALLOWED,
            allowed=True,
            message="m",
        )

    with pytest.raises(TypeError, match="message"):
        RobotsCheckResult(target_url="t", robots_url="r", user_agent="u", status=RobotsStatus.ALLOWED, allowed=True, message=123)  # type: ignore

    with pytest.raises(ValueError, match="message"):
        RobotsCheckResult(
            target_url="t",
            robots_url="r",
            user_agent="u",
            status=RobotsStatus.ALLOWED,
            allowed=True,
            message=" ",
        )

    with pytest.raises(TypeError, match="status"):
        RobotsCheckResult(target_url="t", robots_url="r", user_agent="u", status="allowed", allowed=True, message="m")  # type: ignore

    with pytest.raises(TypeError, match="allowed"):
        RobotsCheckResult(target_url="t", robots_url="r", user_agent="u", status=RobotsStatus.ALLOWED, allowed="true", message="m")  # type: ignore

    with pytest.raises(ValueError, match="allowed must be True"):
        RobotsCheckResult(
            target_url="t",
            robots_url="r",
            user_agent="u",
            status=RobotsStatus.ALLOWED,
            allowed=False,
            message="m",
        )

    with pytest.raises(ValueError, match="allowed must be False"):
        RobotsCheckResult(
            target_url="t",
            robots_url="r",
            user_agent="u",
            status=RobotsStatus.DISALLOWED,
            allowed=True,
            message="m",
        )

    with pytest.raises(ValueError, match="allowed must be None"):
        RobotsCheckResult(
            target_url="t",
            robots_url="r",
            user_agent="u",
            status=RobotsStatus.MISSING,
            allowed=True,
            message="m",
        )
