from __future__ import annotations

from dataclasses import dataclass
from datetime import date as Date, datetime, timedelta
from typing import Sequence

from .constants import LUNAR_INFO
from .types import LunarDate, SolarDate


def normalize_date_str(value: str | datetime | Date) -> list[int]:
    """Split a date string or datetime into numeric components.

    Mirrors the TS implementation:
    - When a datetime/date is provided: return [Y, M, D, H, m, s] (missing parts set to 0).
    - When a string is provided: split by whitespace, then split parts by [-:/.], flatten, abs(int()).
    """
    if isinstance(value, datetime):
        return [
            value.year,
            value.month,
            value.day,
            value.hour,
            value.minute,
            value.second,
        ]
    if isinstance(value, Date):
        return [value.year, value.month, value.day, 0, 0, 0]

    parts: list[str] = []
    for chunk in value.split():
        for p in __import__("re").split(r"[-:/.]", chunk):
            if p != "":
                parts.append(p)
    return [abs(int(float(p))) for p in parts]


_BASE_SOLAR = Date(1900, 1, 31)  # 1900-01-31 is lunar 1900-01-01


def _check_solar_range(y: int) -> None:
    if y < 1900 or y > 2100:
        raise ValueError("year should be between 1900 and 2100.")


def _check_solar_date_after_base(d: Date) -> None:
    if d < _BASE_SOLAR:
        raise ValueError("date must be after 1900-1-31.")


def _leap_month(year: int) -> int:
    return LUNAR_INFO[year - 1900] & 0xF


def _leap_days(year: int) -> int:
    lm = _leap_month(year)
    if lm == 0:
        return 0
    return 30 if (LUNAR_INFO[year - 1900] & 0x10000) else 29


def _month_days(year: int, month: int) -> int:
    if month < 1 or month > 12:
        raise ValueError("invalid date.")
    return 30 if (LUNAR_INFO[year - 1900] & (0x10000 >> month)) else 29


def _year_days(year: int) -> int:
    info = LUNAR_INFO[year - 1900]
    days = 348
    mask = 0x8000
    for _ in range(12):
        if info & mask:
            days += 1
        mask >>= 1
    return days + _leap_days(year)


def solar_to_lunar(date_value: str | datetime | Date) -> LunarDate:
    y, m, d, *_ = normalize_date_str(date_value) + [0, 0, 0]
    _check_solar_range(y)
    if m < 1 or m > 12:
        raise ValueError(f"wrong month {m}")

    solar = Date(y, m, d)
    _check_solar_date_after_base(solar)

    offset = (solar - _BASE_SOLAR).days

    lunar_year = 1900
    while lunar_year <= 2100:
        yd = _year_days(lunar_year)
        if offset < yd:
            break
        offset -= yd
        lunar_year += 1

    if lunar_year > 2100:
        raise ValueError("invalid date.")

    leap_month = _leap_month(lunar_year)

    # Build an explicit month sequence to avoid subtle leap-month state bugs.
    seq: list[tuple[int, bool]] = []
    for mo in range(1, 13):
        seq.append((mo, False))
        if leap_month and mo == leap_month:
            seq.append((mo, True))

    lunar_month = 1
    is_leap = False
    for mo, is_leap_flag in seq:
        md = _leap_days(lunar_year) if is_leap_flag else _month_days(lunar_year, mo)
        if offset < md:
            lunar_month = mo
            is_leap = is_leap_flag
            break
        offset -= md

    lunar_day = offset + 1
    return LunarDate(lunar_year=lunar_year, lunar_month=lunar_month, lunar_day=lunar_day, is_leap=is_leap)


def lunar_to_solar(date_str: str, is_leap_month: bool | None = None) -> SolarDate:
    y, m, d, *_ = normalize_date_str(date_str) + [0, 0, 0]
    if y < 1900 or y > 2100:
        raise ValueError("invalid date.")
    if m < 1 or m > 12 or d < 1 or d > 30:
        raise ValueError("invalid date.")

    leap_month = _leap_month(y)

    offset = 0
    for yr in range(1900, y):
        offset += _year_days(yr)

    target_is_leap = bool(is_leap_month) and (leap_month == m)

    # Month sequence for the target lunar year.
    seq: list[tuple[int, bool]] = []
    for mo in range(1, 13):
        seq.append((mo, False))
        if leap_month and mo == leap_month:
            seq.append((mo, True))

    found = False
    for mo, is_leap_flag in seq:
        md = _leap_days(y) if is_leap_flag else _month_days(y, mo)
        if mo == m and is_leap_flag == target_is_leap:
            if d > md:
                raise ValueError("invalid date.")
            offset += d - 1
            found = True
            break
        offset += md

    if not found:
        raise ValueError("invalid date.")

    solar = _BASE_SOLAR + timedelta(days=offset)
    return SolarDate(solar_year=solar.year, solar_month=solar.month, solar_day=solar.day)


_CN_NUM = {0: "〇", 1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七", 8: "八", 9: "九"}

_CN_MONTH = {
    1: "正月",
    2: "二月",
    3: "三月",
    4: "四月",
    5: "五月",
    6: "六月",
    7: "七月",
    8: "八月",
    9: "九月",
    10: "十月",
    11: "冬月",
    12: "腊月",
}

_CN_DAY_PREFIX = {1: "初", 2: "十", 3: "廿", 4: "三"}
_CN_DAY_NUM = {0: "十", 1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七", 8: "八", 9: "九"}


def _cn_year(y: int) -> str:
    return "".join(_CN_NUM[int(ch)] for ch in str(y))


def _cn_day(d: int) -> str:
    if d <= 10:
        return "初" + ("十" if d == 10 else _CN_DAY_NUM[d])
    if 11 <= d <= 19:
        return "十" + _CN_DAY_NUM[d - 10]
    if d == 20:
        return "二十"
    if 21 <= d <= 29:
        return "廿" + _CN_DAY_NUM[d - 20]
    if d == 30:
        return "三十"
    raise ValueError("invalid date.")


def lunar_date_to_cn_string(lunar: LunarDate) -> str:
    year = _cn_year(lunar.lunar_year)
    month = _CN_MONTH.get(lunar.lunar_month)
    if not month:
        raise ValueError("invalid date.")
    day = _cn_day(lunar.lunar_day)
    leap = "闰" if lunar.is_leap else ""
    return f"{year}年{leap}{month}{day}"
