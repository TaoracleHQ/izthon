from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from ..data import MUTAGEN
from ..i18n import kot
from ..star.functional_star import FunctionalStar


Scope = Literal["origin", "decadal", "yearly", "monthly", "daily", "hourly"]


@dataclass(frozen=True)
class HoroscopeItem:
    index: int
    name: str
    heavenly_stem: str
    earthly_branch: str
    palace_names: list[str]
    mutagen: list[str]
    stars: list[list[FunctionalStar]] | None = None


@dataclass(frozen=True)
class AgeHoroscopeItem(HoroscopeItem):
    nominal_age: int = 0


@dataclass(frozen=True)
class YearlyCycleStars:
    jiangqian_12: list[str]
    suiqian_12: list[str]


@dataclass(frozen=True)
class YearlyHoroscopeItem(HoroscopeItem):
    yearly_cycle_stars: YearlyCycleStars | None = None


@dataclass(frozen=True)
class Horoscope:
    lunar_date: str
    solar_date: str
    decadal: HoroscopeItem
    age: AgeHoroscopeItem
    yearly: YearlyHoroscopeItem
    monthly: HoroscopeItem
    daily: HoroscopeItem
    hourly: HoroscopeItem


def _get_horoscope_palace_index(h: "FunctionalHoroscope", scope: Scope, palace_name: str) -> int:
    if scope == "origin":
        for idx, p in enumerate(h.astrolabe.palaces):
            if p.name == palace_name:
                return idx
        return -1
    try:
        return getattr(h.data, scope).palace_names.index(palace_name)
    except ValueError:
        return -1


class FunctionalHoroscope:
    def __init__(self, data: Horoscope, astrolabe: "FunctionalAstrolabe"):
        self.data = data
        self.astrolabe = astrolabe

    @property
    def lunar_date(self) -> str:
        return self.data.lunar_date

    @property
    def solar_date(self) -> str:
        return self.data.solar_date

    @property
    def decadal(self) -> HoroscopeItem:
        return self.data.decadal

    @property
    def age(self) -> AgeHoroscopeItem:
        return self.data.age

    @property
    def yearly(self) -> YearlyHoroscopeItem:
        return self.data.yearly

    @property
    def monthly(self) -> HoroscopeItem:
        return self.data.monthly

    @property
    def daily(self) -> HoroscopeItem:
        return self.data.daily

    @property
    def hourly(self) -> HoroscopeItem:
        return self.data.hourly

    def age_palace(self):
        return self.astrolabe.palace(self.age.index)

    def palace(self, palace_name: str, scope: Scope):
        if scope == "origin":
            return self.astrolabe.palace(palace_name)
        try:
            idx = getattr(self.data, scope).palace_names.index(palace_name)
        except ValueError as exc:
            raise ValueError("invalid palace name.") from exc
        return self.astrolabe.palace(idx)

    def surrounding_palaces(self, palace_name: str, scope: Scope):
        if scope == "origin":
            return self.astrolabe.surrounding_palaces(palace_name)
        try:
            idx = getattr(self.data, scope).palace_names.index(palace_name)
        except ValueError as exc:
            raise ValueError("invalid palace name.") from exc
        return self.astrolabe.surrounding_palaces(idx)

    def has_horoscope_stars(self, palace_name: str, scope: Scope, horoscope_star: list[str]) -> bool:
        if not self.decadal.stars or not self.yearly.stars:
            return False

        palace_index = _get_horoscope_palace_index(self, scope, palace_name)
        if palace_index < 0:
            return False

        stars = [*self.decadal.stars[palace_index], *self.yearly.stars[palace_index]]
        star_keys = [kot(s.name) for s in stars]
        target_keys = [kot(s) for s in horoscope_star]
        return all(key in star_keys for key in target_keys)

    def lacks_horoscope_stars(self, palace_name: str, scope: Scope, horoscope_star: list[str]) -> bool:
        if not self.decadal.stars or not self.yearly.stars:
            return False

        palace_index = _get_horoscope_palace_index(self, scope, palace_name)
        if palace_index < 0:
            return False

        stars = [*self.decadal.stars[palace_index], *self.yearly.stars[palace_index]]
        star_keys = [kot(s.name) for s in stars]
        target_keys = [kot(s) for s in horoscope_star]
        return all(key not in star_keys for key in target_keys)

    def has_any_horoscope_star(self, palace_name: str, scope: Scope, horoscope_star: list[str]) -> bool:
        if not self.decadal.stars or not self.yearly.stars:
            return False

        palace_index = _get_horoscope_palace_index(self, scope, palace_name)
        if palace_index < 0:
            return False

        stars = [*self.decadal.stars[palace_index], *self.yearly.stars[palace_index]]
        star_keys = [kot(s.name) for s in stars]
        target_keys = [kot(s) for s in horoscope_star]
        return any(key in star_keys for key in target_keys)

    def has_horoscope_mutagen(self, palace_name: str, scope: Scope, horoscope_mutagen: str) -> bool:
        if scope == "origin":
            return False

        palace_index = _get_horoscope_palace_index(self, scope, palace_name)
        if palace_index < 0:
            return False

        palace = self.astrolabe.palace(palace_index)
        palace_star_keys = [kot(s.name) for s in [*palace.major_stars, *palace.minor_stars]]

        try:
            mutagen_index = MUTAGEN.index(kot(horoscope_mutagen))
        except ValueError:
            return False

        mutagen_star_name = getattr(self.data, scope).mutagen[mutagen_index]
        return kot(mutagen_star_name) in palace_star_keys


from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .functional_astrolabe import FunctionalAstrolabe
