from __future__ import annotations

import pytest

from izthon.lunar_lite import (
    get_heavenly_stem_and_earthly_branch_by_lunar_date,
    get_heavenly_stem_and_earthly_branch_by_solar_date,
)


@pytest.mark.parametrize(
    ("date_str", "time_index", "is_leap", "year_divide", "expected"),
    [
        ("2023-6-13", 1, False, "exact", "癸卯 己未 己丑 乙丑"),
        ("2023-6-13", 12, False, "exact", "癸卯 己未 庚寅 丙子"),
        ("2023-2-11", 1, True, "exact", "癸卯 乙卯 己丑 乙丑"),
        ("2023-2-11", 1, False, "exact", "癸卯 甲寅 己未 乙丑"),
        ("2023-1-1", 1, False, "exact", "壬寅 癸丑 庚辰 丁丑"),
        ("2023-1-1", 1, False, "normal", "癸卯 癸丑 庚辰 丁丑"),
        ("2022-12-30", 1, False, "exact", "壬寅 癸丑 己卯 乙丑"),
        ("2023-1-29", 12, False, "exact", "癸卯 甲寅 己酉 甲子"),
    ],
)
def test_get_heavenly_stem_and_earthly_branch_by_lunar_date(
    date_str: str,
    time_index: int,
    is_leap: bool,
    year_divide: str,
    expected: str,
):
    res = get_heavenly_stem_and_earthly_branch_by_lunar_date(date_str, time_index, is_leap, {"year": year_divide})
    assert str(res) == expected


@pytest.mark.parametrize(
    ("date_str", "time_index", "options", "expected"),
    [
        ("2023-1-21", 1, None, "壬寅 癸丑 己卯 乙丑"),
        ("2023-1-21", 12, None, "壬寅 癸丑 庚辰 丙子"),
        ("2023-03-09", 5, None, "癸卯 乙卯 丙寅 癸巳"),
        ("2023-4-8", 5, None, "癸卯 丙辰 丙申 癸巳"),
        ("2023-1-22", 5, None, "壬寅 癸丑 庚辰 辛巳"),
        ("2023-2-19", 12, None, "癸卯 甲寅 己酉 甲子"),
        ("1987-12-6", 11, None, "丁卯 辛亥 己丑 乙亥"),
        ("1987-12-6", 12, None, "丁卯 辛亥 庚寅 丙子"),
        ("1983-4-22", 0, None, "癸亥 丙辰 庚辰 丙子"),
        ("1979-8-7", 0, None, "己未 辛未 丙午 戊子"),
        ("1979-8-8", 0, {"month": "exact"}, "己未 辛未 丁未 庚子"),
        ("1979-8-8", 0, {"month": "normal"}, "己未 壬申 丁未 庚子"),
        ("2025-7-7", 0, {"month": "normal"}, "乙巳 癸未 丁丑 庚子"),
        ("2025-12-20", 0, {"month": "normal"}, "乙巳 戊子 癸亥 壬子"),
        (
            "2026-2-5",
            0,
            {"year": "exact", "month": "exact"},
            "丙午 庚寅 庚戌 丙子",
        ),
        (
            "2026-2-5",
            0,
            {"year": "normal", "month": "exact"},
            "乙巳 庚寅 庚戌 丙子",
        ),
        (
            "2026-2-5",
            0,
            {"year": "normal", "month": "normal"},
            "乙巳 己丑 庚戌 丙子",
        ),
    ],
)
def test_get_heavenly_stem_and_earthly_branch_by_solar_date(
    date_str: str,
    time_index: int,
    options: dict | None,
    expected: str,
):
    res = get_heavenly_stem_and_earthly_branch_by_solar_date(date_str, time_index, options)
    assert str(res) == expected
