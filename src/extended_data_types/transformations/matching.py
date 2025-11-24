"""Utilities for string and value matching.

This module provides utilities for matching strings and comparing values,
with support for partial matches and type-aware comparisons.

Typical usage:
    >>> from extended_data_types.transformations.matching import is_partial_match
    >>> is_partial_match("hello", "hell")
    True
    >>> is_partial_match("HELLO", "hello")
    True
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from extended_data_types.serialization.types import encode_json


def is_partial_match(
    a: str | None,
    b: str | None,
    check_prefix_only: bool = False,
) -> bool:
    """Check if two strings partially match.

    Args:
        a: The first string
        b: The second string
        check_prefix_only: Whether to check only the prefix

    Returns:
        bool: True if there is a partial match

    Examples:
        >>> is_partial_match("hello", "hell")
        True
        >>> is_partial_match("hello", "lo")
        True
        >>> is_partial_match("hello", "help")
        False
        >>> is_partial_match("HELLO", "hello")
        True
    """
    if a is None or b is None:
        return False

    # Two empty strings are considered a match
    if a == "" and b == "":
        return True

    # Empty strings don't match non-empty strings
    if a == "" or b == "":
        return False

    # Convert strings to lowercase for case-insensitive comparison
    a = a.casefold() if a else ""
    b = b.casefold() if b else ""

    # Check if one string is a prefix of the other
    if check_prefix_only:
        return a.startswith(b) or b.startswith(a)

    # Check if one string is contained within the other
    return a in b or b in a


def _normalize_for_match(value: Any) -> Any:
    """Normalize a value for order-insensitive comparison."""
    if isinstance(value, Mapping):
        # Recursively normalize dict values, sort by key
        normalized_dict = {k: _normalize_for_match(v) for k, v in value.items()}
        # Return as tuple with type marker: ('dict', sorted_items)
        return ("dict", tuple(sorted(normalized_dict.items())))
    elif isinstance(value, list):
        # Recursively normalize list elements, then sort
        normalized = [_normalize_for_match(item) for item in value]
        try:
            # Try to sort, but handle uncomparable types
            # Return as tuple with type marker: ('list', sorted_items)
            return ("list", tuple(sorted(normalized)))
        except TypeError:
            # If elements are not comparable, return None to signal incomparability
            return None
    elif isinstance(value, set):
        # Convert set to sorted tuple with type marker
        try:
            normalized = [_normalize_for_match(item) for item in value]
            return ("set", tuple(sorted(normalized)))
        except TypeError:
            return ("set", tuple(value))
    return value


def is_non_empty_match(a: Any, b: Any) -> bool:
    """Check if two non-empty values match.

    Args:
        a: The first value
        b: The second value

    Returns:
        bool: True if the values match

    Examples:
        >>> is_non_empty_match("Hello", "HELLO")
        True
        >>> is_non_empty_match([1, 2], [2, 1])
        True
        >>> is_non_empty_match({"a": 1}, {"a": 1})
        True
        >>> is_non_empty_match(None, "value")
        False
    """
    # Empty strings should match, so only check for None
    if a is None or b is None:
        return False

    # Ensure both values are of exactly the same type (not subclass)
    if type(a) is not type(b):
        return False

    # Handle string comparisons case-insensitively
    if isinstance(a, str):
        return a.casefold() == b.casefold()

    # Handle mapping types - normalize recursively
    if isinstance(a, Mapping):
        try:
            a_norm = _normalize_for_match(a)
            b_norm = _normalize_for_match(b)
            return encode_json(a_norm, sort_keys=True) == encode_json(
                b_norm, sort_keys=True
            )
        except Exception:
            return False

    # Handle lists - normalize recursively
    if isinstance(a, list):
        # Check if lists have same length
        if len(a) != len(b):
            return False
        # If lists are identical, they match (even if elements have different types)
        if a == b:
            return True
        # Check if corresponding elements have compatible types
        # Container types (dict/list) vs primitives are uncomparable
        for item_a, item_b in zip(a, b):
            a_is_container = isinstance(item_a, (dict, list))
            b_is_container = isinstance(item_b, (dict, list))
            # If one is container and other is not, they're uncomparable
            if a_is_container != b_is_container:
                return False
            # If both are containers but different types (dict vs list), they're uncomparable
            if a_is_container and b_is_container:
                if type(item_a) is not type(item_b):
                    return False
        try:
            a_norm = _normalize_for_match(a)
            b_norm = _normalize_for_match(b)
            # If normalization returned None, elements are uncomparable
            if a_norm is None or b_norm is None:
                return False
            # Compare normalized values
            return a_norm == b_norm
        except TypeError:
            # Sorting failed due to uncomparable types
            return False
        except Exception:
            return False

    # Handle sets - normalize recursively
    if isinstance(a, set):
        try:
            a_norm = _normalize_for_match(a)
            b_norm = _normalize_for_match(b)
            return a_norm == b_norm
        except Exception:
            return False

    # For other types, direct comparison
    return a == b
