from __future__ import annotations


def fix_index(index: int, max_value: int = 12) -> int:
    """Clamp an index into [0, max_value) using the same recursive semantics as the TS version."""
    if index < 0:
        return fix_index(index + max_value, max_value)
    if index > max_value - 1:
        return fix_index(index - max_value, max_value)
    return index

