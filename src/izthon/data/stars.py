from __future__ import annotations

# Ported from the upstream iztro (TypeScript) `src/data/stars.ts`.

MUTAGEN = ("sihuaLu", "sihuaQuan", "sihuaKe", "sihuaJi")

STARS_INFO = {
    "ziweiMaj": {
        "brightness": ["wang", "wang", "de", "wang", "miao", "miao", "wang", "wang", "de", "wang", "ping", "miao"],
        "five_elements": "土",
        "yin_yang": "阴",
    },
    "tianjiMaj": {
        "brightness": ["de", "wang", "li", "ping", "miao", "xian", "de", "wang", "li", "ping", "miao", "xian"],
        "five_elements": "木",
        "yin_yang": "阴",
    },
    "taiyangMaj": {"brightness": ["wang", "miao", "wang", "wang", "wang", "de", "de", "xian", "bu", "xian", "xian", "bu"], "five_elements": "", "yin_yang": ""},
    "wuquMaj": {
        "brightness": ["de", "li", "miao", "ping", "wang", "miao", "de", "li", "miao", "ping", "wang", "miao"],
        "five_elements": "金",
        "yin_yang": "阴",
    },
    "tiantongMaj": {
        "brightness": ["li", "ping", "ping", "miao", "xian", "bu", "wang", "ping", "ping", "miao", "wang", "bu"],
        "five_elements": "水",
        "yin_yang": "阳",
    },
    "lianzhenMaj": {
        "brightness": ["miao", "ping", "li", "xian", "ping", "li", "miao", "ping", "li", "xian", "ping", "li"],
        "five_elements": "火",
        "yin_yang": "阴",
    },
    "tianfuMaj": {
        "brightness": ["miao", "de", "miao", "de", "wang", "miao", "de", "wang", "miao", "de", "miao", "miao"],
        "five_elements": "土",
        "yin_yang": "阳",
    },
    "taiyinMaj": {"brightness": ["wang", "xian", "xian", "xian", "bu", "bu", "li", "bu", "wang", "miao", "miao", "miao"], "five_elements": "水", "yin_yang": "阴"},
    "tanlangMaj": {"brightness": ["ping", "li", "miao", "xian", "wang", "miao", "ping", "li", "miao", "xian", "wang", "miao"], "five_elements": "水", "yin_yang": ""},
    "jumenMaj": {"brightness": ["miao", "miao", "xian", "wang", "wang", "bu", "miao", "miao", "xian", "wang", "wang", "bu"], "five_elements": "土", "yin_yang": "阴"},
    "tianxiangMaj": {"brightness": ["miao", "xian", "de", "de", "miao", "de", "miao", "xian", "de", "de", "miao", "miao"], "five_elements": "水", "yin_yang": ""},
    "tianliangMaj": {"brightness": ["miao", "miao", "miao", "xian", "miao", "wang", "xian", "de", "miao", "xian", "miao", "wang"], "five_elements": "土", "yin_yang": ""},
    "qishaMaj": {"brightness": ["miao", "wang", "miao", "ping", "wang", "miao", "miao", "miao", "miao", "ping", "wang", "miao"], "five_elements": "", "yin_yang": ""},
    "pojunMaj": {"brightness": ["de", "xian", "wang", "ping", "miao", "wang", "de", "xian", "wang", "ping", "miao", "wang"], "five_elements": "水", "yin_yang": ""},
    "wenchangMin": {"brightness": ["xian", "li", "de", "miao", "xian", "li", "de", "miao", "xian", "li", "de", "miao"]},
    "wenquMin": {"brightness": ["ping", "wang", "de", "miao", "xian", "wang", "de", "miao", "xian", "wang", "de", "miao"]},
    "huoxingMin": {"brightness": ["miao", "li", "xian", "de", "miao", "li", "xian", "de", "miao", "li", "xian", "de"]},
    "lingxingMin": {"brightness": ["miao", "li", "xian", "de", "miao", "li", "xian", "de", "miao", "li", "xian", "de"]},
    "qingyangMin": {"brightness": ["", "xian", "miao", "", "xian", "miao", "", "xian", "miao", "", "xian", "miao"]},
    "tuoluoMin": {"brightness": ["xian", "", "miao", "xian", "", "miao", "xian", "", "miao", "xian", "", "miao"]},
}
