# izthon

[English README](README.md)

`izthon` 是 TypeScript 库 `iztro`（紫微斗数排盘库）的纯 Python 复刻实现。
项目以 TS 版源码与测试作为“规格”，但 Python 运行时完全不依赖任何 TS 代码。

## 设计目标

- 纯 Python 实现；TS 代码仅作为规格参考（不依赖 TS 运行时代码）。
- 对外只提供 Python 风格 `snake_case` API（不提供 TS 同名别名）。
- 内置 i18n 使用 Python 标准库 `gettext` 语义，并提供 iztro 兼容的 `kot()` 反查能力。
- 用 pytest 覆盖核心能力，并用 `uv` 管理依赖/环境。

## 环境要求

- Python >= 3.12
- `uv`（推荐；本仓库默认用 uv 管理环境与依赖）

## 安装 / 运行

### 在本仓库直接运行（开发模式）

```bash
uv run python -c "from izthon.astro import by_solar; print(by_solar('2000-8-16', 2, '女').five_elements_class)"
```

### 作为依赖使用（uv）

在另一个项目中（示例）：

```bash
# 本地 editable（开发推荐）
uv add --editable /path/to/izthon
```

## 快速开始

### 通过公历排盘（by_solar）

```python
from izthon.astro import by_solar

astrolabe = by_solar("2000-8-16", time_index=2, gender="女")
print(astrolabe.lunar_date)          # 二〇〇〇年七月十七
print(astrolabe.chinese_date)        # 庚辰 甲申 丙午 庚寅
print(astrolabe.five_elements_class) # 木三局
```

### 通过农历排盘（by_lunar）

```python
from izthon.astro import by_lunar

# lunar_date: "YYYY-M-D"，闰月日期用 is_leap_month=True
astrolabe = by_lunar("2023-2-20", time_index=4, gender="女", is_leap_month=True)
```

## 主要 API（`izthon.astro`）

入口函数：

- `by_solar(solar_date, time_index, gender, fix_leap=True, language=None) -> FunctionalAstrolabe`
- `by_lunar(lunar_date, time_index, gender, is_leap_month=False, fix_leap=True, language=None) -> FunctionalAstrolabe`
- `with_options(option: dict) -> FunctionalAstrolabe`
  - `option["type"]`：`"solar"` | `"lunar"`（默认 `"solar"`）
  - `option["date_str"]`：日期字符串
  - `option["time_index"]`：`0..12`
  - `option["gender"]`：例如 `"male"` / `"female"` / `"男"` / `"女"`
  - `option["is_leap_month"]`：农历闰月标记
  - `option["fix_leap"]`：闰月修正
  - `option["language"]`：`"zh-CN"`, `"en-US"` 等
  - `option["astro_type"]`：`"earth"` | `"human"`（可选：天地人盘重排）
  - `option["config"]`：配置字典（见“全局配置”）
- 常用辅助查询：
  - `get_zodiac_by_solar_date(...)`
  - `get_sign_by_solar_date(...)`, `get_sign_by_lunar_date(...)`
  - `get_major_star_by_solar_date(...)`, `get_major_star_by_lunar_date(...)`

### with_options（含天地人盘重排）

```python
from izthon.astro import with_options

astrolabe = with_options(
    {
        "type": "solar",
        "date_str": "1979-08-21",
        "time_index": 7,
        "gender": "male",
        # 可选：本次运行设置 config（注意：config 为全局状态）
        "config": {"algorithm": "zhongzhou"},
        # 可选：天地人盘重排
        "astro_type": "earth",  # 或 "human"
    }
)
```

### 常用辅助接口（生肖/星座/命宫主星等）

```python
from izthon.astro import (
    get_major_star_by_lunar_date,
    get_major_star_by_solar_date,
    get_sign_by_lunar_date,
    get_sign_by_solar_date,
    get_zodiac_by_solar_date,
)

print(get_zodiac_by_solar_date("2023-2-20"))                    # 兔
print(get_zodiac_by_solar_date("2023-2-20", "en-US"))           # rabbit
print(get_sign_by_solar_date("2023-9-5"))                       # 处女座
print(get_sign_by_lunar_date("2023-2-3", is_leap_month=True))   # 白羊座（闰月）

print(get_major_star_by_solar_date("1987-05-16", 7))            # 天机,天梁
print(get_major_star_by_lunar_date("2023-2-17", 0, True))       # 贪狼
```

## 核心对象与概念

主要 API 都在 `izthon.astro`：

- `FunctionalAstrolabe`：`by_solar()` / `by_lunar()` 返回的星盘对象
- `FunctionalPalace`：12 宫位，通过 `astrolabe.palace(...)` 获取
- `FunctionalStar`：星曜对象，通过 `astrolabe.star(...)` 或 `palace.major_stars` 等访问
- `FunctionalHoroscope`：运限视图，通过 `astrolabe.horoscope(...)` 获取
- `FunctionalSurpalaces`：三方四正，通过 `astrolabe.surrounded_palaces(...)` 获取

### 查询宫位 / 星曜 / 三方四正

```python
from izthon.astro import by_solar

astrolabe = by_solar("2023-8-15", 0, "女")

ming = astrolabe.palace("命宫")
print(ming.name, ming.heavenly_stem, ming.earthly_branch)
print([s.name for s in ming.major_stars])

ziwei = astrolabe.star("紫微")
print(ziwei.palace().name)

sur = astrolabe.surrounded_palaces("命宫")
print(sur.opposite.name, sur.wealth.name, sur.career.name)
print(sur.have(["武曲", "贪狼"]))         # 是否全部包含
print(sur.have_one_of(["太阳", "文曲"]))  # 是否命中其一
```

### 运限（大限/流年/流月/流日/流时）

```python
from izthon.astro import by_solar

astrolabe = by_solar("2000-8-16", 2, "女")
horoscope = astrolabe.horoscope("2023-8-19 3:12")

print(horoscope.decadal.index, horoscope.decadal.heavenly_stem, horoscope.decadal.earthly_branch)
print(horoscope.yearly.index, horoscope.yearly.heavenly_stem, horoscope.yearly.earthly_branch)

# 运限星曜/四化查询
print(horoscope.has_horoscope_stars("疾厄", "decadal", ["流陀", "流曲", "运昌"]))
print(horoscope.has_horoscope_mutagen("兄弟", "decadal", "禄"))
```

## 参数与约定

### time_index（0..12）

`time_index` 使用 iztro 约定的时辰序号（含早晚子时）。

| time_index | 中文 | 时间段 |
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

辅助函数：

```python
from izthon.util import time_to_index
print(time_to_index(23))  # 12
```

### gender

`gender` 支持任何已内置语言的输入（例如 `"male"`/`"female"`、`"男"`/`"女"`），因为内部通过 `kot()` 做了反查归一化。

### 闰月修正（fix_leap）

`fix_leap=True` 时，会按 iztro 的逻辑处理闰月：闰月在 15 之后的日期，部分安星/定位会按“下一个月”处理（`time_index==12` 另有边界规则）。

## 全局配置（config）

配置为全局状态（与 iztro 一致）。使用 `izthon.astro.config()`：

```python
from izthon.astro import config, get_config

config(
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

也可以配置：

- `mutagens`：按年干自定义四化（禄/权/科/忌）所对应的 4 颗星
- `brightness`：按星曜自定义 12 宫亮度（每宫 1 个值）

上述配置的 key/value 同样支持多语言输入。

## 多语言（i18n）

支持语言：

- `en-US`, `ja-JP`, `ko-KR`, `zh-CN`, `zh-TW`, `vi-VN`

两种切换方式：

1) 调用时传 `language`：

```python
from izthon.astro import by_solar
print(by_solar("2000-8-16", 2, "女", language="vi-VN").chinese_date)
```

2) 设置全局语言：

```python
from izthon.i18n import set_language
set_language("ko-KR")
```

注意：语言是全局状态；若同一进程内混用多语言，请显式调用 `set_language(...)` 或在每次调用时传 `language=...`。

## 插件（Plugins）

插件同样是全局注册，对每个新生成的 `FunctionalAstrolabe` 都会自动应用。
Python 插件签名为：`plugin(astrolabe) -> None`。

```python
from izthon.astro import by_solar, load_plugin

def my_plugin(astrolabe) -> None:
    astrolabe.my_new_func = lambda: astrolabe.five_elements_class

load_plugin(my_plugin)
astrolabe = by_solar("2023-10-18", 4, "female")
print(astrolabe.my_new_func())
```

## 农历转换（lunar_lite）

`izthon.lunar_lite` 是 `lunar-lite` 的 Python 复刻（支持范围 1900..2100）。

```python
from izthon.lunar_lite import lunar_to_solar, solar_to_lunar

print(solar_to_lunar("2023-4-1").to_string(True))  # 二〇二三年闰二月十一
print(lunar_to_solar("2023-2-11", is_leap_month=True).to_string())  # 2023-4-1
```

## 开发与测试

运行测试：

```bash
uv run --extra dev pytest
```

如果你更新了上游 iztro 的多语言资源，需要重新生成 catalogs：

```bash
uv run python tools/generate_iztro_i18n_catalogs.py --src-locales /path/to/iztro/src/i18n/locales
```

## 对齐版本 / 致谢

本项目以以下版本的行为与测试为对齐目标（作为规格参考）：

- `iztro@2.5.7`
- `lunar-lite@0.2.8`
