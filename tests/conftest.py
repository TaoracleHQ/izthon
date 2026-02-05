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
    """Reset global state between tests (language, config, plugins)."""
    from izthon.i18n import set_language
    from izthon.astro import _config

    set_language("zh-CN")

    _config._plugins.clear()
    _config._mutagens.clear()
    _config._brightness.clear()

    _config._year_divide = "normal"
    _config._horoscope_divide = "normal"
    _config._age_divide = "normal"
    _config._day_divide = "forward"
    _config._algorithm = "default"

    yield

