from __future__ import annotations, division, print_function, unicode_literals

import pytest

from extended_data_types.nothing_utils import (
    all_non_empty,
    any_non_empty,
    are_nothing,
    first_non_empty,
    is_nothing,
    yield_non_empty,
)


@pytest.mark.parametrize(
    "value, expected",
    [
        (None, True),
        ("", True),
        ({}, True),
        ([], True),
        ("   ", True),
        (0, False),
        ("non-empty", False),
        ([None, ""], True),
        ([1, 2], False),
    ],
)
def test_is_nothing(value, expected):
    assert is_nothing(value) == expected


@pytest.mark.parametrize(
    "values, expected",
    [
        ((None, "", [], {}), []),
        ((None, "value", 0, "another"), ["value", 0, "another"]),
        ((1, 2, None), [1, 2]),
    ],
)
def test_all_non_empty(values, expected):
    assert all_non_empty(*values) == expected


@pytest.mark.parametrize(
    "values, expected",
    [
        ((None, "", [], {}), True),
        ((None, "value", 0, "another"), False),
        ((1, 2, None), False),
    ],
)
def test_are_nothing(values, expected):
    assert are_nothing(*values) == expected


@pytest.mark.parametrize(
    "values, expected",
    [
        ((None, "", "value", "another"), "value"),
        ((None, "", [], {}), None),
        ((1, 2, None), 1),
    ],
)
def test_first_non_empty(values, expected):
    assert first_non_empty(*values) == expected


@pytest.mark.parametrize(
    "mapping, keys, expected",
    [
        ({"key1": None, "key2": "value"}, ("key1", "key2"), {"key2": "value"}),
        ({"key1": None, "key2": None}, ("key1", "key2"), {}),
        ({"key1": "value1", "key2": "value2"}, ("key3", "key1"), {"key1": "value1"}),
    ],
)
def test_any_non_empty(mapping, keys, expected):
    assert any_non_empty(mapping, *keys) == expected


def test_yield_non_empty():
    mapping = {"key1": None, "key2": "value", "key3": "another"}
    keys = ("key1", "key2", "key3")
    expected = [{"key2": "value"}, {"key3": "another"}]
    result = list(yield_non_empty(mapping, *keys))
    assert result == expected
