from __future__ import annotations

import pytest

from izthon.astro import by_solar


def test_get_palace_by_index_name_and_special_names():
    astrolabe = by_solar("2023-8-15", 0, "女", fix_leap=True)

    palace_names = [
        "疾厄",
        "财帛",
        "子女",
        "夫妻",
        "兄弟",
        "命宫",
        "父母",
        "福德",
        "田宅",
        "官禄",
        "仆役",
        "迁移",
    ]

    for idx, name in enumerate(palace_names):
        assert astrolabe.palace(idx).name == name
        assert astrolabe.palace(name).name == name

    assert astrolabe.palace("来因").name == "官禄"
    assert astrolabe.palace("身宫").name == "命宫"

    with pytest.raises(ValueError) as exc:
        astrolabe.palace(-1)
    assert str(exc.value) == "invalid palace index."

    with pytest.raises(ValueError) as exc:
        astrolabe.palace(12)
    assert str(exc.value) == "invalid palace index."

    with pytest.raises(ValueError) as exc:
        astrolabe.palace("不存在")
    assert str(exc.value) == "invalid palace name."


def test_has_not_have_has_one_of_stars_in_palace():
    astrolabe = by_solar("2023-8-15", 0, "女", fix_leap=True)

    assert astrolabe.palace(1).contains_stars(["太阳"]) is False
    assert astrolabe.palace(1).contains_stars(["天相"]) is True
    assert astrolabe.palace(2).contains_stars(["天机", "天梁"]) is True
    assert astrolabe.palace(3).contains_stars(["紫微", "天梁"]) is False
    assert astrolabe.palace(4).contains_stars(["天喜", "天姚", "天官", "台辅"]) is True
    assert astrolabe.palace(7).contains_stars(["廉贞", "破军", "左辅", "火星"]) is True
    assert astrolabe.palace(9).contains_stars(["天府", "陀罗", "地空", "地劫", "天厨"]) is True

    assert astrolabe.palace("命宫").contains_stars(["武曲"]) is False
    assert astrolabe.palace("迁移").contains_stars(["武曲", "贪狼", "擎羊", "三台", "八座"]) is True
    assert astrolabe.palace("财帛").contains_stars(["天相"]) is True
    assert astrolabe.palace("子女").contains_stars(["天机", "天梁", "文曲", "天空", "阴煞"]) is True

    assert astrolabe.palace(1).excludes_stars(["太阳"]) is True
    assert astrolabe.palace(1).excludes_stars(["天相"]) is False
    assert astrolabe.palace(2).excludes_stars(["天机", "天梁"]) is False
    assert astrolabe.palace(3).excludes_stars(["紫微", "天梁"]) is False
    assert astrolabe.palace(4).excludes_stars(["天喜", "天姚", "天官", "台辅"]) is False
    assert astrolabe.palace(7).excludes_stars(["廉贞", "破军", "左辅", "火星"]) is False
    assert astrolabe.palace(9).excludes_stars(["天府", "陀罗", "地空", "地劫", "天厨"]) is False

    assert astrolabe.palace("命宫").excludes_stars(["武曲"]) is True
    assert astrolabe.palace("迁移").excludes_stars(["武曲", "贪狼", "擎羊", "三台", "八座"]) is False
    assert astrolabe.palace("财帛").excludes_stars(["天相"]) is False
    assert astrolabe.palace("子女").excludes_stars(["天机", "天梁", "文曲", "天空", "阴煞"]) is False

    assert astrolabe.palace(1).contains_any_star(["太阳", "天相"]) is True
    assert astrolabe.palace(2).contains_any_star(["天机", "天梁"]) is True
    assert astrolabe.palace(3).contains_any_star(["紫微", "天梁"]) is True
    assert astrolabe.palace(7).contains_any_star(["天喜", "天姚", "天官", "台辅"]) is False
    assert astrolabe.palace(9).contains_any_star(["太阳", "天梁", "天官", "天姚", "天厨"]) is True
    assert astrolabe.palace("命宫").contains_any_star(["武曲", "天贵"]) is True
    assert astrolabe.palace("父母").contains_any_star(["月德", "天巫", "巨门"]) is True


def test_surrounded_palaces_contains_stars():
    astrolabe = by_solar("2023-8-15", 0, "女", fix_leap=True)

    assert (
        astrolabe.surrounded_palaces("命宫").contains_stars(["武曲", "贪狼", "擎羊", "天相", "天魁", "天月", "地空", "地劫"])
        is True
    )
    assert (
        astrolabe.surrounded_palaces("命宫").contains_stars(["武曲", "擎羊", "天相", "天魁", "天月", "地空", "地劫", "太阴"])
        is False
    )
    assert (
        astrolabe.surrounded_palaces("命宫").contains_stars(
            ["太阳", "巨门", "月德", "天巫", "天喜", "天姚", "天官", "台辅", "文昌", "铃星", "天才", "天寿", "天刑", "天使", "封诰"]
        )
        is False
    )
    assert (
        astrolabe.surrounded_palaces("命宫").contains_stars(
            [
                "天机",
                "天梁",
                "文曲",
                "天空",
                "阴煞",
                "旬空",
                "文昌",
                "铃星",
                "天才",
                "天寿",
                "月德",
                "天巫",
                "天同",
                "太阴",
                "禄存",
                "解神",
                "红鸾",
                "咸池",
                "天伤",
                "天德",
                "截空",
            ]
        )
        is False
    )

    sp0 = astrolabe.surrounded_palaces(0)
    assert sp0.target.name == "疾厄"
    assert sp0.opposite.name == "父母"
    assert sp0.wealth.name == "田宅"
    assert sp0.career.name == "兄弟"

    sp = astrolabe.surrounded_palaces("命宫")
    assert sp.target.name == "命宫"
    assert sp.opposite.name == "迁移"
    assert sp.wealth.name == "财帛"
    assert sp.career.name == "官禄"


def test_surrounded_palaces_contains_any_star():
    astrolabe = by_solar("2023-8-16", 2, "女", fix_leap=True)

    assert astrolabe.surrounded_palaces("命宫").contains_any_star(["太阳", "文曲"]) is True
    assert astrolabe.surrounded_palaces("命宫").contains_any_star(["天喜", "天钺"]) is True
    assert astrolabe.surrounded_palaces("命宫").contains_any_star(["天梁", "禄存"]) is True
    assert astrolabe.surrounded_palaces("命宫").contains_any_star(["左辅", "右弼"]) is True
    assert astrolabe.surrounded_palaces("命宫").contains_any_star(["地空", "地劫"]) is False

    assert astrolabe.surrounded_palaces(3).contains_any_star(["武曲", "天马"]) is True
    assert astrolabe.surrounded_palaces(3).contains_any_star(["火星", "贪狼"]) is True
    assert astrolabe.surrounded_palaces(3).contains_any_star(["天空", "天官"]) is False


def test_surrounded_palaces_excludes_stars():
    astrolabe = by_solar("2023-8-16", 2, "女", fix_leap=True)

    assert astrolabe.surrounded_palaces("命宫").excludes_stars(["太阳", "文曲"]) is False
    assert astrolabe.surrounded_palaces("命宫").excludes_stars(["天喜", "天钺"]) is False
    assert astrolabe.surrounded_palaces("命宫").excludes_stars(["天梁", "禄存"]) is False
    assert astrolabe.surrounded_palaces("命宫").excludes_stars(["左辅", "右弼"]) is False
    assert astrolabe.surrounded_palaces("命宫").excludes_stars(["地空", "地劫"]) is True

    assert astrolabe.surrounded_palaces(3).excludes_stars(["武曲", "天马"]) is False
    assert astrolabe.surrounded_palaces(3).excludes_stars(["火星", "贪狼"]) is False
    assert astrolabe.surrounded_palaces(3).excludes_stars(["天魁", "天官"]) is True


def test_mutagen_and_star_helpers():
    astrolabe = by_solar("2013-8-21", 4, "女", fix_leap=True)

    assert astrolabe.palace("迁移").contains_mutagen("禄") is True
    assert astrolabe.palace("兄弟").contains_mutagen("权") is True
    assert astrolabe.palace("子女").contains_mutagen("科") is True
    assert astrolabe.palace("夫妻").contains_mutagen("忌") is True
    assert astrolabe.palace("命宫").contains_mutagen("忌") is False

    assert astrolabe.palace("迁移").lacks_mutagen("禄") is False
    assert astrolabe.palace("兄弟").lacks_mutagen("权") is False
    assert astrolabe.palace("子女").lacks_mutagen("科") is False
    assert astrolabe.palace("夫妻").lacks_mutagen("忌") is False
    assert astrolabe.palace("命宫").lacks_mutagen("忌") is True

    assert astrolabe.surrounded_palaces("命宫").opposite.contains_mutagen("禄") is True
    assert astrolabe.surrounded_palaces("官禄").opposite.contains_mutagen("忌") is True
    assert astrolabe.surrounded_palaces("仆役").opposite.contains_mutagen("权") is True
    assert astrolabe.surrounded_palaces("田宅").opposite.contains_mutagen("科") is True
    assert astrolabe.surrounded_palaces("福德").opposite.contains_mutagen("科") is False

    assert astrolabe.surrounded_palaces("福德").contains_mutagen("禄") is True
    assert astrolabe.surrounded_palaces("福德").contains_mutagen("忌") is True
    assert astrolabe.surrounded_palaces("迁移").contains_mutagen("禄") is True
    assert astrolabe.surrounded_palaces("迁移").contains_mutagen("忌") is True
    assert astrolabe.surrounded_palaces("疾厄").contains_mutagen("权") is True
    assert astrolabe.surrounded_palaces("财帛").contains_mutagen("科") is False
    assert astrolabe.surrounded_palaces("身宫").contains_mutagen("忌") is False

    # FunctionalStar helpers.
    assert astrolabe.star("紫微").with_mutagen("禄") is False
    assert astrolabe.star("破军").with_mutagen("禄") is True
    assert astrolabe.star("巨门").with_mutagen("权") is True
    assert astrolabe.star("太阴").with_mutagen("科") is True
    assert astrolabe.star("贪狼").with_mutagen("忌") is True
    assert astrolabe.star("贪狼").with_mutagen(["忌", "权"]) is True
    assert astrolabe.star("贪狼").with_mutagen(["科", "权"]) is False

    assert astrolabe.star("紫微").with_brightness("庙") is False
    assert astrolabe.star("紫微").with_brightness(["庙", "得"]) is True
    assert astrolabe.star("巨门").with_brightness("庙") is True
    assert astrolabe.star("太阴").with_brightness(["不", "陷"]) is False
    assert astrolabe.star("贪狼").with_brightness("平") is True

    assert astrolabe.star("紫微").opposite_palace().name == "迁移"
    assert astrolabe.star("天同").opposite_palace().name == "父母"
    assert astrolabe.star("巨门").opposite_palace().name == "仆役"
    assert astrolabe.star("太阴").opposite_palace().name == "田宅"
    assert astrolabe.star("贪狼").opposite_palace().name == "官禄"
    assert astrolabe.star("廉贞").opposite_palace().contains_mutagen("忌") is True
    assert astrolabe.star("天相").opposite_palace().contains_mutagen("禄") is True
    assert astrolabe.star("火星").opposite_palace().contains_mutagen("科") is True
    assert astrolabe.star("天才").opposite_palace().contains_mutagen("权") is True
    assert astrolabe.star("文昌").opposite_palace().contains_mutagen("禄") is False

    assert astrolabe.star("咸池").surrounded_palaces().target.name == "福德"
    assert astrolabe.star("咸池").surrounded_palaces().target.earthly_branch == "午"
    assert astrolabe.star("咸池").surrounded_palaces().contains_mutagen("禄") is True
    assert astrolabe.star("左辅").surrounded_palaces().contains_mutagen("忌") is True
    assert astrolabe.star("紫微").surrounded_palaces().contains_mutagen("忌") is False
