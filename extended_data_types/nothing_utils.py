"""This module provides utilities for handling 'nothing' values.

It includes functions to check if a value is 'nothing', to filter out 'nothing' values,
and to yield non-empty values from a mapping.
"""

from __future__ import annotations

from typing import Any, Generator, Mapping


def is_nothing(v: Any) -> bool:
    """Checks if a value is considered 'nothing'.

    Args:
        v (Any): The value to check.

    Returns:
        bool: True if the value is considered 'nothing', False otherwise.
    """
    if v in [None, "", {}, []]:
        return True

    if str(v) == "" or str(v).isspace():
        return True

    if isinstance(v, (list, set)):
        v = [vv for vv in v if vv not in [None, "", {}, []]]
        if len(v) == 0:
            return True

    return False


def all_non_empty(*vals: Any) -> list:
    """Returns a list of all non-empty values.

    Args:
        vals (Any): The values to check.

    Returns:
        list: The list of non-empty values.
    """
    return [val for val in vals if not is_nothing(val)]


def are_nothing(*vals: Any) -> bool:
    """Checks if all values are 'nothing'.

    Args:
        vals (Any): The values to check.

    Returns:
        bool: True if all values are 'nothing', False otherwise.
    """
    return len(all_non_empty(*vals)) == 0


def first_non_empty(*vals: Any) -> Any:
    """Returns the first non-empty value.

    Args:
        vals (Any): The values to check.

    Returns:
        Any: The first non-empty value, or None if all are 'nothing'.
    """
    non_empty_vals = all_non_empty(*vals)
    return non_empty_vals[0] if non_empty_vals else None


def any_non_empty(m: Mapping, *keys: Any) -> Mapping:
    """Returns the first non-empty value from a mapping for the given keys.

    Args:
        m (Mapping): The mapping to check.
        keys (Any): The keys to check.

    Returns:
        Mapping: A mapping containing the first non-empty value.
    """
    for k in keys:
        v = m.get(k)
        if not is_nothing(v):
            return {k: v}
    return {}


def yield_non_empty(m: Mapping, *keys: Any) -> Generator[Mapping, None, None]:
    """Yields non-empty values from a mapping for the given keys.

    Args:
        m (Mapping): The mapping to check.
        keys (Any): The keys to check.

    Yields:
        Generator[Mapping, None, None]: A generator yielding non-empty values.
    """
    for k in keys:
        v = m.get(k)
        if not is_nothing(v):
            yield {k: v}
