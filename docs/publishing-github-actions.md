# Publishing With GitHub Actions

This repository uses Trusted Publishing for both TestPyPI and PyPI.

## Workflows

- `.github/workflows/ci.yml`
  - Runs tests, builds package, checks metadata on push/PR.
- `.github/workflows/publish-testpypi.yml`
  - Manual publish to TestPyPI (`workflow_dispatch`).
- `.github/workflows/publish-pypi.yml`
  - Auto publish to PyPI when a non-prerelease GitHub Release is published.

## PyPI/TestPyPI Setup

Create a Trusted Publisher on both PyPI and TestPyPI with:

- Owner: `TaoracleHQ`
- Repository name: `izthon`
- Workflow name:
  - `publish-testpypi.yml` for TestPyPI
  - `publish-pypi.yml` for PyPI
- Environment:
  - `testpypi` for TestPyPI
  - `pypi` for PyPI

No API token secret is required after Trusted Publisher is configured.
