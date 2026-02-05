from __future__ import annotations

from dataclasses import dataclass
from datetime import date as Date, datetime
from typing import Any

from ..data import EARTHLY_BRANCHES
from ..i18n import kot, t
from ..lunar_lite import get_heavenly_stem_and_earthly_branch_by_solar_date, normalize_date_str, solar_to_lunar
from ..star import get_horoscope_star, get_yearly_12
from ..util import fix_earthly_branch_index, fix_index, get_mutagens_by_heavenly_stem, time_to_index
from . import analyzer
from ._config import get_config, get_plugins
from .functional_horoscope import (
    AgeHoroscopeItem,
    FunctionalHoroscope,
    Horoscope,
    HoroscopeItem,
    YearlyDecStar,
    YearlyHoroscopeItem,
)
from .palace import get_palace_names


def _as_datetime(value: str | datetime | Date) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, Date):
        return datetime(value.year, value.month, value.day)
    parts = normalize_date_str(value) + [0, 0, 0]
    y, m, d, hh, mm, ss = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]
    return datetime(y, m, d, hh, mm, ss)


def _get_horoscope_by_solar_date(
    astrolabe: "FunctionalAstrolabe",
    target_date: str | datetime | Date | None = None,
    time_index: int | None = None,
) -> FunctionalHoroscope:
    target_date = target_date or datetime.now()

    birthday_lunar = solar_to_lunar(astrolabe.solar_date)
    date_lunar = solar_to_lunar(target_date)

    convert_time_index = time_to_index(_as_datetime(target_date).hour)
    ti = time_index if time_index is not None else convert_time_index

    cfg = get_config()
    chinese_date = get_heavenly_stem_and_earthly_branch_by_solar_date(
        target_date,
        ti,
        {"year": cfg["horoscope_divide"], "month": cfg["horoscope_divide"]},
    )
    yearly, monthly, daily, hourly = (
        chinese_date.yearly,
        chinese_date.monthly,
        chinese_date.daily,
        chinese_date.hourly,
    )

    # 虚岁（nominal age）
    nominal_age = date_lunar.lunar_year - birthday_lunar.lunar_year
    is_childhood = False

    if cfg["age_divide"] == "birthday":
        if (
            (
                date_lunar.lunar_year == birthday_lunar.lunar_year
                and date_lunar.lunar_month == birthday_lunar.lunar_month
                and date_lunar.lunar_day > birthday_lunar.lunar_day
            )
            or date_lunar.lunar_month > birthday_lunar.lunar_month
        ):
            nominal_age += 1
    else:
        nominal_age += 1

    decadal_index = -1
    heavenly_stem_of_decade = "甲"
    earthly_branch_of_decade = "子"

    for idx, p in enumerate(astrolabe.palaces):
        if not p.decadal:
            continue
        if p.decadal.range[0] <= nominal_age <= p.decadal.range[1]:
            decadal_index = idx
            heavenly_stem_of_decade = p.decadal.heavenly_stem
            earthly_branch_of_decade = p.decadal.earthly_branch
            break

    if decadal_index < 0:
        # If not started, use childhood limit.
        childhood_seq = ["命宫", "财帛", "疾厄", "夫妻", "福德", "官禄"]
        if 1 <= nominal_age <= len(childhood_seq):
            target_name = childhood_seq[nominal_age - 1]
            target_palace = astrolabe.palace(target_name)
            if target_palace:
                is_childhood = True
                decadal_index = target_palace.index
                heavenly_stem_of_decade = target_palace.heavenly_stem
                earthly_branch_of_decade = target_palace.earthly_branch

    age_index = -1
    heavenly_stem_of_age = "甲"
    earthly_branch_of_age = "子"
    for idx, p in enumerate(astrolabe.palaces):
        if nominal_age in (p.ages or []):
            age_index = idx
            heavenly_stem_of_age = p.heavenly_stem
            earthly_branch_of_age = p.earthly_branch
            break

    yearly_index = fix_earthly_branch_index(yearly[1])

    # Flow-month index: reverse from yearly branch to birth month palace,
    # then forward to birth hour; that gives the "first month" palace.
    leap_addition = 1 if (birthday_lunar.is_leap and birthday_lunar.lunar_day > 15) else 0
    date_leap_addition = 1 if (date_lunar.is_leap and date_lunar.lunar_day > 15) else 0
    birth_hour_branch_key = kot(astrolabe.raw_dates["chinese_date"].hourly[1])
    birth_hour_branch_index = EARTHLY_BRANCHES.index(birth_hour_branch_key)

    monthly_index = fix_index(
        yearly_index
        - (birthday_lunar.lunar_month + leap_addition)
        + birth_hour_branch_index
        + (date_lunar.lunar_month + date_leap_addition)
    )

    daily_index = fix_index(monthly_index + date_lunar.lunar_day - 1)
    hourly_index = fix_index(daily_index + EARTHLY_BRANCHES.index(kot(hourly[1], "Earthly")))

    y, m, d, *_ = normalize_date_str(target_date)
    solar_date = f"{y}-{m}-{d}"

    data = Horoscope(
        solar_date=solar_date,
        lunar_date=date_lunar.to_string(True),
        decadal=HoroscopeItem(
            index=decadal_index,
            name=t("childhood") if is_childhood else t("decadal"),
            heavenly_stem=t(kot(heavenly_stem_of_decade, "Heavenly")),
            earthly_branch=t(kot(earthly_branch_of_decade, "Earthly")),
            palace_names=get_palace_names(decadal_index),
            mutagen=get_mutagens_by_heavenly_stem(heavenly_stem_of_decade),
            stars=get_horoscope_star(heavenly_stem_of_decade, earthly_branch_of_decade, "decadal"),
        ),
        age=AgeHoroscopeItem(
            index=age_index,
            nominal_age=nominal_age,
            name=t("turn"),
            heavenly_stem=heavenly_stem_of_age,
            earthly_branch=earthly_branch_of_age,
            palace_names=get_palace_names(age_index),
            mutagen=get_mutagens_by_heavenly_stem(heavenly_stem_of_age),
            stars=None,
        ),
        yearly=YearlyHoroscopeItem(
            index=yearly_index,
            name=t("yearly"),
            heavenly_stem=t(kot(yearly[0], "Heavenly")),
            earthly_branch=t(kot(yearly[1], "Earthly")),
            palace_names=get_palace_names(yearly_index),
            mutagen=get_mutagens_by_heavenly_stem(yearly[0]),
            stars=get_horoscope_star(yearly[0], yearly[1], "yearly"),
            yearly_dec_star=YearlyDecStar(**get_yearly_12(target_date)),
        ),
        monthly=HoroscopeItem(
            index=monthly_index,
            name=t("monthly"),
            heavenly_stem=t(kot(monthly[0], "Heavenly")),
            earthly_branch=t(kot(monthly[1], "Earthly")),
            palace_names=get_palace_names(monthly_index),
            mutagen=get_mutagens_by_heavenly_stem(monthly[0]),
            stars=get_horoscope_star(monthly[0], monthly[1], "monthly"),
        ),
        daily=HoroscopeItem(
            index=daily_index,
            name=t("daily"),
            heavenly_stem=t(kot(daily[0], "Heavenly")),
            earthly_branch=t(kot(daily[1], "Earthly")),
            palace_names=get_palace_names(daily_index),
            mutagen=get_mutagens_by_heavenly_stem(daily[0]),
            stars=get_horoscope_star(daily[0], daily[1], "daily"),
        ),
        hourly=HoroscopeItem(
            index=hourly_index,
            name=t("hourly"),
            heavenly_stem=t(kot(hourly[0], "Heavenly")),
            earthly_branch=t(kot(hourly[1], "Earthly")),
            palace_names=get_palace_names(hourly_index),
            mutagen=get_mutagens_by_heavenly_stem(hourly[0]),
            stars=get_horoscope_star(hourly[0], hourly[1], "hourly"),
        ),
    )

    return FunctionalHoroscope(data, astrolabe)


@dataclass
class FunctionalAstrolabe:
    gender: str
    solar_date: str
    lunar_date: str
    chinese_date: str
    raw_dates: dict[str, Any]
    time: str
    time_range: str
    sign: str
    zodiac: str
    earthly_branch_of_soul_palace: str
    earthly_branch_of_body_palace: str
    soul: str
    body: str
    five_elements_class: str
    palaces: list["FunctionalPalace"]
    copyright: str

    # Keep track of installed plugins on this instance.
    plugins: list[Any] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.plugins is None:
            self.plugins = []

    def use(self, plugin) -> None:
        self.plugins.append(plugin)
        # Python plugin signature is explicit (plugin(astrolabe)).
        plugin(self)

    def star(self, star_name: str):
        target = None
        for p in self.palaces:
            for item in [*p.major_stars, *p.minor_stars, *p.adjective_stars]:
                if kot(item.name) == kot(star_name):
                    target = item
                    target.set_palace(p)
                    target.set_astrolabe(self)
                    break
            if target:
                break
        if not target:
            raise ValueError("invalid star name.")
        return target

    def horoscope(self, date: str | datetime | Date | None = None, time_index: int | None = None) -> FunctionalHoroscope:
        return _get_horoscope_by_solar_date(self, date, time_index)

    def palace(self, index_or_name: int | str):
        return analyzer.get_palace(self, index_or_name)

    def surrounded_palaces(self, index_or_name: int | str):
        return analyzer.get_surrounded_palaces(self, index_or_name)

    # Deprecated compat (snake_case)
    def is_surrounded(self, index_or_name: int | str, stars: list[str]) -> bool:
        return self.surrounded_palaces(index_or_name).have(stars)

    def is_surrounded_one_of(self, index_or_name: int | str, stars: list[str]) -> bool:
        return self.surrounded_palaces(index_or_name).have_one_of(stars)

    def not_surrounded(self, index_or_name: int | str, stars: list[str]) -> bool:
        return self.surrounded_palaces(index_or_name).not_have(stars)

