"""
Event hooks (telemetry) example for safe-web-access.

This script demonstrates how to attach event hook functions to observe
what the client is doing at each stage of a request — without exposing
any sensitive data such as response body bytes or authorization headers.

To run:
    python examples/event_hooks.py
"""

import asyncio

from safe_web_access import SafeWebClient, SafeWebEvent, SafeWebEventType


# A synchronous hook function.
# It receives a SafeWebEvent object for every lifecycle event.
# The SafeWebEvent never contains response body, headers, or credentials.
def log_event(event: SafeWebEvent) -> None:
    print(
        f"[{event.event_type:<30}] "
        f"url={event.requested_url!r} "
        f"attempt={event.attempt_number} "
        f"elapsed={event.elapsed_ms}ms"
    )


# An async hook function is also supported.
# Use this when your hook needs to call async code (e.g. write to a database).
async def log_retry(event: SafeWebEvent) -> None:
    if event.event_type == SafeWebEventType.RETRY_SCHEDULED:
        print(f"  ↻ Retry scheduled: {event.message}")


async def main() -> None:
    # Pass one or more hook callables to SafeWebClient.
    # Hooks are called sequentially in registration order.
    # By default, a crashing hook does not affect the request outcome.
    async with SafeWebClient(event_hooks=(log_event, log_retry)) as client:

        # Replace "https://example.com" with your target URL.
        result = await client.fetch("https://example.com")

    print()
    print(f"Final result: success={result.success}")
    if result.success:
        print(f"Status: {result.status_code}  Size: {result.size_bytes} bytes")
    else:
        print(f"Error [{result.error_code}]: {result.error_message}")


if __name__ == "__main__":
    asyncio.run(main())
