from __future__ import annotations

import pytest

from izthon.astro import by_solar
from izthon.star import (
    get_chang_qu_index,
    get_chang_qu_index_by_heavenly_stem,
    get_daily_star_index,
    get_dahao_index,
    get_gu_gua_index,
    get_huagai_xianchi_index,
    get_huo_ling_index,
    get_kong_jie_index,
    get_kui_yue_index,
    get_lu_yang_tuo_ma_index,
    get_luan_xi_index,
    get_monthly_star_index,
    get_nianjie_index,
    get_timely_star_index,
    get_yearly_star_index,
    get_zuo_you_index,
)


def test_get_dahao_index():
    assert get_dahao_index("siEarthly") == 8


def test_santai_bazuo_for_lunar_month():
    res = by_solar("1979-08-21", 6, "male", language="zh-CN")
    assert res.star("三台").palace().index == 0
    assert res.star("八座").palace().index == 10


def test_xunkong_for_yin_year():
    res = by_solar("1979-08-21", 6, "male", language="zh-CN")
    assert res.star("旬空").palace().index == 11


def test_xunkong_for_yang_year():
    res = by_solar("1980-08-21", 6, "male", language="zh-CN")
    assert res.star("旬空").palace().index == 10


@pytest.mark.parametrize(
    ("heavenly_stem", "earthly_branch", "expected"),
    [
        ("癸", "卯", {"lu_index": 10, "yang_index": 11, "tuo_index": 9, "ma_index": 3}),
        ("庚", "寅", {"lu_index": 6, "yang_index": 7, "tuo_index": 5, "ma_index": 6}),
        ("辛", "巳", {"lu_index": 7, "yang_index": 8, "tuo_index": 6, "ma_index": 9}),
        ("壬", "午", {"lu_index": 9, "yang_index": 10, "tuo_index": 8, "ma_index": 6}),
        ("癸", "未", {"lu_index": 10, "yang_index": 11, "tuo_index": 9, "ma_index": 3}),
        ("甲", "申", {"lu_index": 0, "yang_index": 1, "tuo_index": 11, "ma_index": 0}),
        ("丁", "亥", {"lu_index": 4, "ma_index": 3, "tuo_index": 3, "yang_index": 5}),
        ("乙", "酉", {"lu_index": 1, "ma_index": 9, "tuo_index": 0, "yang_index": 2}),
        ("戊", "戌", {"lu_index": 3, "ma_index": 6, "tuo_index": 2, "yang_index": 4}),
        ("己", "未", {"lu_index": 4, "ma_index": 3, "tuo_index": 3, "yang_index": 5}),
        ("丙", "午", {"lu_index": 3, "ma_index": 6, "tuo_index": 2, "yang_index": 4}),
        # vi-VN input should also work via kot()
        ("Quý", "Mão", {"lu_index": 10, "yang_index": 11, "tuo_index": 9, "ma_index": 3}),
        ("Canh", "Dần", {"lu_index": 6, "yang_index": 7, "tuo_index": 5, "ma_index": 6}),
        ("Tân", "Tỵ", {"lu_index": 7, "yang_index": 8, "tuo_index": 6, "ma_index": 9}),
        ("Nhâm", "Ngọ", {"lu_index": 9, "yang_index": 10, "tuo_index": 8, "ma_index": 6}),
        ("Quý", "Mùi", {"lu_index": 10, "yang_index": 11, "tuo_index": 9, "ma_index": 3}),
        ("Giáp", "Thân", {"lu_index": 0, "yang_index": 1, "tuo_index": 11, "ma_index": 0}),
        ("Đinh", "Hợi", {"lu_index": 4, "ma_index": 3, "tuo_index": 3, "yang_index": 5}),
        ("Ất", "Dậu", {"lu_index": 1, "ma_index": 9, "tuo_index": 0, "yang_index": 2}),
        ("Mậu", "Tuất", {"lu_index": 3, "ma_index": 6, "tuo_index": 2, "yang_index": 4}),
        ("Kỷ", "Mùi", {"lu_index": 4, "ma_index": 3, "tuo_index": 3, "yang_index": 5}),
        ("Bính", "Ngọ", {"lu_index": 3, "ma_index": 6, "tuo_index": 2, "yang_index": 4}),
    ],
)
def test_get_lu_yang_tuo_ma_index(heavenly_stem: str, earthly_branch: str, expected: dict):
    assert get_lu_yang_tuo_ma_index(heavenly_stem, earthly_branch) == expected


@pytest.mark.parametrize(
    ("heavenly_stem", "expected"),
    [
        ("壬", {"kui_index": 1, "yue_index": 3}),
        ("癸", {"kui_index": 1, "yue_index": 3}),
        ("甲", {"kui_index": 11, "yue_index": 5}),
        ("戊", {"kui_index": 11, "yue_index": 5}),
        ("庚", {"kui_index": 11, "yue_index": 5}),
        ("乙", {"kui_index": 10, "yue_index": 6}),
        ("己", {"kui_index": 10, "yue_index": 6}),
        ("辛", {"kui_index": 4, "yue_index": 0}),
        ("丙", {"kui_index": 9, "yue_index": 7}),
        ("丁", {"kui_index": 9, "yue_index": 7}),
    ],
)
def test_get_kui_yue_index(heavenly_stem: str, expected: dict):
    assert get_kui_yue_index(heavenly_stem) == expected


@pytest.mark.parametrize(
    ("lunar_month", "expected"),
    [
        (1, {"zuo_index": 2, "you_index": 8}),
        (2, {"zuo_index": 3, "you_index": 7}),
        (3, {"zuo_index": 4, "you_index": 6}),
        (4, {"zuo_index": 5, "you_index": 5}),
        (5, {"zuo_index": 6, "you_index": 4}),
        (6, {"zuo_index": 7, "you_index": 3}),
        (7, {"zuo_index": 8, "you_index": 2}),
        (8, {"zuo_index": 9, "you_index": 1}),
        (9, {"zuo_index": 10, "you_index": 0}),
        (10, {"zuo_index": 11, "you_index": 11}),
        (11, {"zuo_index": 0, "you_index": 10}),
        (12, {"zuo_index": 1, "you_index": 9}),
    ],
)
def test_get_zuo_you_index(lunar_month: int, expected: dict):
    assert get_zuo_you_index(lunar_month) == expected


@pytest.mark.parametrize(
    ("time_index", "expected"),
    [
        (0, {"chang_index": 8, "qu_index": 2}),
        (1, {"chang_index": 7, "qu_index": 3}),
        (2, {"chang_index": 6, "qu_index": 4}),
        (3, {"chang_index": 5, "qu_index": 5}),
        (4, {"chang_index": 4, "qu_index": 6}),
        (5, {"chang_index": 3, "qu_index": 7}),
        (6, {"chang_index": 2, "qu_index": 8}),
        (7, {"chang_index": 1, "qu_index": 9}),
        (8, {"chang_index": 0, "qu_index": 10}),
        (9, {"chang_index": 11, "qu_index": 11}),
        (10, {"chang_index": 10, "qu_index": 0}),
        (11, {"chang_index": 9, "qu_index": 1}),
    ],
)
def test_get_chang_qu_index(time_index: int, expected: dict):
    assert get_chang_qu_index(time_index) == expected


@pytest.mark.parametrize(
    ("time_index", "expected"),
    [
        (0, {"kong_index": 9, "jie_index": 9}),
        (1, {"kong_index": 8, "jie_index": 10}),
        (2, {"kong_index": 7, "jie_index": 11}),
        (3, {"kong_index": 6, "jie_index": 0}),
        (4, {"kong_index": 5, "jie_index": 1}),
        (5, {"kong_index": 4, "jie_index": 2}),
        (6, {"kong_index": 3, "jie_index": 3}),
        (7, {"kong_index": 2, "jie_index": 4}),
        (8, {"kong_index": 1, "jie_index": 5}),
        (9, {"kong_index": 0, "jie_index": 6}),
        (10, {"kong_index": 11, "jie_index": 7}),
        (11, {"kong_index": 10, "jie_index": 8}),
    ],
)
def test_get_kong_jie_index(time_index: int, expected: dict):
    assert get_kong_jie_index(time_index) == expected


def test_get_huo_ling_index():
    expected_by_time = [
        {"huo_index": 11, "ling_index": 1},
        {"huo_index": 0, "ling_index": 2},
        {"huo_index": 1, "ling_index": 3},
        {"huo_index": 2, "ling_index": 4},
        {"huo_index": 3, "ling_index": 5},
        {"huo_index": 4, "ling_index": 6},
        {"huo_index": 5, "ling_index": 7},
        {"huo_index": 6, "ling_index": 8},
        {"huo_index": 7, "ling_index": 9},
        {"huo_index": 8, "ling_index": 10},
        {"huo_index": 9, "ling_index": 11},
        {"huo_index": 10, "ling_index": 0},
    ]
    for idx, expected in enumerate(expected_by_time):
        assert get_huo_ling_index("午", idx) == expected

    expected_by_year_branch = [
        ("寅", {"huo_index": 11, "ling_index": 1}),
        ("申", {"huo_index": 0, "ling_index": 8}),
        ("子", {"huo_index": 0, "ling_index": 8}),
        ("巳", {"huo_index": 1, "ling_index": 8}),
        ("酉", {"huo_index": 1, "ling_index": 8}),
        ("丑", {"huo_index": 1, "ling_index": 8}),
        ("亥", {"huo_index": 7, "ling_index": 8}),
        ("未", {"huo_index": 7, "ling_index": 8}),
    ]
    for branch, expected in expected_by_year_branch:
        assert get_huo_ling_index(branch, 0) == expected


@pytest.mark.parametrize(
    ("earthly_branch", "expected"),
    [
        ("卯", {"hongluan_index": 10, "tianxi_index": 4}),
        ("辰", {"hongluan_index": 9, "tianxi_index": 3}),
        ("巳", {"hongluan_index": 8, "tianxi_index": 2}),
        ("午", {"hongluan_index": 7, "tianxi_index": 1}),
        ("未", {"hongluan_index": 6, "tianxi_index": 0}),
        ("申", {"hongluan_index": 5, "tianxi_index": 11}),
        ("酉", {"hongluan_index": 4, "tianxi_index": 10}),
        ("戌", {"hongluan_index": 3, "tianxi_index": 9}),
        ("亥", {"hongluan_index": 2, "tianxi_index": 8}),
        ("子", {"hongluan_index": 1, "tianxi_index": 7}),
        ("丑", {"hongluan_index": 0, "tianxi_index": 6}),
        ("寅", {"hongluan_index": 11, "tianxi_index": 5}),
    ],
)
def test_get_luan_xi_index(earthly_branch: str, expected: dict):
    assert get_luan_xi_index(earthly_branch) == expected


def test_get_nianjie_index():
    cases = {"子": 8, "丑": 7, "寅": 6, "卯": 5, "辰": 4, "巳": 3, "午": 2, "未": 1, "申": 0, "酉": 11, "戌": 10, "亥": 9}
    for k, v in cases.items():
        assert get_nianjie_index(k) == v


def test_get_yearly_star_index():
    assert get_yearly_star_index(
        {"solar_date": "2023-03-06", "time_index": 2, "fix_leap": True, "gender": "女"}
    ) == {
        "xianchi_index": 10,
        "huagai_index": 5,
        "guchen_index": 3,
        "guasu_index": 11,
        "tiancai_index": 2,
        "tianshou_index": 6,
        "tianchu_index": 9,
        "posui_index": 3,
        "feilian_index": 3,
        "longchi_index": 5,
        "fengge_index": 5,
        "tianku_index": 1,
        "tianxu_index": 7,
        "tianguan_index": 4,
        "tianfu_index": 3,
        "jielu_index": 10,
        "kongwang_index": 11,
        "xunkong_index": 3,
        "tiankong_index": 2,
        "tiande_index": 10,
        "yuede_index": 6,
        "tianshang_index": 4,
        "tianshi_index": 6,
        "dahao_adj_index": 6,
        "jiekong_index": 11,
        "jiesha_adj_index": 6,
        "nianjie_index": 5,
    }

    assert get_yearly_star_index(
        {"solar_date": "2001-08-16", "time_index": 2, "fix_leap": True, "gender": "女"}
    ) == {
        "xianchi_index": 4,
        "huagai_index": 11,
        "guchen_index": 6,
        "guasu_index": 2,
        "tiancai_index": 8,
        "tianshou_index": 0,
        "tianchu_index": 4,
        "posui_index": 7,
        "feilian_index": 5,
        "longchi_index": 7,
        "fengge_index": 3,
        "tianku_index": 11,
        "tianxu_index": 9,
        "tianguan_index": 7,
        "tianfu_index": 3,
        "jielu_index": 2,
        "kongwang_index": 3,
        "xunkong_index": 7,
        "tiankong_index": 4,
        "tiande_index": 0,
        "yuede_index": 8,
        "tianshang_index": 8,
        "tianshi_index": 10,
        "dahao_adj_index": 8,
        "jiekong_index": 3,
        "jiesha_adj_index": 0,
        "nianjie_index": 3,
    }


def test_get_monthly_star_index():
    assert get_monthly_star_index("2021-08-09", 2, True) == {
        "yuejie_index": 0,
        "tianyao_index": 5,
        "tianxing_index": 1,
        "yinsha_index": 0,
        "tianyue_index": 9,
        "tianwu_index": 0,
    }
    assert get_monthly_star_index("2023-08-15", 0, True) == {
        "yuejie_index": 10,
        "tianyao_index": 4,
        "tianxing_index": 0,
        "yinsha_index": 2,
        "tianyue_index": 1,
        "tianwu_index": 6,
    }


def test_get_daily_star_index():
    assert get_daily_star_index("2020-08-05", 1) == {
        "santai_index": 10,
        "bazuo_index": 0,
        "enguang_index": 9,
        "tiangui_index": 5,
    }


def test_get_timely_star_index():
    expected = [
        {"taifu_index": 4, "fenggao_index": 0},
        {"taifu_index": 5, "fenggao_index": 1},
        {"taifu_index": 6, "fenggao_index": 2},
        {"taifu_index": 7, "fenggao_index": 3},
        {"taifu_index": 8, "fenggao_index": 4},
        {"taifu_index": 9, "fenggao_index": 5},
        {"taifu_index": 10, "fenggao_index": 6},
        {"taifu_index": 11, "fenggao_index": 7},
        {"taifu_index": 0, "fenggao_index": 8},
        {"taifu_index": 1, "fenggao_index": 9},
        {"taifu_index": 2, "fenggao_index": 10},
        {"taifu_index": 3, "fenggao_index": 11},
    ]
    for idx, item in enumerate(expected):
        assert get_timely_star_index(idx) == item


def test_get_chang_qu_index_by_heavenly_stem():
    cases = [
        ("甲", {"chang_index": 3, "qu_index": 7}),
        ("乙", {"chang_index": 4, "qu_index": 6}),
        ("丙", {"chang_index": 6, "qu_index": 4}),
        ("戊", {"chang_index": 6, "qu_index": 4}),
        ("丁", {"chang_index": 7, "qu_index": 3}),
        ("己", {"chang_index": 7, "qu_index": 3}),
        ("辛", {"chang_index": 10, "qu_index": 0}),
        ("壬", {"chang_index": 0, "qu_index": 10}),
    ]
    for stem, expected in cases:
        assert get_chang_qu_index_by_heavenly_stem(stem) == expected


def test_get_huagai_xianchi_index():
    cases = {
        "yin": {"huagai_index": 8, "xianchi_index": 1},
        "woo": {"huagai_index": 8, "xianchi_index": 1},
        "xu": {"huagai_index": 8, "xianchi_index": 1},
        "shen": {"huagai_index": 2, "xianchi_index": 7},
        "zi": {"huagai_index": 2, "xianchi_index": 7},
        "chen": {"huagai_index": 2, "xianchi_index": 7},
        "si": {"huagai_index": 11, "xianchi_index": 4},
        "you": {"huagai_index": 11, "xianchi_index": 4},
        "chou": {"huagai_index": 11, "xianchi_index": 4},
        "hai": {"huagai_index": 5, "xianchi_index": 10},
        "wei": {"huagai_index": 5, "xianchi_index": 10},
        "mao": {"huagai_index": 5, "xianchi_index": 10},
    }
    for k, v in cases.items():
        assert get_huagai_xianchi_index(k) == v


def test_get_gu_gua_index():
    cases = {
        "yin": {"guchen_index": 3, "guasu_index": 11},
        "mao": {"guchen_index": 3, "guasu_index": 11},
        "chen": {"guchen_index": 3, "guasu_index": 11},
        "si": {"guchen_index": 6, "guasu_index": 2},
        "woo": {"guchen_index": 6, "guasu_index": 2},
        "wei": {"guchen_index": 6, "guasu_index": 2},
        "shen": {"guchen_index": 9, "guasu_index": 5},
        "you": {"guchen_index": 9, "guasu_index": 5},
        "xu": {"guchen_index": 9, "guasu_index": 5},
        "hai": {"guchen_index": 0, "guasu_index": 8},
        "zi": {"guchen_index": 0, "guasu_index": 8},
        "chou": {"guchen_index": 0, "guasu_index": 8},
    }
    for k, v in cases.items():
        assert get_gu_gua_index(k) == v
