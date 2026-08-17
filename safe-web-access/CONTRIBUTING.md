# Contributing to Safe Web Access

Thank you for considering contributing to `safe-web-access`!

## Development Setup

1. Clone the repository and navigate to the project directory:
   ```bash
   cd safe_web_access
   ```

2. Create a virtual environment and install the package in editable mode with development dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

## Running Verification Commands

Before submitting code changes, ensure all verification checks pass clean:

```bash
# Run pytest with coverage
python -m pytest tests --cov=safe_web_access --cov-report=term-missing

# Run linting and formatting checks
python -m ruff check src tests
python -m black --check src tests

# Run static type checking
python -m mypy src/safe_web_access

# Verify package build
python -m build
python -m twine check dist/*
```

## Security Guidelines

- Do not perform real DNS or HTTP network requests in unit tests.
- Always use mock fixtures for network calls.
- Never log or include sensitive headers, cookies, credentials, or response body data in event hooks.
