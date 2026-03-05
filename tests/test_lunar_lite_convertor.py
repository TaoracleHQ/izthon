from __future__ import annotations

from datetime import date, datetime

import pytest

from izthon.lunar_lite import lunar_to_solar, normalize_date_str, solar_to_lunar


def test_solar_to_lunar():
    cases = {
        "2023-7-29": ("二〇二三年六月十二", "2023-6-12", False),
        "2023-4-1": ("二〇二三年闰二月十一", "2023-2-11", True),
        "2023-4-20": ("二〇二三年三月初一", "2023-3-1", False),
        "2023-3-21": ("二〇二三年二月三十", "2023-2-30", False),
        "2023-1-22": ("二〇二三年正月初一", "2023-1-1", False),
        "2023-1-21": ("二〇二二年腊月三十", "2022-12-30", False),
        "1900-03-01": ("一九〇〇年二月初一", "1900-2-1", False),
        "1921-08-01": ("一九二一年六月廿八", "1921-6-28", False),
        "2020-01-24": ("二〇一九年腊月三十", "2019-12-30", False),
        "2020-01-25": ("二〇二〇年正月初一", "2020-1-1", False),
        "1996-07-15": ("一九九六年五月三十", "1996-5-30", False),
        "1996-07-16": ("一九九六年六月初一", "1996-6-1", False),
        "1995-03-30": ("一九九五年二月三十", "1995-2-30", False),
    }

    for solar, (cn, plain, is_leap) in cases.items():
        res = solar_to_lunar(solar)
        assert res.to_chinese() == cn
        assert res.isoformat() == plain
        assert res.is_leap is is_leap

    with pytest.raises(ValueError) as exc:
        solar_to_lunar("2023-22-22")
    assert str(exc.value) == "wrong month 22"

    with pytest.raises(ValueError) as exc:
        solar_to_lunar("1899-1-22")
    assert str(exc.value) == "year should be between 1900 and 2100."

    with pytest.raises(ValueError) as exc:
        solar_to_lunar("2101-1-22")
    assert str(exc.value) == "year should be between 1900 and 2100."

    with pytest.raises(ValueError) as exc:
        solar_to_lunar("1900-1-22")
    assert str(exc.value) == "date must be after 1900-1-31."


def test_lunar_to_solar():
    cases = {
        "2023-7-29": ("2023-6-12", False),
        "2023-4-1": ("2023-2-11", True),
        "2023-4-20": ("2023-3-1", False),
        "2023-3-21": ("2023-2-30", False),
        "2023-1-22": ("2023-1-1", False),
        "2023-1-21": ("2022-12-30", False),
        "1900-3-1": ("1900-2-1", False),
        "1921-8-1": ("1921-6-28", False),
        "2020-1-24": ("2019-12-30", False),
        "2020-1-25": ("2020-1-1", False),
        "2023-7-30": ("2023-6-13", False),
        "1995-3-30": ("1995-2-30", True),
    }

    for solar, (lunar, is_leap) in cases.items():
        assert lunar_to_solar(lunar, is_leap).isoformat() == solar

    with pytest.raises(ValueError) as exc:
        lunar_to_solar("1899-1-22")
    assert str(exc.value) == "invalid date."

    with pytest.raises(ValueError) as exc:
        lunar_to_solar("2101-1-22")
    assert str(exc.value) == "invalid date."


def test_normalize_date_str():
    cases = {
        "2023-12-1": [2023, 12, 1],
        "1998-01-02": [1998, 1, 2],
        "1987-1-08": [1987, 1, 8],
        "2016-08-18": [2016, 8, 18],
        "1986-7-15 12:23:59": [1986, 7, 15, 12, 23, 59],
        "1986.7/15 12:23:59": [1986, 7, 15, 12, 23, 59],
        "1986.07-15 12:23": [1986, 7, 15, 12, 23],
    }

    for key, expected in cases.items():
        assert normalize_date_str(key) == expected

    assert normalize_date_str(date(2023, 12, 1)) == [2023, 12, 1, 0, 0, 0]
    assert normalize_date_str(datetime(2023, 12, 1, 12)) == [2023, 12, 1, 12, 0, 0]
