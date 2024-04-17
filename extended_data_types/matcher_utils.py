from __future__ import annotations, division, print_function, unicode_literals

from typing import Any, Mapping, Optional

import orjson

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

    if type(a) != type(b):
        return False

    if isinstance(a, str):
        a = a.casefold()
        b = b.casefold()
    elif isinstance(a, Mapping):
        a = orjson.dumps(a, default=str, option=orjson.OPT_SORT_KEYS).decode("utf-8")
        b = orjson.dumps(b, default=str, option=orjson.OPT_SORT_KEYS).decode("utf-8")
    elif isinstance(a, list):
        a.sort()
        b.sort()

    return a == b
