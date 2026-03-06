from __future__ import annotations

from ..astro._config import get_config
from ..astro.palace import get_five_elements_class, get_soul_and_body
from ..data import GENDER, FiveElementsClass, earthly_branches
from ..i18n import kot, t
from ..lunar_lite import get_heavenly_stem_and_earthly_branch_by_solar_date
from ..util import fix_earthly_branch_index, fix_index
from .location import get_lu_yang_tuo_ma_index


def get_changsheng_12_start_index(five_elements_class_name: str) -> int:
    five_elements_class_key = kot(five_elements_class_name)
    start_idx = 0

    val = int(FiveElementsClass[five_elements_class_key])
    if val == 2:
        start_idx = fix_earthly_branch_index("shen")
    elif val == 3:
        start_idx = fix_earthly_branch_index("hai")
    elif val == 4:
        start_idx = fix_earthly_branch_index("si")
    elif val == 5:
        start_idx = fix_earthly_branch_index("shen")
    elif val == 6:
        start_idx = fix_earthly_branch_index("yin")

    return start_idx


def get_changsheng_12(param: dict) -> list[str]:
    solar_date = param["solar_date"]
    gender = param["gender"]

    gender_key = kot(gender)
    cfg = get_config()
    yearly = get_heavenly_stem_and_earthly_branch_by_solar_date(
        solar_date,
        0,
        {"year": cfg["year_divide"]},
    ).yearly
    earthly_branch_of_year_key = kot(yearly[1], "Earthly")

    sb = get_soul_and_body(
        solar_date=solar_date,
        time_index=param["time_index"],
        fix_leap=param.get("fix_leap"),
        from_=param.get("from_") or param.get("from"),
    )
    five_elements_class = get_five_elements_class(sb.heavenly_stem_of_soul, sb.earthly_branch_of_soul)
    stars = (
        "changsheng",
        "muyu",
        "guandai",
        "linguan",
        "diwang",
        "shuai",
        "bing",
        "si",
        "mu",
        "jue",
        "tai",
        "yang",
    )

    start_idx = get_changsheng_12_start_index(five_elements_class)
    changsheng_12: list[str] = [""] * 12

    same_yinyang = GENDER[gender_key] == earthly_branches[earthly_branch_of_year_key]["yin_yang"]
    for i, key in enumerate(stars):
        idx = fix_index(i + start_idx) if same_yinyang else fix_index(start_idx - i)
        changsheng_12[idx] = t(key)

    return changsheng_12


def get_boshi_12(solar_date: str, gender: str) -> list[str]:
    gender_key = kot(gender)
    cfg = get_config()
    yearly = get_heavenly_stem_and_earthly_branch_by_solar_date(
        solar_date,
        0,
        {"year": cfg["year_divide"]},
    ).yearly

    heavenly_stem_name_of_year, earthly_branch_name_of_year = yearly
    earthly_branch_of_year_key = kot(earthly_branch_name_of_year, "Earthly")

    stars = (
        "boshi",
        "lishi",
        "qinglong",
        "xiaohao",
        "jiangjun",
        "zhoushu",
        "faylian",
        "xishen",
        "bingfu",
        "dahao",
        "fubing",
        "guanfu",
    )
    lu_index = get_lu_yang_tuo_ma_index(heavenly_stem_name_of_year, earthly_branch_name_of_year)["lu_index"]

    boshi12: list[str] = [""] * 12
    same_yinyang = GENDER[gender_key] == earthly_branches[earthly_branch_of_year_key]["yin_yang"]
    for i, key in enumerate(stars):
        idx = fix_index(lu_index + i) if same_yinyang else fix_index(lu_index - i)
        boshi12[idx] = t(key)

    return boshi12


def get_jiangqian_12_start_index(earthly_branch_name: str) -> int:
    earthly_branch_key = kot(earthly_branch_name, "Earthly")

    if earthly_branch_key in {"yinEarthly", "wuEarthly", "xuEarthly"}:
        return fix_index(fix_earthly_branch_index("woo"))
    if earthly_branch_key in {"shenEarthly", "ziEarthly", "chenEarthly"}:
        return fix_index(fix_earthly_branch_index("zi"))
    if earthly_branch_key in {"siEarthly", "youEarthly", "chouEarthly"}:
        return fix_index(fix_earthly_branch_index("you"))
    if earthly_branch_key in {"haiEarthly", "maoEarthly", "weiEarthly"}:
        return fix_index(fix_earthly_branch_index("mao"))

    return 0


def get_yearly_12(solar_date: str | object) -> dict[str, list[str]]:
    cfg = get_config()
    yearly = get_heavenly_stem_and_earthly_branch_by_solar_date(
        solar_date,
        0,
        {"year": cfg["horoscope_divide"]},
    ).yearly

    algorithm = cfg["algorithm"]
    suiqian_12: list[str] = [""] * 12
    jiangqian_12: list[str] = [""] * 12

    ts12shen = (
        (
            "suijian",
            "huiqi",
            "sangmen",
            "guansuo",
            "gwanfu",
            "xiaohao",
            "suipo",
            "longde",
            "baihu",
            "tiande",
            "diaoke",
            "bingfu",
        )
        if algorithm == "zhongzhou"
        else (
            "suijian",
            "huiqi",
            "sangmen",
            "guansuo",
            "gwanfu",
            "xiaohao",
            "dahao",
            "longde",
            "baihu",
            "tiande",
            "diaoke",
            "bingfu",
        )
    )

    for i, key in enumerate(ts12shen):
        idx = fix_index(fix_earthly_branch_index(yearly[1]) + i)
        suiqian_12[idx] = t(key)

    jq12shen = (
        "jiangxing",
        "panan",
        "suiyi",
        "xiishen",
        "huagai",
        "jiesha",
        "zhaisha",
        "tiansha",
        "zhibei",
        "xianchi",
        "yuesha",
        "wangshen",
    )
    jq_start = get_jiangqian_12_start_index(yearly[1])
    for i, key in enumerate(jq12shen):
        idx = fix_index(jq_start + i)
        jiangqian_12[idx] = t(key)

    return {"suiqian_12": suiqian_12, "jiangqian_12": jiangqian_12}
