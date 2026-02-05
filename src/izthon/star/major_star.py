from __future__ import annotations

from ..astro._config import get_config
from ..i18n import t
from ..lunar_lite import get_heavenly_stem_and_earthly_branch_by_solar_date
from ..util import fix_index, get_brightness, get_mutagen
from . import init_stars
from .functional_star import FunctionalStar
from .location import AstrolabeParam, get_start_index


def get_major_star(param: AstrolabeParam) -> list[list[FunctionalStar]]:
    solar_date = param["solar_date"]
    time_index = param["time_index"]

    start = get_start_index(param)
    ziwei_index = start["ziwei_index"]
    tianfu_index = start["tianfu_index"]

    cfg = get_config()
    yearly = get_heavenly_stem_and_earthly_branch_by_solar_date(
        solar_date,
        time_index,
        {"year": cfg["year_divide"]},
    ).yearly

    stars = init_stars()

    ziwei_group = (
        "ziweiMaj",
        "tianjiMaj",
        "",
        "taiyangMaj",
        "wuquMaj",
        "tiantongMaj",
        "",
        "",
        "lianzhenMaj",
    )
    tianfu_group = (
        "tianfuMaj",
        "taiyinMaj",
        "tanlangMaj",
        "jumenMaj",
        "tianxiangMaj",
        "tianliangMaj",
        "qishaMaj",
        "",
        "",
        "",
        "pojunMaj",
    )

    for i, s in enumerate(ziwei_group):
        if not s:
            continue
        idx = fix_index(ziwei_index - i)
        name = t(s)
        stars[idx].append(
            FunctionalStar(
                name=name,
                type="major",
                scope="origin",
                brightness=get_brightness(name, idx),
                mutagen=get_mutagen(name, yearly[0]),
            )
        )

    for i, s in enumerate(tianfu_group):
        if not s:
            continue
        idx = fix_index(tianfu_index + i)
        name = t(s)
        stars[idx].append(
            FunctionalStar(
                name=name,
                type="major",
                scope="origin",
                brightness=get_brightness(name, idx),
                mutagen=get_mutagen(name, yearly[0]),
            )
        )

    return stars

