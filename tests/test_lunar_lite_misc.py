from __future__ import annotations

import pytest

from izthon.lunar_lite import get_sign, get_total_days_of_lunar_month, get_zodiac
from izthon.lunar_lite.utils import fix_index


def test_fix_index():
    assert fix_index(-1, 12) == 11
    assert fix_index(0, 12) == 0
    assert fix_index(10, 12) == 10
    assert fix_index(13, 12) == 1


@pytest.mark.parametrize(
    ("date_str", "expected"),
    [
        ("2023-3-21", "白羊座"),
        ("2023-4-21", "金牛座"),
        ("2023-5-22", "双子座"),
        ("2023-6-22", "巨蟹座"),
        ("2023-7-23", "狮子座"),
        ("2023-8-23", "处女座"),
        ("2023-9-23", "天秤座"),
        ("2023-10-24", "天蝎座"),
        ("2023-11-23", "射手座"),
        ("2023-12-22", "摩羯座"),
        ("2023-1-20", "水瓶座"),
        ("2023-2-19", "双鱼座"),
    ],
)
def test_get_sign(date_str: str, expected: str):
    assert get_sign(date_str) == expected


@pytest.mark.parametrize(
    ("branch", "expected"),
    [
        ("子", "鼠"),
        ("丑", "牛"),
        ("寅", "虎"),
        ("卯", "兔"),
        ("辰", "龙"),
        ("巳", "蛇"),
        ("午", "马"),
        ("未", "羊"),
        ("申", "猴"),
        ("酉", "鸡"),
        ("戌", "狗"),
        ("亥", "猪"),
    ],
)
def test_get_zodiac(branch: str, expected: str):
    assert get_zodiac(branch) == expected


def test_get_total_days_of_lunar_month():
    assert get_total_days_of_lunar_month("2023-10-10") == 30
    assert get_total_days_of_lunar_month("2023-3-1") == 30
    assert get_total_days_of_lunar_month("2023-4-2") == 29

