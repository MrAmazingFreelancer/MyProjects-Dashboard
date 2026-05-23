---
description: "Use when writing or updating tests (unit, integration, component, or regression). Enforces reliable structure, behavior-focused assertions, and pragmatic coverage expectations."
name: "Testing Standards"
applyTo:
  - "**/*.test.ts"
  - "**/*.test.tsx"
  - "**/*.test.js"
  - "**/*.test.jsx"
  - "**/*.spec.ts"
  - "**/*.spec.tsx"
  - "**/*.spec.js"
  - "**/*.spec.jsx"
---
# Testing Standards

## Intent
- Prefer tests that validate observable behavior rather than implementation details.
- Keep tests deterministic, isolated, and easy to diagnose when failures occur.

## Structure
- Use Arrange-Act-Assert ordering with clear variable names.
- Keep one primary behavior expectation per test case.
- Use table-driven tests for repeated input-output scenarios.

## Assertions
- Assert outcomes users or callers care about (returned values, rendered output, side effects).
- Avoid brittle assertions on private helpers, exact internal call counts, or incidental markup.
- Include at least one negative-path test for validation, error, or boundary behavior.

## Data and Mocks
- Prefer realistic fixtures over excessive mocking.
- Mock only external boundaries (network, filesystem, time, random, process env) when needed.
- Reset shared state between tests and avoid hidden cross-test coupling.

## Reliability
- Control nondeterminism: freeze or mock time, seed random values, and avoid real network calls.
- Avoid arbitrary sleeps; wait on explicit conditions.
- Keep tests independent so they can run in any order.

## Coverage Expectations
- Add or update tests for every bug fix and behavior change.
- Cover success path, at least one failure path, and at least one edge case.
- Prefer meaningful branch coverage in changed logic over chasing global percentage-only goals.

## PR Readiness
- Ensure changed tests are runnable locally with the project test command.
- If a scenario is intentionally untested, document the reason in the PR notes.
