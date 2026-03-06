from __future__ import annotations

import importlib

from .functional_star import FunctionalStar


def init_stars() -> list[list[FunctionalStar]]:
    """Create a 12-palace star container (palaces are ordered from Yin palace)."""
    return [[] for _ in range(12)]


_LAZY_ATTRS: dict[str, str] = {
    # location helpers
    "get_start_index": "location",
    "get_lu_yang_tuo_ma_index": "location",
    "get_kui_yue_index": "location",
    "get_zuo_you_index": "location",
    "get_chang_qu_index": "location",
    "get_daily_star_index": "location",
    "get_timely_star_index": "location",
    "get_kong_jie_index": "location",
    "get_huo_ling_index": "location",
    "get_luan_xi_index": "location",
    "get_huagai_xianchi_index": "location",
    "get_gu_gua_index": "location",
    "get_yearly_star_index": "location",
    "get_tianshi_tianshang_index": "location",
    "get_nianjie_index": "location",
    "get_monthly_star_index": "location",
    "get_chang_qu_index_by_heavenly_stem": "location",
    "get_jiesha_adj_index": "location",
    "get_dahao_index": "location",
    # star groups
    "get_major_star": "major_star",
    "get_minor_star": "minor_star",
    "get_adjective_star": "adjective_star",
    # decorative / yearly helpers
    "get_changsheng_12_start_index": "decorative_star",
    "get_jiangqian_12_start_index": "decorative_star",
    "get_changsheng_12": "decorative_star",
    "get_boshi_12": "decorative_star",
    "get_yearly_12": "decorative_star",
    # horoscope
    "get_horoscope_star": "horoscope_star",
}


def __getattr__(name: str):
    mod_name = _LAZY_ATTRS.get(name)
    if not mod_name:
        raise AttributeError(name)
    mod = importlib.import_module(f"{__name__}.{mod_name}")
    return getattr(mod, name)


__all__ = [
    "FunctionalStar",
    "init_stars",
    # location helpers
    "get_start_index",
    "get_lu_yang_tuo_ma_index",
    "get_kui_yue_index",
    "get_zuo_you_index",
    "get_chang_qu_index",
    "get_daily_star_index",
    "get_timely_star_index",
    "get_kong_jie_index",
    "get_huo_ling_index",
    "get_luan_xi_index",
    "get_huagai_xianchi_index",
    "get_gu_gua_index",
    "get_yearly_star_index",
    "get_tianshi_tianshang_index",
    "get_nianjie_index",
    "get_monthly_star_index",
    "get_chang_qu_index_by_heavenly_stem",
    "get_jiesha_adj_index",
    "get_dahao_index",
    # star groups
    "get_major_star",
    "get_minor_star",
    "get_adjective_star",
    # decorative
    "get_changsheng_12_start_index",
    "get_jiangqian_12_start_index",
    "get_changsheng_12",
    "get_boshi_12",
    "get_yearly_12",
    # horoscope
    "get_horoscope_star",
]
