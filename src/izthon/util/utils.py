from __future__ import annotations

from typing import Iterable

from ..astro._config import get_config
from ..data import EARTHLY_BRANCHES, HEAVENLY_STEMS, MUTAGEN, STARS_INFO, heavenly_stems
from ..i18n import kot, t
from ..lunar_lite import solar_to_lunar


def fix_index(index: int, max_value: int = 12) -> int:
    if index < 0:
        return fix_index(index + max_value, max_value)
    if index > max_value - 1:
        return fix_index(index - max_value, max_value)
    return index


def earthly_branch_index_to_palace_index(earthly_branch_name: str) -> int:
    earthly_branch = kot(earthly_branch_name, "Earthly")
    yin = kot("yinEarthly", "Earthly")
    return fix_index(EARTHLY_BRANCHES.index(earthly_branch) - EARTHLY_BRANCHES.index(yin))


def get_brightness(star_name: str, index: int) -> str:
    star_key = kot(star_name)
    cfg = get_config()
    custom = cfg["brightness"].get(star_key)
    target = custom if custom is not None else STARS_INFO.get(star_key, {}).get("brightness")
    if not target:
        return ""
    return t(target[fix_index(index)])


def _get_target_mutagens(heavenly_stem_key: str) -> list[str]:
    cfg = get_config()
    custom = cfg["mutagens"].get(heavenly_stem_key)
    if custom is not None:
        return list(custom)
    return list(heavenly_stems[heavenly_stem_key].get("mutagen") or [])


def get_mutagen(star_name: str, heavenly_stem_name: str) -> str:
    heavenly_stem_key = kot(heavenly_stem_name, "Heavenly")
    star_key = kot(star_name)
    target = _get_target_mutagens(heavenly_stem_key)
    idx = target.index(star_key) if star_key in target else -1
    if idx < 0:
        return ""
    return t(MUTAGEN[idx])


def get_mutagens_by_heavenly_stem(heavenly_stem_name: str) -> list[str]:
    heavenly_stem_key = kot(heavenly_stem_name, "Heavenly")
    target = _get_target_mutagens(heavenly_stem_key)
    return [t(star) for star in target]


def fix_earthly_branch_index(earthly_branch_name: str) -> int:
    earthly_branch = kot(earthly_branch_name, "Earthly")
    return fix_index(EARTHLY_BRANCHES.index(earthly_branch) - EARTHLY_BRANCHES.index("yinEarthly"))


def fix_lunar_month_index(solar_date_str: str, time_index: int, fix_leap: bool | None = None) -> int:
    lunar = solar_to_lunar(solar_date_str)
    first_index = EARTHLY_BRANCHES.index("yinEarthly")
    need_to_add = bool(lunar.is_leap and fix_leap and lunar.lunar_day > 15 and time_index != 12)
    return fix_index(lunar.lunar_month + 1 - first_index + (1 if need_to_add else 0))


def fix_lunar_day_index(lunar_day: int, time_index: int) -> int:
    return lunar_day if time_index >= 12 else lunar_day - 1


def merge_stars(*stars: Iterable[list[list]]):
    # Avoid importing star.init_stars here to prevent cycles; create a 12-slot list.
    final: list[list] = [[] for _ in range(12)]
    for item in stars:
        for idx, sub in enumerate(item):
            final[idx].extend(sub)
    return final


def time_to_index(hour: int) -> int:
    if hour == 0:
        return 0
    if hour == 23:
        return 12
    return (hour + 1) // 2


def get_age_index(earthly_branch_name: str) -> int:
    earthly_branch = kot(earthly_branch_name, "Earthly")
    if earthly_branch in {"yinEarthly", "wuEarthly", "xuEarthly"}:
        return fix_earthly_branch_index("chen")
    if earthly_branch in {"shenEarthly", "ziEarthly", "chenEarthly"}:
        return fix_earthly_branch_index("xu")
    if earthly_branch in {"siEarthly", "youEarthly", "chouEarthly"}:
        return fix_earthly_branch_index("wei")
    if earthly_branch in {"haiEarthly", "maoEarthly", "weiEarthly"}:
        return fix_index(fix_earthly_branch_index("chou"))
    return -1


def translate_chinese_date(chinese_date) -> str:
    yearly, monthly, daily, hourly = (
        chinese_date.yearly,
        chinese_date.monthly,
        chinese_date.daily,
        chinese_date.hourly,
    )

    def _len_gt_1(pair):
        return len(t(kot(pair[0]))) > 1 or len(t(kot(pair[1]))) > 1

    if any(_len_gt_1(p) for p in (yearly, monthly, daily, hourly)):
        return (
            f"{t(kot(yearly[0]))} {t(kot(yearly[1]))} - "
            f"{t(kot(monthly[0]))} {t(kot(monthly[1]))} - "
            f"{t(kot(daily[0]))} {t(kot(daily[1]))} - "
            f"{t(kot(hourly[0]))} {t(kot(hourly[1]))}"
        )

    return (
        f"{t(kot(yearly[0]))}{t(kot(yearly[1]))} "
        f"{t(kot(monthly[0]))}{t(kot(monthly[1]))} "
        f"{t(kot(daily[0]))}{t(kot(daily[1]))} "
        f"{t(kot(hourly[0]))}{t(kot(hourly[1]))}"
    )
