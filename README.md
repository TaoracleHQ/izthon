# izthon

[中文 README](README_CN.md)

`izthon` is a pure-Python re-implementation of the TypeScript library `iztro` (Zi Wei Dou Shu astrolabe generator).
It is implemented as a normal Python package (no runtime dependency on the TypeScript code).

## Design Goals

- Pure Python implementation; TS sources are only used as a spec (no runtime dependency on TS).
- Public APIs are Pythonic `snake_case` (no TS-style alias names).
- Built-in i18n follows stdlib `gettext` semantics, plus an iztro-compatible reverse lookup helper `kot()`.
- Behavior is regression-tested against upstream Jest test cases via pytest.

## Requirements

- Python >= 3.12
- `uv` (recommended; this repo uses uv to manage environments and dependencies)

## Install / Run

### Run From Source (this repo)

```bash
uv run python -c "from izthon.astro import by_solar; print(by_solar('2000-8-16', 2, '女').five_elements_class)"
```

### Use As a Dependency (uv)

In another project (example):

```bash
# Local editable (recommended for development)
uv add --editable /path/to/izthon
```

## Quick Start

### Generate An Astrolabe (Solar Date)

```python
from izthon.astro import by_solar

astrolabe = by_solar("2000-8-16", time_index=2, gender="女")
print(astrolabe.lunar_date)          # 二〇〇〇年七月十七
print(astrolabe.chinese_date)        # 庚辰 甲申 丙午 庚寅
print(astrolabe.five_elements_class) # 木三局
```

### Generate An Astrolabe (Lunar Date)

```python
from izthon.astro import by_lunar

# lunar_date: "YYYY-M-D", use is_leap_month=True for leap-month dates
astrolabe = by_lunar("2023-2-20", time_index=4, gender="女", is_leap_month=True)
```

## High-level API (`izthon.astro`)

Entry points:

- `by_solar(solar_date, time_index, gender, *, fix_leap=True, language="zh-CN", config=None, plate="sky") -> FunctionalAstrolabe`
- `by_lunar(lunar_date, time_index, gender, *, is_leap_month=False, fix_leap=True, language="zh-CN", config=None, plate="sky") -> FunctionalAstrolabe`
- `with_options(*, date_value, time_index, gender, date_type="solar", is_leap_month=False, fix_leap=True, language="zh-CN", config=None, plate="sky") -> FunctionalAstrolabe`
  - `plate`: `"sky"` | `"earth"` | `"human"`
  - `config`: per-call config patch (no cross-call leakage)
- Plugins:
  - `load_plugin(plugin)` / `load_plugins([...])`
  - `astrolabe.use(plugin)`
- Helpers:
  - `get_zodiac_by_solar_date(..., language=..., config=...)`
  - `get_sign_by_solar_date(..., language=..., config=...)`
  - `get_sign_by_lunar_date(..., is_leap_month=..., language=..., config=...)`
  - `get_major_star_by_solar_date(..., fix_leap=..., language=..., config=...)`
  - `get_major_star_by_lunar_date(..., is_leap_month=..., fix_leap=..., language=..., config=...)`

### Plate Selection (Sky / Earth / Human)

```python
from izthon.astro import by_solar

astrolabe = by_solar(
    "1979-08-21",
    7,
    "male",
    plate="earth",  # "sky" | "earth" | "human"
    config={"algorithm": "zhongzhou"},
)
```

### Unified Entry (`with_options`)

```python
from izthon.astro import with_options

astrolabe = with_options(
    date_value="2023-10-18",
    date_type="lunar",
    time_index=4,
    gender="female",
)
```

### Plugins

```python
from izthon.astro import by_solar, load_plugin


def add_five_elements(self):
    self.five_elements = lambda: self.five_elements_class


load_plugin(add_five_elements)

astrolabe = by_solar("2023-10-18", 4, "female")
print(astrolabe.five_elements())
```

### Helper APIs (sign/zodiac/major stars)

```python
from izthon.astro import (
    get_major_star_by_lunar_date,
    get_major_star_by_solar_date,
    get_sign_by_lunar_date,
    get_sign_by_solar_date,
    get_zodiac_by_solar_date,
)

print(get_zodiac_by_solar_date("2023-2-20"))                 # 兔
print(get_zodiac_by_solar_date("2023-2-20", language="en-US"))        # rabbit
print(get_sign_by_solar_date("2023-9-5"))                    # 处女座
print(get_sign_by_lunar_date("2023-2-3", is_leap_month=True))  # 白羊座 (leap month)

print(get_major_star_by_solar_date("1987-05-16", 7))         # 天机,天梁
print(get_major_star_by_lunar_date("2023-2-17", 0, is_leap_month=True))    # 贪狼
```

## Core Concepts & Objects

All main APIs live in `izthon.astro`.

- `FunctionalAstrolabe`: the astrolabe object returned by `by_solar()` / `by_lunar()`.
- `FunctionalPalace`: 12 palaces, accessed via `astrolabe.palace(...)`.
- `FunctionalStar`: stars in each palace; accessed via `astrolabe.star(...)` or `palace.major_stars` etc.
- `FunctionalHoroscope`: luck-cycle view for a given target date (`astrolabe.horoscope(...)`).
- `FunctionalSurroundingPalaces`: surrounded palaces (三方四正), accessed via `astrolabe.surrounding_palaces(...)`.

### Query Palaces / Stars

```python
astrolabe = by_solar("2023-8-15", 0, "女")

ming = astrolabe.palace("命宫")
print(ming.name, ming.heavenly_stem, ming.earthly_branch)
print([s.name for s in ming.major_stars])

ziwei = astrolabe.star("紫微")
print(ziwei.palace().name)

surroundings = astrolabe.surrounding_palaces("命宫")
print(surroundings.opposite.name, surroundings.wealth.name, surroundings.career.name)
print(surroundings.has_stars(["武曲", "贪狼"]))  # all included?
print(surroundings.has_any_star(["太阳", "文曲"]))  # any included?
```

### Horoscope (Decadal/Yearly/Monthly/Daily/Hourly)

```python
astrolabe = by_solar("2000-8-16", 2, "女")
horoscope = astrolabe.horoscope("2023-8-19 3:12")

print(horoscope.decadal.index, horoscope.decadal.heavenly_stem, horoscope.decadal.earthly_branch)
print(horoscope.yearly.index, horoscope.yearly.heavenly_stem, horoscope.yearly.earthly_branch)

# Query horoscope stars (decadal + yearly stars on a given palace in a given scope)
print(horoscope.has_horoscope_stars("疾厄", "decadal", ["流陀", "流曲", "运昌"]))
print(horoscope.has_horoscope_mutagen("兄弟", "decadal", "禄"))
```

## Parameters & Conventions

### `time_index` (0..12)

`time_index` is the traditional 12-branch hour index used by iztro.

| time_index | time (zh-CN) | range |
|---:|---|---|
| 0 | 早子时 | 00:00~01:00 |
| 1 | 丑时 | 01:00~03:00 |
| 2 | 寅时 | 03:00~05:00 |
| 3 | 卯时 | 05:00~07:00 |
| 4 | 辰时 | 07:00~09:00 |
| 5 | 巳时 | 09:00~11:00 |
| 6 | 午时 | 11:00~13:00 |
| 7 | 未时 | 13:00~15:00 |
| 8 | 申时 | 15:00~17:00 |
| 9 | 酉时 | 17:00~19:00 |
| 10 | 戌时 | 19:00~21:00 |
| 11 | 亥时 | 21:00~23:00 |
| 12 | 晚子时 | 23:00~00:00 |

Helper:

```python
from izthon.util import time_to_index
print(time_to_index(23))  # 12
```

### `gender`

`gender` accepts values in any supported language (e.g. `"male"`, `"female"`, `"男"`, `"女"`), thanks to `kot()`.

Note: `astrolabe.gender` is localized to the current language (default: `zh-CN`), so you may see `"男"`/`"女"` even if you pass `"male"`/`"female"`.

```python
from izthon.astro import by_solar

print(by_solar("2000-8-16", 2, "female").gender)                 # 女 (default zh-CN)
print(by_solar("2000-8-16", 2, "female", language="en-US").gender)  # female
```

### Leap Month Fix (`fix_leap`)

`fix_leap=True` follows iztro behavior for leap months:
for a leap month, days after the 15th may be treated as the next month for some placements (unless `time_index==12`).

## Global Config

Use `set_config()` to set defaults for the current context, or pass `config=...` per call to avoid cross-call state:

```python
from izthon.astro import get_config, set_config

set_config(
    {
        "year_divide": "exact",         # "normal" | "exact"
        "horoscope_divide": "exact",    # "normal" | "exact"
        "age_divide": "birthday",       # "normal" | "birthday"
        "day_divide": "forward",        # "current" | "forward"
        "algorithm": "default",         # "default" | "zhongzhou"
    }
)
print(get_config())
```

You can also customize:

- `mutagens`: map a heavenly stem to 4 stars (禄/权/科/忌)
- `brightness`: map a star to 12 brightness values (one per palace index)

Both keys/values can be provided in any supported language.

## Multi-language (i18n)

Supported languages:

- `en-US`, `ja-JP`, `ko-KR`, `zh-CN`, `zh-TW`, `vi-VN`

Two ways to set language:

1) Pass `language` to `by_solar` / `by_lunar` / helper APIs:

```python
from izthon.astro import by_solar
print(by_solar("2000-8-16", 2, "女", language="vi-VN").chinese_date)
```

2) Set global language:

```python
from izthon.i18n import set_language

set_language("ko-KR")
```

Language is context-local and can be safely overridden per API call.

## Lunar Conversion (lunar_lite)

`izthon.lunar_lite` is a Python port of `lunar-lite` (range: 1900..2100).

```python
from izthon.lunar_lite import lunar_to_solar, solar_to_lunar

print(solar_to_lunar("2023-4-1").to_chinese())  # 二〇二三年闰二月十一
print(lunar_to_solar("2023-2-11", is_leap_month=True).isoformat())  # 2023-4-1
```

## Development

Run tests:

```bash
uv run --extra dev pytest
```

Generate i18n catalogs (maintainer only; requires the upstream iztro locale sources):

```bash
uv run python tools/generate_iztro_i18n_catalogs.py --src-locales /path/to/iztro/src/i18n/locales
```

## Attribution

This project re-implements (as a spec) the behavior of:

- `iztro@2.5.7`
- `lunar-lite@0.2.8`
