"""
Synchronous fetch example for safe-web-access.

This script demonstrates fetching a single URL using SyncSafeWebClient,
which provides a plain synchronous interface — no async/await required.

To run:
    python examples/sync_fetch.py
"""

from safe_web_access import SyncSafeWebClient


def main() -> None:
    # SyncSafeWebClient is used as a context manager.
    # It runs a background event loop and thread internally.
    # The context manager closes everything cleanly when the block ends.
    with SyncSafeWebClient() as client:

        # fetch() blocks until the result is ready.
        # It never raises — all outcomes come back as SafeWebResult.
        # Replace "https://example.com" with your target URL.
        result = client.fetch("https://example.com")

        if result.success:
            # result.body is always raw bytes when success=True.
            print(f"Status:        {result.status_code}")
            print(f"Content-Type:  {result.content_type}")
            print(f"Body size:     {result.size_bytes} bytes")
            print(f"Redirects:     {result.redirect_count}")
            print(f"Elapsed:       {result.elapsed_ms} ms")
        else:
            # result.error_code is a short machine-readable code.
            # result.error_message is a human-readable description.
            print(f"Fetch failed [{result.error_code}]: {result.error_message}")


if __name__ == "__main__":
    main()
