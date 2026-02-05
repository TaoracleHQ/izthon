"""
izthon

Python re-implementation of the TypeScript library `iztro` (Zi Wei Dou Shu astrolabe generator).

Public APIs are provided in Pythonic snake_case only.
"""

from __future__ import annotations

import importlib

__all__ = ["astro", "data", "i18n", "lunar_lite", "star", "util", "main"]


def __getattr__(name: str):
    # Lazy import to avoid circular imports while the package is initializing.
    if name in {"astro", "data", "i18n", "lunar_lite", "star", "util"}:
        return importlib.import_module(f"{__name__}.{name}")
    raise AttributeError(name)


def main() -> None:
    # Keep a minimal CLI entrypoint for the project.scripts hook.
    print("izthon: Python toolkit for Zi Wei Dou Shu (Zi Wei Dou Shu astrolabe generator).")
