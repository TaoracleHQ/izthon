from __future__ import annotations

from collections.abc import Mapping, Sequence
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Literal

from ..i18n import kot

YearDivide = Literal["normal", "exact"]
HoroscopeDivide = Literal["normal", "exact"]
AgeDivide = Literal["normal", "birthday"]
DayDivide = Literal["current", "forward"]
Algorithm = Literal["default", "zhongzhou"]

_YEAR_DIVIDE_SET: set[YearDivide] = {"normal", "exact"}
_HOROSCOPE_DIVIDE_SET: set[HoroscopeDivide] = {"normal", "exact"}
_AGE_DIVIDE_SET: set[AgeDivide] = {"normal", "birthday"}
_DAY_DIVIDE_SET: set[DayDivide] = {"current", "forward"}
_ALGORITHM_SET: set[Algorithm] = {"default", "zhongzhou"}


def _new_default_config() -> dict[str, Any]:
    return {
        "mutagens": {},
        "brightness": {},
        "year_divide": "normal",
        "horoscope_divide": "normal",
        "age_divide": "normal",
        "day_divide": "forward",
        "algorithm": "default",
    }


_CURRENT_CONFIG: ContextVar[dict[str, Any]] = ContextVar("izthon_config", default=_new_default_config())


def _copy_config(cfg: Mapping[str, Any]) -> dict[str, Any]:
    mutagens_raw = cfg.get("mutagens", {})
    brightness_raw = cfg.get("brightness", {})
    mutagens: dict[str, list[str]] = {}
    brightness: dict[str, list[str]] = {}

    if isinstance(mutagens_raw, Mapping):
        for key, value in mutagens_raw.items():
            if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
                mutagens[str(key)] = [str(item) for item in value]

    if isinstance(brightness_raw, Mapping):
        for key, value in brightness_raw.items():
            if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
                brightness[str(key)] = [str(item) for item in value]

    return {
        "mutagens": mutagens,
        "brightness": brightness,
        "year_divide": cfg.get("year_divide", "normal"),
        "horoscope_divide": cfg.get("horoscope_divide", "normal"),
        "age_divide": cfg.get("age_divide", "normal"),
        "day_divide": cfg.get("day_divide", "forward"),
        "algorithm": cfg.get("algorithm", "default"),
    }


def _validate_literal(name: str, value: Any, valid_values: set[str]) -> str:
    if value not in valid_values:
        allowed = ", ".join(sorted(valid_values))
        raise ValueError(f"invalid {name}: {value!r}. allowed values: {allowed}")
    return str(value)


def _normalize_sequence(name: str, value: Any, expected_len: int) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError(f"{name} must be a sequence of strings")
    normalized = [kot(str(item)) for item in value]
    if len(normalized) != expected_len:
        raise ValueError(f"{name} must contain exactly {expected_len} items")
    return normalized


def _merge_config(base: Mapping[str, Any], patch: Mapping[str, Any]) -> dict[str, Any]:
    merged = _copy_config(base)

    mutagens = patch.get("mutagens")
    if mutagens is not None:
        if not isinstance(mutagens, Mapping):
            raise ValueError("mutagens must be a mapping of heavenly stem -> 4 stars")
        for key, value in mutagens.items():
            merged["mutagens"][kot(str(key))] = _normalize_sequence("mutagens entry", value, 4)

    brightness = patch.get("brightness")
    if brightness is not None:
        if not isinstance(brightness, Mapping):
            raise ValueError("brightness must be a mapping of star -> 12 brightness values")
        for key, value in brightness.items():
            merged["brightness"][kot(str(key))] = _normalize_sequence("brightness entry", value, 12)

    if "year_divide" in patch:
        merged["year_divide"] = _validate_literal("year_divide", patch["year_divide"], _YEAR_DIVIDE_SET)
    if "horoscope_divide" in patch:
        merged["horoscope_divide"] = _validate_literal(
            "horoscope_divide",
            patch["horoscope_divide"],
            _HOROSCOPE_DIVIDE_SET,
        )
    if "age_divide" in patch:
        merged["age_divide"] = _validate_literal("age_divide", patch["age_divide"], _AGE_DIVIDE_SET)
    if "day_divide" in patch:
        merged["day_divide"] = _validate_literal("day_divide", patch["day_divide"], _DAY_DIVIDE_SET)
    if "algorithm" in patch:
        merged["algorithm"] = _validate_literal("algorithm", patch["algorithm"], _ALGORITHM_SET)

    return merged


def set_config(cfg: Mapping[str, Any]) -> None:
    _CURRENT_CONFIG.set(_merge_config(_CURRENT_CONFIG.get(), cfg))


def reset_config() -> None:
    _CURRENT_CONFIG.set(_new_default_config())


@contextmanager
def using_config(cfg: Mapping[str, Any] | None):
    if cfg is None:
        yield
        return
    token = _CURRENT_CONFIG.set(_merge_config(_CURRENT_CONFIG.get(), cfg))
    try:
        yield
    finally:
        _CURRENT_CONFIG.reset(token)


def get_config() -> dict[str, Any]:
    return _copy_config(_CURRENT_CONFIG.get())
