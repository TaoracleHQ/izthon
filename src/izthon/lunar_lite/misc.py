from __future__ import annotations

from .constants import EARTHLY_BRANCHES, ZODIAC
from .convertor import normalize_date_str, solar_to_lunar
from .types import LunarDate


def get_sign(solar_date_str: str) -> str:
    # Ranges are inclusive on start, inclusive on end as per the TS tests.
    y, m, d, *_ = normalize_date_str(solar_date_str) + [0, 0, 0]

    # (start_month, start_day, name)
    # The start dates match the TS test cases.
    if (m == 3 and d >= 21) or (m == 4 and d <= 20):
        return "白羊座"
    if (m == 4 and d >= 21) or (m == 5 and d <= 21):
        return "金牛座"
    if (m == 5 and d >= 22) or (m == 6 and d <= 21):
        return "双子座"
    if (m == 6 and d >= 22) or (m == 7 and d <= 22):
        return "巨蟹座"
    if (m == 7 and d >= 23) or (m == 8 and d <= 22):
        return "狮子座"
    if (m == 8 and d >= 23) or (m == 9 and d <= 22):
        return "处女座"
    if (m == 9 and d >= 23) or (m == 10 and d <= 23):
        return "天秤座"
    if (m == 10 and d >= 24) or (m == 11 and d <= 22):
        return "天蝎座"
    if (m == 11 and d >= 23) or (m == 12 and d <= 21):
        return "射手座"
    if (m == 12 and d >= 22) or (m == 1 and d <= 19):
        return "摩羯座"
    if (m == 1 and d >= 20) or (m == 2 and d <= 18):
        return "水瓶座"
    # Pisces: Feb 19 - Mar 20
    return "双鱼座"


def get_zodiac(earthly_branch_of_year: str) -> str:
    return ZODIAC[EARTHLY_BRANCHES.index(earthly_branch_of_year)]


def get_total_days_of_lunar_month(solar_date_str: str) -> int:
    lunar: LunarDate = solar_to_lunar(solar_date_str)
    from .convertor import _leap_month, _leap_days, _month_days

    lm = _leap_month(lunar.lunar_year)
    if lunar.is_leap and lm == lunar.lunar_month:
        return _leap_days(lunar.lunar_year)
    return _month_days(lunar.lunar_year, lunar.lunar_month)

