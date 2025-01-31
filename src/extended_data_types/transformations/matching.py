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

from ..core.types import is_nothing
from ..serialization.types import encode_json


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
    if is_nothing(a) or is_nothing(b):
        return False

    # Convert strings to lowercase for case-insensitive comparison
    a = a.casefold() if a else ""
    b = b.casefold() if b else ""

    # Check if one string is a prefix of the other
    if check_prefix_only:
        return a.startswith(b) or b.startswith(a)

    # Check if one string is contained within the other
    return a in b or b in a

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
    if is_nothing(a) or is_nothing(b):
        return False

    # Ensure both values are of the same type
    if not isinstance(a, type(b)):
        return False

    # Handle string comparisons case-insensitively
    if isinstance(a, str):
        a = a.casefold()
        b = b.casefold()
    # Handle mapping types by encoding to JSON with sorted keys
    elif isinstance(a, Mapping):
        a = encode_json(a, sort_keys=True)
        b = encode_json(b, sort_keys=True)
    # Handle lists by sorting, ensuring types within lists are comparable
    elif isinstance(a, list) and isinstance(b, list):
        try:
            a = sorted(a)
            b = sorted(b)
        except TypeError:
            # If elements are not comparable, return False
            return False

    # Return comparison result
    return a == b 