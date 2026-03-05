from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from typing import Any, Literal

from ..data import CHINESE_TIME, EARTHLY_BRANCHES, HEAVENLY_STEMS, TIME_RANGE, earthly_branches
from ..i18n import get_language, kot, t, using_language
from ..lunar_lite import (
    get_heavenly_stem_and_earthly_branch_by_solar_date,
    get_sign,
    get_zodiac,
    lunar_to_solar,
    solar_to_lunar,
)
from ..star import (
    FunctionalStar,
    get_adjective_star,
    get_boshi_12,
    get_changsheng_12,
    get_major_star,
    get_minor_star,
    get_tianshi_tianshang_index,
    get_yearly_12,
)
from ..util import fix_index, translate_chinese_date
from ._config import get_config, using_config
from .functional_astrolabe import FunctionalAstrolabe
from .functional_palace import FunctionalPalace
from .palace import Decadal, SoulAndBody, get_five_elements_class, get_horoscope, get_palace_names, get_soul_and_body


Language = Literal["en-US", "ja-JP", "ko-KR", "zh-CN", "zh-TW", "vi-VN"]
Plate = Literal["sky", "earth", "human"]
ConfigPatch = Mapping[str, Any]


def _build_by_solar(
    solar_date: str,
    time_index: int,
    gender: str,
    *,
    fix_leap: bool,
) -> FunctionalAstrolabe:
    cfg = get_config()
    t_index = time_index
    if cfg["day_divide"] == "current" and t_index >= 12:
        # Late rat hour counted as the current day: treat it as early rat hour for placements.
        t_index = 0

    # Year stem/branch (used for mutagen / original palace etc).
    yearly = get_heavenly_stem_and_earthly_branch_by_solar_date(
        solar_date,
        t_index,
        {"year": cfg["year_divide"], "month": cfg["horoscope_divide"]},
    ).yearly

    earthly_branch_of_year_key = kot(yearly[1], "Earthly")
    heavenly_stem_of_year_key = kot(yearly[0], "Heavenly")

    sb = get_soul_and_body(solar_date=solar_date, time_index=t_index, fix_leap=fix_leap)
    palace_names = get_palace_names(sb.soul_index)

    major_stars = get_major_star({"solar_date": solar_date, "time_index": t_index, "fix_leap": fix_leap})
    minor_stars = get_minor_star(solar_date, t_index, fix_leap)
    adjective_stars = get_adjective_star(
        {"solar_date": solar_date, "time_index": t_index, "gender": gender, "fix_leap": fix_leap}
    )
    changsheng12 = get_changsheng_12(
        {"solar_date": solar_date, "time_index": t_index, "gender": gender, "fix_leap": fix_leap}
    )
    boshi12 = get_boshi_12(solar_date, gender)
    yearly12 = get_yearly_12(solar_date)
    decadals, ages = get_horoscope(solar_date=solar_date, time_index=t_index, gender=gender, fix_leap=fix_leap)

    palaces: list[FunctionalPalace] = []
    for i in range(12):
        heavenly_stem_of_palace_key = HEAVENLY_STEMS[
            fix_index(HEAVENLY_STEMS.index(kot(sb.heavenly_stem_of_soul, "Heavenly")) - sb.soul_index + i, 10)
        ]
        earthly_branch_of_palace_key = EARTHLY_BRANCHES[fix_index(2 + i)]

        palaces.append(
            FunctionalPalace(
                index=i,
                name=palace_names[i],
                is_body_palace=sb.body_index == i,
                is_original_palace=(
                    earthly_branch_of_palace_key not in {"ziEarthly", "chouEarthly"}
                    and heavenly_stem_of_palace_key == heavenly_stem_of_year_key
                ),
                heavenly_stem=t(heavenly_stem_of_palace_key),
                earthly_branch=t(earthly_branch_of_palace_key),
                major_stars=major_stars[i],
                minor_stars=minor_stars[i],
                adjective_stars=adjective_stars[i],
                changsheng12=changsheng12[i],
                boshi12=boshi12[i],
                jiangqian12=yearly12["jiangqian12"][i],
                suiqian12=yearly12["suiqian12"][i],
                decadal=decadals[i],
                ages=ages[i],
            )
        )

    earthly_branch_of_soul_palace_key = EARTHLY_BRANCHES[fix_index(sb.soul_index + 2)]
    earthly_branch_of_body_palace = t(EARTHLY_BRANCHES[fix_index(sb.body_index + 2)])

    chinese_date = get_heavenly_stem_and_earthly_branch_by_solar_date(
        solar_date,
        time_index,
        {"year": cfg["year_divide"], "month": cfg["horoscope_divide"]},
    )
    lunar_date = solar_to_lunar(solar_date)

    soul_base = earthly_branch_of_year_key if cfg["algorithm"] == "zhongzhou" else earthly_branch_of_soul_palace_key
    soul = t(earthly_branches[soul_base]["soul"])

    return FunctionalAstrolabe(
        gender=t(kot(gender)),
        solar_date=solar_date,
        lunar_date=lunar_date.to_chinese(),
        chinese_date=translate_chinese_date(chinese_date),
        raw_dates={"lunar_date": lunar_date, "chinese_date": chinese_date},
        time=t(CHINESE_TIME[time_index]),
        time_range=TIME_RANGE[time_index],
        sign=get_sign_by_solar_date(solar_date),
        zodiac=get_zodiac_by_solar_date(solar_date),
        earthly_branch_of_soul_palace=t(earthly_branch_of_soul_palace_key),
        earthly_branch_of_body_palace=earthly_branch_of_body_palace,
        soul=soul,
        body=t(earthly_branches[earthly_branch_of_year_key]["body"]),
        five_elements_class=get_five_elements_class(sb.heavenly_stem_of_soul, sb.earthly_branch_of_soul),
        palaces=palaces,
        copyright=f"copyright © 2023-{datetime.now().year} iztro (https://github.com/SylarLong/iztro)",
        runtime_language=get_language(),
        runtime_config=cfg,
    )


def _rearrange_for_plate(
    *,
    astrolabe: FunctionalAstrolabe,
    plate: Plate,
    time_index: int,
    fix_leap: bool,
) -> FunctionalAstrolabe:
    if plate == "sky":
        return astrolabe
    if plate == "earth":
        body_palace = astrolabe.palace("身宫")
        return rearrange_astrolabe(
            from_={"heavenly_stem": body_palace.heavenly_stem, "earthly_branch": body_palace.earthly_branch},
            astrolabe=astrolabe,
            time_index=time_index,
            fix_leap=fix_leap,
        )
    if plate == "human":
        fude_palace = astrolabe.palace("福德")
        return rearrange_astrolabe(
            from_={"heavenly_stem": fude_palace.heavenly_stem, "earthly_branch": fude_palace.earthly_branch},
            astrolabe=astrolabe,
            time_index=time_index,
            fix_leap=fix_leap,
        )
    raise ValueError("invalid plate. expected 'sky', 'earth', or 'human'.")


def by_solar(
    solar_date: str,
    time_index: int,
    gender: str,
    *,
    fix_leap: bool = True,
    language: Language = "zh-CN",
    config: ConfigPatch | None = None,
    plate: Plate = "sky",
) -> FunctionalAstrolabe:
    with using_language(language), using_config(config):
        astrolabe = _build_by_solar(solar_date, time_index, gender, fix_leap=fix_leap)
        return _rearrange_for_plate(astrolabe=astrolabe, plate=plate, time_index=time_index, fix_leap=fix_leap)


def by_lunar(
    lunar_date: str,
    time_index: int,
    gender: str,
    *,
    is_leap_month: bool = False,
    fix_leap: bool = True,
    language: Language = "zh-CN",
    config: ConfigPatch | None = None,
    plate: Plate = "sky",
) -> FunctionalAstrolabe:
    with using_language(language), using_config(config):
        solar = lunar_to_solar(lunar_date, is_leap_month)
        astrolabe = _build_by_solar(solar.isoformat(), time_index, gender, fix_leap=fix_leap)
        return _rearrange_for_plate(astrolabe=astrolabe, plate=plate, time_index=time_index, fix_leap=fix_leap)


def rearrange_astrolabe(
    *,
    from_: dict[str, str],
    astrolabe: FunctionalAstrolabe,
    time_index: int,
    fix_leap: bool = True,
) -> FunctionalAstrolabe:
    sb = get_soul_and_body(
        solar_date=astrolabe.solar_date,
        time_index=time_index,
        fix_leap=fix_leap,
        from_=from_,
    )
    five_elements_class = get_five_elements_class(from_["heavenly_stem"], from_["earthly_branch"])
    palace_names = get_palace_names(sb.soul_index)

    major_stars = get_major_star(
        {"solar_date": astrolabe.solar_date, "time_index": time_index, "fix_leap": fix_leap, "from": from_}
    )
    changsheng12 = get_changsheng_12(
        {
            "solar_date": astrolabe.solar_date,
            "time_index": time_index,
            "gender": astrolabe.gender,
            "fix_leap": fix_leap,
            "from": from_,
        }
    )
    decadals, ages = get_horoscope(
        solar_date=astrolabe.solar_date,
        time_index=time_index,
        gender=astrolabe.gender,
        fix_leap=fix_leap,
        from_=from_,
    )

    astrolabe.five_elements_class = five_elements_class

    # Recalculate tianshi/tianshang positions (algorithm-specific).
    year_branch_key = kot(astrolabe.raw_dates["chinese_date"].yearly[1])
    tianshi_tianshang = get_tianshi_tianshang_index(astrolabe.gender, year_branch_key, sb.soul_index)
    tianshi_index, tianshang_index = tianshi_tianshang["tianshi_index"], tianshi_tianshang["tianshang_index"]

    # Recalculate tiancai position.
    tiancai_index = fix_index(sb.soul_index + EARTHLY_BRANCHES.index(year_branch_key))

    for i, palace in enumerate(astrolabe.palaces):
        # Ensure tianshang exists only in its target palace.
        _tianshang_idx = next((j for j, s in enumerate(palace.adjective_stars) if kot(s.name) == "tianshang"), -1)
        if _tianshang_idx != -1 and tianshang_index != i:
            palace.adjective_stars.pop(_tianshang_idx)
        if _tianshang_idx == -1 and tianshang_index == i:
            palace.adjective_stars.append(FunctionalStar(name=t("tianshang"), type="adjective", scope="origin"))

        # Ensure tianshi exists only in its target palace.
        _tianshi_idx = next((j for j, s in enumerate(palace.adjective_stars) if kot(s.name) == "tianshi"), -1)
        if _tianshi_idx != -1 and tianshi_index != i:
            palace.adjective_stars.pop(_tianshi_idx)
        if _tianshi_idx == -1 and tianshi_index == i:
            palace.adjective_stars.append(FunctionalStar(name=t("tianshi"), type="adjective", scope="origin"))

        # Ensure tiancai exists only in its target palace.
        _tiancai_idx = next((j for j, s in enumerate(palace.adjective_stars) if kot(s.name) == "tiancai"), -1)
        if _tiancai_idx != -1 and tiancai_index != i:
            palace.adjective_stars.pop(_tiancai_idx)
        if _tiancai_idx == -1 and tiancai_index == i:
            palace.adjective_stars.append(FunctionalStar(name=t("tiancai"), type="adjective", scope="origin"))

        palace.name = palace_names[i]
        palace.major_stars = major_stars[i]
        palace.changsheng12 = changsheng12[i]
        palace.decadal = decadals[i]
        palace.ages = ages[i]
        palace.is_body_palace = sb.body_index == i

    astrolabe.earthly_branch_of_soul_palace = astrolabe.palace("命宫").earthly_branch
    return astrolabe


def get_zodiac_by_solar_date(
    solar_date: str,
    *,
    language: Language | None = None,
    config: ConfigPatch | None = None,
) -> str:
    with using_language(language), using_config(config):
        cfg = get_config()
        yearly = get_heavenly_stem_and_earthly_branch_by_solar_date(
            solar_date,
            0,
            {"year": cfg["year_divide"]},
        ).yearly
        return t(kot(get_zodiac(yearly[1])))


def get_sign_by_solar_date(
    solar_date: str,
    *,
    language: Language | None = None,
    config: ConfigPatch | None = None,
) -> str:
    with using_language(language), using_config(config):
        return t(kot(get_sign(solar_date)))


def get_sign_by_lunar_date(
    lunar_date: str,
    *,
    is_leap_month: bool = False,
    language: Language | None = None,
    config: ConfigPatch | None = None,
) -> str:
    with using_language(language), using_config(config):
        solar = lunar_to_solar(lunar_date, is_leap_month)
        return get_sign_by_solar_date(solar.isoformat())


def get_major_star_by_solar_date(
    solar_date: str,
    time_index: int,
    *,
    fix_leap: bool = True,
    language: Language | None = None,
    config: ConfigPatch | None = None,
) -> str:
    with using_language(language), using_config(config):
        sb = get_soul_and_body(solar_date=solar_date, time_index=time_index, fix_leap=fix_leap)
        major_stars = get_major_star({"solar_date": solar_date, "time_index": time_index, "fix_leap": fix_leap})
        stars = [s for s in major_stars[sb.soul_index] if s.type == "major"]
        if stars:
            return ",".join(t(s.name) for s in stars)
        # Borrow opposite palace if soul palace is empty.
        return ",".join(t(s.name) for s in major_stars[fix_index(sb.soul_index + 6)] if s.type == "major")


def get_major_star_by_lunar_date(
    lunar_date: str,
    time_index: int,
    *,
    is_leap_month: bool = False,
    fix_leap: bool = True,
    language: Language | None = None,
    config: ConfigPatch | None = None,
) -> str:
    with using_language(language), using_config(config):
        solar = lunar_to_solar(lunar_date, is_leap_month)
        return get_major_star_by_solar_date(solar.isoformat(), time_index, fix_leap=fix_leap)
