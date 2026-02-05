#!/usr/bin/env python3
from __future__ import annotations

import argparse
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


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Generate iztro i18n JSON catalogs for izthon.")
    parser.add_argument(
        "--src-locales",
        required=True,
        help="Path to the upstream iztro locales directory: <iztro>/src/i18n/locales",
    )
    parser.add_argument(
        "--out-dir",
        default=str(Path(__file__).resolve().parents[1] / "src" / "izthon" / "i18n" / "_catalogs"),
        help="Output directory for generated JSON catalogs (default: izthon's built-in catalogs dir).",
    )
    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parents[1]
    src_locales = Path(args.src_locales)
    if not src_locales.is_absolute():
        src_locales = (repo_root / src_locales).resolve()
    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = (repo_root / out_dir).resolve()

    if not src_locales.is_dir():
        raise SystemExit(f"--src-locales is not a directory: {src_locales}")

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
