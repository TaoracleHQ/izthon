from __future__ import annotations

import importlib

from ._config import get_config, reset_config, set_config

__all__ = [
    # config
    "set_config",
    "get_config",
    "reset_config",
    # palace core
    "get_soul_and_body",
    "get_five_elements_class",
    "get_palace_names",
    "get_horoscope",
    # main API
    "by_solar",
    "by_lunar",
    "rearrange_astrolabe",
    "get_zodiac_by_solar_date",
    "get_sign_by_solar_date",
    "get_sign_by_lunar_date",
    "get_major_star_by_solar_date",
    "get_major_star_by_lunar_date",
    # functional models
    "FunctionalAstrolabe",
    "FunctionalPalace",
    "FunctionalSurpalaces",
    "FunctionalHoroscope",
]

_LAZY_ATTRS: dict[str, str] = {
    # palace core
    "get_soul_and_body": "palace",
    "get_five_elements_class": "palace",
    "get_palace_names": "palace",
    "get_horoscope": "palace",
    # main API
    "by_solar": "astro",
    "by_lunar": "astro",
    "rearrange_astrolabe": "astro",
    "get_zodiac_by_solar_date": "astro",
    "get_sign_by_solar_date": "astro",
    "get_sign_by_lunar_date": "astro",
    "get_major_star_by_solar_date": "astro",
    "get_major_star_by_lunar_date": "astro",
    # functional models
    "FunctionalAstrolabe": "functional_astrolabe",
    "FunctionalPalace": "functional_palace",
    "FunctionalSurpalaces": "functional_surpalaces",
    "FunctionalHoroscope": "functional_horoscope",
}


def __getattr__(name: str):
    mod_name = _LAZY_ATTRS.get(name)
    if not mod_name:
        raise AttributeError(name)
    mod = importlib.import_module(f"{__name__}.{mod_name}")
    return getattr(mod, name)
