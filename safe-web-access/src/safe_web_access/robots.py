"""
This module evaluates advisory robots.txt rules for the requested URL.
It parses raw robots.txt files and determines path access permissions.
Its main functions are evaluate_robots_rules and build_robots_url.
It works with urls, robots_fetcher, and client modules during requests.
It checks user agent directives and returns a structured advisory status.
It does not automatically block requests or download the robots.txt itself.
"""

from dataclasses import dataclass
from enum import StrEnum
from urllib.parse import urlsplit, urlunsplit
from urllib.robotparser import RobotFileParser

from .urls import validate_and_normalize_url


class RobotsStatus(StrEnum):
    """Lists the possible robots.txt policy results."""

    ALLOWED = "allowed"
    DISALLOWED = "disallowed"
    MISSING = "missing"
    UNREACHABLE = "unreachable"
    INVALID = "invalid"


@dataclass(frozen=True, slots=True)
class RobotsCheckResult:
    """Stores the advisory robots.txt status for one page."""

    target_url: str
    robots_url: str
    user_agent: str
    status: RobotsStatus
    allowed: bool | None
    message: str

    def __post_init__(self) -> None:
        """Checks that the robots result is valid and consistent."""
        if not isinstance(self.target_url, str):
            raise TypeError("target_url must be a string.")
        if not self.target_url.strip():
            raise ValueError("target_url cannot be empty or whitespace-only.")

        if not isinstance(self.robots_url, str):
            raise TypeError("robots_url must be a string.")
        if not self.robots_url.strip():
            raise ValueError("robots_url cannot be empty or whitespace-only.")

        if not isinstance(self.user_agent, str):
            raise TypeError("user_agent must be a string.")
        if not self.user_agent.strip():
            raise ValueError("user_agent cannot be empty or whitespace-only.")

        if not isinstance(self.message, str):
            raise TypeError("message must be a string.")
        if not self.message.strip():
            raise ValueError("message cannot be empty or whitespace-only.")

        if not isinstance(self.status, RobotsStatus):
            raise TypeError("status must be a RobotsStatus enum member.")
        if self.allowed is not None and not isinstance(self.allowed, bool):
            raise TypeError("allowed must be a boolean or None.")

        if self.status == RobotsStatus.ALLOWED:
            if self.allowed is not True:
                raise ValueError("allowed must be True when status is ALLOWED.")
        elif self.status == RobotsStatus.DISALLOWED:
            if self.allowed is not False:
                raise ValueError("allowed must be False when status is DISALLOWED.")
        elif (
            self.status
            in {
                RobotsStatus.MISSING,
                RobotsStatus.UNREACHABLE,
                RobotsStatus.INVALID,
            }
            and self.allowed is not None
        ):
            raise ValueError(
                "allowed must be None when status is MISSING, "
                "UNREACHABLE, or INVALID."
            )


def build_robots_url(target_url: str) -> str:
    """Builds the robots.txt URL for a validated website URL."""
    if isinstance(target_url, bool) or not isinstance(target_url, str):
        raise TypeError("target_url must be a string.")
    if not target_url or not target_url.strip():
        raise ValueError("target_url cannot be empty or whitespace-only.")

    validated = validate_and_normalize_url(target_url)
    parsed = urlsplit(validated.normalized)

    return urlunsplit(
        (
            parsed.scheme,
            parsed.netloc,
            "/robots.txt",
            "",
            "",
        )
    )


def evaluate_robots_rules(
    target_url: str,
    robots_text: str,
    user_agent: str,
) -> RobotsCheckResult:
    """Checks robots.txt text and returns an advisory access result."""
    if isinstance(target_url, bool) or not isinstance(target_url, str):
        raise TypeError("target_url must be a string.")
    if isinstance(robots_text, bool) or not isinstance(robots_text, str):
        raise TypeError("robots_text must be a string.")
    if isinstance(user_agent, bool) or not isinstance(user_agent, str):
        raise TypeError("user_agent must be a string.")

    if not target_url or not target_url.strip():
        raise ValueError("target_url cannot be empty or whitespace-only.")
    if not user_agent or not user_agent.strip():
        raise ValueError("user_agent cannot be empty or whitespace-only.")

    validated = validate_and_normalize_url(target_url)
    robots_url = build_robots_url(validated.normalized)
    cleaned_user_agent = user_agent.strip()

    if not robots_text or not robots_text.strip():
        return RobotsCheckResult(
            target_url=validated.normalized,
            robots_url=robots_url,
            user_agent=cleaned_user_agent,
            status=RobotsStatus.MISSING,
            allowed=None,
            message="robots.txt was not available.",
        )

    parser = RobotFileParser()
    parser.set_url(robots_url)

    try:
        parser.parse(robots_text.splitlines())
    except ValueError:
        return RobotsCheckResult(
            target_url=validated.normalized,
            robots_url=robots_url,
            user_agent=cleaned_user_agent,
            status=RobotsStatus.INVALID,
            allowed=None,
            message="robots.txt could not be parsed.",
        )

    is_allowed = parser.can_fetch(cleaned_user_agent, validated.normalized)

    if is_allowed:
        status = RobotsStatus.ALLOWED
        allowed = True
        message = "robots.txt allows this page."
    else:
        status = RobotsStatus.DISALLOWED
        allowed = False
        message = "robots.txt disallows this page."

    return RobotsCheckResult(
        target_url=validated.normalized,
        robots_url=robots_url,
        user_agent=cleaned_user_agent,
        status=status,
        allowed=allowed,
        message=message,
    )


def create_robots_unreachable_result(
    target_url: str,
    user_agent: str,
) -> RobotsCheckResult:
    """Returns an advisory result when robots.txt could not be fetched."""
    if isinstance(target_url, bool) or not isinstance(target_url, str):
        raise TypeError("target_url must be a string.")
    if not target_url or not target_url.strip():
        raise ValueError("target_url cannot be empty or whitespace-only.")
    if isinstance(user_agent, bool) or not isinstance(user_agent, str):
        raise TypeError("user_agent must be a string.")
    if not user_agent or not user_agent.strip():
        raise ValueError("user_agent cannot be empty or whitespace-only.")

    validated = validate_and_normalize_url(target_url)
    robots_url = build_robots_url(validated.normalized)
    cleaned_user_agent = user_agent.strip()

    return RobotsCheckResult(
        target_url=validated.normalized,
        robots_url=robots_url,
        user_agent=cleaned_user_agent,
        status=RobotsStatus.UNREACHABLE,
        allowed=None,
        message="robots.txt could not be reached.",
    )
