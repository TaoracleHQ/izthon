izthon
======

`izthon` is a Python re-implementation of the TypeScript library `iztro` (Zi Wei Dou Shu astrolabe generator).

Design goals
------------
- No runtime dependency on the TypeScript implementation (pure Python).
- Public APIs are Pythonic `snake_case` (no TS-style aliases).
- Built-in i18n uses stdlib `gettext` semantics, with a `kot()` reverse-lookup helper to match iztro behavior.

Quick start (dev)
-----------------
Run from source:

```bash
PYTHONPATH=src python3 -c "from izthon.astro import by_solar; print(by_solar('2000-8-16', 2, '女').five_elements_class)"
```

Run smoke tests:

```bash
PYTHONPATH=src python3 tools/run_smoke_tests.py
```
