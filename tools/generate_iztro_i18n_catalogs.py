#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


def _parse_ts_default_object(path: Path) -> dict[str, str]:
    """Parse a very small subset of TS/JS object-literal syntax used in iztro locales.

    Expected format:
      export default {
        key: 'value',
        ...
      } as const;
    """
    text = path.read_text(encoding="utf-8")
    # Remove /* */ and // comments (good enough for these locale files).
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"//.*", "", text)

    m = re.search(r"\{(.*)\}", text, flags=re.S)
    if not m:
        raise RuntimeError(f"Cannot find object literal in {path}")

    body = m.group(1)
    out: dict[str, str] = {}
    pair_re = re.compile(r"^([A-Za-z0-9_]+)\s*:\s*'((?:\\'|[^'])*)'\s*,?$")

    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith("..."):
            continue
        m2 = pair_re.match(line)
        if not m2:
            continue
        key, val = m2.group(1), m2.group(2)
        out[key] = val.replace("\\'", "'")
    return out


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    src_locales = repo_root / "ref" / "iztro-main" / "src" / "i18n" / "locales"
    out_dir = repo_root / "src" / "izthon" / "i18n" / "_catalogs"
    out_dir.mkdir(parents=True, exist_ok=True)

    langs = ["en-US", "ja-JP", "ko-KR", "zh-CN", "zh-TW", "vi-VN"]
    merge_order = [
        "fiveElementsClass",
        "heavenlyStem",
        "earthlyBranch",
        "brightness",
        "mutagen",
        "star",
        "palace",
        "gender",
    ]

    for lang in langs:
        lang_dir = src_locales / lang
        catalog: dict[str, str] = {}

        catalog.update(json.loads((lang_dir / "common.json").read_text(encoding="utf-8")))
        for name in merge_order:
            catalog.update(_parse_ts_default_object(lang_dir / f"{name}.ts"))

        (out_dir / f"{lang}.json").write_text(
            json.dumps(catalog, ensure_ascii=False, indent=2, sort_keys=False),
            encoding="utf-8",
        )
        print(f"{lang}: {len(catalog)} entries")


if __name__ == "__main__":
    main()

