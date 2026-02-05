from __future__ import annotations

from ..astro._config import get_config
from ..i18n import kot, t
from ..lunar_lite import get_heavenly_stem_and_earthly_branch_by_solar_date
from . import init_stars
from .decorative_star import get_yearly_12
from .functional_star import FunctionalStar
from .location import (
    AstrolabeParam,
    get_daily_star_index,
    get_luan_xi_index,
    get_monthly_star_index,
    get_timely_star_index,
    get_yearly_star_index,
)


def get_adjective_star(param: AstrolabeParam) -> list[list[FunctionalStar]]:
    solar_date = param["solar_date"]
    time_index = param["time_index"]
    fix_leap = param.get("fix_leap")

    cfg = get_config()
    algorithm = cfg["algorithm"]
    stars = init_stars()

    yearly = get_heavenly_stem_and_earthly_branch_by_solar_date(
        solar_date,
        time_index,
        {"year": cfg["year_divide"]},
    ).yearly

    yearly_index = get_yearly_star_index(param)
    monthly_index = get_monthly_star_index(solar_date, time_index, fix_leap)
    daily_index = get_daily_star_index(solar_date, time_index, fix_leap)
    timely_index = get_timely_star_index(time_index)
    luan_xi = get_luan_xi_index(yearly[1])

    yearly12 = get_yearly_12(solar_date)
    suiqian12 = yearly12["suiqian12"]

    stars[luan_xi["hongluan_index"]].append(FunctionalStar(name=t("hongluan"), type="flower", scope="origin"))
    stars[luan_xi["tianxi_index"]].append(FunctionalStar(name=t("tianxi"), type="flower", scope="origin"))
    stars[monthly_index["tianyao_index"]].append(FunctionalStar(name=t("tianyao"), type="flower", scope="origin"))
    stars[yearly_index["xianchi_index"]].append(FunctionalStar(name=t("xianchi"), type="flower", scope="origin"))
    stars[monthly_index["yuejie_index"]].append(FunctionalStar(name=t("jieshen"), type="helper", scope="origin"))

    stars[daily_index["santai_index"]].append(FunctionalStar(name=t("santai"), type="adjective", scope="origin"))
    stars[daily_index["bazuo_index"]].append(FunctionalStar(name=t("bazuo"), type="adjective", scope="origin"))
    stars[daily_index["enguang_index"]].append(FunctionalStar(name=t("engguang"), type="adjective", scope="origin"))
    stars[daily_index["tiangui_index"]].append(FunctionalStar(name=t("tiangui"), type="adjective", scope="origin"))

    stars[yearly_index["longchi_index"]].append(FunctionalStar(name=t("longchi"), type="adjective", scope="origin"))
    stars[yearly_index["fengge_index"]].append(FunctionalStar(name=t("fengge"), type="adjective", scope="origin"))
    stars[yearly_index["tiancai_index"]].append(FunctionalStar(name=t("tiancai"), type="adjective", scope="origin"))
    stars[yearly_index["tianshou_index"]].append(FunctionalStar(name=t("tianshou"), type="adjective", scope="origin"))
    stars[timely_index["taifu_index"]].append(FunctionalStar(name=t("taifu"), type="adjective", scope="origin"))
    stars[timely_index["fenggao_index"]].append(FunctionalStar(name=t("fenggao"), type="adjective", scope="origin"))
    stars[monthly_index["tianwu_index"]].append(FunctionalStar(name=t("tianwu"), type="adjective", scope="origin"))
    stars[yearly_index["huagai_index"]].append(FunctionalStar(name=t("huagai"), type="adjective", scope="origin"))
    stars[yearly_index["tianguan_index"]].append(FunctionalStar(name=t("tianguan"), type="adjective", scope="origin"))
    stars[yearly_index["tianfu_index"]].append(FunctionalStar(name=t("tianfu"), type="adjective", scope="origin"))
    stars[yearly_index["tianchu_index"]].append(FunctionalStar(name=t("tianchu"), type="adjective", scope="origin"))
    stars[monthly_index["tianyue_index"]].append(FunctionalStar(name=t("tianyue"), type="adjective", scope="origin"))
    stars[yearly_index["tiande_index"]].append(FunctionalStar(name=t("tiande"), type="adjective", scope="origin"))
    stars[yearly_index["yuede_index"]].append(FunctionalStar(name=t("yuede"), type="adjective", scope="origin"))
    stars[yearly_index["tiankong_index"]].append(FunctionalStar(name=t("tiankong"), type="adjective", scope="origin"))
    stars[yearly_index["xunkong_index"]].append(FunctionalStar(name=t("xunkong"), type="adjective", scope="origin"))

    if algorithm != "zhongzhou":
        stars[yearly_index["jielu_index"]].append(FunctionalStar(name=t("jielu"), type="adjective", scope="origin"))
        stars[yearly_index["kongwang_index"]].append(
            FunctionalStar(name=t("kongwang"), type="adjective", scope="origin")
        )
    else:
        try:
            idx = suiqian12.index(t(kot("longde")))
        except ValueError:
            idx = -1
        if idx != -1:
            stars[idx].append(FunctionalStar(name=t("longde"), type="adjective", scope="origin"))

        stars[yearly_index["jiekong_index"]].append(FunctionalStar(name=t("jiekong"), type="adjective", scope="origin"))
        stars[yearly_index["jiesha_adj_index"]].append(
            FunctionalStar(name=t("jieshaAdj"), type="adjective", scope="origin")
        )
        stars[yearly_index["dahao_adj_index"]].append(FunctionalStar(name=t("dahao"), type="adjective", scope="origin"))

    stars[yearly_index["guchen_index"]].append(FunctionalStar(name=t("guchen"), type="adjective", scope="origin"))
    stars[yearly_index["guasu_index"]].append(FunctionalStar(name=t("guasu"), type="adjective", scope="origin"))
    stars[yearly_index["feilian_index"]].append(FunctionalStar(name=t("feilian"), type="adjective", scope="origin"))
    stars[yearly_index["posui_index"]].append(FunctionalStar(name=t("posui"), type="adjective", scope="origin"))
    stars[monthly_index["tianxing_index"]].append(FunctionalStar(name=t("tianxing"), type="adjective", scope="origin"))
    stars[monthly_index["yinsha_index"]].append(FunctionalStar(name=t("yinsha"), type="adjective", scope="origin"))
    stars[yearly_index["tianku_index"]].append(FunctionalStar(name=t("tianku"), type="adjective", scope="origin"))
    stars[yearly_index["tianxu_index"]].append(FunctionalStar(name=t("tianxu"), type="adjective", scope="origin"))
    stars[yearly_index["tianshi_index"]].append(FunctionalStar(name=t("tianshi"), type="adjective", scope="origin"))
    stars[yearly_index["tianshang_index"]].append(FunctionalStar(name=t("tianshang"), type="adjective", scope="origin"))

    stars[yearly_index["nianjie_index"]].append(FunctionalStar(name=t("nianjie"), type="helper", scope="origin"))

    return stars

