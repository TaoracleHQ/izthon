from __future__ import annotations

import pytest

from izthon.astro import config
from izthon.i18n import set_language
from izthon.star import (
    get_adjective_star,
    get_boshi_12,
    get_changesheng_12_start_index,
    get_changsheng_12,
    get_horoscope_star,
    get_jiangqian12_start_index,
    get_major_star,
    get_minor_star,
    get_start_index,
    get_yearly_12,
)
from izthon.util import merge_stars


def test_get_start_index():
    cases = [
        (0, "2023-08-01", {"ziwei_index": 11, "tianfu_index": 1}),
        (1, "2023-08-01", {"ziwei_index": 11, "tianfu_index": 1}),
        (2, "2023-08-01", {"ziwei_index": 2, "tianfu_index": 10}),
        (3, "2023-08-01", {"ziwei_index": 2, "tianfu_index": 10}),
        (4, "2023-08-01", {"ziwei_index": 6, "tianfu_index": 6}),
        (5, "2023-08-01", {"ziwei_index": 6, "tianfu_index": 6}),
        (6, "2023-08-01", {"ziwei_index": 2, "tianfu_index": 10}),
        (7, "2023-08-01", {"ziwei_index": 2, "tianfu_index": 10}),
        (8, "2023-08-01", {"ziwei_index": 6, "tianfu_index": 6}),
        (9, "2023-08-01", {"ziwei_index": 6, "tianfu_index": 6}),
        (10, "2023-08-01", {"ziwei_index": 4, "tianfu_index": 8}),
        (11, "2023-08-01", {"ziwei_index": 4, "tianfu_index": 8}),
        (12, "2023-08-01", {"ziwei_index": 4, "tianfu_index": 8}),
        (12, "2023-02-19", {"ziwei_index": 11, "tianfu_index": 1}),
    ]
    for time_index, solar_date, expected in cases:
        assert get_start_index({"solar_date": solar_date, "time_index": time_index, "fix_leap": True}) == expected


def _dump_star_props(stars):
    return [
        [
            {
                "name": s.name,
                "type": s.type,
                "scope": s.scope,
                "brightness": s.brightness,
                "mutagen": s.mutagen or "",
            }
            for s in group
        ]
        for group in stars
    ]


def test_get_major_star():
    config({"year_divide": "exact"})
    res = get_major_star({"solar_date": "2023-03-06", "time_index": 4, "fix_leap": True})
    assert _dump_star_props(res) == [
        [{"name": "七杀", "type": "major", "brightness": "庙", "scope": "origin", "mutagen": ""}],
        [{"name": "天同", "type": "major", "brightness": "平", "scope": "origin", "mutagen": ""}],
        [{"name": "武曲", "type": "major", "brightness": "庙", "scope": "origin", "mutagen": ""}],
        [{"name": "太阳", "type": "major", "brightness": "旺", "scope": "origin", "mutagen": ""}],
        [{"name": "破军", "type": "major", "brightness": "庙", "scope": "origin", "mutagen": "禄"}],
        [{"name": "天机", "type": "major", "brightness": "陷", "scope": "origin", "mutagen": ""}],
        [
            {"name": "紫微", "type": "major", "brightness": "旺", "scope": "origin", "mutagen": ""},
            {"name": "天府", "type": "major", "brightness": "得", "scope": "origin", "mutagen": ""},
        ],
        [{"name": "太阴", "type": "major", "brightness": "不", "scope": "origin", "mutagen": "科"}],
        [{"name": "贪狼", "type": "major", "brightness": "庙", "scope": "origin", "mutagen": "忌"}],
        [{"name": "巨门", "type": "major", "brightness": "旺", "scope": "origin", "mutagen": "权"}],
        [
            {"name": "廉贞", "type": "major", "brightness": "平", "scope": "origin", "mutagen": ""},
            {"name": "天相", "type": "major", "brightness": "庙", "scope": "origin", "mutagen": ""},
        ],
        [{"name": "天梁", "type": "major", "brightness": "旺", "scope": "origin", "mutagen": ""}],
    ]


def test_get_major_star_vi_vn():
    set_language("vi-VN")
    config({"year_divide": "exact"})
    res = get_major_star({"solar_date": "2023-03-06", "time_index": 4, "fix_leap": True})
    assert _dump_star_props(res) == [
        [{"name": "Thất Sát", "type": "major", "brightness": "Miếu", "scope": "origin", "mutagen": ""}],
        [{"name": "Thiên Đồng", "type": "major", "brightness": "Bình", "scope": "origin", "mutagen": ""}],
        [{"name": "Vũ Khúc", "type": "major", "brightness": "Miếu", "scope": "origin", "mutagen": ""}],
        [{"name": "Thái Dương", "type": "major", "brightness": "Vượng", "scope": "origin", "mutagen": ""}],
        [{"name": "Phá Quân", "type": "major", "brightness": "Miếu", "scope": "origin", "mutagen": "Lộc"}],
        [{"name": "Thiên Cơ", "type": "major", "brightness": "Hạn", "scope": "origin", "mutagen": ""}],
        [
            {"name": "Tử Vi", "type": "major", "brightness": "Vượng", "scope": "origin", "mutagen": ""},
            {"name": "Thiên Phủ", "type": "major", "brightness": "Đắc", "scope": "origin", "mutagen": ""},
        ],
        [{"name": "Thái Âm", "type": "major", "brightness": "Bất", "scope": "origin", "mutagen": "Khoa"}],
        [{"name": "Tham Lang", "type": "major", "brightness": "Miếu", "scope": "origin", "mutagen": "Kỵ"}],
        [{"name": "Cự Môn", "type": "major", "brightness": "Vượng", "scope": "origin", "mutagen": "Quyền"}],
        [
            {"name": "Liêm Trinh", "type": "major", "brightness": "Bình", "scope": "origin", "mutagen": ""},
            {"name": "Thiên Tướng", "type": "major", "brightness": "Miếu", "scope": "origin", "mutagen": ""},
        ],
        [{"name": "Thiên Lương", "type": "major", "brightness": "Vượng", "scope": "origin", "mutagen": ""}],
    ]


def test_star_total_count():
    primary = get_major_star({"solar_date": "2023-03-06", "time_index": 2, "fix_leap": True})
    secondary = get_minor_star("2023-03-06", 2, True)
    other = get_adjective_star({"solar_date": "2023-03-06", "time_index": 2, "fix_leap": True, "gender": "女"})
    merged = merge_stars(primary, other, secondary)
    total = sum(len(x) for x in merged)
    assert len(merged) == 12
    assert total == 66


def test_get_changsheng_12():
    assert get_changsheng_12({"solar_date": "2023-8-15", "time_index": 0, "gender": "女", "fix_leap": True}) == [
        "长生",
        "沐浴",
        "冠带",
        "临官",
        "帝旺",
        "衰",
        "病",
        "死",
        "墓",
        "绝",
        "胎",
        "养",
    ]

    assert get_changsheng_12({"solar_date": "1999-5-3", "time_index": 8, "gender": "女", "fix_leap": True}) == [
        "绝",
        "胎",
        "养",
        "长生",
        "沐浴",
        "冠带",
        "临官",
        "帝旺",
        "衰",
        "病",
        "死",
        "墓",
    ]

    assert get_changsheng_12(
        {
            "solar_date": "1999-5-3",
            "time_index": 8,
            "gender": "男",
            "fix_leap": True,
            "from_": {"heavenly_stem": "丙", "earthly_branch": "子"},
        }
    ) == ["病", "衰", "帝旺", "临官", "冠带", "沐浴", "长生", "养", "胎", "绝", "墓", "死"]

    assert get_changsheng_12(
        {
            "solar_date": "1999-5-3",
            "time_index": 8,
            "gender": "女",
            "fix_leap": True,
            "from_": {"heavenly_stem": "丙", "earthly_branch": "子"},
        }
    ) == ["病", "死", "墓", "绝", "胎", "养", "长生", "沐浴", "冠带", "临官", "帝旺", "衰"]


def test_get_changsheng_12_vi_vn():
    set_language("vi-VN")
    assert get_changsheng_12({"solar_date": "2023-8-15", "time_index": 0, "gender": "女", "fix_leap": True}) == [
        "Trường Sinh",
        "Mục Dục",
        "Quan Đới",
        "Lâm Quan",
        "Đế Vượng",
        "Suy",
        "Bệnh",
        "Tử",
        "Mộ",
        "Tuyệt",
        "Thai",
        "Dưỡng",
    ]


def test_get_boshi_12():
    assert get_boshi_12("2023-8-15", "女") == [
        "青龙",
        "小耗",
        "将军",
        "奏书",
        "飞廉",
        "喜神",
        "病符",
        "大耗",
        "伏兵",
        "官府",
        "博士",
        "力士",
    ]


def test_get_yearly_12():
    assert get_yearly_12("2025-8-15") == {
        "suiqian12": ["天德", "吊客", "病符", "岁建", "晦气", "丧门", "贯索", "官符", "小耗", "大耗", "龙德", "白虎"],
        "jiangqian12": ["劫煞", "灾煞", "天煞", "指背", "咸池", "月煞", "亡神", "将星", "攀鞍", "岁驿", "息神", "华盖"],
    }


def test_get_horoscope_star_decadal():
    stars = get_horoscope_star("庚", "辰", "decadal")
    dumped = [[{"name": s.name, "type": s.type, "scope": s.scope} for s in group] for group in stars]
    assert dumped == [
        [{"name": "运马", "type": "tianma", "scope": "decadal"}],
        [{"name": "运曲", "type": "soft", "scope": "decadal"}],
        [],
        [{"name": "运喜", "type": "flower", "scope": "decadal"}],
        [],
        [
            {"name": "运钺", "type": "soft", "scope": "decadal"},
            {"name": "运陀", "type": "tough", "scope": "decadal"},
        ],
        [{"name": "运禄", "type": "lucun", "scope": "decadal"}],
        [{"name": "运羊", "type": "tough", "scope": "decadal"}],
        [],
        [
            {"name": "运昌", "type": "soft", "scope": "decadal"},
            {"name": "运鸾", "type": "flower", "scope": "decadal"},
        ],
        [],
        [{"name": "运魁", "type": "soft", "scope": "decadal"}],
    ]


def test_get_horoscope_star_yearly():
    stars = get_horoscope_star("癸", "卯", "yearly")
    dumped = [[{"name": s.name, "type": s.type, "scope": s.scope} for s in group] for group in stars]
    assert dumped == [
        [],
        [
            {"name": "流魁", "type": "soft", "scope": "yearly"},
            {"name": "流昌", "type": "soft", "scope": "yearly"},
        ],
        [],
        [
            {"name": "流钺", "type": "soft", "scope": "yearly"},
            {"name": "流马", "type": "tianma", "scope": "yearly"},
        ],
        [{"name": "流喜", "type": "flower", "scope": "yearly"}],
        [{"name": "年解", "type": "helper", "scope": "yearly"}],
        [],
        [],
        [],
        [
            {"name": "流曲", "type": "soft", "scope": "yearly"},
            {"name": "流陀", "type": "tough", "scope": "yearly"},
        ],
        [
            {"name": "流禄", "type": "lucun", "scope": "yearly"},
            {"name": "流鸾", "type": "flower", "scope": "yearly"},
        ],
        [{"name": "流羊", "type": "tough", "scope": "yearly"}],
    ]


def test_get_changesheng_12_start_index():
    cases = {"水二局": 6, "木三局": 9, "金四局": 3, "土五局": 6, "火六局": 0}
    for k, v in cases.items():
        assert get_changesheng_12_start_index(k) == v


def test_get_jiangqian12_start_index():
    cases = {
        "yin": 4,
        "woo": 4,
        "xu": 4,
        "shen": 10,
        "zi": 10,
        "chen": 10,
        "si": 7,
        "you": 7,
        "chou": 7,
        "hai": 1,
        "mao": 1,
        "wei": 1,
    }
    for k, v in cases.items():
        assert get_jiangqian12_start_index(k) == v


def test_get_adjective_star_algorithm_switch():
    data = get_adjective_star({"solar_date": "2001-08-16", "time_index": 2, "gender": "男"})

    def _has(star_name: str) -> bool:
        return any(any(s.name == star_name for s in group) for group in data)

    # default algorithm: no 截空/劫杀/大耗, but has 截路/年解
    assert _has("截空") is False
    assert _has("劫杀") is False
    assert _has("大耗") is False
    assert _has("截路") is True
    assert _has("年解") is True

    # check tianshi/tianshang positions
    for idx, group in enumerate(data):
        for s in group:
            if s.name == "天使":
                assert idx == 10
            if s.name == "天伤":
                assert idx == 8

    config({"algorithm": "zhongzhou"})
    data2 = get_adjective_star({"solar_date": "2001-08-16", "time_index": 2, "gender": "男"})

    def _has2(star_name: str) -> bool:
        return any(any(s.name == star_name for s in group) for group in data2)

    assert _has2("截空") is True
    assert _has2("劫杀") is True
    assert _has2("截路") is False
    assert _has2("年解") is True
    assert _has2("大耗") is True

    for idx, group in enumerate(data2):
        for s in group:
            if s.name == "天使":
                assert idx == 8
            if s.name == "天伤":
                assert idx == 10

