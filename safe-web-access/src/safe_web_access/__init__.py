"""
This package initializes the Safe Web Access system for crawlers and AI agents.
It exports the core clients, settings, policies, retries, and results.
Its main public interface includes SafeWebClient, SyncSafeWebClient, and CrawlBudget.
It bundles settings, policies, retries, events, transport, and exceptions.
It prevents SSRF, domain violations, loops, and oversized content during crawling.
It does not parse HTML or extract business data from webpages.
"""

from importlib.metadata import PackageNotFoundError, version

from .budgets import CrawlBudget
from .client import SafeWebClient
from .events import EventHook, SafeWebEvent, SafeWebEventType
from .policies import DomainPolicy
from .results import SafeWebResult
from .retries import RetryPolicy
from .settings import SafeWebSettings
from .sync_client import SyncSafeWebClient

try:
    __version__ = version("safe-web-access")
except PackageNotFoundError:
    __version__ = "0.1.2"

__all__ = [
    "CrawlBudget",
    "DomainPolicy",
    "EventHook",
    "RetryPolicy",
    "SafeWebClient",
    "SafeWebEvent",
    "SafeWebEventType",
    "SafeWebResult",
    "SafeWebSettings",
    "SyncSafeWebClient",
    "__version__",
]
