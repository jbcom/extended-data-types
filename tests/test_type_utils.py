"""
Tests for Type Utilities.

This module contains test functions for verifying the functionality of utility functions
in `type_utils` for handling type-based default values and determining whether to return
primitive or exact types of a given value.

Functions:
    - test_get_default_value_for_type: Tests default values for various types.
    - test_get_primitive_type_for_instance_type: Tests matching instance types to their primitive equivalents.
    - test_typeof: Tests the functionality of the typeof function for both primitive and exact types.
"""

from __future__ import annotations

from typing import Any

import pytest

from extended_data_types.type_utils import (
    get_default_value_for_type,
    get_primitive_type_for_instance_type,
    typeof,
)


@pytest.mark.parametrize(
    ("input_type", "expected"),
    [
        (list, []),
        (dict, {}),
        (str, ""),
        (int, None),
        (float, None),
        (bool, None),
        (set, None),
    ],
)
def test_get_default_value_for_type(input_type: type, expected: Any) -> None:
    """
    Tests default values for various types.

    Args:
        input_type (type): The type for which the default value is retrieved.
        expected (Any): The expected default value.

    Asserts:
        The result of get_default_value_for_type matches the expected default value.
    """
    assert get_default_value_for_type(input_type) == expected


@pytest.mark.parametrize(
    ("instance", "expected_type"),
    [
        ({"a": 1, "b": 2}, dict),
        ({"a", "b", "c"}, set),
        (frozenset({"a", "b", "c"}), set),
        ([1, 2, 3], list),
        ((1, 2, 3), list),
        ("string", str),
        (b"bytes", bytes),
        (1, int),
        (1.0, float),
        (True, bool),
        (None, type(None)),  # Use type(None) to represent NoneType
    ],
)
def test_get_primitive_type_for_instance_type(
    instance: Any, expected_type: type
) -> None:
    """
    Tests matching instance types to their primitive equivalents.

    Args:
        instance (Any): The instance whose type is to be checked.
        expected_type (type): The expected primitive type.

    Asserts:
        The result of get_primitive_type_for_instance_type matches the expected type.
    """
    assert get_primitive_type_for_instance_type(instance) == expected_type


@pytest.mark.parametrize(
    ("item", "primitive_only", "expected_type"),
    [
        ({"a": 1, "b": 2}, True, dict),
        ({"a", "b", "c"}, True, set),
        (frozenset({"a", "b", "c"}), True, set),
        ([1, 2, 3], True, list),
        ((1, 2, 3), True, list),
        ("string", True, str),
        (b"bytes", True, bytes),
        (1, True, int),
        (1.0, True, float),
        (True, True, bool),
        (None, True, type(None)),
        # Testing with primitive_only=False
        ({"a": 1, "b": 2}, False, dict),
        ({"a", "b", "c"}, False, set),
        (frozenset({"a", "b", "c"}), False, frozenset),
        ([1, 2, 3], False, list),
        ((1, 2, 3), False, tuple),
        ("string", False, str),
        (b"bytes", False, bytes),
        (1, False, int),
        (1.0, False, float),
        (True, False, bool),
        (None, False, type(None)),
    ],
)
def test_typeof(item: Any, primitive_only: bool, expected_type: type) -> None:
    """
    Tests the functionality of the typeof function for both primitive and exact types.

    Args:
        item (Any): The value to determine the type of.
        primitive_only (bool): Whether to return the primitive type.
        expected_type (type): The expected type or primitive type.

    Asserts:
        The result of typeof matches the expected type.
    """
    assert typeof(item, primitive_only=primitive_only) == expected_type
