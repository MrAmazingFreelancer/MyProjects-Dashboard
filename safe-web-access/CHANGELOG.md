# Changelog

All notable changes to the `safe-web-access` package will be documented in this file.

## [0.1.2] - 2026-08-13

### Added
- `SafeWebClient.start()` and `SyncSafeWebClient.start()` — return the client so a manual lifecycle reads as `start()` / `close()`, matching the context-manager form. Idempotent; raise `RuntimeError` once the client has been closed. They perform no setup work, because the constructor already builds everything.
- `SafeWebClient.close()` — awaitable alias of `aclose()`, so the asynchronous client offers the same method pair as the synchronous one. `aclose()` is unchanged and is not deprecated.

### Fixed
- Long-lived wrapper objects that construct the client once, keep it for the process lifetime and close it on shutdown previously had no `start()` to call and raised `AttributeError` on first use. That pattern now works without an `async with` block.

### Changed
- Documented the two lifecycle styles in the README, `docs/README.md`, `docs/USAGE.md`, `docs/HANDOVER.md` and `docs/SECURITY.md`.
- No behavioural change to fetching, safety checks, budgets, retries or results. This release is purely additive.

## [0.1.1] - 2026-08-02

### Added
- Corrected public links and improved documentation navigation.
- Improved PyPI and GitHub metadata (project URLs added to pyproject.toml).
- README discoverability improvements (added Who Is This Package For and Search Keywords).
- Added dedicated PyPI links for the usage, security, and maintainer guides.
- No runtime behavior changes.

## [0.1.0] - 2026-08-02

### Added
- Independent package structure using standard `src/safe_web_access` layout.
- Support for `DomainPolicy` for exact and wildcard domain/subdomain matching and port restrictions.
- Support for `RetryPolicy` with bounded exponential backoff, Retry-After header parsing, jitter, and custom status code configuration.
- `SyncSafeWebClient` synchronous wrapper backed by an internally managed background event loop.
- Structured telemetry event model (`SafeWebEventType`, `SafeWebEvent`) and event hooks.
- Package API exports: `SafeWebClient`, `SyncSafeWebClient`, `SafeWebSettings`, `DomainPolicy`, `RetryPolicy`, `CrawlBudget`, `SafeWebResult`, `SafeWebEvent`, `SafeWebEventType`.
- PyPI-ready build setup using Hatchling, ruff, black, mypy, pytest, and twine verification.
