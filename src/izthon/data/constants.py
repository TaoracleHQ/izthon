from __future__ import annotations

from enum import IntEnum


LANGUAGES = ("en-US", "ja-JP", "ko-KR", "zh-CN", "zh-TW", "vi-VN")

HEAVENLY_STEMS = (
    "jiaHeavenly",
    "yiHeavenly",
    "bingHeavenly",
    "dingHeavenly",
    "wuHeavenly",
    "jiHeavenly",
    "gengHeavenly",
    "xinHeavenly",
    "renHeavenly",
    "guiHeavenly",
)

EARTHLY_BRANCHES = (
    "ziEarthly",
    "chouEarthly",
    "yinEarthly",
    "maoEarthly",
    "chenEarthly",
    "siEarthly",
    "wuEarthly",
    "weiEarthly",
    "shenEarthly",
    "youEarthly",
    "xuEarthly",
    "haiEarthly",
)

ZODIAC = ("rat", "ox", "tiger", "rabbit", "dragon", "snake", "horse", "sheep", "monkey", "rooster", "dog", "pig")

PALACES = (
    "soulPalace",
    "parentsPalace",
    "spiritPalace",
    "propertyPalace",
    "careerPalace",
    "friendsPalace",
    "surfacePalace",
    "healthPalace",
    "wealthPalace",
    "childrenPalace",
    "spousePalace",
    "siblingsPalace",
)

GENDER = {"male": "阳", "female": "阴"}


class FiveElementsClass(IntEnum):
    water2nd = 2
    wood3rd = 3
    metal4th = 4
    earth5th = 5
    fire6th = 6


CHINESE_TIME = (
    "earlyRatHour",
    "oxHour",
    "tigerHour",
    "rabbitHour",
    "dragonHour",
    "snakeHour",
    "horseHour",
    "goatHour",
    "monkeyHour",
    "roosterHour",
    "dogHour",
    "pigHour",
    "lateRatHour",
)

TIME_RANGE = (
    "00:00~01:00",
    "01:00~03:00",
    "03:00~05:00",
    "05:00~07:00",
    "07:00~09:00",
    "09:00~11:00",
    "11:00~13:00",
    "13:00~15:00",
    "15:00~17:00",
    "17:00~19:00",
    "19:00~21:00",
    "21:00~23:00",
    "23:00~00:00",
)

TIGER_RULE = {
    "jiaHeavenly": "bingHeavenly",
    "yiHeavenly": "wuHeavenly",
    "bingHeavenly": "gengHeavenly",
    "dingHeavenly": "renHeavenly",
    "wuHeavenly": "jiaHeavenly",
    "jiHeavenly": "bingHeavenly",
    "gengHeavenly": "wuHeavenly",
    "xinHeavenly": "gengHeavenly",
    "renHeavenly": "renHeavenly",
    "guiHeavenly": "jiaHeavenly",
}

RAT_RULE = {
    "jiaHeavenly": "jiaHeavenly",
    "yiHeavenly": "bingHeavenly",
    "bingHeavenly": "wuHeavenly",
    "dingHeavenly": "gengHeavenly",
    "wuHeavenly": "renHeavenly",
    "jiHeavenly": "jiaHeavenly",
    "gengHeavenly": "bingHeavenly",
    "xinHeavenly": "wuHeavenly",
    "renHeavenly": "gengHeavenly",
    "guiHeavenly": "renHeavenly",
}

