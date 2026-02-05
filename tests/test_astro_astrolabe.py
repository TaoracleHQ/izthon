from __future__ import annotations

import pytest

from izthon.astro import (
    by_lunar,
    by_solar,
    config,
    get_major_star_by_lunar_date,
    get_major_star_by_solar_date,
    get_sign_by_lunar_date,
    get_sign_by_solar_date,
    get_zodiac_by_solar_date,
    with_options,
)


def test_by_solar_basic_and_horoscope_queries():
    # Match iztro upstream test cases (`src/__tests__/astro/astro.test.ts`).
    config({"year_divide": "exact", "algorithm": "default"})
    astrolabe = by_solar("2000-8-16", 2, "女", True)

    assert astrolabe.solar_date == "2000-8-16"
    assert astrolabe.lunar_date == "二〇〇〇年七月十七"
    assert astrolabe.chinese_date == "庚辰 甲申 丙午 庚寅"
    assert astrolabe.time == "寅时"
    assert astrolabe.sign == "狮子座"
    assert astrolabe.zodiac == "龙"
    assert astrolabe.earthly_branch_of_soul_palace == "午"
    assert astrolabe.earthly_branch_of_body_palace == "戌"
    assert astrolabe.soul == "破军"
    assert astrolabe.body == "文昌"
    assert astrolabe.five_elements_class == "木三局"

    assert astrolabe.palace("父母").is_empty() is True
    assert astrolabe.palace("父母").is_empty(["陀罗"]) is False
    assert astrolabe.palace("命宫").is_empty() is False
    assert astrolabe.palace("父母").is_empty(["文昌", "文曲"]) is True

    horoscope = astrolabe.horoscope("2023-8-19 3:12")

    assert horoscope.solar_date == "2023-8-19"
    assert horoscope.decadal.index == 2
    assert horoscope.decadal.heavenly_stem == "庚"
    assert horoscope.decadal.earthly_branch == "辰"
    assert horoscope.decadal.palace_names == [
        "夫妻",
        "兄弟",
        "命宫",
        "父母",
        "福德",
        "田宅",
        "官禄",
        "仆役",
        "迁移",
        "疾厄",
        "财帛",
        "子女",
    ]
    assert horoscope.decadal.mutagen == ["太阳", "武曲", "太阴", "天同"]
    assert horoscope.age.index == 9
    assert horoscope.age.nominal_age == 24

    assert horoscope.yearly.index == 1
    assert horoscope.yearly.heavenly_stem == "癸"
    assert horoscope.yearly.earthly_branch == "卯"
    assert horoscope.yearly.palace_names == [
        "兄弟",
        "命宫",
        "父母",
        "福德",
        "田宅",
        "官禄",
        "仆役",
        "迁移",
        "疾厄",
        "财帛",
        "子女",
        "夫妻",
    ]
    assert horoscope.yearly.mutagen == ["破军", "巨门", "太阴", "贪狼"]

    assert horoscope.monthly.index == 3
    assert horoscope.monthly.heavenly_stem == "庚"
    assert horoscope.monthly.earthly_branch == "申"
    assert horoscope.monthly.palace_names == [
        "子女",
        "夫妻",
        "兄弟",
        "命宫",
        "父母",
        "福德",
        "田宅",
        "官禄",
        "仆役",
        "迁移",
        "疾厄",
        "财帛",
    ]
    assert horoscope.monthly.mutagen == ["太阳", "武曲", "太阴", "天同"]

    assert horoscope.daily.index == 6
    assert horoscope.daily.heavenly_stem == "己"
    assert horoscope.daily.earthly_branch == "酉"
    assert horoscope.daily.palace_names == [
        "迁移",
        "疾厄",
        "财帛",
        "子女",
        "夫妻",
        "兄弟",
        "命宫",
        "父母",
        "福德",
        "田宅",
        "官禄",
        "仆役",
    ]
    assert horoscope.daily.mutagen == ["武曲", "贪狼", "天梁", "文曲"]

    assert horoscope.hourly.index == 8
    assert horoscope.hourly.heavenly_stem == "丙"
    assert horoscope.hourly.earthly_branch == "寅"
    assert horoscope.hourly.palace_names == [
        "官禄",
        "仆役",
        "迁移",
        "疾厄",
        "财帛",
        "子女",
        "夫妻",
        "兄弟",
        "命宫",
        "父母",
        "福德",
        "田宅",
    ]
    assert horoscope.hourly.mutagen == ["天同", "天机", "文昌", "廉贞"]

    assert horoscope.has_horoscope_stars("疾厄", "decadal", ["流陀", "流曲", "运昌"]) is True
    assert horoscope.has_horoscope_stars("财帛", "yearly", ["流陀", "流曲", "运昌"]) is True
    assert horoscope.has_horoscope_stars("迁移", "monthly", ["流陀", "流曲", "运昌"]) is True
    assert horoscope.has_horoscope_stars("田宅", "daily", ["流陀", "流曲", "运昌"]) is True
    assert horoscope.not_have_horoscope_stars("疾厄", "decadal", ["流陀", "流曲", "运昌"]) is False
    assert horoscope.not_have_horoscope_stars("疾厄", "decadal", ["流陀", "流鸾", "运昌"]) is False
    assert horoscope.not_have_horoscope_stars("疾厄", "decadal", ["流喜", "流鸾", "流魁"]) is True
    assert horoscope.has_one_of_horoscope_stars("疾厄", "decadal", ["流陀", "流曲", "运昌"]) is True
    assert horoscope.has_one_of_horoscope_stars("疾厄", "decadal", ["流喜", "流鸾", "流魁"]) is False

    assert horoscope.has_horoscope_mutagen("兄弟", "decadal", "禄") is True
    assert horoscope.has_horoscope_mutagen("夫妻", "decadal", "权") is True
    assert horoscope.has_horoscope_mutagen("疾厄", "decadal", "科") is True
    assert horoscope.has_horoscope_mutagen("子女", "decadal", "忌") is True

    assert horoscope.has_horoscope_mutagen("仆役", "yearly", "禄") is True
    assert horoscope.has_horoscope_mutagen("夫妻", "yearly", "权") is True
    assert horoscope.has_horoscope_mutagen("财帛", "yearly", "科") is True
    assert horoscope.has_horoscope_mutagen("子女", "yearly", "忌") is True

    assert horoscope.has_horoscope_mutagen("夫妻", "monthly", "禄") is True
    assert horoscope.has_horoscope_mutagen("子女", "monthly", "权") is True
    assert horoscope.has_horoscope_mutagen("迁移", "monthly", "科") is True
    assert horoscope.has_horoscope_mutagen("财帛", "monthly", "忌") is True

    assert horoscope.has_horoscope_mutagen("迁移", "daily", "禄") is True
    assert horoscope.has_horoscope_mutagen("官禄", "daily", "权") is True
    assert horoscope.has_horoscope_mutagen("疾厄", "daily", "科") is True
    assert horoscope.has_horoscope_mutagen("夫妻", "daily", "忌") is True

    age_palace = horoscope.age_palace()
    assert age_palace.name == "仆役"
    assert age_palace.heavenly_stem == "丁"
    assert age_palace.earthly_branch == "亥"

    original_palace = horoscope.palace("命宫", "origin")
    assert original_palace.name == "命宫"
    assert original_palace.heavenly_stem == "壬"
    assert original_palace.earthly_branch == "午"

    decadal_palace = horoscope.palace("命宫", "decadal")
    assert decadal_palace.name == "夫妻"
    assert decadal_palace.heavenly_stem == "庚"
    assert decadal_palace.earthly_branch == "辰"

    decadal_surpalaces = horoscope.surround_palaces("命宫", "decadal")
    assert decadal_surpalaces.target.name == "夫妻"
    assert decadal_surpalaces.target.heavenly_stem == "庚"
    assert decadal_surpalaces.target.earthly_branch == "辰"
    assert decadal_surpalaces.opposite.name == "官禄"
    assert decadal_surpalaces.opposite.heavenly_stem == "丙"
    assert decadal_surpalaces.opposite.earthly_branch == "戌"
    assert decadal_surpalaces.career.name == "福德"
    assert decadal_surpalaces.career.heavenly_stem == "甲"
    assert decadal_surpalaces.career.earthly_branch == "申"
    assert decadal_surpalaces.wealth.name == "迁移"
    assert decadal_surpalaces.wealth.heavenly_stem == "戊"
    assert decadal_surpalaces.wealth.earthly_branch == "子"

    original_surpalaces = horoscope.surround_palaces("夫妻", "origin")
    assert original_surpalaces.target.name == "夫妻"
    assert original_surpalaces.target.heavenly_stem == "庚"
    assert original_surpalaces.target.earthly_branch == "辰"
    assert original_surpalaces.opposite.name == "官禄"
    assert original_surpalaces.opposite.heavenly_stem == "丙"
    assert original_surpalaces.opposite.earthly_branch == "戌"
    assert original_surpalaces.career.name == "福德"
    assert original_surpalaces.career.heavenly_stem == "甲"
    assert original_surpalaces.career.earthly_branch == "申"
    assert original_surpalaces.wealth.name == "迁移"
    assert original_surpalaces.wealth.heavenly_stem == "戊"
    assert original_surpalaces.wealth.earthly_branch == "子"

    yearly_palace = horoscope.palace("命宫", "yearly")
    assert yearly_palace.name == "子女"
    assert yearly_palace.heavenly_stem == "己"
    assert yearly_palace.earthly_branch == "卯"

    monthly_palace = horoscope.palace("命宫", "monthly")
    assert monthly_palace.name == "兄弟"
    assert monthly_palace.heavenly_stem == "辛"
    assert monthly_palace.earthly_branch == "巳"

    daily_palace = horoscope.palace("命宫", "daily")
    assert daily_palace.name == "福德"
    assert daily_palace.heavenly_stem == "甲"
    assert daily_palace.earthly_branch == "申"

    hourly_palace = horoscope.palace("命宫", "hourly")
    assert hourly_palace.name == "官禄"
    assert hourly_palace.heavenly_stem == "丙"
    assert hourly_palace.earthly_branch == "戌"

    horoscope2 = astrolabe.horoscope("2023-10-19 3:12")
    assert horoscope2.age.index == 9
    assert horoscope2.age.nominal_age == 24


def test_horoscope_smoke():
    config({"year_divide": "exact", "algorithm": "default"})
    astrolabe = by_solar("1991-3-7", 6, "女", True)
    horoscope = astrolabe.horoscope("2025-3-26")

    assert horoscope.solar_date == "2025-3-26"
    assert horoscope.decadal.index == 8
    assert horoscope.decadal.heavenly_stem == "戊"
    assert horoscope.decadal.earthly_branch == "戌"
    assert horoscope.yearly.index == 3
    assert horoscope.yearly.heavenly_stem == "乙"
    assert horoscope.yearly.earthly_branch == "巳"
    assert horoscope.monthly.index == 10
    assert horoscope.monthly.heavenly_stem == "己"
    assert horoscope.monthly.earthly_branch == "卯"
    assert horoscope.daily.index == 0
    assert horoscope.daily.heavenly_stem == "甲"
    assert horoscope.daily.earthly_branch == "午"


@pytest.mark.parametrize(
    ("language", "expected_chinese_date"),
    [
        ("ko-KR", "경진 갑신 병오 경인"),
        ("vi-VN", "Canh Thìn - Giáp Thân - Bính Ngọ - Canh Dần"),
    ],
)
def test_by_solar_multilanguage_chinese_date(language: str, expected_chinese_date: str):
    astrolabe = by_solar("2000-8-16", 2, "女", True, language)
    assert astrolabe.chinese_date == expected_chinese_date


def test_by_lunar_do_not_fix_leap_month():
    # `is_leap_month=True`, `fix_leap=False`
    astrolabe = by_lunar("2023-2-20", 4, "女", is_leap_month=True, fix_leap=False)

    assert astrolabe.earthly_branch_of_soul_palace == "亥"
    assert astrolabe.earthly_branch_of_body_palace == "未"
    assert astrolabe.soul == "巨门"
    assert astrolabe.body == "天同"
    assert astrolabe.five_elements_class == "水二局"
    assert astrolabe.star("紫微").palace().name == "命宫"


def test_get_zodiac_by_solar_date():
    assert get_zodiac_by_solar_date("2023-2-20") == "兔"
    assert get_zodiac_by_solar_date("2023-2-20", "en-US") == "rabbit"


def test_get_sign_by_solar_date():
    assert get_sign_by_solar_date("2023-9-5") == "处女座"
    assert get_sign_by_solar_date("2023-9-5", "en-US") == "virgo"


def test_get_sign_by_lunar_date():
    assert get_sign_by_lunar_date("2023-7-21") == "处女座"
    assert get_sign_by_lunar_date("2023-7-21", False, "en-US") == "virgo"


def test_get_sign_by_lunar_date_leap_month():
    # Leap lunar month affects sign mapping.
    assert get_sign_by_lunar_date("2023-2-3") == "双鱼座"
    assert get_sign_by_lunar_date("2023-2-3", True) == "白羊座"


def test_get_major_star_by_solar_date_leap_month():
    # Leap month fixes affect major-star lookup.
    assert get_major_star_by_solar_date("2023-4-7", 0) == "贪狼"
    assert get_major_star_by_solar_date("2023-4-7", 0, False) == "紫微,贪狼"
    assert get_major_star_by_solar_date("2023-4-7", 0, True, "ko-KR") == "탐랑"


def test_get_major_star_by_solar_date():
    assert get_major_star_by_solar_date("1987-05-16", 7) == "天机,天梁"


def test_get_major_star_by_lunar_date_leap_month():
    assert get_major_star_by_lunar_date("2023-2-17", 0) == "紫微,贪狼"
    assert get_major_star_by_lunar_date("2023-2-17", 0, True) == "贪狼"
    assert get_major_star_by_lunar_date("2023-2-17", 0, True, False) == "紫微,贪狼"


def test_childhood_decadal_name_and_index():
    astrolabe = by_solar("2023-10-18", 4, "female")

    horo1 = astrolabe.horoscope("2023-12-19")
    assert horo1.decadal.name == "童限"
    assert horo1.decadal.index == astrolabe.palace("命宫").index

    horo2 = astrolabe.horoscope("2024-12-29")
    assert horo2.decadal.name == "童限"
    assert horo2.decadal.index == astrolabe.palace("财帛").index

    horo3 = astrolabe.horoscope("2025-12-29")
    assert horo3.decadal.name == "童限"
    assert horo3.decadal.index == astrolabe.palace("疾厄").index


def test_nominal_age_divide_normal_vs_birthday():
    astrolabe1 = with_options(
        {
            "type": "solar",
            "date_str": "2000-8-16",
            "time_index": 2,
            "gender": "female",
            "config": {"age_divide": "normal"},
        }
    )
    horo1 = astrolabe1.horoscope("2023-8-19 3:12")
    assert horo1.age.index == 9
    assert horo1.age.nominal_age == 24

    astrolabe2 = with_options(
        {
            "type": "solar",
            "date_str": "2000-8-16",
            "time_index": 2,
            "gender": "female",
            "config": {"age_divide": "birthday"},
        }
    )
    horo2 = astrolabe2.horoscope("2023-8-19 3:12")
    assert horo2.age.index == 10
    assert horo2.age.nominal_age == 23
