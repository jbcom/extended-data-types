"""
This module contains test functions for verifying the functionality of various utility functions for handling
"nothing" values using the `extended_data_types` package. It includes parameterized tests for checking emptiness,
filtering non-empty values, and more.

Functions:
    - test_is_nothing: Tests determining if a value is considered "nothing".
    - test_all_non_empty: Tests retrieving all non-empty values from a set of inputs.
    - test_are_nothing: Tests determining if all values in a set of inputs are "nothing".
    - test_first_non_empty: Tests retrieving the first non-empty value from a set of inputs.
    - test_any_non_empty: Tests retrieving any non-empty values from a mapping given a set of keys.
    - test_yield_non_empty: Tests yielding non-empty values from a mapping given a set of keys.
"""

from __future__ import annotations

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
    ("value", "expected"),
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
def test_is_nothing(value: any, expected: bool) -> None:
    """
    Tests determining if a value is considered "nothing".

    Args:
        value (any): The value to check.
        expected (bool): The expected result indicating if the value is "nothing".

    Asserts:
        The result of is_nothing matches the expected boolean value.
    """
    assert is_nothing(value) == expected


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ((None, "", [], {}), []),
        ((None, "value", 0, "another"), ["value", 0, "another"]),
        ((1, 2, None), [1, 2]),
    ],
)
def test_all_non_empty(values: tuple, expected: list) -> None:
    """
    Tests retrieving all non-empty values from a set of inputs.

    Args:
        values (tuple): A tuple of values to check.
        expected (list): The expected list of non-empty values.

    Asserts:
        The result of all_non_empty matches the expected list of non-empty values.
    """
    assert all_non_empty(*values) == expected


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ((None, "", [], {}), True),
        ((None, "value", 0, "another"), False),
        ((1, 2, None), False),
    ],
)
def test_are_nothing(values: tuple, expected: bool) -> None:
    """
    Tests determining if all values in a set of inputs are "nothing".

    Args:
        values (tuple): A tuple of values to check.
        expected (bool): The expected result indicating if all values are "nothing".

    Asserts:
        The result of are_nothing matches the expected boolean value.
    """
    assert are_nothing(*values) == expected


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ((None, "", "value", "another"), "value"),
        ((None, "", [], {}), None),
        ((1, 2, None), 1),
    ],
)
def test_first_non_empty(values: tuple, expected: any) -> None:
    """
    Tests retrieving the first non-empty value from a set of inputs.

    Args:
        values (tuple): A tuple of values to check.
        expected (any): The expected first non-empty value.

    Asserts:
        The result of first_non_empty matches the expected first non-empty value.
    """
    assert first_non_empty(*values) == expected


@pytest.mark.parametrize(
    ("mapping", "keys", "expected"),
    [
        ({"key1": None, "key2": "value"}, ("key1", "key2"), {"key2": "value"}),
        ({"key1": None, "key2": None}, ("key1", "key2"), {}),
        ({"key1": "value1", "key2": "value2"}, ("key3", "key1"), {"key1": "value1"}),
    ],
)
def test_any_non_empty(mapping: dict, keys: tuple, expected: dict) -> None:
    """
    Tests retrieving any non-empty values from a mapping given a set of keys.

    Args:
        mapping (dict): The mapping to check.
        keys (tuple): The keys to look for in the mapping.
        expected (dict): The expected mapping of non-empty values.

    Asserts:
        The result of any_non_empty matches the expected mapping of non-empty values.
    """
    assert any_non_empty(mapping, *keys) == expected


def test_yield_non_empty() -> None:
    """
    Tests yielding non-empty values from a mapping given a set of keys.

    Asserts:
        The result of yield_non_empty matches the expected list of non-empty mappings.
    """
    mapping = {"key1": None, "key2": "value", "key3": "another"}
    keys = ("key1", "key2", "key3")
    expected = [{"key2": "value"}, {"key3": "another"}]
    result = list(yield_non_empty(mapping, *keys))
    assert result == expected
