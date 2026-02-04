# iztro (TypeScript) -> izthon (Python) 迁移计划

目标：在不依赖任何 TypeScript 运行时代码的前提下，用 Python 复刻 `ref/iztro-main`（紫微斗数排盘）与其关键依赖 `ref/lunar-lite-main`（公历/农历转换与干支计算）的全部核心能力；以 TS 源码与测试用例作为“规格”，用 Python 实现同等输出与行为。

本计划以 `iztro@2.5.7` 与 `lunar-lite@0.2.8` 为对齐版本（见各自 `package.json`）。

---

## 0. 定义迁移范围（以 TS 作为规格）

### 0.1 需要复刻的对外 API（最小可用 + 完整对齐）

对齐 `ref/iztro-main/src/index.ts` 的模块形态：

- `data`：常量与数据表（天干地支、宫位、星耀信息、四化、五行局、五虎遁/五鼠遁、地支/天干附带信息等）。
- `util`：索引修正、闰月修正、亮度/四化查询、干支文本格式化、流耀合并、时辰换算等。
- `star`：主星/辅星/杂耀/装饰星（长生12、博士12、流年岁前/将前诸星、流耀等）的定位与生成。
- `astro`：排盘入口（`by_solar`/`by_lunar`/`with_options` 等）、配置（`config/get_config`）、插件系统、重排（天地人盘）、以及围绕星盘的对象模型（星盘/宫位/星曜/三方四正/运限）。

对齐 `ref/lunar-lite-main/src/index.ts` 的模块形态：

- `convertor`：`normalizeDateStr`、`solar2lunar`、`lunar2solar`
- `ganzhi`：`getHeavenlyStemAndEarthlyBranchBySolarDate`、`getHeavenlyStemAndEarthlyBranchByLunarDate`（支持 year/month 分界配置）
- `misc`：`getSign`、`getZodiac`、`getTotalDaysOfLunarMonth`

### 0.2 必须对齐的行为点（来自 TS 源码/测试）

来自 `ref/iztro-main/src/astro/astro.ts` / `FunctionalAstrolabe.ts` 等：

- `time_index` 取值 `0..12`（TS: `timeIndex`），其中 `12` 为“晚子时”。
- 全局配置项（Python 参数名；括号内为 TS 同义项）：
  - `year_divide`（TS: `yearDivide`）: `normal | exact`（正月初一 vs 立春分界）
  - `horoscope_divide`（TS: `horoscopeDivide`）: `normal | exact`（运限的年/月分界）
  - `age_divide`（TS: `ageDivide`）: `normal | birthday`（虚岁分界）
  - `day_divide`（TS: `dayDivide`）: `current | forward`（晚子时算当日/次日）
  - `algorithm`: `default | zhongzhou`（通行 vs 中州派差异）
  - `mutagens/brightness` 允许按“任意语言输入”配置（通过 `kot` 反查 key）。
- 插件：`astro.load_plugin(some_fn)`，生成的星盘 `astrolabe.use(plugin)` 会以“this=astrolabe”的方式执行插件（TS 里用 `plugin.apply(this)`）。
- `rearrange_astrolabe` 与 `with_options(astro_type="earth"|"human")` 的重排逻辑。

来自 `ref/lunar-lite-main/src/__tests__`：

- 日期解析 `normalizeDateStr` 支持 `YYYY-M-D`、`YYYY-MM-DD`、`YYYY.M/D HH:mm:ss` 等混合分隔符。
- `solar2lunar` 年份限定 `1900..2100` 且日期必须在 `1900-01-31` 之后；异常信息与边界行为以测试为准。
- 干支计算支持 `options.year`（normal/exact）与 `options.month`（normal/exact）。

---

## 1. Python 端总体架构设计

### 1.1 包结构（建议）

在 `src/izthon/` 下实现：

- `izthon/data/`：常量与数据表（从 TS 数据移植成 Python 常量）。
- `izthon/i18n/`：语言资源、`t()` 翻译、`kot()` 反查、`set_language()`。
- `izthon/lunar_lite/`：Python 版 `lunar-lite`（不依赖 TS）。
- `izthon/utils/`：通用工具函数（`fix_index`、闰月修正、格式化等）。
- `izthon/star/`：星曜定位与生成（major/minor/adjective/decorative/horoscope）。
- `izthon/astro/`：排盘主逻辑与对象模型（Astrolabe/Palace/Star/Surpalaces/Horoscope）。
- `izthon/__init__.py`：对齐 TS 的导出风格：`data/star/util/astro`。

### 1.2 命名策略：仅 Python（snake_case）

- 对外 API 仅提供 Python 风格的 `snake_case`（不提供与 TS 同名的别名）。
- 内部实现同样采用 `snake_case`，并在文档中提供“TS 名称 -> Python 名称”对照表，方便核对规格与回归测试。

### 1.3 类型与对象模型

用 `dataclasses` + 显式方法实现：

- `FunctionalStar`：name/type/scope/brightness/mutagen + palace/astrolabe 关联方法 + 查询方法（`with_brightness/with_mutagen`）。
- `FunctionalPalace`：宫位字段 + `has/not_have/has_one_of` + 四化飞化/自化相关方法。
- `FunctionalSurpalaces`：target/opposite/wealth/career + `have/not_have/have_one_of`。
- `FunctionalHoroscope`：各运限 scope 数据 + 查询方法（`palace/surround_palaces/has_horoscope_stars/has_horoscope_mutagen`）。
- `FunctionalAstrolabe`：星盘主对象 + `horoscope()` + `palace()` + `star()` + `surrounded_palaces()` + 插件 `use()`。

原则：数据结构与行为对齐 TS；内部实现保持可测试、可拆分。

---

## 2. 迁移步骤（分阶段交付）

### Phase A：冻结规格与验收基线（1-2 天）

1) 盘点 TS 公开 API 与关键行为：
   - 以 `ref/iztro-main/src/index.ts`、`ref/iztro-main/src/astro/astro.ts`、`ref/iztro-main/src/star/index.ts`、`ref/lunar-lite-main/src/index.ts` 为准。
2) 将 TS 测试用例映射为 Python 验收用例清单：
   - `ref/lunar-lite-main/src/__tests__/*` => `tests/test_lunar_lite_*.py`
   - `ref/iztro-main/src/__tests__/*` => `tests/test_iztro_*.py`
3) 选定“对齐优先级”：
   - 第一优先：计算结果（宫位、星曜分布、四化、干支、日期字符串）。
   - 第二优先：API 形态与方法名（遵循 Python `snake_case`，不做 TS 别名兼容）。
   - 第三优先：错误信息/异常文本（能对齐则对齐）。

交付物：`docs/plans` 下补充一份“验收用例索引”（可直接链接到将要写的 pytest 文件）。

### Phase B：移植 lunar-lite（核心基础设施）（3-7 天，风险最高）

目标：实现 Python `izthon.lunar_lite`，对齐 `lunar-lite`（你提到的 “LunarLight”）的功能与测试。

#### B1. API 与数据结构

- `normalize_date_str(date: str | datetime) -> list[int]`
- `solar_to_lunar(date: str|datetime) -> LunarDate`
- `lunar_to_solar(date_str: str, is_leap_month: bool=False) -> SolarDate`
- `get_total_days_of_lunar_month(solar_date_str: str) -> int`
- `get_sign(solar_date_str: str) -> str`
- `get_zodiac(earthly_branch: str) -> str`
- `get_heavenly_stem_and_earthly_branch_by_solar_date(date, time_index, options) -> HeavenlyStemAndEarthlyBranchDate`
- `get_heavenly_stem_and_earthly_branch_by_lunar_date(date_str, time_index, is_leap, options) -> ...`

其中 `LunarDate/SolarDate/HeavenlyStemAndEarthlyBranchDate` 用 dataclass 表达，并提供 `to_string()`。

#### B2. 实现策略（按 lunar-lite 规格实现，Python 内部自带）

按你的要求：直接参照 `ref/lunar-lite-main` 的接口与测试用例，在 Python 内部实现同等能力（不依赖任何 TS 端运行时代码）。

注意：TS 版 `lunar-lite` 实际上依赖 `lunar-typescript` 来完成核心的历法/节气/干支计算（`ref/lunar-lite-main/src/*` 只是薄封装）。因此 Python 侧不能“逐行翻译 TS 实现”就完成迁移，需要实现其底层算法以达到相同输出。

计划实现点：

- 内置 1900-2100 的农历年数据（闰月、大小月、与公历的对齐基准），完成 `solar_to_lunar/lunar_to_solar/get_total_days_of_lunar_month`。
- 实现四柱干支：
  - 年柱：`options.year="normal"`（正月初一分界）与 `options.year="exact"`（立春分界）。
  - 月柱：`options.month="normal"`（按初一 + 闰月修正，等价于 TS 的 `calculateMonthlyGanZhi`）与 `options.month="exact"`（按节气分界）。
  - 日柱：按基准日推算并校验（以 `ref/lunar-lite-main` 测试数据回归）。
  - 时柱：按 `time_index`（0..12）对应小时区间推算。

实现原则：以 `ref/lunar-lite-main/src/__tests__/*.test.ts` 的断言作为硬基线；任何不一致都以补齐算法/边界为准，而不是“改测试/改输出”。

（可选保底方案，需你明确同意才启用）：如果纯自研在节气精确交界时刻上出现不可接受的偏差，可考虑将一个成熟的纯 Python 历法实现以 vendoring 形式放入 `izthon/lunar_lite/_vendor/`，并在 LICENSE/NOTICE 中注明来源与许可，用它来保证与 `lunar-typescript` 的一致性。

#### B3. 验收

- 逐条复刻 `ref/lunar-lite-main/src/__tests__/*.test.ts` 的断言数据（尤其是 1900 边界、闰月、2026-02-05 立春分界用例）。

交付物：`izthon/lunar_lite/*` + pytest 测试全绿。

### Phase C：移植 iztro 的 i18n 与数据表（2-4 天）

#### C1. 数据表迁移

从以下 TS 文件迁移为 Python 常量（保持 key 一致）：

- `ref/iztro-main/src/data/constants.ts`
- `ref/iztro-main/src/data/heavenlyStems.ts`
- `ref/iztro-main/src/data/earthlyBranches.ts`
- `ref/iztro-main/src/data/stars.ts`

#### C2. i18n 迁移（建议使用 gettext + 自建 kot 反查）

可以使用 Python 自带的 `gettext`，但需要补齐 iztro 特有的 `kot()` 反查能力。

目标：实现与 TS `t/kot/setLanguage` 等价的能力（Python 对应：`t/kot/set_language`）。

- 使用 `gettext`：将 `ref/iztro-main/src/i18n/locales/**` 的键值对转换为 `.po/.mo`（`msgid=key`, `msgstr=翻译`），并提供 `set_language(lang)` 切换当前语言。
- 实现 `t(key)`：直接调用当前语言的 gettext 翻译（与 TS `t()` 等价）。
- 实现 `kot(value, k_prefix=None)`：
  - 启动时加载所有支持语言的 catalog，构建 `value -> key` 的反查索引（按 TS 的资源遍历顺序：en-US, ja-JP, ko-KR, zh-CN, zh-TW, vi-VN）。
  - 支持 `k_prefix` 过滤（等价于 TS 的 `kot(value, k?)` 中 `transKey.includes(k)` 行为），用于消歧（如 Heavenly/Earthly）。
- 保证 `translate_chinese_date()` 的格式分支与 TS 一致（长度>1 的语言使用 `A B - C D` 形式）。

备注：gettext 原生不提供“按翻译值反查 msgid”，因此 `kot()` 必须由我们自行建立索引；这是 iztro 允许“跨语言输入配置/星名”的关键能力。

交付物：`izthon/i18n/*`，并通过 iztro 相关测试里多语言断言（例如韩/越用例）。

### Phase D：移植 utils + star 定位算法（3-6 天）

#### D1. utils

复刻 `ref/iztro-main/src/utils/index.ts`：

- `fix_index`
- `earthly_branch_index_to_palace_index`
- `fix_earthly_branch_index`
- `fix_lunar_month_index`（依赖 B 阶段的 `solar_to_lunar`）
- `fix_lunar_day_index`
- `time_to_index`
- `get_age_index`
- `merge_stars`
- `get_brightness/get_mutagen/get_mutagens_by_heavenly_stem`（依赖配置 + i18n）
- `translate_chinese_date`（依赖 i18n）

#### D2. star/location

复刻 `ref/iztro-main/src/star/location.ts` 的所有索引算法：

- `get_start_index`（紫微/天府起星，强依赖 lunar-lite 的农历日与当月天数）
- `get_lu_yang_tuo_ma_index / get_kui_yue_index / get_zuo_you_index / get_chang_qu_index`
- `get_daily_star_index / get_timely_star_index / get_kong_jie_index / get_huo_ling_index`
- `get_luan_xi_index / get_huagai_xianchi_index / get_gu_gua_index`
- `get_yearly_star_index`（含中州派差异、天使天伤差异、截空/劫杀/大耗等）
- `get_monthly_star_index`
- `get_chang_qu_index_by_heavenly_stem`

验收：移植 `ref/iztro-main/src/__tests__/star/location.test.ts`。

#### D3. star 生成

- `get_major_star`（紫微系/天府系）
- `get_minor_star`（14 辅星）
- `get_adjective_star`（38 杂耀 + 中州派差异）
- `get_changsheng_12 / get_boshi_12 / get_yearly_12`
- `get_horoscope_star`

验收：移植 `ref/iztro-main/src/__tests__/star/star.test.ts`。

### Phase E：移植 astro 主流程与对象模型（4-8 天）

复刻 `ref/iztro-main/src/astro/*`：

- `config/get_config/load_plugin(s)`：全局配置与插件注册。
- `by_solar/by_lunar/with_options`：排盘入口。
- `FunctionalAstrolabe`：
  - `star()`：跨语言星名查找（依赖 `kot`）。
  - `palace()` / `surrounded_palaces()`：依赖 analyzer。
  - `horoscope()`：复刻 `_get_horoscope_by_solar_date`（大限/小限/流年/月/日/时索引、闰月/生日分界、流耀/四化）。
- `FunctionalPalace`：
  - `has/not_have/has_one_of`
  - `has_mutagen/not_have_mutagen`
  - `flies_to/not_fly_to/flies_one_of_to`
  - `self_mutaged/self_mutaged_one_of/not_self_mutaged`
  - `mutaged_places`
- `FunctionalHoroscope`：
  - `palace/surround_palaces/has_horoscope_stars/has_horoscope_mutagen`。
- `FunctionalSurpalaces` 与 `analyzer`（三方四正、星曜包含判断、四化反查）。

验收：移植 `ref/iztro-main/src/__tests__/astro/*.test.ts`（含多语言、插件、重排、中州派用例）。

### Phase F：封装、文档与发布准备（1-3 天）

- `README.md`：给出与 TS 等价的 Python 用法示例（solar/lunar、语言、配置、插件、运限查询）。
- 版本策略：从 `0.1.0` 递增；在文档中标注对齐的 iztro/lunar-lite 版本。
- 打包：确保 `pyproject.toml`、`uv.lock`、入口脚本一致；必要时增加 `typing_extensions` 等轻依赖。

---

## 3. 风险点与对策

1) 农历/干支算法差异风险（最高）：
   - 对策：以 `lunar-lite` 测试为硬基线；优先打通 2026-02-05 等节气分界用例；如节气交界精度难以对齐且你同意，则启用 Phase B2 的 vendoring 保底方案。
2) 多语言 `kot()` 反查一致性：
   - 对策：构建“全语言 value->key”索引并加入冲突检测（同 value 多 key 时的处理策略需与 TS 一致）。
3) 晚子时/闰月修正的边界：
   - 对策：将 `day_divide`、`fix_leap`、`time_index==12` 的所有组合加入回归用例。
4) 中州派差异覆盖不足：
   - 对策：以 iztro 自带测试为准，确保 `algorithm="zhongzhou"` 的所有测试覆盖（天使天伤、星曜增删、岁破等）。

---

## 4. 里程碑与验收标准

- M1（完成 Phase B）：`izthon.lunar_lite` 全部 pytest 通过（等价于 `ref/lunar-lite-main` 测试集）。
- M2（完成 Phase C+D）：星曜定位与生成的 pytest 通过（等价于 iztro 的 star/location/star 测试集）。
- M3（完成 Phase E）：星盘生成 + 运限 + 插件 + 多语言 + 中州派全部通过（等价于 iztro 的 astro 测试集）。
- M4（完成 Phase F）：补齐 README 与发布配置；提供最少 3 个端到端示例（solar/lunar、配置、插件）。

---

## 5. 我作为执行者的工作方式（便于你审阅）

- 每个 Phase 都会拆成小 PR/提交：先加测试与骨架，再实现；保证可回滚、可审阅。
- 每次提交都附带：
  - 变更的模块清单
  - 新增/更新的测试点
  - 与 TS 行为对齐的证据（对应 TS 测试用例/断言）

---

## 6. 需要你确认/已确认的决策（审阅时请重点看）

已确认：

1) 对外 API：只提供 Python 风格 `snake_case`，不提供 TS 同名别名。
2) 农历转换：参照 `ref/lunar-lite-main` 的接口与测试，在 Python 内部实现一套 `lunar_lite`（不依赖 TS 端运行时代码）。

仍需你确认：

3) i18n 是否采用 `gettext`（我建议采用）：若采用，则按 Phase C2 的方案实现 `t/kot/set_language`；若不采用，则退回“JSON/dict + 自建索引”的轻量实现。
