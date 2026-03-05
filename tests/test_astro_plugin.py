from __future__ import annotations

from izthon.astro import by_lunar, by_solar


_CUSTOM_CONFIG = {
    "mutagens": {"庚": ["太阳", "武曲", "天同", "天相"]},
    "brightness": {"贪狼": ["旺"] * 12},
}


def test_custom_config_by_solar():
    astrolabe = by_solar("2010-10-18", 4, "female", config=_CUSTOM_CONFIG)

    assert astrolabe.palace("命宫").contains_mutagen("忌") is False
    assert astrolabe.palace("夫妻").contains_mutagen("忌") is True
    assert astrolabe.star("贪狼").with_brightness("旺") is True


def test_custom_config_by_lunar():
    astrolabe = by_lunar("2023-10-18", 4, "female", config=_CUSTOM_CONFIG)

    assert astrolabe.palace("命宫").contains_mutagen("权") is False
    assert astrolabe.star("贪狼").with_brightness("旺") is True


def test_custom_config_isolation_between_calls():
    with_cfg = by_solar("2010-10-18", 4, "female", config=_CUSTOM_CONFIG)
    default_cfg = by_solar("2010-10-18", 4, "female")

    assert with_cfg.palace("夫妻").contains_mutagen("忌") is True
    assert default_cfg.palace("夫妻").contains_mutagen("忌") is False
