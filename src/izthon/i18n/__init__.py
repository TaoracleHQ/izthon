from __future__ import annotations

import json
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path
from typing import Literal

import gettext

Language = Literal["en-US", "ja-JP", "ko-KR", "zh-CN", "zh-TW", "vi-VN"]

# Keep the same resource iteration order as the TS implementation.
LANG_ORDER: tuple[Language, ...] = ("en-US", "ja-JP", "ko-KR", "zh-CN", "zh-TW", "vi-VN")


class DictTranslations(gettext.NullTranslations):
    def __init__(self, catalog: dict[str, str]):
        super().__init__()
        self._catalog = catalog

    def gettext(self, message: str) -> str:  # type: ignore[override]
        if not message:
            return ""
        return self._catalog.get(message, message)


_BASE_DIR = Path(__file__).resolve().parent
_CATALOG_DIR = _BASE_DIR / "_catalogs"


def _load_catalog(lang: Language) -> dict[str, str]:
    p = _CATALOG_DIR / f"{lang}.json"
    return json.loads(p.read_text(encoding="utf-8"))


# Load all catalogs eagerly; they are small (~260 entries each) and needed for kot().
RESOURCES: dict[Language, dict[str, str]] = {lang: _load_catalog(lang) for lang in LANG_ORDER}
_TRANSLATIONS: dict[Language, DictTranslations] = {lang: DictTranslations(RESOURCES[lang]) for lang in LANG_ORDER}

_CURRENT_LANGUAGE: ContextVar[Language] = ContextVar("izthon_language", default="zh-CN")


def _validate_language(language: Language) -> Language:
    if language not in LANG_ORDER:
        raise ValueError(f"unsupported language: {language}")
    return language


def set_language(language: Language) -> None:
    _CURRENT_LANGUAGE.set(_validate_language(language))


def get_language() -> Language:
    return _CURRENT_LANGUAGE.get()


@contextmanager
def using_language(language: Language | None):
    if language is None:
        yield
        return
    token = _CURRENT_LANGUAGE.set(_validate_language(language))
    try:
        yield
    finally:
        _CURRENT_LANGUAGE.reset(token)


def translate(key: str) -> str:
    """Translate a key using the current language (gettext semantics)."""
    return _TRANSLATIONS[_CURRENT_LANGUAGE.get()].gettext(key)


def t(key: str) -> str:
    return translate(key)


def kot(value: str, k_prefix: str | None = None) -> str:
    """Key of translation (reverse lookup), matching iztro's TS behavior."""
    res = value
    for lang in LANG_ORDER:
        for trans_key, trans_val in RESOURCES[lang].items():
            if ((k_prefix and k_prefix in trans_key) or not k_prefix) and trans_val == value:
                return trans_key
    return res
