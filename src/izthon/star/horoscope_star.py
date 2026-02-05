from __future__ import annotations

from typing import Literal

from ..i18n import t
from . import init_stars
from .functional_star import FunctionalStar
from .location import (
    get_chang_qu_index_by_heavenly_stem,
    get_kui_yue_index,
    get_luan_xi_index,
    get_lu_yang_tuo_ma_index,
    get_nianjie_index,
)


Scope = Literal["origin", "decadal", "yearly", "monthly", "daily", "hourly"]


def get_horoscope_star(heavenly_stem: str, earthly_branch: str, scope: Scope) -> list[list[FunctionalStar]]:
    kui_yue = get_kui_yue_index(heavenly_stem)
    chang_qu = get_chang_qu_index_by_heavenly_stem(heavenly_stem)
    lu_yang_tuo_ma = get_lu_yang_tuo_ma_index(heavenly_stem, earthly_branch)
    luan_xi = get_luan_xi_index(earthly_branch)

    stars = init_stars()

    trans: dict[Scope, dict[str, str]] = {
        "origin": {
            "tiankui": t("tiankuiMin"),
            "tianyue": t("tianyueMin"),
            "wenchang": t("wenchangMin"),
            "wenqu": t("wenquMin"),
            "lucun": t("lucunMin"),
            "qingyang": t("qingyangMin"),
            "tuoluo": t("tuoluoMin"),
            "tianma": t("tianmaMin"),
            "hongluan": t("hongluanMin"),
            "tianxi": t("tianxi"),
        },
        "decadal": {
            "tiankui": t("yunkui"),
            "tianyue": t("yunyue"),
            "wenchang": t("yunchang"),
            "wenqu": t("yunqu"),
            "lucun": t("yunlu"),
            "qingyang": t("yunyang"),
            "tuoluo": t("yuntuo"),
            "tianma": t("yunma"),
            "hongluan": t("yunluan"),
            "tianxi": t("yunxi"),
        },
        "yearly": {
            "tiankui": t("liukui"),
            "tianyue": t("liuyue"),
            "wenchang": t("liuchang"),
            "wenqu": t("liuqu"),
            "lucun": t("liulu"),
            "qingyang": t("liuyang"),
            "tuoluo": t("liutuo"),
            "tianma": t("liuma"),
            "hongluan": t("liuluan"),
            "tianxi": t("liuxi"),
        },
        "monthly": {
            "tiankui": t("yuekui"),
            "tianyue": t("yueyue"),
            "wenchang": t("yuechang"),
            "wenqu": t("yuequ"),
            "lucun": t("yuelu"),
            "qingyang": t("yueyang"),
            "tuoluo": t("yuetuo"),
            "tianma": t("yuema"),
            "hongluan": t("yueluan"),
            "tianxi": t("yuexi"),
        },
        "daily": {
            "tiankui": t("rikui"),
            "tianyue": t("riyue"),
            "wenchang": t("richang"),
            "wenqu": t("riqu"),
            "lucun": t("rilu"),
            "qingyang": t("riyang"),
            "tuoluo": t("rituo"),
            "tianma": t("rima"),
            "hongluan": t("riluan"),
            "tianxi": t("rixi"),
        },
        "hourly": {
            "tiankui": t("shikui"),
            "tianyue": t("shiyue"),
            "wenchang": t("shichang"),
            "wenqu": t("shiqu"),
            "lucun": t("shilu"),
            "qingyang": t("shiyang"),
            "tuoluo": t("shituo"),
            "tianma": t("shima"),
            "hongluan": t("shiluan"),
            "tianxi": t("shixi"),
        },
    }

    if scope == "yearly":
        nianjie_index = get_nianjie_index(earthly_branch)
        stars[nianjie_index].append(FunctionalStar(name=t("nianjie"), type="helper", scope="yearly"))

    stars[kui_yue["kui_index"]].append(FunctionalStar(name=trans[scope]["tiankui"], type="soft", scope=scope))
    stars[kui_yue["yue_index"]].append(FunctionalStar(name=trans[scope]["tianyue"], type="soft", scope=scope))
    stars[chang_qu["chang_index"]].append(FunctionalStar(name=trans[scope]["wenchang"], type="soft", scope=scope))
    stars[chang_qu["qu_index"]].append(FunctionalStar(name=trans[scope]["wenqu"], type="soft", scope=scope))
    stars[lu_yang_tuo_ma["lu_index"]].append(FunctionalStar(name=trans[scope]["lucun"], type="lucun", scope=scope))
    stars[lu_yang_tuo_ma["yang_index"]].append(FunctionalStar(name=trans[scope]["qingyang"], type="tough", scope=scope))
    stars[lu_yang_tuo_ma["tuo_index"]].append(FunctionalStar(name=trans[scope]["tuoluo"], type="tough", scope=scope))
    stars[lu_yang_tuo_ma["ma_index"]].append(FunctionalStar(name=trans[scope]["tianma"], type="tianma", scope=scope))
    stars[luan_xi["hongluan_index"]].append(FunctionalStar(name=trans[scope]["hongluan"], type="flower", scope=scope))
    stars[luan_xi["tianxi_index"]].append(FunctionalStar(name=trans[scope]["tianxi"], type="flower", scope=scope))

    return stars

