from __future__ import annotations

import sys
from pathlib import Path

import pytest


# Allow `import izthon` without requiring callers to set PYTHONPATH=src.
_ROOT = Path(__file__).resolve().parents[1]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))


@pytest.fixture(autouse=True)
def _reset_izthon_state():
    """Reset contextual state between tests (language/config)."""
    from izthon.i18n import set_language
    from izthon.astro import reset_config, reset_plugins

    set_language("zh-CN")
    reset_config()
    reset_plugins()

    yield
