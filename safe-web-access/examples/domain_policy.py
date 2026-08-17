"""
Domain policy configuration example for safe-web-access.

This script shows how to restrict outbound requests using DomainPolicy.
It demonstrates:
  - Allowlist (only allow specific domains)
  - Blocklist (block specific subdomains even within allowed domains)
  - Port policy (allow non-default ports)

To run:
    python examples/domain_policy.py
"""

import asyncio

from safe_web_access import DomainPolicy, SafeWebClient, SafeWebSettings


async def main() -> None:
    # Build a domain policy:
    # - Only allow requests to example.com and its subdomains
    # - Explicitly block internal.example.com
    # - Allow standard ports plus 8443
    # - allow_subdomains=True means api.example.com is also allowed
    policy = DomainPolicy(
        allowed_domains=("example.com",),
        blocked_domains=("internal.example.com",),
        allowed_ports=(80, 443, 8443),
        allow_subdomains=True,
    )

    # Attach the policy to SafeWebSettings.
    # All other settings use their defaults.
    settings = SafeWebSettings(domain_policy=policy)

    async with SafeWebClient(settings=settings) as client:

        # This URL is within the allowed domain — it will proceed to the network check.
        # (In this example, the fetch may succeed or fail depending on real DNS/network.)
        result = await client.fetch("https://example.com")
        print(
            f"example.com → success={result.success} code={result.error_code or result.status_code}"
        )

        # This URL is explicitly blocked by blocked_domains.
        # The fetch will fail immediately with error_code="blocked_domain" — no network call.
        blocked_result = await client.fetch("https://internal.example.com/admin")
        print(
            f"internal.example.com → success={blocked_result.success} error_code={blocked_result.error_code}"
        )

        # This URL is a subdomain of example.com and allow_subdomains=True,
        # so it is allowed. The fetch proceeds to the SSRF and network checks.
        sub_result = await client.fetch("https://api.example.com")
        print(
            f"api.example.com → success={sub_result.success} code={sub_result.error_code or sub_result.status_code}"
        )


if __name__ == "__main__":
    asyncio.run(main())
