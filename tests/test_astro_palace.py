from __future__ import annotations

from izthon.astro import by_solar, set_config, get_five_elements_class, get_horoscope, get_palace_names, get_soul_and_body


def test_get_soul_and_body():
    set_config({"year_divide": "exact"})

    cases = [
        (
            "2023-1-22",
            5,
            {"soul_index": 7, "body_index": 5, "heavenly_stem_of_soul": "己", "earthly_branch_of_soul": "酉"},
        ),
        (
            "2023-1-22",
            6,
            {"soul_index": 6, "body_index": 6, "heavenly_stem_of_soul": "戊", "earthly_branch_of_soul": "申"},
        ),
        (
            "2023-2-19",
            12,
            {"soul_index": 0, "body_index": 0, "heavenly_stem_of_soul": "甲", "earthly_branch_of_soul": "寅"},
        ),
    ]

    for date_str, time_index, expected in cases:
        sb = get_soul_and_body(solar_date=date_str, time_index=time_index)
        assert sb.soul_index == expected["soul_index"]
        assert sb.body_index == expected["body_index"]
        assert sb.heavenly_stem_of_soul == expected["heavenly_stem_of_soul"]
        assert sb.earthly_branch_of_soul == expected["earthly_branch_of_soul"]


def test_get_five_elements_class():
    assert get_five_elements_class("庚", "申") == "木三局"
    assert get_five_elements_class("己", "未") == "火六局"
    assert get_five_elements_class("戊", "午") == "火六局"
    assert get_five_elements_class("丁", "巳") == "土五局"
    assert get_five_elements_class("丙", "辰") == "土五局"
    assert get_five_elements_class("乙", "卯") == "水二局"
    assert get_five_elements_class("甲", "寅") == "水二局"
    assert get_five_elements_class("乙", "丑") == "金四局"
    assert get_five_elements_class("甲", "子") == "金四局"
    assert get_five_elements_class("癸", "亥") == "水二局"
    assert get_five_elements_class("壬", "戌") == "水二局"
    assert get_five_elements_class("辛", "酉") == "木三局"


def test_get_palace_names_rotate():
    target = ["兄弟", "命宫", "父母", "福德", "田宅", "官禄", "仆役", "迁移", "疾厄", "财帛", "子女", "夫妻"]
    assert get_palace_names(1) == target
    assert get_palace_names(13) == target
    assert get_palace_names(-11) == target


def test_get_horoscope_ages_for_female():
    decadals, ages = get_horoscope(solar_date="2023-11-15", time_index=3, gender="女")
    _ = decadals  # not asserted; smoke only

    assert ages == [
        [12, 24, 36, 48, 60, 72, 84, 96, 108, 120],
        [11, 23, 35, 47, 59, 71, 83, 95, 107, 119],
        [10, 22, 34, 46, 58, 70, 82, 94, 106, 118],
        [9, 21, 33, 45, 57, 69, 81, 93, 105, 117],
        [8, 20, 32, 44, 56, 68, 80, 92, 104, 116],
        [7, 19, 31, 43, 55, 67, 79, 91, 103, 115],
        [6, 18, 30, 42, 54, 66, 78, 90, 102, 114],
        [5, 17, 29, 41, 53, 65, 77, 89, 101, 113],
        [4, 16, 28, 40, 52, 64, 76, 88, 100, 112],
        [3, 15, 27, 39, 51, 63, 75, 87, 99, 111],
        [2, 14, 26, 38, 50, 62, 74, 86, 98, 110],
        [1, 13, 25, 37, 49, 61, 73, 85, 97, 109],
    ]


def test_get_horoscope_ages_for_male():
    decadals, ages = get_horoscope(solar_date="2023-11-15", time_index=3, gender="男")
    _ = decadals  # not asserted; smoke only

    assert ages == [
        [2, 14, 26, 38, 50, 62, 74, 86, 98, 110],
        [3, 15, 27, 39, 51, 63, 75, 87, 99, 111],
        [4, 16, 28, 40, 52, 64, 76, 88, 100, 112],
        [5, 17, 29, 41, 53, 65, 77, 89, 101, 113],
        [6, 18, 30, 42, 54, 66, 78, 90, 102, 114],
        [7, 19, 31, 43, 55, 67, 79, 91, 103, 115],
        [8, 20, 32, 44, 56, 68, 80, 92, 104, 116],
        [9, 21, 33, 45, 57, 69, 81, 93, 105, 117],
        [10, 22, 34, 46, 58, 70, 82, 94, 106, 118],
        [11, 23, 35, 47, 59, 71, 83, 95, 107, 119],
        [12, 24, 36, 48, 60, 72, 84, 96, 108, 120],
        [1, 13, 25, 37, 49, 61, 73, 85, 97, 109],
    ]


def test_palace_mutagen_and_flying_helpers():
    astrolabe = by_solar("2017-12-4", 12, "male")

    assert astrolabe.palace("命宫").flies_to("兄弟", "忌") is True
    assert astrolabe.palace("命宫").not_fly_to("兄弟", "科") is True
    assert astrolabe.palace("田宅").flies_to("福德", ["禄", "科"]) is True
    assert astrolabe.palace("田宅").not_fly_to("福德", ["禄", "科"]) is False
    assert astrolabe.palace("兄弟").flies_to("夫妻", ["权", "科"]) is False
    assert astrolabe.palace("兄弟").flies_one_of_to("夫妻", ["权", "科"]) is True
    assert astrolabe.palace("兄弟").flies_one_of_to("夫妻", ["权", "禄"]) is False
    assert astrolabe.palace("兄弟").not_fly_to("夫妻", ["权", "科"]) is False

    assert astrolabe.palace("仆役").self_mutaged("科") is True
    assert astrolabe.palace("仆役").self_mutaged(["科", "权"]) is False
    assert astrolabe.palace("仆役").self_mutaged_one_of(["科", "权"]) is True
    assert astrolabe.palace("仆役").self_mutaged_one_of() is True
    assert astrolabe.palace("仆役").self_mutaged("权") is False
    assert astrolabe.palace("仆役").not_self_mutaged() is False
    assert astrolabe.palace("仆役").not_self_mutaged("权") is True
    assert astrolabe.palace("仆役").not_self_mutaged(["权", "科"]) is False

    palaces = astrolabe.palace("命宫").mutaged_places()
    assert len(palaces) == 4
    assert palaces[0].name == "命宫"
    assert palaces[1].name == "迁移"
    assert palaces[2].name == "仆役"
    assert palaces[3].name == "兄弟"
