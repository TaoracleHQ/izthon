from __future__ import annotations

import pytest

from izthon.astro import (
    by_lunar,
    by_solar,
    set_config,
    get_major_star_by_lunar_date,
    get_major_star_by_solar_date,
    get_sign_by_lunar_date,
    get_sign_by_solar_date,
    get_zodiac_by_solar_date,
)


def _dump_horoscope_stars(stars):
    return [[{"name": s.name, "type": s.type, "scope": s.scope} for s in group] for group in (stars or [])]


def test_by_solar_basic_and_horoscope_queries():
    # Match iztro upstream test cases (`src/__tests__/astro/astro.test.ts`).
    set_config({"year_divide": "exact", "algorithm": "default"})
    astrolabe = by_solar("2000-8-16", 2, "女", fix_leap=True)

    assert astrolabe.solar_date == "2000-8-16"
    assert astrolabe.lunar_date == "二〇〇〇年七月十七"
    assert astrolabe.chinese_date == "庚辰 甲申 丙午 庚寅"
    assert astrolabe.time == "寅时"
    assert astrolabe.sign == "狮子座"
    assert astrolabe.zodiac == "龙"
    assert astrolabe.earthly_branch_of_soul_palace == "午"
    assert astrolabe.earthly_branch_of_body_palace == "戌"
    assert astrolabe.soul == "破军"
    assert astrolabe.body == "文昌"
    assert astrolabe.five_elements_class == "木三局"

    assert astrolabe.palace("父母").is_empty() is True
    assert astrolabe.palace("父母").is_empty(["陀罗"]) is False
    assert astrolabe.palace("命宫").is_empty() is False
    assert astrolabe.palace("父母").is_empty(["文昌", "文曲"]) is True

    horoscope = astrolabe.horoscope("2023-8-19 3:12")

    assert horoscope.solar_date == "2023-8-19"
    assert horoscope.decadal.index == 2
    assert horoscope.decadal.heavenly_stem == "庚"
    assert horoscope.decadal.earthly_branch == "辰"
    assert horoscope.decadal.palace_names == [
        "夫妻",
        "兄弟",
        "命宫",
        "父母",
        "福德",
        "田宅",
        "官禄",
        "仆役",
        "迁移",
        "疾厄",
        "财帛",
        "子女",
    ]
    assert horoscope.decadal.mutagen == ["太阳", "武曲", "太阴", "天同"]
    assert horoscope.age.index == 9
    assert horoscope.age.nominal_age == 24

    assert horoscope.yearly.index == 1
    assert horoscope.yearly.heavenly_stem == "癸"
    assert horoscope.yearly.earthly_branch == "卯"
    assert horoscope.yearly.palace_names == [
        "兄弟",
        "命宫",
        "父母",
        "福德",
        "田宅",
        "官禄",
        "仆役",
        "迁移",
        "疾厄",
        "财帛",
        "子女",
        "夫妻",
    ]
    assert horoscope.yearly.mutagen == ["破军", "巨门", "太阴", "贪狼"]

    assert horoscope.monthly.index == 3
    assert horoscope.monthly.heavenly_stem == "庚"
    assert horoscope.monthly.earthly_branch == "申"
    assert horoscope.monthly.palace_names == [
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
        "疾厄",
        "财帛",
    ]
    assert horoscope.monthly.mutagen == ["太阳", "武曲", "太阴", "天同"]

    assert horoscope.daily.index == 6
    assert horoscope.daily.heavenly_stem == "己"
    assert horoscope.daily.earthly_branch == "酉"
    assert horoscope.daily.palace_names == [
        "迁移",
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
    ]
    assert horoscope.daily.mutagen == ["武曲", "贪狼", "天梁", "文曲"]

    assert horoscope.hourly.index == 8
    assert horoscope.hourly.heavenly_stem == "丙"
    assert horoscope.hourly.earthly_branch == "寅"
    assert horoscope.hourly.palace_names == [
        "官禄",
        "仆役",
        "迁移",
        "疾厄",
        "财帛",
        "子女",
        "夫妻",
        "兄弟",
        "命宫",
        "父母",
        "福德",
        "田宅",
    ]
    assert horoscope.hourly.mutagen == ["天同", "天机", "文昌", "廉贞"]

    assert horoscope.has_horoscope_stars("疾厄", "decadal", ["流陀", "流曲", "运昌"]) is True
    assert horoscope.has_horoscope_stars("财帛", "yearly", ["流陀", "流曲", "运昌"]) is True
    assert horoscope.has_horoscope_stars("迁移", "monthly", ["流陀", "流曲", "运昌"]) is True
    assert horoscope.has_horoscope_stars("田宅", "daily", ["流陀", "流曲", "运昌"]) is True
    assert horoscope.lacks_horoscope_stars("疾厄", "decadal", ["流陀", "流曲", "运昌"]) is False
    assert horoscope.lacks_horoscope_stars("疾厄", "decadal", ["流陀", "流鸾", "运昌"]) is False
    assert horoscope.lacks_horoscope_stars("疾厄", "decadal", ["流喜", "流鸾", "流魁"]) is True
    assert horoscope.has_any_horoscope_star("疾厄", "decadal", ["流陀", "流曲", "运昌"]) is True
    assert horoscope.has_any_horoscope_star("疾厄", "decadal", ["流喜", "流鸾", "流魁"]) is False

    assert horoscope.has_horoscope_mutagen("兄弟", "decadal", "禄") is True
    assert horoscope.has_horoscope_mutagen("夫妻", "decadal", "权") is True
    assert horoscope.has_horoscope_mutagen("疾厄", "decadal", "科") is True
    assert horoscope.has_horoscope_mutagen("子女", "decadal", "忌") is True

    assert horoscope.has_horoscope_mutagen("仆役", "yearly", "禄") is True
    assert horoscope.has_horoscope_mutagen("夫妻", "yearly", "权") is True
    assert horoscope.has_horoscope_mutagen("财帛", "yearly", "科") is True
    assert horoscope.has_horoscope_mutagen("子女", "yearly", "忌") is True

    assert horoscope.has_horoscope_mutagen("夫妻", "monthly", "禄") is True
    assert horoscope.has_horoscope_mutagen("子女", "monthly", "权") is True
    assert horoscope.has_horoscope_mutagen("迁移", "monthly", "科") is True
    assert horoscope.has_horoscope_mutagen("财帛", "monthly", "忌") is True

    assert horoscope.has_horoscope_mutagen("迁移", "daily", "禄") is True
    assert horoscope.has_horoscope_mutagen("官禄", "daily", "权") is True
    assert horoscope.has_horoscope_mutagen("疾厄", "daily", "科") is True
    assert horoscope.has_horoscope_mutagen("夫妻", "daily", "忌") is True

    age_palace = horoscope.age_palace()
    assert age_palace.name == "仆役"
    assert age_palace.heavenly_stem == "丁"
    assert age_palace.earthly_branch == "亥"

    original_palace = horoscope.palace("命宫", "origin")
    assert original_palace.name == "命宫"
    assert original_palace.heavenly_stem == "壬"
    assert original_palace.earthly_branch == "午"

    decadal_palace = horoscope.palace("命宫", "decadal")
    assert decadal_palace.name == "夫妻"
    assert decadal_palace.heavenly_stem == "庚"
    assert decadal_palace.earthly_branch == "辰"

    decadal_surroundings = horoscope.surrounding_palaces("命宫", "decadal")
    assert decadal_surroundings.target.name == "夫妻"
    assert decadal_surroundings.target.heavenly_stem == "庚"
    assert decadal_surroundings.target.earthly_branch == "辰"
    assert decadal_surroundings.opposite.name == "官禄"
    assert decadal_surroundings.opposite.heavenly_stem == "丙"
    assert decadal_surroundings.opposite.earthly_branch == "戌"
    assert decadal_surroundings.career.name == "福德"
    assert decadal_surroundings.career.heavenly_stem == "甲"
    assert decadal_surroundings.career.earthly_branch == "申"
    assert decadal_surroundings.wealth.name == "迁移"
    assert decadal_surroundings.wealth.heavenly_stem == "戊"
    assert decadal_surroundings.wealth.earthly_branch == "子"

    original_surroundings = horoscope.surrounding_palaces("夫妻", "origin")
    assert original_surroundings.target.name == "夫妻"
    assert original_surroundings.target.heavenly_stem == "庚"
    assert original_surroundings.target.earthly_branch == "辰"
    assert original_surroundings.opposite.name == "官禄"
    assert original_surroundings.opposite.heavenly_stem == "丙"
    assert original_surroundings.opposite.earthly_branch == "戌"
    assert original_surroundings.career.name == "福德"
    assert original_surroundings.career.heavenly_stem == "甲"
    assert original_surroundings.career.earthly_branch == "申"
    assert original_surroundings.wealth.name == "迁移"
    assert original_surroundings.wealth.heavenly_stem == "戊"
    assert original_surroundings.wealth.earthly_branch == "子"

    yearly_palace = horoscope.palace("命宫", "yearly")
    assert yearly_palace.name == "子女"
    assert yearly_palace.heavenly_stem == "己"
    assert yearly_palace.earthly_branch == "卯"

    monthly_palace = horoscope.palace("命宫", "monthly")
    assert monthly_palace.name == "兄弟"
    assert monthly_palace.heavenly_stem == "辛"
    assert monthly_palace.earthly_branch == "巳"

    daily_palace = horoscope.palace("命宫", "daily")
    assert daily_palace.name == "福德"
    assert daily_palace.heavenly_stem == "甲"
    assert daily_palace.earthly_branch == "申"

    hourly_palace = horoscope.palace("命宫", "hourly")
    assert hourly_palace.name == "官禄"
    assert hourly_palace.heavenly_stem == "丙"
    assert hourly_palace.earthly_branch == "戌"

    horoscope2 = astrolabe.horoscope("2023-10-19 3:12")
    assert horoscope2.age.index == 9
    assert horoscope2.age.nominal_age == 24
    age_palace2 = horoscope2.age_palace()
    assert age_palace2.name == "仆役"
    assert age_palace2.heavenly_stem == "丁"
    assert age_palace2.earthly_branch == "亥"


def test_horoscope_smoke():
    set_config({"year_divide": "exact", "algorithm": "default"})
    astrolabe = by_solar("1991-3-7", 6, "女", fix_leap=True)
    horoscope = astrolabe.horoscope("2025-3-26")

    assert horoscope.solar_date == "2025-3-26"
    assert horoscope.decadal.index == 8
    assert horoscope.decadal.heavenly_stem == "戊"
    assert horoscope.decadal.earthly_branch == "戌"
    assert horoscope.yearly.index == 3
    assert horoscope.yearly.heavenly_stem == "乙"
    assert horoscope.yearly.earthly_branch == "巳"
    assert horoscope.monthly.index == 10
    assert horoscope.monthly.heavenly_stem == "己"
    assert horoscope.monthly.earthly_branch == "卯"
    assert horoscope.daily.index == 0
    assert horoscope.daily.heavenly_stem == "甲"
    assert horoscope.daily.earthly_branch == "午"


def test_by_solar_korean():
    astrolabe = by_solar("2000-8-16", 2, "女", fix_leap=True, language="ko-KR")

    assert astrolabe.solar_date == "2000-8-16"
    assert astrolabe.lunar_date == "二〇〇〇年七月十七"
    assert astrolabe.chinese_date == "경진 갑신 병오 경인"
    assert astrolabe.time == "인시"
    assert astrolabe.sign == "사자궁"
    assert astrolabe.zodiac == "용"
    assert astrolabe.earthly_branch_of_soul_palace == "오"
    assert astrolabe.earthly_branch_of_body_palace == "술"
    assert astrolabe.soul == "파군"
    assert astrolabe.body == "문창"
    assert astrolabe.five_elements_class == "목삼국"

    horoscope = astrolabe.horoscope("2023-8-19 3:12")
    assert horoscope.solar_date == "2023-8-19"
    assert horoscope.decadal.index == 2
    assert horoscope.decadal.heavenly_stem == "경"
    assert horoscope.decadal.earthly_branch == "진"
    assert _dump_horoscope_stars(horoscope.decadal.stars) == [
        [{"name": "천마(십년)", "type": "tianma", "scope": "decadal"}],
        [{"name": "문곡(십년)", "type": "soft", "scope": "decadal"}],
        [],
        [{"name": "천희(십년)", "type": "flower", "scope": "decadal"}],
        [],
        [
            {"name": "천월(십년)", "type": "soft", "scope": "decadal"},
            {"name": "타라(십년)", "type": "tough", "scope": "decadal"},
        ],
        [{"name": "록존(십년)", "type": "lucun", "scope": "decadal"}],
        [{"name": "경양(십년)", "type": "tough", "scope": "decadal"}],
        [],
        [
            {"name": "문창(십년)", "type": "soft", "scope": "decadal"},
            {"name": "홍란(십년)", "type": "flower", "scope": "decadal"},
        ],
        [],
        [{"name": "천괴(십년)", "type": "soft", "scope": "decadal"}],
    ]
    assert horoscope.decadal.palace_names == [
        "부처",
        "형제",
        "명궁",
        "부모",
        "복덕",
        "전택",
        "관록",
        "노복",
        "천이",
        "질액",
        "재백",
        "자녀",
    ]
    assert horoscope.decadal.mutagen == ["태양", "무곡", "태음", "천동"]
    assert horoscope.age.index == 9
    assert horoscope.age.nominal_age == 24
    assert horoscope.yearly.index == 1
    assert horoscope.yearly.heavenly_stem == "계"
    assert horoscope.yearly.earthly_branch == "묘"
    assert _dump_horoscope_stars(horoscope.yearly.stars) == [
        [],
        [
            {"name": "천괴(년)", "type": "soft", "scope": "yearly"},
            {"name": "문창(년)", "type": "soft", "scope": "yearly"},
        ],
        [],
        [
            {"name": "천월(년)", "type": "soft", "scope": "yearly"},
            {"name": "천마(년)", "type": "tianma", "scope": "yearly"},
        ],
        [{"name": "천희(년)", "type": "flower", "scope": "yearly"}],
        [{"name": "해신(년)", "type": "helper", "scope": "yearly"}],
        [],
        [],
        [],
        [
            {"name": "문곡(년)", "type": "soft", "scope": "yearly"},
            {"name": "타라(년)", "type": "tough", "scope": "yearly"},
        ],
        [
            {"name": "록존(년)", "type": "lucun", "scope": "yearly"},
            {"name": "홍란(년)", "type": "flower", "scope": "yearly"},
        ],
        [{"name": "경양(년)", "type": "tough", "scope": "yearly"}],
    ]
    assert horoscope.yearly.palace_names == [
        "형제",
        "명궁",
        "부모",
        "복덕",
        "전택",
        "관록",
        "노복",
        "천이",
        "질액",
        "재백",
        "자녀",
        "부처",
    ]
    assert horoscope.yearly.mutagen == ["파군", "거문", "태음", "탐랑"]
    assert horoscope.monthly.index == 3
    assert horoscope.monthly.heavenly_stem == "경"
    assert horoscope.monthly.earthly_branch == "신"
    assert horoscope.monthly.palace_names == [
        "자녀",
        "부처",
        "형제",
        "명궁",
        "부모",
        "복덕",
        "전택",
        "관록",
        "노복",
        "천이",
        "질액",
        "재백",
    ]
    assert horoscope.monthly.mutagen == ["태양", "무곡", "태음", "천동"]
    assert horoscope.daily.index == 6
    assert horoscope.daily.heavenly_stem == "기"
    assert horoscope.daily.earthly_branch == "유"
    assert horoscope.daily.palace_names == [
        "천이",
        "질액",
        "재백",
        "자녀",
        "부처",
        "형제",
        "명궁",
        "부모",
        "복덕",
        "전택",
        "관록",
        "노복",
    ]
    assert horoscope.daily.mutagen == ["무곡", "탐랑", "천량", "문곡"]
    assert horoscope.hourly.index == 8
    assert horoscope.hourly.heavenly_stem == "병"
    assert horoscope.hourly.earthly_branch == "인"
    assert horoscope.hourly.palace_names == [
        "관록",
        "노복",
        "천이",
        "질액",
        "재백",
        "자녀",
        "부처",
        "형제",
        "명궁",
        "부모",
        "복덕",
        "전택",
    ]
    assert horoscope.hourly.mutagen == ["천동", "천기", "문창", "염정"]


def test_by_solar_vietnamese():
    astrolabe = by_solar("2000-8-16", 2, "女", fix_leap=True, language="vi-VN")

    assert astrolabe.solar_date == "2000-8-16"
    assert astrolabe.lunar_date == "二〇〇〇年七月十七"
    assert astrolabe.chinese_date == "Canh Thìn - Giáp Thân - Bính Ngọ - Canh Dần"
    assert astrolabe.time == "Giờ dần"
    assert astrolabe.sign == "Cung Sư Tử"
    assert astrolabe.zodiac == "Rồng"
    assert astrolabe.earthly_branch_of_soul_palace == "Ngọ"
    assert astrolabe.earthly_branch_of_body_palace == "Tuất"
    assert astrolabe.soul == "Phá Quân"
    assert astrolabe.body == "Văn Xương"
    assert astrolabe.five_elements_class == "Mộc Tam Cục"

    horoscope = astrolabe.horoscope("2023-8-19 3:12")
    assert horoscope.solar_date == "2023-8-19"
    assert horoscope.decadal.index == 2
    assert horoscope.decadal.heavenly_stem == "Canh"
    assert horoscope.decadal.earthly_branch == "Thìn"
    assert _dump_horoscope_stars(horoscope.decadal.stars) == [
        [{"name": "Vận Mã", "type": "tianma", "scope": "decadal"}],
        [{"name": "Vận Khúc", "type": "soft", "scope": "decadal"}],
        [],
        [{"name": "Vận Hỷ", "type": "flower", "scope": "decadal"}],
        [],
        [
            {"name": "Vận Việt", "type": "soft", "scope": "decadal"},
            {"name": "Vận Đà", "type": "tough", "scope": "decadal"},
        ],
        [{"name": "Vận Lộc", "type": "lucun", "scope": "decadal"}],
        [{"name": "Vận Dương", "type": "tough", "scope": "decadal"}],
        [],
        [
            {"name": "Vận Xương", "type": "soft", "scope": "decadal"},
            {"name": "Vận Loan", "type": "flower", "scope": "decadal"},
        ],
        [],
        [{"name": "Vận Khôi", "type": "soft", "scope": "decadal"}],
    ]
    assert horoscope.decadal.palace_names == [
        "Phu Thê",
        "Huynh Đệ",
        "Mệnh",
        "Phụ Mẫu",
        "Phúc Đức",
        "Điền Trạch",
        "Quan Lộc",
        "Nô Bộc",
        "Thiên Di",
        "Tật Ách",
        "Tài Bạch",
        "Tử Nữ",
    ]
    assert horoscope.decadal.mutagen == ["Thái Dương", "Vũ Khúc", "Thái Âm", "Thiên Đồng"]
    assert horoscope.age.index == 9
    assert horoscope.age.nominal_age == 24
    assert horoscope.yearly.index == 1
    assert horoscope.yearly.heavenly_stem == "Quý"
    assert horoscope.yearly.earthly_branch == "Mão"
    assert _dump_horoscope_stars(horoscope.yearly.stars) == [
        [],
        [
            {"name": "Lưu Khôi", "type": "soft", "scope": "yearly"},
            {"name": "Lưu Xương", "type": "soft", "scope": "yearly"},
        ],
        [],
        [
            {"name": "Lưu Việt", "type": "soft", "scope": "yearly"},
            {"name": "Lưu Mã", "type": "tianma", "scope": "yearly"},
        ],
        [{"name": "Lưu Hỷ", "type": "flower", "scope": "yearly"}],
        [{"name": "Niên Giải", "type": "helper", "scope": "yearly"}],
        [],
        [],
        [],
        [
            {"name": "Lưu Khúc", "type": "soft", "scope": "yearly"},
            {"name": "Lưu Đà", "type": "tough", "scope": "yearly"},
        ],
        [
            {"name": "Lưu Lộc", "type": "lucun", "scope": "yearly"},
            {"name": "Lưu Loan", "type": "flower", "scope": "yearly"},
        ],
        [{"name": "Lưu Dương", "type": "tough", "scope": "yearly"}],
    ]
    assert horoscope.yearly.palace_names == [
        "Huynh Đệ",
        "Mệnh",
        "Phụ Mẫu",
        "Phúc Đức",
        "Điền Trạch",
        "Quan Lộc",
        "Nô Bộc",
        "Thiên Di",
        "Tật Ách",
        "Tài Bạch",
        "Tử Nữ",
        "Phu Thê",
    ]
    assert horoscope.yearly.mutagen == ["Phá Quân", "Cự Môn", "Thái Âm", "Tham Lang"]
    assert horoscope.monthly.index == 3
    assert horoscope.monthly.heavenly_stem == "Canh"
    assert horoscope.monthly.earthly_branch == "Thân"
    assert horoscope.monthly.palace_names == [
        "Tử Nữ",
        "Phu Thê",
        "Huynh Đệ",
        "Mệnh",
        "Phụ Mẫu",
        "Phúc Đức",
        "Điền Trạch",
        "Quan Lộc",
        "Nô Bộc",
        "Thiên Di",
        "Tật Ách",
        "Tài Bạch",
    ]
    assert horoscope.monthly.mutagen == ["Thái Dương", "Vũ Khúc", "Thái Âm", "Thiên Đồng"]
    assert horoscope.daily.index == 6
    assert horoscope.daily.heavenly_stem == "Kỷ"
    assert horoscope.daily.earthly_branch == "Dậu"
    assert horoscope.daily.palace_names == [
        "Thiên Di",
        "Tật Ách",
        "Tài Bạch",
        "Tử Nữ",
        "Phu Thê",
        "Huynh Đệ",
        "Mệnh",
        "Phụ Mẫu",
        "Phúc Đức",
        "Điền Trạch",
        "Quan Lộc",
        "Nô Bộc",
    ]
    assert horoscope.daily.mutagen == ["Vũ Khúc", "Tham Lang", "Thiên Lương", "Văn Khúc"]
    assert horoscope.hourly.index == 8
    assert horoscope.hourly.heavenly_stem == "Bính"
    assert horoscope.hourly.earthly_branch == "Dần"
    assert horoscope.hourly.palace_names == [
        "Quan Lộc",
        "Nô Bộc",
        "Thiên Di",
        "Tật Ách",
        "Tài Bạch",
        "Tử Nữ",
        "Phu Thê",
        "Huynh Đệ",
        "Mệnh",
        "Phụ Mẫu",
        "Phúc Đức",
        "Điền Trạch",
    ]
    assert horoscope.hourly.mutagen == ["Thiên Đồng", "Thiên Cơ", "Văn Xương", "Liêm Trinh"]


def test_by_lunar_basic():
    astrolabe = by_lunar("2000-7-17", 2, "女", is_leap_month=True, fix_leap=True)

    assert astrolabe.solar_date == "2000-8-16"
    assert astrolabe.lunar_date == "二〇〇〇年七月十七"
    assert astrolabe.chinese_date == "庚辰 甲申 丙午 庚寅"
    assert astrolabe.time == "寅时"
    assert astrolabe.sign == "狮子座"
    assert astrolabe.zodiac == "龙"
    assert astrolabe.earthly_branch_of_soul_palace == "午"
    assert astrolabe.earthly_branch_of_body_palace == "戌"
    assert astrolabe.soul == "破军"
    assert astrolabe.body == "文昌"
    assert astrolabe.five_elements_class == "木三局"
    assert len(astrolabe.palaces) == 12
    assert astrolabe.palaces[0].decadal.range == (43, 52)
    assert astrolabe.palaces[0].decadal.heavenly_stem == "戊"
    assert astrolabe.palaces[0].decadal.earthly_branch == "寅"
    assert astrolabe.palaces[11].decadal.range == (53, 62)
    assert astrolabe.palaces[11].decadal.heavenly_stem == "己"
    assert astrolabe.palaces[11].decadal.earthly_branch == "丑"


def test_by_lunar_with_exact_year_divider():
    set_config({"year_divide": "exact"})
    astrolabe = by_lunar("1999-12-29", 2, "女", is_leap_month=True, fix_leap=True)

    assert astrolabe.solar_date == "2000-2-4"
    assert astrolabe.lunar_date == "一九九九年腊月廿九"
    assert astrolabe.chinese_date == "庚辰 己丑 壬辰 壬寅"
    assert astrolabe.time == "寅时"
    assert astrolabe.zodiac == "龙"
    assert astrolabe.earthly_branch_of_soul_palace == "亥"
    assert astrolabe.earthly_branch_of_body_palace == "卯"
    assert astrolabe.soul == "巨门"
    assert astrolabe.body == "文昌"
    assert astrolabe.five_elements_class == "土五局"


def test_by_lunar_with_normal_year_divider():
    set_config({"year_divide": "normal"})
    astrolabe = by_lunar("1999-12-29", 2, "女", is_leap_month=True, fix_leap=True)

    assert astrolabe.solar_date == "2000-2-4"
    assert astrolabe.lunar_date == "一九九九年腊月廿九"
    assert astrolabe.chinese_date == "己卯 丁丑 壬辰 壬寅"
    assert astrolabe.time == "寅时"
    assert astrolabe.zodiac == "兔"
    assert astrolabe.earthly_branch_of_soul_palace == "亥"
    assert astrolabe.earthly_branch_of_body_palace == "卯"
    assert astrolabe.soul == "巨门"
    assert astrolabe.body == "天同"
    assert astrolabe.five_elements_class == "火六局"


def test_by_solar_with_normal_year_divider():
    set_config({"year_divide": "normal", "horoscope_divide": "normal"})
    astrolabe = by_solar("1980-2-14", 0, "male", fix_leap=True)

    assert astrolabe.solar_date == "1980-2-14"
    assert astrolabe.lunar_date == "一九七九年腊月廿八"
    assert astrolabe.chinese_date == "己未 丁丑 丁巳 庚子"
    assert astrolabe.time == "早子时"
    assert astrolabe.zodiac == "羊"
    assert astrolabe.earthly_branch_of_soul_palace == "丑"
    assert astrolabe.earthly_branch_of_body_palace == "丑"
    assert astrolabe.soul == "巨门"
    assert astrolabe.body == "天相"
    assert astrolabe.five_elements_class == "水二局"
    assert astrolabe.palaces[0].decadal.range == (112, 121)

    horoscope = astrolabe.horoscope("1980-2-14")
    assert horoscope.yearly.earthly_branch == "未"
    assert horoscope.yearly.heavenly_stem == "己"


def test_special_date_1995_3_30():
    set_config({"year_divide": "normal"})
    astrolabe = by_solar("1995-03-30", 0, "male", fix_leap=True)
    assert astrolabe.solar_date == "1995-03-30"
    assert astrolabe.lunar_date == "一九九五年二月三十"

    astrolabe2 = by_lunar("1995-2-30", 0, "male", is_leap_month=True)
    assert astrolabe2.solar_date == "1995-3-30"
    assert astrolabe2.lunar_date == "一九九五年二月三十"


def test_by_lunar_with_per_call_year_divide_normal():
    astrolabe = by_lunar(
        "1999-12-29",
        2,
        "female",
        is_leap_month=False,
        fix_leap=True,
        language="zh-CN",
        config={"year_divide": "normal"},
    )
    assert astrolabe.solar_date == "2000-2-4"
    assert astrolabe.lunar_date == "一九九九年腊月廿九"
    assert astrolabe.chinese_date == "己卯 丁丑 壬辰 壬寅"
    assert astrolabe.time == "寅时"
    assert astrolabe.zodiac == "兔"
    assert astrolabe.earthly_branch_of_soul_palace == "亥"
    assert astrolabe.earthly_branch_of_body_palace == "卯"
    assert astrolabe.soul == "巨门"
    assert astrolabe.body == "天同"
    assert astrolabe.five_elements_class == "火六局"


def test_by_solar_with_per_call_day_divide_current():
    astrolabe = by_solar(
        "1987-9-23",
        12,
        "female",
        fix_leap=True,
        language="zh-CN",
        config={"year_divide": "normal", "day_divide": "current"},
    )
    assert astrolabe.solar_date == "1987-9-23"
    assert astrolabe.lunar_date == "一九八七年八月初一"
    assert astrolabe.chinese_date == "丁卯 己酉 丙子 戊子"
    assert astrolabe.time == "晚子时"
    assert astrolabe.zodiac == "兔"
    assert astrolabe.earthly_branch_of_soul_palace == "酉"
    assert astrolabe.earthly_branch_of_body_palace == "酉"
    assert astrolabe.soul == "文曲"
    assert astrolabe.body == "天同"
    assert astrolabe.five_elements_class == "土五局"
    assert astrolabe.palace("命宫").index == 7
    assert astrolabe.palace("命宫").is_empty() is True
    assert astrolabe.palace("命宫").has_stars(["火星", "天钺"]) is True
    assert astrolabe.palace("迁移").has_stars(["太阳", "天梁", "右弼", "八座", "天贵", "空亡", "天哭"]) is True


def test_by_lunar_with_exact_dividers():
    astrolabe = by_lunar(
        "1999-12-29",
        2,
        "female",
        is_leap_month=False,
        fix_leap=True,
        language="zh-CN",
        config={"year_divide": "exact", "horoscope_divide": "exact"},
    )
    assert astrolabe.solar_date == "2000-2-4"
    assert astrolabe.lunar_date == "一九九九年腊月廿九"
    assert astrolabe.chinese_date == "庚辰 丁丑 壬辰 壬寅"
    assert astrolabe.time == "寅时"
    assert astrolabe.zodiac == "龙"
    assert astrolabe.earthly_branch_of_soul_palace == "亥"
    assert astrolabe.earthly_branch_of_body_palace == "卯"
    assert astrolabe.soul == "巨门"
    assert astrolabe.body == "文昌"
    assert astrolabe.five_elements_class == "土五局"


def test_by_lunar_with_per_call_horoscope_divide():
    astrolabe = by_lunar(
        "1979-12-28",
        0,
        "female",
        is_leap_month=False,
        fix_leap=True,
        language="zh-CN",
        config={"year_divide": "normal", "horoscope_divide": "normal"},
    )
    assert astrolabe.solar_date == "1980-2-14"
    assert astrolabe.lunar_date == "一九七九年腊月廿八"
    assert astrolabe.chinese_date == "己未 丁丑 丁巳 庚子"
    assert astrolabe.time == "早子时"
    assert astrolabe.zodiac == "羊"
    assert astrolabe.earthly_branch_of_soul_palace == "丑"
    assert astrolabe.earthly_branch_of_body_palace == "丑"
    assert astrolabe.soul == "巨门"
    assert astrolabe.body == "天相"
    assert astrolabe.five_elements_class == "水二局"
    assert astrolabe.horoscope("1980-2-14").yearly.earthly_branch == "未"

    astrolabe2 = by_lunar(
        "1979-12-28",
        0,
        "female",
        is_leap_month=False,
        fix_leap=True,
        language="zh-CN",
        config={"year_divide": "normal", "horoscope_divide": "exact"},
    )
    assert astrolabe2.horoscope("1980-2-14").yearly.earthly_branch == "申"


def test_by_solar_fix_leap_month():
    astrolabe = by_solar("2023-4-10", 4, "女", fix_leap=True)
    assert astrolabe.earthly_branch_of_soul_palace == "子"
    assert astrolabe.earthly_branch_of_body_palace == "申"
    assert astrolabe.soul == "贪狼"
    assert astrolabe.body == "天同"
    assert astrolabe.five_elements_class == "金四局"
    assert astrolabe.star("紫微").palace().name == "迁移"


def test_by_solar_default_fix_leap_month():
    astrolabe = by_solar("2023-4-10", 4, "女")
    assert astrolabe.earthly_branch_of_soul_palace == "子"
    assert astrolabe.earthly_branch_of_body_palace == "申"
    assert astrolabe.soul == "贪狼"
    assert astrolabe.body == "天同"
    assert astrolabe.five_elements_class == "金四局"
    assert astrolabe.star("紫微").palace().name == "迁移"


def test_by_solar_do_not_fix_leap_month():
    astrolabe = by_solar("2023-4-10", 4, "女", fix_leap=False)
    assert astrolabe.earthly_branch_of_soul_palace == "亥"
    assert astrolabe.earthly_branch_of_body_palace == "未"
    assert astrolabe.soul == "巨门"
    assert astrolabe.body == "天同"
    assert astrolabe.five_elements_class == "水二局"
    assert astrolabe.star("紫微").palace().name == "命宫"


def test_by_lunar_fix_leap_month():
    astrolabe = by_lunar("2023-2-20", 4, "女", is_leap_month=True, fix_leap=True)
    assert astrolabe.earthly_branch_of_soul_palace == "子"
    assert astrolabe.earthly_branch_of_body_palace == "申"
    assert astrolabe.soul == "贪狼"
    assert astrolabe.body == "天同"
    assert astrolabe.five_elements_class == "金四局"
    assert astrolabe.star("紫微").palace().name == "迁移"


def test_by_lunar_default_is_leap_month():
    astrolabe = by_lunar("2023-2-20", 4, "女")
    assert astrolabe.earthly_branch_of_soul_palace == "亥"
    assert astrolabe.earthly_branch_of_body_palace == "未"
    assert astrolabe.soul == "巨门"
    assert astrolabe.body == "天同"
    assert astrolabe.five_elements_class == "水二局"
    assert astrolabe.star("紫微").palace().name == "命宫"


@pytest.mark.parametrize(
    ("language", "expected_chinese_date"),
    [
        ("ko-KR", "경진 갑신 병오 경인"),
        ("vi-VN", "Canh Thìn - Giáp Thân - Bính Ngọ - Canh Dần"),
    ],
)
def test_by_solar_multilanguage_chinese_date(language: str, expected_chinese_date: str):
    astrolabe = by_solar("2000-8-16", 2, "女", fix_leap=True, language=language)
    assert astrolabe.chinese_date == expected_chinese_date


def test_by_lunar_do_not_fix_leap_month():
    # `is_leap_month=True`, `fix_leap=False`
    astrolabe = by_lunar("2023-2-20", 4, "女", is_leap_month=True, fix_leap=False)

    assert astrolabe.earthly_branch_of_soul_palace == "亥"
    assert astrolabe.earthly_branch_of_body_palace == "未"
    assert astrolabe.soul == "巨门"
    assert astrolabe.body == "天同"
    assert astrolabe.five_elements_class == "水二局"
    assert astrolabe.star("紫微").palace().name == "命宫"


def test_get_zodiac_by_solar_date():
    assert get_zodiac_by_solar_date("2023-2-20") == "兔"
    assert get_zodiac_by_solar_date("2023-2-20", language="en-US") == "rabbit"


def test_get_sign_by_solar_date():
    assert get_sign_by_solar_date("2023-9-5") == "处女座"
    assert get_sign_by_solar_date("2023-9-5", language="en-US") == "virgo"


def test_get_sign_by_lunar_date():
    assert get_sign_by_lunar_date("2023-7-21") == "处女座"
    assert get_sign_by_lunar_date("2023-7-21", is_leap_month=False, language="en-US") == "virgo"


def test_get_sign_by_lunar_date_leap_month():
    # Leap lunar month affects sign mapping.
    assert get_sign_by_lunar_date("2023-2-3") == "双鱼座"
    assert get_sign_by_lunar_date("2023-2-3", is_leap_month=True) == "白羊座"


def test_get_major_star_by_solar_date_leap_month():
    # Leap month fixes affect major-star lookup.
    assert get_major_star_by_solar_date("2023-4-7", 0) == "贪狼"
    assert get_major_star_by_solar_date("2023-4-7", 0, fix_leap=False) == "紫微,贪狼"
    assert get_major_star_by_solar_date("2023-4-7", 0, fix_leap=True, language="ko-KR") == "탐랑"


def test_get_major_star_by_solar_date():
    assert get_major_star_by_solar_date("1987-05-16", 7) == "天机,天梁"


def test_get_major_star_by_lunar_date_leap_month():
    assert get_major_star_by_lunar_date("2023-2-17", 0) == "紫微,贪狼"
    assert get_major_star_by_lunar_date("2023-2-17", 0, is_leap_month=True) == "贪狼"
    assert get_major_star_by_lunar_date("2023-2-17", 0, is_leap_month=True, fix_leap=False) == "紫微,贪狼"


def test_childhood_decadal_name_and_index():
    astrolabe = by_solar("2023-10-18", 4, "female")

    horo1 = astrolabe.horoscope("2023-12-19")
    assert horo1.decadal.name == "童限"
    assert horo1.decadal.index == astrolabe.palace("命宫").index

    horo2 = astrolabe.horoscope("2024-12-29")
    assert horo2.decadal.name == "童限"
    assert horo2.decadal.index == astrolabe.palace("财帛").index

    horo3 = astrolabe.horoscope("2025-12-29")
    assert horo3.decadal.name == "童限"
    assert horo3.decadal.index == astrolabe.palace("疾厄").index


def test_nominal_age_divide_normal_vs_birthday():
    astrolabe1 = by_solar("2000-8-16", 2, "female", config={"age_divide": "normal"})
    horo1 = astrolabe1.horoscope("2023-8-19 3:12")
    assert horo1.age.index == 9
    assert horo1.age.nominal_age == 24

    astrolabe2 = by_solar("2000-8-16", 2, "female", config={"age_divide": "birthday"})
    horo2 = astrolabe2.horoscope("2023-8-19 3:12")
    assert horo2.age.index == 10
    assert horo2.age.nominal_age == 23
