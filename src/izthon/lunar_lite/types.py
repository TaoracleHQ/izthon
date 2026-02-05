from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


YearDivide = Literal["exact", "normal"]
MonthDivide = Literal["exact", "normal"]


@dataclass(frozen=True)
class Options:
    year: YearDivide = "exact"
    month: MonthDivide = "exact"


@dataclass(frozen=True)
class LunarDate:
    lunar_year: int
    lunar_month: int
    lunar_day: int
    is_leap: bool

    def to_string(self, to_cn_str: bool = False) -> str:
        from .convertor import lunar_date_to_cn_string

        if to_cn_str:
            return lunar_date_to_cn_string(self)
        return f"{self.lunar_year}-{self.lunar_month}-{self.lunar_day}"


@dataclass(frozen=True)
class SolarDate:
    solar_year: int
    solar_month: int
    solar_day: int

    def to_string(self) -> str:
        return f"{self.solar_year}-{self.solar_month}-{self.solar_day}"


HeavenlyStemAndEarthlyBranch = tuple[str, str]


@dataclass(frozen=True)
class HeavenlyStemAndEarthlyBranchDate:
    yearly: HeavenlyStemAndEarthlyBranch
    monthly: HeavenlyStemAndEarthlyBranch
    daily: HeavenlyStemAndEarthlyBranch
    hourly: HeavenlyStemAndEarthlyBranch

    def to_string(self) -> str:
        return (
            f"{self.yearly[0]}{self.yearly[1]} "
            f"{self.monthly[0]}{self.monthly[1]} "
            f"{self.daily[0]}{self.daily[1]} "
            f"{self.hourly[0]}{self.hourly[1]}"
        )

