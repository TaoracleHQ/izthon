from __future__ import annotations

from izthon.astro import by_lunar, by_solar, config, load_plugin, load_plugins, with_options


def _install_test_plugins_and_config() -> None:
    def my_test_plugin(astrolabe) -> None:
        astrolabe.my_new_func = lambda: astrolabe.five_elements_class

    def my_test_plugin2(astrolabe) -> None:
        def major_star() -> str:
            palace = astrolabe.palace("命宫")
            stars = ",".join(
                s.name
                for s in (palace.major_stars if palace else [])
                if s.type == "major" and s.name not in {"禄存", "天马"}
            )
            if not stars:
                palace2 = astrolabe.palace("迁移")
                stars = ",".join(
                    s.name
                    for s in (palace2.major_stars if palace2 else [])
                    if s.type == "major" and s.name not in {"禄存", "天马"}
                )
            return stars or ""

        astrolabe.major_star = major_star

    load_plugins([my_test_plugin])
    load_plugin(my_test_plugin2)

    config(
        {
            "mutagens": {"庚": ["太阳", "武曲", "天同", "天相"]},
            "brightness": {"贪狼": ["旺"] * 12},
        }
    )


def test_plugin_by_solar():
    _install_test_plugins_and_config()
    astrolabe = by_solar("2023-10-18", 4, "female")
    assert astrolabe.my_new_func() == "火六局"
    assert astrolabe.major_star() == "七杀"


def test_plugin_by_lunar():
    _install_test_plugins_and_config()
    astrolabe = by_lunar("2023-10-18", 4, "female")
    assert astrolabe.my_new_func() == "火六局"
    assert astrolabe.major_star() == "太阳,太阴"


def test_plugin_with_options():
    _install_test_plugins_and_config()
    astrolabe = with_options({"date_str": "2023-10-18", "time_index": 4, "gender": "female", "type": "lunar"})
    assert astrolabe.my_new_func() == "火六局"
    assert astrolabe.major_star() == "太阳,太阴"


def test_plugin_changed_configuration():
    _install_test_plugins_and_config()
    astrolabe = by_solar("2010-10-18", 4, "female")

    assert astrolabe.palace("命宫").has_mutagen("忌") is False
    assert astrolabe.palace("夫妻").has_mutagen("忌") is True
    assert astrolabe.star("贪狼").with_brightness("旺") is True


def test_plugin_not_changed_configuration():
    _install_test_plugins_and_config()
    astrolabe = by_solar("2011-10-18", 4, "female")

    assert astrolabe.palace("命宫").has_mutagen("权") is True
    assert astrolabe.palace("命宫").has_mutagen("忌") is True
    assert astrolabe.palace("福德").has_mutagen("科") is True
    assert astrolabe.palace("田宅").has_mutagen("禄") is False
    assert astrolabe.palace("财帛").flies_to("夫妻", "科") is True
    assert astrolabe.palace("财帛").flies_to("仆役", "忌") is True
    assert astrolabe.star("紫微").with_brightness("旺") is True

