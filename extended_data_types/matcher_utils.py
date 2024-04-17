"""This module provides utilities for string and value matching.

It includes functions to partially match strings and to compare non-empty values
for equality, handling different data types including strings, mappings, and lists.
"""  # noqa: E501

from __future__ import annotations, division, print_function, unicode_literals

from typing import Any, Mapping, Optional

from extended_data_types.json_utils import encode_json
from extended_data_types.nothing_utils import is_nothing


def is_partial_match(
        a: Optional[str], b: Optional[str], check_prefix_only: bool = False
) -> bool:
    """Checks if two strings partially match.

    Args:
        a (Optional[str]): The first string.
        b (Optional[str]): The second string.
        check_prefix_only (bool): Whether to check only the prefix.

    Returns:
        bool: True if there is a partial match, False otherwise.
    """
    if is_nothing(a) or is_nothing(b):
        return False

    a = a.casefold() if a is not None else ""
    b = b.casefold() if b is not None else ""

    if check_prefix_only:
        return a.startswith(b) or b.startswith(a)

    return a in b or b in a


def is_non_empty_match(a: Any, b: Any) -> bool:
    """Checks if two non-empty values match.

    Args:
        a (Any): The first value.
        b (Any): The second value.

    Returns:
        bool: True if the values match, False otherwise.
    """
    if is_nothing(a) or is_nothing(b):
        return False

    if not isinstance(a, type(b)):
        return False

    if isinstance(a, str):
        a = a.casefold()
        b = b.casefold()
    elif isinstance(a, Mapping):
        a = encode_json(a, sort_keys=True)
        b = encode_json(b, sort_keys=True)
    elif isinstance(a, list):
        a.sort()
        b.sort()

    return a == b
