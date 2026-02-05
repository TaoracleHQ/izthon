from __future__ import annotations

from ..astro._config import get_config
from ..i18n import t
from ..lunar_lite import get_heavenly_stem_and_earthly_branch_by_solar_date
from ..util import fix_lunar_month_index, get_brightness, get_mutagen
from . import init_stars
from .functional_star import FunctionalStar
from .location import (
    get_chang_qu_index,
    get_huo_ling_index,
    get_kong_jie_index,
    get_kui_yue_index,
    get_lu_yang_tuo_ma_index,
    get_zuo_you_index,
)


def get_minor_star(solar_date: str, time_index: int, fix_leap: bool | None = None) -> list[list[FunctionalStar]]:
    stars = init_stars()
    cfg = get_config()
    yearly = get_heavenly_stem_and_earthly_branch_by_solar_date(
        solar_date,
        time_index,
        {"year": cfg["year_divide"]},
    ).yearly

    month_index = fix_lunar_month_index(solar_date, time_index, fix_leap)

    zuo_you = get_zuo_you_index(month_index + 1)
    chang_qu = get_chang_qu_index(time_index)
    kui_yue = get_kui_yue_index(yearly[0])
    huo_ling = get_huo_ling_index(yearly[1], time_index)
    kong_jie = get_kong_jie_index(time_index)
    lu_yang_tuo_ma = get_lu_yang_tuo_ma_index(yearly[0], yearly[1])

    stars[zuo_you["zuo_index"]].append(
        FunctionalStar(
            name=t("zuofuMin"),
            type="soft",
            scope="origin",
            brightness=get_brightness("左辅", zuo_you["zuo_index"]),
            mutagen=get_mutagen("左辅", yearly[0]),
        )
    )
    stars[zuo_you["you_index"]].append(
        FunctionalStar(
            name=t("youbiMin"),
            type="soft",
            scope="origin",
            brightness=get_brightness("右弼", zuo_you["you_index"]),
            mutagen=get_mutagen("右弼", yearly[0]),
        )
    )
    stars[chang_qu["chang_index"]].append(
        FunctionalStar(
            name=t("wenchangMin"),
            type="soft",
            scope="origin",
            brightness=get_brightness("文昌", chang_qu["chang_index"]),
            mutagen=get_mutagen("文昌", yearly[0]),
        )
    )
    stars[chang_qu["qu_index"]].append(
        FunctionalStar(
            name=t("wenquMin"),
            type="soft",
            scope="origin",
            brightness=get_brightness("文曲", chang_qu["qu_index"]),
            mutagen=get_mutagen("文曲", yearly[0]),
        )
    )
    stars[kui_yue["kui_index"]].append(
        FunctionalStar(
            name=t("tiankuiMin"),
            type="soft",
            scope="origin",
            brightness=get_brightness("天魁", kui_yue["kui_index"]),
        )
    )
    stars[kui_yue["yue_index"]].append(
        FunctionalStar(
            name=t("tianyueMin"),
            type="soft",
            scope="origin",
            brightness=get_brightness("天钺", kui_yue["yue_index"]),
        )
    )
    stars[lu_yang_tuo_ma["lu_index"]].append(
        FunctionalStar(
            name=t("lucunMin"),
            type="lucun",
            scope="origin",
            brightness=get_brightness("禄存", lu_yang_tuo_ma["lu_index"]),
        )
    )
    stars[lu_yang_tuo_ma["ma_index"]].append(
        FunctionalStar(
            name=t("tianmaMin"),
            type="tianma",
            scope="origin",
            brightness=get_brightness("天马", lu_yang_tuo_ma["ma_index"]),
        )
    )
    stars[kong_jie["kong_index"]].append(
        FunctionalStar(
            name=t("dikongMin"),
            type="tough",
            scope="origin",
            brightness=get_brightness("地空", kong_jie["kong_index"]),
        )
    )
    stars[kong_jie["jie_index"]].append(
        FunctionalStar(
            name=t("dijieMin"),
            type="tough",
            scope="origin",
            brightness=get_brightness("地劫", kong_jie["jie_index"]),
        )
    )
    stars[huo_ling["huo_index"]].append(
        FunctionalStar(
            name=t("huoxingMin"),
            type="tough",
            scope="origin",
            brightness=get_brightness("火星", huo_ling["huo_index"]),
        )
    )
    stars[huo_ling["ling_index"]].append(
        FunctionalStar(
            name=t("lingxingMin"),
            type="tough",
            scope="origin",
            brightness=get_brightness("铃星", huo_ling["ling_index"]),
        )
    )
    stars[lu_yang_tuo_ma["yang_index"]].append(
        FunctionalStar(
            name=t("qingyangMin"),
            type="tough",
            scope="origin",
            brightness=get_brightness("擎羊", lu_yang_tuo_ma["yang_index"]),
        )
    )
    stars[lu_yang_tuo_ma["tuo_index"]].append(
        FunctionalStar(
            name=t("tuoluoMin"),
            type="tough",
            scope="origin",
            brightness=get_brightness("陀罗", lu_yang_tuo_ma["tuo_index"]),
        )
    )

    return stars

