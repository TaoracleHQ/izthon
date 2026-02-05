from __future__ import annotations

import pytest

from izthon.astro import by_solar


def test_get_palace_by_index_name_and_special_names():
    astrolabe = by_solar("2023-8-15", 0, "女", True)

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


def test_has_not_have_has_one_of_stars_in_palace():
    astrolabe = by_solar("2023-8-15", 0, "女", True)

    assert astrolabe.palace(1).has(["太阳"]) is False
    assert astrolabe.palace(1).has(["天相"]) is True
    assert astrolabe.palace(2).has(["天机", "天梁"]) is True
    assert astrolabe.palace(3).has(["紫微", "天梁"]) is False
    assert astrolabe.palace(4).has(["天喜", "天姚", "天官", "台辅"]) is True
    assert astrolabe.palace(7).has(["廉贞", "破军", "左辅", "火星"]) is True
    assert astrolabe.palace(9).has(["天府", "陀罗", "地空", "地劫", "天厨"]) is True

    assert astrolabe.palace("命宫").has(["武曲"]) is False
    assert astrolabe.palace("迁移").has(["武曲", "贪狼", "擎羊", "三台", "八座"]) is True
    assert astrolabe.palace("财帛").has(["天相"]) is True
    assert astrolabe.palace("子女").has(["天机", "天梁", "文曲", "天空", "阴煞"]) is True

    assert astrolabe.palace(1).not_have(["太阳"]) is True
    assert astrolabe.palace(1).not_have(["天相"]) is False

    assert astrolabe.palace(1).has_one_of(["太阳", "天相"]) is True
    assert astrolabe.palace(9).has_one_of(["太阳", "天梁", "天官", "天姚", "天厨"]) is True


def test_surrounded_palaces_have_and_deprecated_helpers():
    astrolabe = by_solar("2023-8-15", 0, "女", True)

    assert (
        astrolabe.surrounded_palaces("命宫").have(["武曲", "贪狼", "擎羊", "天相", "天魁", "天月", "地空", "地劫"])
        is True
    )
    assert astrolabe.is_surrounded("命宫", ["武曲", "贪狼", "擎羊", "天相", "天魁", "天月", "地空", "地劫"]) is True

    assert (
        astrolabe.surrounded_palaces("命宫").have(["武曲", "擎羊", "天相", "天魁", "天月", "地空", "地劫", "太阴"])
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


def test_surrounded_palaces_have_one_of_and_deprecated_helpers():
    astrolabe = by_solar("2023-8-16", 2, "女", True)

    assert astrolabe.surrounded_palaces("命宫").have_one_of(["太阳", "文曲"]) is True
    assert astrolabe.is_surrounded_one_of("命宫", ["太阳", "文曲"]) is True
    assert astrolabe.surrounded_palaces("命宫").have_one_of(["天喜", "天钺"]) is True
    assert astrolabe.surrounded_palaces("命宫").have_one_of(["天梁", "禄存"]) is True
    assert astrolabe.surrounded_palaces("命宫").have_one_of(["左辅", "右弼"]) is True
    assert astrolabe.surrounded_palaces("命宫").have_one_of(["地空", "地劫"]) is False

    assert astrolabe.surrounded_palaces(3).have_one_of(["武曲", "天马"]) is True
    assert astrolabe.surrounded_palaces(3).have_one_of(["火星", "贪狼"]) is True
    assert astrolabe.surrounded_palaces(3).have_one_of(["天空", "天官"]) is False


def test_surrounded_palaces_not_have_and_deprecated_helpers():
    astrolabe = by_solar("2023-8-16", 2, "女", True)

    assert astrolabe.surrounded_palaces("命宫").not_have(["太阳", "文曲"]) is False
    assert astrolabe.not_surrounded("命宫", ["太阳", "文曲"]) is False
    assert astrolabe.surrounded_palaces("命宫").not_have(["天喜", "天钺"]) is False
    assert astrolabe.surrounded_palaces("命宫").not_have(["天梁", "禄存"]) is False
    assert astrolabe.surrounded_palaces("命宫").not_have(["左辅", "右弼"]) is False
    assert astrolabe.surrounded_palaces("命宫").not_have(["地空", "地劫"]) is True

    assert astrolabe.surrounded_palaces(3).not_have(["武曲", "天马"]) is False
    assert astrolabe.surrounded_palaces(3).not_have(["火星", "贪狼"]) is False
    assert astrolabe.surrounded_palaces(3).not_have(["天魁", "天官"]) is True


def test_mutagen_and_star_helpers():
    astrolabe = by_solar("2013-8-21", 4, "女", True)

    assert astrolabe.palace("迁移").has_mutagen("禄") is True
    assert astrolabe.palace("兄弟").has_mutagen("权") is True
    assert astrolabe.palace("子女").has_mutagen("科") is True
    assert astrolabe.palace("夫妻").has_mutagen("忌") is True
    assert astrolabe.palace("命宫").has_mutagen("忌") is False

    assert astrolabe.palace("命宫").not_have_mutagen("忌") is True

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

    assert astrolabe.star("咸池").surrounded_palaces().target.name == "福德"
    assert astrolabe.star("咸池").surrounded_palaces().target.earthly_branch == "午"
    assert astrolabe.star("咸池").surrounded_palaces().have_mutagen("禄") is True
    assert astrolabe.star("左辅").surrounded_palaces().have_mutagen("忌") is True
    assert astrolabe.star("紫微").surrounded_palaces().have_mutagen("忌") is False
