from __future__ import annotations

import pytest

from izthon.util import (
    earthly_branch_index_to_palace_index,
    fix_earthly_branch_index,
    fix_index,
    get_age_index,
    get_brightness,
    time_to_index,
)


def test_fix_index():
    assert fix_index(1) == 1
    assert fix_index(11) == 11
    assert fix_index(15, 20) == 15
    assert fix_index(-2) == 10
    assert fix_index(-3) == 9
    assert fix_index(-13) == 11
    assert fix_index(-2, 10) == 8
    assert fix_index(-3, 10) == 7
    assert fix_index(-15, 10) == 5
    assert fix_index(-27, 10) == 3
    assert fix_index(12) == 0
    assert fix_index(13) == 1
    assert fix_index(23) == 11
    assert fix_index(23, 10) == 3
    assert fix_index(37, 10) == 7


def test_get_brightness():
    assert get_brightness("破军", fix_earthly_branch_index("午")) == "庙"
    assert get_brightness("太阴", fix_earthly_branch_index("酉")) == "不"
    assert get_brightness("天机", fix_earthly_branch_index("未")) == "陷"
    assert get_brightness("天府", fix_earthly_branch_index("申")) == "得"
    assert get_brightness("廉贞", fix_earthly_branch_index("子")) == "平"
    assert get_brightness("陀罗", fix_earthly_branch_index("亥")) == "陷"
    assert get_brightness("擎羊", fix_earthly_branch_index("亥")) == ""
    assert get_brightness("擎羊", fix_earthly_branch_index("酉")) == "陷"


@pytest.mark.parametrize(
    ("hour", "expected"),
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 2),
        (5, 3),
        (6, 3),
        (7, 4),
        (8, 4),
        (9, 5),
        (10, 5),
        (11, 6),
        (12, 6),
        (13, 7),
        (14, 7),
        (15, 8),
        (16, 8),
        (17, 9),
        (18, 9),
        (19, 10),
        (20, 10),
        (21, 11),
        (22, 11),
        (23, 12),
    ],
)
def test_time_to_index(hour: int, expected: int):
    assert time_to_index(hour) == expected


def test_get_age_index():
    cases = {
        "yin": 2,
        "woo": 2,
        "xu": 2,
        "shen": 8,
        "zi": 8,
        "chen": 8,
        "si": 5,
        "you": 5,
        "chou": 5,
        "hai": 11,
        "mao": 11,
        "wei": 11,
    }

    for k, v in cases.items():
        assert get_age_index(k) == v


def test_earthly_branch_index_to_palace_index():
    cases = {
        "yin": 0,
        "mao": 1,
        "chen": 2,
        "si": 3,
        "woo": 4,
        "wei": 5,
        "shen": 6,
        "you": 7,
        "xu": 8,
        "hai": 9,
        "zi": 10,
        "chou": 11,
    }

    for k, v in cases.items():
        assert earthly_branch_index_to_palace_index(k) == v

