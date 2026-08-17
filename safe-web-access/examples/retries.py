"""
Retry policy configuration example for safe-web-access.

This script demonstrates how to configure automatic retries with exponential
backoff for temporary server failures such as 429 (rate limited) or 503
(service temporarily unavailable).

To run:
    python examples/retries.py
"""

import asyncio

from safe_web_access import RetryPolicy, SafeWebClient, SafeWebSettings


async def main() -> None:
    # RetryPolicy controls how many times to retry and how long to wait.
    #
    # max_attempts=3: Try up to 3 times total (1 initial + 2 retries).
    # backoff_base_seconds=0.5: Wait 0.5s before the first retry.
    # backoff_multiplier=2.0: Double the wait on each retry (0.5s → 1.0s → cap).
    # backoff_max_seconds=10.0: Never wait more than 10 seconds between retries.
    # retry_status_codes=(429, 503, 504): Retry on these HTTP status codes.
    # respect_retry_after=True: Use the server's Retry-After header if present.
    # jitter_seconds=0.1: Add 0.1s to every delay to prevent retry storms.
    retry_policy = RetryPolicy(
        max_attempts=3,
        backoff_base_seconds=0.5,
        backoff_multiplier=2.0,
        backoff_max_seconds=10.0,
        retry_status_codes=(429, 503, 504),
        respect_retry_after=True,
        jitter_seconds=0.1,
    )

    settings = SafeWebSettings(retry_policy=retry_policy)

    async with SafeWebClient(settings=settings) as client:
        # Replace "https://example.com" with your target URL.
        result = await client.fetch("https://example.com")

        if result.success:
            print(f"Success after {result.attempt_count} attempt(s).")
            print(f"Status:    {result.status_code}")
            print(f"Elapsed:   {result.elapsed_ms} ms")
        else:
            print(f"Failed after {result.attempt_count} attempt(s).")
            print(f"Error [{result.error_code}]: {result.error_message}")
            if result.status_code:
                print(f"Final HTTP status: {result.status_code}")


if __name__ == "__main__":
    asyncio.run(main())
