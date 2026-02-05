from __future__ import annotations

from collections.abc import Callable
from typing import Any, Literal

from ..i18n import kot

YearDivide = Literal["normal", "exact"]
HoroscopeDivide = Literal["normal", "exact"]
AgeDivide = Literal["normal", "birthday"]
DayDivide = Literal["current", "forward"]
Algorithm = Literal["default", "zhongzhou"]

Plugin = Callable[[Any], None]

_plugins: list[Plugin] = []
_mutagens: dict[str, list[str]] = {}
_brightness: dict[str, list[str]] = {}

_year_divide: YearDivide = "normal"
_horoscope_divide: HoroscopeDivide = "normal"
_age_divide: AgeDivide = "normal"
_day_divide: DayDivide = "forward"
_algorithm: Algorithm = "default"


def load_plugins(plugins: list[Plugin]) -> None:
    _plugins.extend(plugins)


def load_plugin(plugin: Plugin) -> None:
    _plugins.append(plugin)


def get_plugins() -> list[Plugin]:
    return list(_plugins)


def config(cfg: dict[str, Any]) -> None:
    """Global config entrypoint (Pythonic equivalent of iztro.astro.config())."""
    global _year_divide, _horoscope_divide, _age_divide, _day_divide, _algorithm

    mutagens = cfg.get("mutagens")
    brightness = cfg.get("brightness")

    if mutagens:
        for key, value in mutagens.items():
            _mutagens[kot(str(key))] = [kot(str(item)) for item in (value or [])]

    if brightness:
        for key, value in brightness.items():
            _brightness[kot(str(key))] = [kot(str(item)) for item in (value or [])]

    _year_divide = cfg.get("year_divide", _year_divide)
    _horoscope_divide = cfg.get("horoscope_divide", _horoscope_divide)
    _age_divide = cfg.get("age_divide", _age_divide)
    _day_divide = cfg.get("day_divide", _day_divide)
    _algorithm = cfg.get("algorithm", _algorithm)


def get_config() -> dict[str, Any]:
    return {
        "mutagens": _mutagens,
        "brightness": _brightness,
        "year_divide": _year_divide,
        "horoscope_divide": _horoscope_divide,
        "age_divide": _age_divide,
        "day_divide": _day_divide,
        "algorithm": _algorithm,
    }

