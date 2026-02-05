from __future__ import annotations

from dataclasses import dataclass

from ..data import (
    EARTHLY_BRANCHES,
    GENDER,
    HEAVENLY_STEMS,
    PALACES,
    TIGER_RULE,
    FiveElementsClass,
    earthly_branches,
)
from ..i18n import kot, t
from ..lunar_lite import get_heavenly_stem_and_earthly_branch_by_solar_date
from ..util import fix_earthly_branch_index, fix_index, fix_lunar_month_index, get_age_index
from ._config import get_config


@dataclass(frozen=True)
class SoulAndBody:
    soul_index: int
    body_index: int
    heavenly_stem_of_soul: str
    earthly_branch_of_soul: str


@dataclass(frozen=True)
class Decadal:
    range: tuple[int, int]
    heavenly_stem: str
    earthly_branch: str


def get_soul_and_body(
    *,
    solar_date: str,
    time_index: int,
    fix_leap: bool | None = None,
    from_: dict[str, str] | None = None,
) -> SoulAndBody:
    """Compute soul/body palace indices and the soul palace stem/branch (translated)."""
    cfg = get_config()
    chinese_date = get_heavenly_stem_and_earthly_branch_by_solar_date(
        solar_date,
        time_index,
        {"year": cfg["year_divide"], "month": cfg["horoscope_divide"]},
    )
    yearly, hourly = chinese_date.yearly, chinese_date.hourly

    earthly_branch_of_time = kot(hourly[1], "Earthly")
    heavenly_stem_of_year = kot(yearly[0], "Heavenly")

    # Zi Wei Dou Shu uses Yin palace as the first palace.
    first_index = EARTHLY_BRANCHES.index("yinEarthly")

    month_index = fix_lunar_month_index(solar_date, time_index, fix_leap)

    # Soul: move to birth lunar-month palace, then reverse to birth hour branch palace.
    soul_index = fix_index(month_index - EARTHLY_BRANCHES.index(earthly_branch_of_time))
    # Body: move to birth lunar-month palace, then forward to birth hour branch palace.
    body_index = fix_index(month_index + EARTHLY_BRANCHES.index(earthly_branch_of_time))

    if from_ and from_.get("heavenly_stem") and from_.get("earthly_branch"):
        # Zhongzhou "earth/human plate": treat the passed earthly branch as the soul palace.
        soul_index = fix_earthly_branch_index(from_["earthly_branch"])
        body_offset = [0, 2, 4, 6, 8, 10, 0, 2, 4, 6, 8, 10, 0]
        body_index = fix_index(body_offset[time_index] + soul_index)

    # Tiger rule gives the heavenly stem for the Yin palace from the year's heavenly stem.
    start_heavenly_stem_key = TIGER_RULE[heavenly_stem_of_year]

    heavenly_stem_of_soul_index = fix_index(
        HEAVENLY_STEMS.index(start_heavenly_stem_key) + soul_index,
        10,
    )
    heavenly_stem_of_soul = t(HEAVENLY_STEMS[heavenly_stem_of_soul_index])

    earthly_branch_of_soul = t(EARTHLY_BRANCHES[fix_index(soul_index + first_index)])

    return SoulAndBody(
        soul_index=soul_index,
        body_index=body_index,
        heavenly_stem_of_soul=heavenly_stem_of_soul,
        earthly_branch_of_soul=earthly_branch_of_soul,
    )


def get_five_elements_class(heavenly_stem_name: str, earthly_branch_name: str) -> str:
    """Determine five-elements class (纳音五行局) from the soul palace stem/branch."""
    five_elements_table = ("wood3rd", "metal4th", "water2nd", "fire6th", "earth5th")
    heavenly_stem = kot(heavenly_stem_name, "Heavenly")
    earthly_branch = kot(earthly_branch_name, "Earthly")

    heavenly_stem_number = (HEAVENLY_STEMS.index(heavenly_stem) // 2) + 1
    earthly_branch_number = (fix_index(EARTHLY_BRANCHES.index(earthly_branch), 6) // 2) + 1
    idx = heavenly_stem_number + earthly_branch_number

    while idx > 5:
        idx -= 5

    return t(five_elements_table[idx - 1])


def get_palace_names(from_index: int) -> list[str]:
    """Get the 12 palace names (translated), ordered from Yin palace."""
    names: list[str] = []
    for i in range(len(PALACES)):
        idx = fix_index(i - from_index)
        names.append(t(PALACES[idx]))
    return names


def get_horoscope(
    *,
    solar_date: str,
    time_index: int,
    gender: str,
    fix_leap: bool | None = None,
    from_: dict[str, str] | None = None,
) -> tuple[list[Decadal], list[list[int]]]:
    """Compute decadals (10-year luck) and small-limit ages per palace."""
    cfg = get_config()
    gender_key = kot(gender)

    chinese_date = get_heavenly_stem_and_earthly_branch_by_solar_date(
        solar_date,
        time_index,
        {"year": cfg["year_divide"]},
    )
    yearly = chinese_date.yearly
    heavenly_stem_key = kot(yearly[0], "Heavenly")
    earthly_branch_key = kot(yearly[1], "Earthly")

    soul_and_body = get_soul_and_body(solar_date=solar_date, time_index=time_index, fix_leap=fix_leap, from_=from_)
    five_elements_class_key = kot(
        get_five_elements_class(
            from_["heavenly_stem"] if from_ and from_.get("heavenly_stem") else soul_and_body.heavenly_stem_of_soul,
            from_["earthly_branch"] if from_ and from_.get("earthly_branch") else soul_and_body.earthly_branch_of_soul,
        )
    )

    start_heavenly_stem_key = TIGER_RULE[heavenly_stem_key]
    decadals: list[Decadal] = [Decadal((0, 0), "", "") for _ in range(12)]

    for i in range(12):
        same_yinyang = GENDER[gender_key] == earthly_branches[earthly_branch_key]["yin_yang"]
        idx = fix_index(soul_and_body.soul_index + i) if same_yinyang else fix_index(soul_and_body.soul_index - i)

        start_age = int(FiveElementsClass[five_elements_class_key]) + 10 * i
        heavenly_stem_index = fix_index(HEAVENLY_STEMS.index(start_heavenly_stem_key) + idx, 10)
        earthly_branch_index = fix_index(EARTHLY_BRANCHES.index("yinEarthly") + idx)

        decadals[idx] = Decadal(
            range=(start_age, start_age + 9),
            heavenly_stem=t(HEAVENLY_STEMS[heavenly_stem_index]),
            earthly_branch=t(EARTHLY_BRANCHES[earthly_branch_index]),
        )

    age_start_idx = get_age_index(yearly[1])
    ages: list[list[int]] = [[] for _ in range(12)]
    for i in range(12):
        seq = [12 * j + i + 1 for j in range(10)]
        idx = fix_index(age_start_idx + i) if kot(gender) == "male" else fix_index(age_start_idx - i)
        ages[idx] = seq

    return decadals, ages

