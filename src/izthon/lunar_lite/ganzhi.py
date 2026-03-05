from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta, timezone

from .constants import (
    EARTHLY_BRANCHES,
    FIVE_TIGER,
    HEAVENLY_STEMS,
    MONTHLY_EARTHLY_BRANCHES,
    S_TERM_INFO_MINUTES,
)
from .convertor import lunar_to_solar, normalize_date_str, solar_to_lunar
from .types import HeavenlyStemAndEarthlyBranchDate, Options
from .utils import fix_index


_TZ_CN = timezone(timedelta(hours=8))


def _as_datetime(value: str | datetime) -> datetime:
    if isinstance(value, datetime):
        # Assume caller already uses local CN time (same as the TS lib's implicit behavior).
        return value.replace(tzinfo=value.tzinfo or _TZ_CN)
    parts = normalize_date_str(value)
    # Accept YYYY-M-D or YYYY-M-D HH:mm[:ss]
    y, m, d = parts[0], parts[1], parts[2]
    hh = parts[3] if len(parts) > 3 else 0
    mm = parts[4] if len(parts) > 4 else 0
    ss = parts[5] if len(parts) > 5 else 0
    return datetime(y, m, d, hh, mm, ss, tzinfo=_TZ_CN)


def _solar_term_dt_cn(year: int, term_index: int) -> datetime:
    # Widely used approximation with a CN-local epoch (same baseline used by lunar-lite/lunar-typescript).
    base_cn = datetime(1900, 1, 6, 2, 5, tzinfo=_TZ_CN)
    ms = (year - 1900) * 31556925974.7 + S_TERM_INFO_MINUTES[term_index] * 60000
    return base_cn + timedelta(milliseconds=ms)


def _year_ganzhi(year: int) -> tuple[str, str]:
    # 4 AD is a 甲子 year. This is the common proleptic rule.
    idx = (year - 4) % 60
    return HEAVENLY_STEMS[idx % 10], EARTHLY_BRANCHES[idx % 12]


def _year_by_lichun(dt: datetime) -> int:
    # LiChun is the 3rd solar term in the common list (index 2).
    # Match lunar-typescript's getYearGanByLiChun()/getYearZhiByLiChun(): compare date only.
    lichun = _solar_term_dt_cn(dt.year, 2)
    return dt.year if dt.date() >= lichun.date() else dt.year - 1


def _year_by_lichun_exact(dt: datetime) -> int:
    # Exact boundary used by month exact calculation in lunar-typescript.
    lichun = _solar_term_dt_cn(dt.year, 2)
    return dt.year if dt >= lichun else dt.year - 1


def _month_ganzhi_exact(dt: datetime) -> tuple[str, str]:
    # Month boundaries for the 12 "jie" terms:
    # XiaoHan(0)->丑, LiChun(2)->寅, JingZhe(4)->卯, QingMing(6)->辰, LiXia(8)->巳,
    # MangZhong(10)->午, XiaoShu(12)->未, LiQiu(14)->申, BaiLu(16)->酉, HanLu(18)->戌,
    # LiDong(20)->亥, DaXue(22)->子.
    term_to_month_index = {
        0: 11,
        2: 0,
        4: 1,
        6: 2,
        8: 3,
        10: 4,
        12: 5,
        14: 6,
        16: 7,
        18: 8,
        20: 9,
        22: 10,
    }

    candidates: list[tuple[datetime, int]] = []
    for y in (dt.year - 1, dt.year, dt.year + 1):
        for term_idx, month_idx in term_to_month_index.items():
            candidates.append((_solar_term_dt_cn(y, term_idx), month_idx))

    # Latest term <= dt.
    start = max((x for x in candidates if x[0] <= dt), key=lambda x: x[0])
    month_index = start[1]  # 0..11, aligned with MONTHLY_EARTHLY_BRANCHES

    # Month heavenly stem is derived from the LiChun-based year heavenly stem.
    year_for_month = _year_by_lichun_exact(dt)
    year_gan, _ = _year_ganzhi(year_for_month)
    start_gan = FIVE_TIGER[HEAVENLY_STEMS.index(year_gan)]
    gan = HEAVENLY_STEMS[fix_index(HEAVENLY_STEMS.index(start_gan) + month_index, 10)]
    zhi = MONTHLY_EARTHLY_BRANCHES[month_index]
    return gan, zhi


def _month_ganzhi_normal(year_gan: str, lunar_month: int, lunar_day: int, is_leap: bool) -> tuple[str, str]:
    # Matches lunar-lite's calculateMonthlyGanZhi(..., monthlyDivide="normal") implementation.
    fix_leap = 1 if (is_leap and lunar_day > 15) else 0
    month_index = (lunar_month - 1) + fix_leap
    if month_index < 0:
        month_index = 0
    if month_index > 11:
        month_index = month_index % 12

    start_gan = FIVE_TIGER[HEAVENLY_STEMS.index(year_gan)]
    gan = HEAVENLY_STEMS[fix_index(HEAVENLY_STEMS.index(start_gan) + month_index, 10)]
    zhi = MONTHLY_EARTHLY_BRANCHES[month_index]
    return gan, zhi


def _day_ganzhi(dt: datetime) -> tuple[str, str]:
    # Use 23:00 as the day boundary (late rat hour belongs to next day),
    # matching the TS test expectations for timeIndex=12.
    dt_for_day = dt
    if dt.hour >= 23:
        dt_for_day = dt + timedelta(days=1)

    y, m, d = dt_for_day.year, dt_for_day.month, dt_for_day.day
    # Fliegel-Van Flandern JDN for Gregorian calendar.
    a = (14 - m) // 12
    y2 = y + 4800 - a
    m2 = m + 12 * a - 3
    jdn = d + ((153 * m2 + 2) // 5) + 365 * y2 + y2 // 4 - y2 // 100 + y2 // 400 - 32045
    idx = (jdn + 49) % 60
    return HEAVENLY_STEMS[idx % 10], EARTHLY_BRANCHES[idx % 12]


def _hour_ganzhi(day_gan: str, time_index: int) -> tuple[str, str]:
    # Time branches per iztro/lunar-lite conventions (0..12, where 12 is late 子 hour).
    time_branches = ("子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子")
    zhi = time_branches[time_index]

    # Rat rule: starting heavenly stem for 子 hour depends on day heavenly stem.
    if day_gan in ("甲", "己"):
        start = "甲"
    elif day_gan in ("乙", "庚"):
        start = "丙"
    elif day_gan in ("丙", "辛"):
        start = "戊"
    elif day_gan in ("丁", "壬"):
        start = "庚"
    else:  # ("戊","癸")
        start = "壬"

    gan = HEAVENLY_STEMS[fix_index(HEAVENLY_STEMS.index(start) + EARTHLY_BRANCHES.index(zhi), 10)]
    return gan, zhi


def get_heavenly_stem_and_earthly_branch_by_solar_date(
    date_value: str | datetime,
    time_index: int,
    options: Options | dict | None = None,
) -> HeavenlyStemAndEarthlyBranchDate:
    dt = _as_datetime(date_value)

    opt = Options()
    if isinstance(options, dict):
        opt = Options(**{k: v for k, v in options.items() if v is not None})
    elif isinstance(options, Options):
        opt = options

    # Pick an internal timestamp consistent with the TS lib (timeIndex -> hour mapping).
    # In TS: Solar.fromYmdHms(..., hour=max(timeIndex*2-1,0), minute=30).
    hour = max(time_index * 2 - 1, 0)
    dt = dt.replace(hour=hour, minute=30, second=0)

    # Year: normal = lunar new year boundary; exact = LiChun boundary.
    if opt.year == "normal":
        lunar = solar_to_lunar(dt.date())
        year_gan, year_zhi = _year_ganzhi(lunar.lunar_year)
    else:
        year_gan, year_zhi = _year_ganzhi(_year_by_lichun(dt))

    yearly = (year_gan, year_zhi)

    # Month: exact = solar term month; normal = lunar month based.
    if opt.month == "exact":
        monthly = _month_ganzhi_exact(dt)
    else:
        lunar = solar_to_lunar(dt.date())
        monthly = _month_ganzhi_normal(yearly[0], lunar.lunar_month, lunar.lunar_day, lunar.is_leap)

    daily = _day_ganzhi(dt)
    hourly = _hour_ganzhi(daily[0], time_index)

    return HeavenlyStemAndEarthlyBranchDate(
        yearly=yearly,
        monthly=monthly,
        daily=daily,
        hourly=hourly,
    )


def get_heavenly_stem_and_earthly_branch_by_lunar_date(
    date_str: str,
    time_index: int,
    is_leap: bool | None = None,
    options: Options | dict | None = None,
) -> HeavenlyStemAndEarthlyBranchDate:
    solar = lunar_to_solar(date_str, is_leap)
    return get_heavenly_stem_and_earthly_branch_by_solar_date(
        solar.isoformat(),
        time_index,
        options if options is not None else {"year": "normal", "month": "exact"},
    )
