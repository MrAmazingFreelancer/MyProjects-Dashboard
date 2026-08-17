"""
Async fetch example for safe-web-access.

This script demonstrates fetching a single URL safely using SafeWebClient.
The URL used here is an example — replace it with your actual target URL.

To run:
    python examples/async_fetch.py
"""

import asyncio

from safe_web_access import SafeWebClient


async def main() -> None:
    # SafeWebClient is used as an async context manager.
    # It closes the underlying HTTP connection automatically when done.
    async with SafeWebClient() as client:

        # fetch() always returns a SafeWebResult — it never raises.
        # Replace "https://example.com" with your target URL.
        result = await client.fetch("https://example.com")

        if result.success:
            # result.body is always raw bytes when success=True.
            # Decode it yourself to choose how to handle encoding issues.
            print(f"Status:        {result.status_code}")
            print(f"Content-Type:  {result.content_type}")
            print(f"Body size:     {result.size_bytes} bytes")
            print(f"Redirects:     {result.redirect_count}")
            print(f"Robots status: {result.robots_status}")
            print(f"Elapsed:       {result.elapsed_ms} ms")
            print(f"Attempt count: {result.attempt_count}")
            print(f"First 100 bytes: {result.body[:100]!r}")
        else:
            # result.error_code is a short machine-readable code.
            # result.error_message is a human-readable description.
            print(f"Fetch failed [{result.error_code}]: {result.error_message}")


if __name__ == "__main__":
    asyncio.run(main())
