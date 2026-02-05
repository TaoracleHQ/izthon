from __future__ import annotations

from typing import TypedDict

from ..astro._config import get_config
from ..astro.palace import get_five_elements_class, get_soul_and_body
from ..data import EARTHLY_BRANCHES, HEAVENLY_STEMS, PALACES, FiveElementsClass
from ..i18n import kot
from ..lunar_lite import get_heavenly_stem_and_earthly_branch_by_solar_date, get_total_days_of_lunar_month, solar_to_lunar
from ..util import fix_earthly_branch_index, fix_index, fix_lunar_day_index, fix_lunar_month_index


class AstrolabeParam(TypedDict, total=False):
    solar_date: str
    time_index: int
    fix_leap: bool
    gender: str
    from_: dict[str, str]


def get_start_index(param: AstrolabeParam) -> dict[str, int]:
    solar_date = param["solar_date"]
    time_index = param["time_index"]
    fix_leap = param.get("fix_leap")
    from_ = param.get("from_") or param.get("from")

    sb = get_soul_and_body(solar_date=solar_date, time_index=time_index, fix_leap=fix_leap)
    lunar = solar_to_lunar(solar_date)

    base_heavenly_stem = from_["heavenly_stem"] if from_ and from_.get("heavenly_stem") else sb.heavenly_stem_of_soul
    base_earthly_branch = from_["earthly_branch"] if from_ and from_.get("earthly_branch") else sb.earthly_branch_of_soul

    five_elements_key = kot(get_five_elements_class(base_heavenly_stem, base_earthly_branch))
    five_elements_value = int(FiveElementsClass[five_elements_key])

    max_days = get_total_days_of_lunar_month(solar_date)

    # Late rat hour counts as the next day in some rules.
    day = lunar.lunar_day + 1 if time_index == 12 else lunar.lunar_day
    if day > max_days:
        day -= max_days

    remainder = -1
    quotient = 0
    offset = -1
    while remainder != 0:
        offset += 1
        divisor = day + offset
        quotient = divisor // five_elements_value
        remainder = divisor % five_elements_value

    quotient %= 12
    ziwei_index = quotient - 1

    if offset % 2 == 0:
        ziwei_index += offset
    else:
        ziwei_index -= offset

    ziwei_index = fix_index(ziwei_index)
    tianfu_index = fix_index(12 - ziwei_index)

    return {"ziwei_index": ziwei_index, "tianfu_index": tianfu_index}


def get_lu_yang_tuo_ma_index(heavenly_stem_name: str, earthly_branch_name: str) -> dict[str, int]:
    lu_index = -1
    ma_index = 0

    heavenly_stem = kot(heavenly_stem_name, "Heavenly")
    earthly_branch = kot(earthly_branch_name, "Earthly")

    if earthly_branch in {"yinEarthly", "wuEarthly", "xuEarthly"}:
        ma_index = fix_earthly_branch_index("shen")
    elif earthly_branch in {"shenEarthly", "ziEarthly", "chenEarthly"}:
        ma_index = fix_earthly_branch_index("yin")
    elif earthly_branch in {"siEarthly", "youEarthly", "chouEarthly"}:
        ma_index = fix_earthly_branch_index("hai")
    elif earthly_branch in {"haiEarthly", "maoEarthly", "weiEarthly"}:
        ma_index = fix_earthly_branch_index("si")

    if heavenly_stem == "jiaHeavenly":
        lu_index = fix_earthly_branch_index("yin")
    elif heavenly_stem == "yiHeavenly":
        lu_index = fix_earthly_branch_index("mao")
    elif heavenly_stem in {"bingHeavenly", "wuHeavenly"}:
        lu_index = fix_earthly_branch_index("si")
    elif heavenly_stem in {"dingHeavenly", "jiHeavenly"}:
        lu_index = fix_earthly_branch_index("woo")
    elif heavenly_stem == "gengHeavenly":
        lu_index = fix_earthly_branch_index("shen")
    elif heavenly_stem == "xinHeavenly":
        lu_index = fix_earthly_branch_index("you")
    elif heavenly_stem == "renHeavenly":
        lu_index = fix_earthly_branch_index("hai")
    elif heavenly_stem == "guiHeavenly":
        lu_index = fix_earthly_branch_index("zi")

    return {
        "lu_index": lu_index,
        "ma_index": ma_index,
        "yang_index": fix_index(lu_index + 1),
        "tuo_index": fix_index(lu_index - 1),
    }


def get_kui_yue_index(heavenly_stem_name: str) -> dict[str, int]:
    kui_index = -1
    yue_index = -1
    heavenly_stem = kot(heavenly_stem_name, "Heavenly")

    if heavenly_stem in {"jiaHeavenly", "wuHeavenly", "gengHeavenly"}:
        kui_index = fix_earthly_branch_index("chou")
        yue_index = fix_earthly_branch_index("wei")
    elif heavenly_stem in {"yiHeavenly", "jiHeavenly"}:
        kui_index = fix_earthly_branch_index("zi")
        yue_index = fix_earthly_branch_index("shen")
    elif heavenly_stem == "xinHeavenly":
        kui_index = fix_earthly_branch_index("woo")
        yue_index = fix_earthly_branch_index("yin")
    elif heavenly_stem in {"bingHeavenly", "dingHeavenly"}:
        kui_index = fix_earthly_branch_index("hai")
        yue_index = fix_earthly_branch_index("you")
    elif heavenly_stem in {"renHeavenly", "guiHeavenly"}:
        kui_index = fix_earthly_branch_index("mao")
        yue_index = fix_earthly_branch_index("si")

    return {"kui_index": kui_index, "yue_index": yue_index}


def get_zuo_you_index(lunar_month: int) -> dict[str, int]:
    zuo_index = fix_index(fix_earthly_branch_index("chen") + (lunar_month - 1))
    you_index = fix_index(fix_earthly_branch_index("xu") - (lunar_month - 1))
    return {"zuo_index": zuo_index, "you_index": you_index}


def get_chang_qu_index(time_index: int) -> dict[str, int]:
    chang_index = fix_index(fix_earthly_branch_index("xu") - fix_index(time_index))
    qu_index = fix_index(fix_earthly_branch_index("chen") + fix_index(time_index))
    return {"chang_index": chang_index, "qu_index": qu_index}


def get_daily_star_index(solar_date: str, time_index: int, fix_leap: bool | None = None) -> dict[str, int]:
    lunar = solar_to_lunar(solar_date)
    month_index = fix_lunar_month_index(solar_date, time_index, fix_leap)
    zuo_you = get_zuo_you_index(month_index + 1)
    chang_qu = get_chang_qu_index(time_index)
    day_index = fix_lunar_day_index(lunar.lunar_day, time_index)

    santai_index = fix_index((zuo_you["zuo_index"] + day_index) % 12)
    bazuo_index = fix_index((zuo_you["you_index"] - day_index) % 12)
    enguang_index = fix_index(((chang_qu["chang_index"] + day_index) % 12) - 1)
    tiangui_index = fix_index(((chang_qu["qu_index"] + day_index) % 12) - 1)

    return {
        "santai_index": santai_index,
        "bazuo_index": bazuo_index,
        "enguang_index": enguang_index,
        "tiangui_index": tiangui_index,
    }


def get_timely_star_index(time_index: int) -> dict[str, int]:
    taifu_index = fix_index(fix_earthly_branch_index("woo") + fix_index(time_index))
    fenggao_index = fix_index(fix_earthly_branch_index("yin") + fix_index(time_index))
    return {"taifu_index": taifu_index, "fenggao_index": fenggao_index}


def get_kong_jie_index(time_index: int) -> dict[str, int]:
    fixed_time_index = fix_index(time_index)
    hai_index = fix_earthly_branch_index("hai")
    kong_index = fix_index(hai_index - fixed_time_index)
    jie_index = fix_index(hai_index + fixed_time_index)
    return {"kong_index": kong_index, "jie_index": jie_index}


def get_huo_ling_index(earthly_branch_name: str, time_index: int) -> dict[str, int]:
    huo_index = -1
    ling_index = -1
    fixed_time_index = fix_index(time_index)
    earthly_branch = kot(earthly_branch_name, "Earthly")

    if earthly_branch in {"yinEarthly", "wuEarthly", "xuEarthly"}:
        huo_index = fix_earthly_branch_index("chou") + fixed_time_index
        ling_index = fix_earthly_branch_index("mao") + fixed_time_index
    elif earthly_branch in {"shenEarthly", "ziEarthly", "chenEarthly"}:
        huo_index = fix_earthly_branch_index("yin") + fixed_time_index
        ling_index = fix_earthly_branch_index("xu") + fixed_time_index
    elif earthly_branch in {"siEarthly", "youEarthly", "chouEarthly"}:
        huo_index = fix_earthly_branch_index("mao") + fixed_time_index
        ling_index = fix_earthly_branch_index("xu") + fixed_time_index
    elif earthly_branch in {"haiEarthly", "weiEarthly", "maoEarthly"}:
        huo_index = fix_earthly_branch_index("you") + fixed_time_index
        ling_index = fix_earthly_branch_index("xu") + fixed_time_index

    return {"huo_index": fix_index(huo_index), "ling_index": fix_index(ling_index)}


def get_luan_xi_index(earthly_branch_name: str) -> dict[str, int]:
    earthly_branch = kot(earthly_branch_name, "Earthly")
    hongluan_index = fix_index(fix_earthly_branch_index("mao") - EARTHLY_BRANCHES.index(earthly_branch))
    tianxi_index = fix_index(hongluan_index + 6)
    return {"hongluan_index": hongluan_index, "tianxi_index": tianxi_index}


def get_huagai_xianchi_index(earthly_branch_name: str) -> dict[str, int]:
    hg_idx = -1
    xc_idx = -1
    earthly_branch = kot(earthly_branch_name, "Earthly")

    if earthly_branch in {"yinEarthly", "wuEarthly", "xuEarthly"}:
        hg_idx = fix_earthly_branch_index("xu")
        xc_idx = fix_earthly_branch_index("mao")
    elif earthly_branch in {"shenEarthly", "ziEarthly", "chenEarthly"}:
        hg_idx = fix_earthly_branch_index("chen")
        xc_idx = fix_earthly_branch_index("you")
    elif earthly_branch in {"siEarthly", "youEarthly", "chouEarthly"}:
        hg_idx = fix_earthly_branch_index("chou")
        xc_idx = fix_earthly_branch_index("woo")
    elif earthly_branch in {"haiEarthly", "weiEarthly", "maoEarthly"}:
        hg_idx = fix_earthly_branch_index("wei")
        xc_idx = fix_earthly_branch_index("zi")

    return {"huagai_index": fix_index(hg_idx), "xianchi_index": fix_index(xc_idx)}


def get_gu_gua_index(earthly_branch_name: str) -> dict[str, int]:
    gu_idx = -1
    gua_idx = -1
    earthly_branch = kot(earthly_branch_name, "Earthly")

    if earthly_branch in {"yinEarthly", "maoEarthly", "chenEarthly"}:
        gu_idx = fix_earthly_branch_index("si")
        gua_idx = fix_earthly_branch_index("chou")
    elif earthly_branch in {"siEarthly", "wuEarthly", "weiEarthly"}:
        gu_idx = fix_earthly_branch_index("shen")
        gua_idx = fix_earthly_branch_index("chen")
    elif earthly_branch in {"shenEarthly", "youEarthly", "xuEarthly"}:
        gu_idx = fix_earthly_branch_index("hai")
        gua_idx = fix_earthly_branch_index("wei")
    elif earthly_branch in {"haiEarthly", "ziEarthly", "chouEarthly"}:
        gu_idx = fix_earthly_branch_index("yin")
        gua_idx = fix_earthly_branch_index("xu")

    return {"guchen_index": fix_index(gu_idx), "guasu_index": fix_index(gua_idx)}


def get_jiesha_adj_index(earthly_branch_key: str) -> int:
    if earthly_branch_key in {"shenEarthly", "ziEarthly", "chenEarthly"}:
        return 3
    if earthly_branch_key in {"haiEarthly", "maoEarthly", "weiEarthly"}:
        return 6
    if earthly_branch_key in {"yinEarthly", "wuEarthly", "xuEarthly"}:
        return 9
    if earthly_branch_key in {"siEarthly", "youEarthly", "chouEarthly"}:
        return 0
    raise ValueError("invalid earthly_branch_key")


def get_dahao_index(earthly_branch_key: str) -> int:
    matched = [
        "weiEarthly",
        "wuEarthly",
        "youEarthly",
        "shenEarthly",
        "haiEarthly",
        "xuEarthly",
        "chouEarthly",
        "ziEarthly",
        "maoEarthly",
        "yinEarthly",
        "siEarthly",
        "chenEarthly",
    ][EARTHLY_BRANCHES.index(earthly_branch_key)]
    return fix_index(EARTHLY_BRANCHES.index(matched) - 2)


def get_yearly_star_index(param: AstrolabeParam) -> dict[str, int]:
    solar_date = param["solar_date"]
    time_index = param["time_index"]
    gender = param.get("gender")
    fix_leap = param.get("fix_leap")
    if not gender:
        raise ValueError("gender is required for yearly star index calculation.")

    cfg = get_config()
    yearly = get_heavenly_stem_and_earthly_branch_by_solar_date(
        solar_date,
        time_index,
        {"year": cfg["horoscope_divide"]},
    ).yearly

    sb = get_soul_and_body(solar_date=solar_date, time_index=time_index, fix_leap=fix_leap)
    heavenly_stem = kot(yearly[0], "Heavenly")
    earthly_branch = kot(yearly[1], "Earthly")

    hg_xc = get_huagai_xianchi_index(yearly[1])
    gu_gua = get_gu_gua_index(yearly[1])

    tiancai_index = fix_index(sb.soul_index + EARTHLY_BRANCHES.index(earthly_branch))
    tianshou_index = fix_index(sb.body_index + EARTHLY_BRANCHES.index(earthly_branch))

    tianchu_index = fix_index(
        fix_earthly_branch_index(
            ["si", "woo", "zi", "si", "woo", "shen", "yin", "woo", "you", "hai"][HEAVENLY_STEMS.index(heavenly_stem)]
        )
    )
    posui_index = fix_index(
        fix_earthly_branch_index(["si", "chou", "you"][EARTHLY_BRANCHES.index(earthly_branch) % 3])
    )
    feilian_index = fix_index(
        fix_earthly_branch_index(
            [
                "shen",
                "you",
                "xu",
                "si",
                "woo",
                "wei",
                "yin",
                "mao",
                "chen",
                "hai",
                "zi",
                "chou",
            ][EARTHLY_BRANCHES.index(earthly_branch)]
        )
    )
    longchi_index = fix_index(fix_earthly_branch_index("chen") + EARTHLY_BRANCHES.index(earthly_branch))
    fengge_index = fix_index(fix_earthly_branch_index("xu") - EARTHLY_BRANCHES.index(earthly_branch))
    tianku_index = fix_index(fix_earthly_branch_index("woo") - EARTHLY_BRANCHES.index(earthly_branch))
    tianxu_index = fix_index(fix_earthly_branch_index("woo") + EARTHLY_BRANCHES.index(earthly_branch))
    tianguan_index = fix_index(
        fix_earthly_branch_index(
            ["wei", "chen", "si", "yin", "mao", "you", "hai", "you", "xu", "woo"][HEAVENLY_STEMS.index(heavenly_stem)]
        )
    )
    tianfu_index = fix_index(
        fix_earthly_branch_index(
            ["you", "shen", "zi", "hai", "mao", "yin", "woo", "si", "woo", "si"][HEAVENLY_STEMS.index(heavenly_stem)]
        )
    )
    tiande_index = fix_index(fix_earthly_branch_index("you") + EARTHLY_BRANCHES.index(earthly_branch))
    yuede_index = fix_index(fix_earthly_branch_index("si") + EARTHLY_BRANCHES.index(earthly_branch))
    tiankong_index = fix_index(fix_earthly_branch_index(yearly[1]) + 1)
    jielu_index = fix_index(
        fix_earthly_branch_index(
            ["shen", "woo", "chen", "yin", "zi"][HEAVENLY_STEMS.index(heavenly_stem) % 5]
        )
    )
    kongwang_index = fix_index(
        fix_earthly_branch_index(
            ["you", "wei", "si", "mao", "chou"][HEAVENLY_STEMS.index(heavenly_stem) % 5]
        )
    )

    xunkong_index = fix_index(
        fix_earthly_branch_index(yearly[1])
        + HEAVENLY_STEMS.index("guiHeavenly")
        - HEAVENLY_STEMS.index(heavenly_stem)
        + 1
    )

    yinyang = EARTHLY_BRANCHES.index(earthly_branch) % 2
    if yinyang != xunkong_index % 2:
        xunkong_index = fix_index(xunkong_index + 1)

    jiekong_index = jielu_index if yinyang == 0 else kongwang_index

    jiesha_adj_index = get_jiesha_adj_index(earthly_branch)
    nianjie_index = get_nianjie_index(yearly[1])
    dahao_adj_index = get_dahao_index(earthly_branch)

    tianshi_tianshang = get_tianshi_tianshang_index(gender, earthly_branch, sb.soul_index)

    return {
        "xianchi_index": hg_xc["xianchi_index"],
        "huagai_index": hg_xc["huagai_index"],
        "guchen_index": gu_gua["guchen_index"],
        "guasu_index": gu_gua["guasu_index"],
        "tiancai_index": tiancai_index,
        "tianshou_index": tianshou_index,
        "tianchu_index": tianchu_index,
        "posui_index": posui_index,
        "feilian_index": feilian_index,
        "longchi_index": longchi_index,
        "fengge_index": fengge_index,
        "tianku_index": tianku_index,
        "tianxu_index": tianxu_index,
        "tianguan_index": tianguan_index,
        "tianfu_index": tianfu_index,
        "tiande_index": tiande_index,
        "yuede_index": yuede_index,
        "tiankong_index": tiankong_index,
        "jielu_index": jielu_index,
        "kongwang_index": kongwang_index,
        "xunkong_index": xunkong_index,
        "tianshang_index": tianshi_tianshang["tianshang_index"],
        "tianshi_index": tianshi_tianshang["tianshi_index"],
        "jiekong_index": jiekong_index,
        "jiesha_adj_index": jiesha_adj_index,
        "nianjie_index": nianjie_index,
        "dahao_adj_index": dahao_adj_index,
    }


def get_tianshi_tianshang_index(gender: str, earthly_branch_key: str, soul_index: int) -> dict[str, int]:
    yinyang = EARTHLY_BRANCHES.index(earthly_branch_key) % 2
    cfg = get_config()

    gender_yinyang = ["male", "female"]
    same_yinyang = yinyang == gender_yinyang.index(kot(gender))

    tianshang_index = fix_index(PALACES.index("friendsPalace") + soul_index)
    tianshi_index = fix_index(PALACES.index("healthPalace") + soul_index)

    if cfg["algorithm"] == "zhongzhou" and not same_yinyang:
        tianshi_index, tianshang_index = tianshang_index, tianshi_index

    return {"tianshang_index": tianshang_index, "tianshi_index": tianshi_index}


def get_nianjie_index(earthly_branch_name: str) -> int:
    earthly_branch = kot(earthly_branch_name, "Earthly")
    return fix_index(
        fix_earthly_branch_index(
            ["xu", "you", "shen", "wei", "woo", "si", "chen", "mao", "yin", "chou", "zi", "hai"][
                EARTHLY_BRANCHES.index(earthly_branch)
            ]
        )
    )


def get_monthly_star_index(solar_date: str, time_index: int, fix_leap: bool | None = None) -> dict[str, int]:
    month_index = fix_lunar_month_index(solar_date, time_index, fix_leap)

    jieshen_index = fix_index(
        fix_earthly_branch_index(["shen", "xu", "zi", "yin", "chen", "woo"][month_index // 2])
    )
    tianyao_index = fix_index(fix_earthly_branch_index("chou") + month_index)
    tianxing_index = fix_index(fix_earthly_branch_index("you") + month_index)
    yinsha_index = fix_index(
        fix_earthly_branch_index(["yin", "zi", "xu", "shen", "woo", "chen"][month_index % 6])
    )
    tianyue_index = fix_index(
        fix_earthly_branch_index(
            [
                "xu",
                "si",
                "chen",
                "yin",
                "wei",
                "mao",
                "hai",
                "wei",
                "yin",
                "woo",
                "xu",
                "yin",
            ][month_index]
        )
    )
    tianwu_index = fix_index(fix_earthly_branch_index(["si", "shen", "yin", "hai"][month_index % 4]))

    return {
        "yuejie_index": jieshen_index,
        "tianyao_index": tianyao_index,
        "tianxing_index": tianxing_index,
        "yinsha_index": yinsha_index,
        "tianyue_index": tianyue_index,
        "tianwu_index": tianwu_index,
    }


def get_chang_qu_index_by_heavenly_stem(heavenly_stem_name: str) -> dict[str, int]:
    chang_index = -1
    qu_index = -1
    heavenly_stem = kot(heavenly_stem_name, "Heavenly")

    if heavenly_stem == "jiaHeavenly":
        chang_index = fix_index(fix_earthly_branch_index("si"))
        qu_index = fix_index(fix_earthly_branch_index("you"))
    elif heavenly_stem == "yiHeavenly":
        chang_index = fix_index(fix_earthly_branch_index("woo"))
        qu_index = fix_index(fix_earthly_branch_index("shen"))
    elif heavenly_stem in {"bingHeavenly", "wuHeavenly"}:
        chang_index = fix_index(fix_earthly_branch_index("shen"))
        qu_index = fix_index(fix_earthly_branch_index("woo"))
    elif heavenly_stem in {"dingHeavenly", "jiHeavenly"}:
        chang_index = fix_index(fix_earthly_branch_index("you"))
        qu_index = fix_index(fix_earthly_branch_index("si"))
    elif heavenly_stem == "gengHeavenly":
        chang_index = fix_index(fix_earthly_branch_index("hai"))
        qu_index = fix_index(fix_earthly_branch_index("mao"))
    elif heavenly_stem == "xinHeavenly":
        chang_index = fix_index(fix_earthly_branch_index("zi"))
        qu_index = fix_index(fix_earthly_branch_index("yin"))
    elif heavenly_stem == "renHeavenly":
        chang_index = fix_index(fix_earthly_branch_index("yin"))
        qu_index = fix_index(fix_earthly_branch_index("zi"))
    elif heavenly_stem == "guiHeavenly":
        chang_index = fix_index(fix_earthly_branch_index("mao"))
        qu_index = fix_index(fix_earthly_branch_index("hai"))

    return {"chang_index": chang_index, "qu_index": qu_index}
