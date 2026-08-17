# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| 0.1.x | ✅ Yes — current release |

## Reporting a Vulnerability

**Please do not open a public GitHub issue to report a security vulnerability.** Public disclosure before a fix is available may put users at risk.

To report a vulnerability in `safe-web-access`:

1. Open a **private security advisory** on GitHub at:
   `https://github.com/mirza1272/safe-web-access/security/advisories/new`

2. Include the following information in your report:
   - A clear description of the vulnerability and the affected component or module
   - Steps to reproduce the issue (a minimal code example is very helpful)
   - The impact you believe this vulnerability has on deployments
   - Any mitigations or workarounds you are aware of
   - Python version and operating system where you reproduced the issue

3. After you submit the advisory, you will receive an acknowledgement. A fix timeline will be agreed upon before any public disclosure.

4. **Please wait for a coordinated fix release before disclosing the vulnerability publicly.** We are committed to working with reporters in good faith.

## What to Expect

- Acknowledgement of your report once the advisory is opened.
- Regular updates on the status of the fix as it progresses.
- Credit in the release notes for your report (unless you prefer to remain anonymous).

## Security Controls Overview

For a detailed description of the security model, threat protections, and known limitations, see [docs/SECURITY.md](docs/SECURITY.md).

Key protections include:

- **SSRF prevention:** Hostname resolution and IP classification blocks private, loopback, link-local, multicast, and reserved addresses before any connection is opened.
- **Domain and port policies:** Configurable allowlists, blocklists, subdomain wildcards, and port restrictions.
- **Manual redirect inspection:** Every 3xx redirect destination is validated against the same safety pipeline as the original URL.
- **Bounded downloads:** Hard byte caps on single responses and cumulative crawl sessions.
- **Event privacy:** Telemetry hooks never receive response body bytes, request headers, or credentials.

## Known Limitations

DNS rebinding (TOCTOU) remains a theoretical risk. IP validation occurs before the TCP connection is opened. A malicious DNS server that changes its answer between resolution and connection establishment can bypass the IP check. Network-level controls (firewalls, security groups) are recommended as a complementary defense. See [docs/SECURITY.md](docs/SECURITY.md) for details.
