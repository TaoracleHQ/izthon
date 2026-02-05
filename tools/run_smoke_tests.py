from __future__ import annotations

"""
Lightweight smoke tests (no external deps).

Run:
  PYTHONPATH=src python3 tools/run_smoke_tests.py
"""

from izthon.astro import config, load_plugin, load_plugins, with_options, by_lunar, by_solar
from izthon.i18n import set_language


def _assert_eq(got, expected, msg: str = "") -> None:
    if got != expected:
        raise AssertionError(f"{msg} expected={expected!r} got={got!r}")


def test_basic_by_solar_and_horoscope() -> None:
    set_language("zh-CN")
    config({"year_divide": "exact", "algorithm": "default"})

    a = by_solar("2000-8-16", 2, "女", True)
    _assert_eq(a.solar_date, "2000-8-16", "solar_date")
    _assert_eq(a.lunar_date, "二〇〇〇年七月十七", "lunar_date")
    _assert_eq(a.chinese_date, "庚辰 甲申 丙午 庚寅", "chinese_date")
    _assert_eq(a.time, "寅时", "time")
    _assert_eq(a.sign, "狮子座", "sign")
    _assert_eq(a.zodiac, "龙", "zodiac")
    _assert_eq(a.earthly_branch_of_soul_palace, "午", "earthly_branch_of_soul_palace")
    _assert_eq(a.earthly_branch_of_body_palace, "戌", "earthly_branch_of_body_palace")
    _assert_eq(a.soul, "破军", "soul")
    _assert_eq(a.body, "文昌", "body")
    _assert_eq(a.five_elements_class, "木三局", "five_elements_class")

    assert a.palace("父母").is_empty() is True
    assert a.palace("父母").is_empty(["陀罗"]) is False
    assert a.palace("父母").is_empty(["文昌", "文曲"]) is True

    h = a.horoscope("2023-8-19 3:12")
    _assert_eq(h.solar_date, "2023-8-19", "horoscope.solar_date")
    _assert_eq((h.decadal.index, h.decadal.heavenly_stem, h.decadal.earthly_branch), (2, "庚", "辰"), "decadal")
    _assert_eq((h.yearly.index, h.yearly.heavenly_stem, h.yearly.earthly_branch), (1, "癸", "卯"), "yearly")
    _assert_eq((h.monthly.index, h.monthly.heavenly_stem, h.monthly.earthly_branch), (3, "庚", "申"), "monthly")
    _assert_eq((h.daily.index, h.daily.heavenly_stem, h.daily.earthly_branch), (6, "己", "酉"), "daily")
    _assert_eq((h.hourly.index, h.hourly.heavenly_stem, h.hourly.earthly_branch), (8, "丙", "寅"), "hourly")


def test_day_divide_current() -> None:
    set_language("zh-CN")
    a = with_options(
        {
            "type": "solar",
            "date_str": "1987-9-23",
            "time_index": 12,
            "gender": "female",
            "fix_leap": True,
            "language": "zh-CN",
            "config": {"year_divide": "normal", "day_divide": "current"},
        }
    )
    _assert_eq(a.lunar_date, "一九八七年八月初一", "lunar_date")
    _assert_eq(a.chinese_date, "丁卯 己酉 丙子 戊子", "chinese_date")
    _assert_eq(a.time, "晚子时", "time")
    assert a.palace("命宫").is_empty() is True
    assert a.palace("命宫").has(["火星", "天钺"]) is True


def test_earth_human_plate() -> None:
    set_language("zh-CN")
    config({"algorithm": "zhongzhou"})

    earth = with_options(
        {"date_str": "1979-08-21", "type": "solar", "time_index": 7, "gender": "male", "astro_type": "earth"}
    )
    _assert_eq(earth.earthly_branch_of_soul_palace, "卯", "earth.earthly_branch_of_soul_palace")
    soul = earth.palace("命宫")
    _assert_eq((soul.index, soul.heavenly_stem, soul.earthly_branch), (1, "丁", "卯"), "earth soul palace")

    human = with_options(
        {"date_str": "1979-08-21", "type": "solar", "time_index": 8, "gender": "male", "astro_type": "human"}
    )
    _assert_eq(human.earthly_branch_of_soul_palace, "寅", "human.earthly_branch_of_soul_palace")
    soul2 = human.palace("命宫")
    _assert_eq((soul2.index, soul2.heavenly_stem, soul2.earthly_branch), (0, "丙", "寅"), "human soul palace")


def test_korean_i18n() -> None:
    set_language("zh-CN")
    config({"year_divide": "exact", "algorithm": "default"})
    a = by_solar("2000-8-16", 2, "女", True, "ko-KR")
    _assert_eq(a.chinese_date, "경진 갑신 병오 경인", "ko chinese_date")
    _assert_eq(a.sign, "사자궁", "ko sign")
    _assert_eq(a.zodiac, "용", "ko zodiac")


def test_plugins() -> None:
    set_language("zh-CN")

    def plugin1(astrolabe):
        astrolabe.my_new_func = lambda: astrolabe.five_elements_class

    def plugin2(astrolabe):
        astrolabe.major_star = lambda: ",".join(s.name for s in (astrolabe.palace("命宫").major_stars or []) if s.type == "major")

    load_plugins([plugin1])
    load_plugin(plugin2)

    a = by_solar("2023-10-18", 4, "female", True)
    assert a.my_new_func() in {"火六局", "火6局", "火六局"}  # allow minor locale variants
    assert isinstance(a.major_star(), str)


def main() -> None:
    test_basic_by_solar_and_horoscope()
    test_day_divide_current()
    test_earth_human_plate()
    test_korean_i18n()
    test_plugins()
    print("smoke tests passed")


if __name__ == "__main__":
    main()

