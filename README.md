# izthon

[中文 README](README_CN.md)

`izthon` is a pure-Python re-implementation of the TypeScript library `iztro` (Zi Wei Dou Shu astrolabe generator).
It is implemented as a normal Python package (no runtime dependency on the TypeScript code).

## Upstream Reference

- `izthon` follows the behavior of the original TypeScript project `iztro` as a specification reference.
- The bundled `lunar_lite` module follows the upstream `lunar-lite` behavior used by `iztro`.
- These upstream projects are references only; `izthon` does not depend on them at runtime.

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
  - `get_plugins()` / `reset_plugins()`
  - `astrolabe.use(plugin)`
- Low-level astro helpers:
  - `get_soul_and_body(...)`
  - `get_five_elements_class(...)`
  - `get_palace_names(...)`
  - `get_horoscope(...)`
  - `rearrange_astrolabe(...)`
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
from izthon.astro import by_solar, get_plugins, load_plugin, reset_plugins


def add_five_elements(self):
    self.five_elements = lambda: self.five_elements_class


load_plugin(add_five_elements)
print(len(get_plugins()))

global_astrolabe = by_solar("2023-10-18", 4, "female")
print(global_astrolabe.five_elements())

reset_plugins()

instance_astrolabe = by_solar("2023-10-18", 4, "female")
instance_astrolabe.use(add_five_elements)
print(instance_astrolabe.five_elements())
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
print(surroundings.lacks_stars(["地空", "地劫"]))
print(surroundings.has_any_star(["太阳", "文曲"]))  # any included?
print(surroundings.has_mutagen("禄"))
print(surroundings.lacks_mutagen("忌"))
```

### Palace Helper Methods

```python
palace = astrolabe.palace("命宫")

print(palace.has_stars(["武曲"]))
print(palace.lacks_stars(["火星"]))
print(palace.has_any_star(["武曲", "贪狼"]))
print(palace.has_mutagen("禄"))
print(palace.lacks_mutagen("忌"))
print(palace.is_empty())

print(palace.flies_to("兄弟", "忌"))
print(palace.flies_one_of_to("夫妻", ["权", "科"]))
print(palace.does_not_fly_to("兄弟", "科"))

print(palace.has_self_mutagen("禄"))
print(palace.has_any_self_mutagen())
print(palace.lacks_self_mutagen("忌"))
print([p.name if p else None for p in palace.mutagen_palaces()])
```

### Star Helper Methods

```python
star = astrolabe.star("紫微")

print(star.palace().name)
print(star.opposite_palace().name)
print(star.surrounding_palaces().target.name)
print(star.with_mutagen(["禄", "权"]))
print(star.with_brightness(["庙", "旺"]))
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

### Horoscope Helper Methods

```python
print(horoscope.age_palace().name)
print(horoscope.palace("命宫", "yearly").name)
print(horoscope.surrounding_palaces("命宫", "decadal").opposite.name)
print(horoscope.lacks_horoscope_stars("疾厄", "decadal", ["流喜", "流鸾"]))
print(horoscope.has_any_horoscope_star("疾厄", "decadal", ["流陀", "流曲"]))
```

### Low-level Astro Helpers

```python
from izthon.astro import (
    get_five_elements_class,
    get_horoscope,
    get_palace_names,
    get_soul_and_body,
)

print(get_palace_names(0))
print(get_five_elements_class("丙", "寅"))
print(get_soul_and_body(solar_date="2023-8-15", time_index=0, fix_leap=True))
decadals, ages = get_horoscope(solar_date="2023-8-15", time_index=0, gender="女", fix_leap=True)
print(decadals[0], ages[0])

# `rearrange_astrolabe(...)` is the low-level primitive behind `plate="earth"` and `plate="human"`.
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
from izthon.astro import get_config, reset_config, set_config

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
reset_config()
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

### Direct i18n Helpers

```python
from izthon.i18n import get_language, kot, set_language, t, translate

set_language("en-US")
print(get_language())
print(t("soulPalace"))
print(translate("bodyPalace"))
print(kot("female"))
```

## Lunar Conversion (lunar_lite)

`izthon.lunar_lite` is a Python port of `lunar-lite` (range: 1900..2100).

```python
from izthon.lunar_lite import (
    Options,
    get_heavenly_stem_and_earthly_branch_by_lunar_date,
    get_heavenly_stem_and_earthly_branch_by_solar_date,
    get_sign,
    get_total_days_of_lunar_month,
    get_zodiac,
    lunar_to_solar,
    solar_to_lunar,
)

print(solar_to_lunar("2023-4-1").to_chinese())  # 二〇二三年闰二月十一
print(lunar_to_solar("2023-2-11", is_leap_month=True).isoformat())  # 2023-4-1
print(get_sign("2023-9-5"))
print(get_zodiac("卯"))
print(get_total_days_of_lunar_month("2023-4-1"))

options = Options(year="exact", month="exact")
print(get_heavenly_stem_and_earthly_branch_by_solar_date("2025-2-3", 12, options).yearly)
print(get_heavenly_stem_and_earthly_branch_by_lunar_date("2023-2-11", 2, True, options).daily)
```

Data classes exported by `izthon.lunar_lite`:

- `LunarDate`
- `SolarDate`
- `HeavenlyStemAndEarthlyBranchDate`
- `Options`

## Low-level Modules

### `izthon.star`

- Container: `init_stars()`
- Location helpers: `get_start_index()`, `get_lu_yang_tuo_ma_index()`, `get_kui_yue_index()`, `get_zuo_you_index()`, `get_chang_qu_index()`, `get_daily_star_index()`, `get_timely_star_index()`, `get_kong_jie_index()`, `get_huo_ling_index()`, `get_luan_xi_index()`, `get_huagai_xianchi_index()`, `get_gu_gua_index()`, `get_yearly_star_index()`, `get_tianshi_tianshang_index()`, `get_nianjie_index()`, `get_monthly_star_index()`, `get_chang_qu_index_by_heavenly_stem()`, `get_jiesha_adj_index()`, `get_dahao_index()`
- Star builders: `get_major_star()`, `get_minor_star()`, `get_adjective_star()`
- Decorative / cycle helpers: `get_changsheng_12_start_index()`, `get_jiangqian_12_start_index()`, `get_changsheng_12()`, `get_boshi_12()`, `get_yearly_12()`, `get_horoscope_star()`

### `izthon.util`

- Index helpers: `fix_index()`, `earthly_branch_index_to_palace_index()`, `fix_earthly_branch_index()`, `fix_lunar_month_index()`, `fix_lunar_day_index()`, `get_age_index()`
- Brightness / mutagen helpers: `get_brightness()`, `get_mutagen()`, `get_mutagens_by_heavenly_stem()`
- Misc helpers: `merge_stars()`, `time_to_index()`, `translate_chinese_date()`

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
