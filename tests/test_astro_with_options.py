from __future__ import annotations

from izthon.astro import config, with_options


def test_with_options_earth_type_rearrange():
    config({"algorithm": "zhongzhou"})

    result = with_options(
        {
            "date_str": "1979-08-21",
            "type": "solar",
            "time_index": 7,
            "gender": "male",
            "astro_type": "earth",
        }
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


def test_with_options_earth_type_changsheng12_diff_by_gender():
    config({"algorithm": "zhongzhou"})

    result_female = with_options(
        {
            "date_str": "1999-05-03",
            "type": "solar",
            "time_index": 8,
            "gender": "female",
            "astro_type": "earth",
        }
    )
    assert result_female.palaces[0].changsheng12 == "病"
    assert result_female.palaces[1].changsheng12 == "死"

    result_male = with_options(
        {
            "date_str": "1999-05-03",
            "type": "solar",
            "time_index": 8,
            "gender": "male",
            "astro_type": "earth",
        }
    )
    assert result_male.palaces[0].changsheng12 == "病"
    assert result_male.palaces[1].changsheng12 == "衰"


def test_with_options_human_type_rearrange():
    config({"algorithm": "zhongzhou"})

    result = with_options(
        {
            "date_str": "1979-08-21",
            "type": "solar",
            "time_index": 8,
            "gender": "male",
            "astro_type": "human",
        }
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


def test_with_options_human_type_rearrange_tianshi_tianshang_tiancai():
    config({"algorithm": "zhongzhou"})

    result = with_options(
        {
            "date_str": "1999-05-03",
            "type": "solar",
            "time_index": 8,
            "gender": "male",
            "astro_type": "human",
        }
    )

    assert result.star("天才").palace().index == 11
    assert result.star("天伤").palace().index == 3
    assert result.star("天使").palace().index == 1


def test_with_options_fix_github_242_244():
    config({"year_divide": "normal"})

    astrolabe = with_options(
        {
            "date_str": "1979.08.21",
            "type": "solar",
            "time_index": 6,
            "gender": "male",
        }
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

