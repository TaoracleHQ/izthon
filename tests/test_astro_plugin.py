from __future__ import annotations

from izthon.astro import by_lunar, by_solar, load_plugin, load_plugins, with_options


_CUSTOM_CONFIG = {
    "mutagens": {"庚": ["太阳", "武曲", "天同", "天相"]},
    "brightness": {"贪狼": ["旺"] * 12},
}


def add_five_elements_method(self):
    self.five_elements = lambda: self.five_elements_class


def add_major_star_method(self):
    def _major_star() -> str:
        stars = ",".join(
            item.name
            for item in self.palace("命宫").major_stars
            if item.type == "major" and item.name not in {"禄存", "天马"}
        )
        if stars:
            return stars
        return ",".join(
            item.name
            for item in self.palace("迁移").major_stars
            if item.type == "major" and item.name not in {"禄存", "天马"}
        )

    self.major_star = _major_star


def test_plugins_apply_to_by_solar():
    load_plugins([add_five_elements_method])
    load_plugin(add_major_star_method)

    astrolabe = by_solar("2023-10-18", 4, "female")

    assert astrolabe.five_elements() == "火六局"
    assert astrolabe.major_star() == "七杀"


def test_plugins_apply_to_by_lunar():
    load_plugins([add_five_elements_method, add_major_star_method])

    astrolabe = by_lunar("2023-10-18", 4, "female")

    assert astrolabe.five_elements() == "火六局"
    assert astrolabe.major_star() == "太阳,太阴"


def test_plugins_apply_to_with_options():
    load_plugins([add_five_elements_method, add_major_star_method])

    astrolabe = with_options(
        date_value="2023-10-18",
        date_type="lunar",
        time_index=4,
        gender="female",
    )

    assert astrolabe.five_elements() == "火六局"
    assert astrolabe.major_star() == "太阳,太阴"


def test_custom_config_by_solar():
    astrolabe = by_solar("2010-10-18", 4, "female", config=_CUSTOM_CONFIG)

    assert astrolabe.palace("命宫").has_mutagen("忌") is False
    assert astrolabe.palace("夫妻").has_mutagen("忌") is True
    assert astrolabe.star("贪狼").with_brightness("旺") is True


def test_custom_config_by_lunar():
    astrolabe = by_lunar("2023-10-18", 4, "female", config=_CUSTOM_CONFIG)

    assert astrolabe.palace("命宫").has_mutagen("权") is False
    assert astrolabe.star("贪狼").with_brightness("旺") is True


def test_custom_config_isolation_between_calls():
    with_cfg = by_solar("2010-10-18", 4, "female", config=_CUSTOM_CONFIG)
    default_cfg = by_solar("2010-10-18", 4, "female")

    assert with_cfg.palace("夫妻").has_mutagen("忌") is True
    assert default_cfg.palace("夫妻").has_mutagen("忌") is False
