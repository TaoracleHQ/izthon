from __future__ import annotations

from izthon.astro import with_options


def test_earth_plate_rearrange():
    result = with_options(
        date_value="1979-08-21",
        date_type="solar",
        time_index=7,
        gender="male",
        plate="earth",
        config={"algorithm": "zhongzhou"},
    )

    soul_palace = result.palace("命宫")
    assert result.earthly_branch_of_soul_palace == "卯"
    assert soul_palace.index == 1
    assert soul_palace.heavenly_stem == "丁"
    assert soul_palace.earthly_branch == "卯"
    assert soul_palace.major_stars[0].name == "天相"
    assert soul_palace.minor_stars[0].name == "文昌"
    assert result.five_elements_class == "火六局"
    assert soul_palace.decadal.range == (6, 15)
    assert soul_palace.decadal.heavenly_stem == "丁"
    assert soul_palace.decadal.earthly_branch == "卯"


def test_earth_plate_changsheng_12_diff_by_gender():
    result_female = with_options(
        date_value="1999-05-03",
        date_type="solar",
        time_index=8,
        gender="female",
        plate="earth",
        config={"algorithm": "zhongzhou"},
    )
    assert result_female.palaces[0].changsheng_12 == "病"
    assert result_female.palaces[1].changsheng_12 == "死"

    result_male = with_options(
        date_value="1999-05-03",
        date_type="solar",
        time_index=8,
        gender="male",
        plate="earth",
        config={"algorithm": "zhongzhou"},
    )
    assert result_male.palaces[0].changsheng_12 == "病"
    assert result_male.palaces[1].changsheng_12 == "衰"


def test_human_plate_rearrange():
    result = with_options(
        date_value="1979-08-21",
        date_type="solar",
        time_index=8,
        gender="male",
        plate="human",
        config={"algorithm": "zhongzhou"},
    )

    soul_palace = result.palace("命宫")
    assert result.earthly_branch_of_soul_palace == "寅"
    assert soul_palace.index == 0
    assert soul_palace.heavenly_stem == "丙"
    assert soul_palace.earthly_branch == "寅"
    assert soul_palace.major_stars[0].name == "太阳"
    assert soul_palace.minor_stars[0].name == "文昌"
    assert result.five_elements_class == "火六局"
    assert soul_palace.decadal.range == (6, 15)
    assert soul_palace.decadal.heavenly_stem == "丙"
    assert soul_palace.decadal.earthly_branch == "寅"


def test_human_plate_tianshi_tianshang_tiancai():
    result = with_options(
        date_value="1999-05-03",
        date_type="solar",
        time_index=8,
        gender="male",
        plate="human",
        config={"algorithm": "zhongzhou"},
    )

    assert result.star("天才").palace().index == 11
    assert result.star("天伤").palace().index == 3
    assert result.star("天使").palace().index == 1


def test_explicit_config_fix_github_242_244():
    astrolabe = with_options(
        date_value="1979.08.21",
        date_type="solar",
        time_index=6,
        gender="male",
        config={"year_divide": "normal"},
    )
    horoscope = astrolabe.horoscope("2025-06-10 12:00")
    assert horoscope.monthly.index == 7
    assert horoscope.daily.index == 9

    horoscope2 = astrolabe.horoscope("2020-6-6")
    assert horoscope2.monthly.index == 1
    assert horoscope2.daily.index == 3

    horoscope3 = astrolabe.horoscope("2020-6-7")
    assert horoscope3.monthly.index == 2
    assert horoscope3.daily.index == 5


def test_explicit_config_for_zhongzhou():
    astrolabe = with_options(
        date_value="2000.01.03",
        date_type="solar",
        time_index=11,
        gender="male",
        config={"algorithm": "zhongzhou"},
    )
    assert astrolabe.soul == "文曲"


def test_explicit_config_for_normal_horoscope():
    astrolabe = with_options(
        date_value="1999.05.03",
        date_type="solar",
        time_index=8,
        gender="male",
        config={"horoscope_divide": "normal"},
    )
    horoscope = astrolabe.horoscope("2025-02-02 10:00")
    assert horoscope.monthly.index == 9
    assert horoscope.daily.index == 1


def test_with_options_for_lunar_date():
    astrolabe = with_options(
        date_value="2023-10-18",
        date_type="lunar",
        time_index=4,
        gender="female",
    )

    assert astrolabe.five_elements_class == "火六局"
