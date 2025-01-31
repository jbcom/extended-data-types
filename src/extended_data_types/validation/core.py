"""Core validation utilities.

This module provides utility functions for handling and evaluating data structure "emptiness".
It includes functions to determine whether a value is considered "nothing", to extract
non-empty values, and to assess the state of provided arguments and keyword arguments.
"""

from __future__ import annotations

from collections.abc import Generator
from typing import Any


def is_nothing(v: Any) -> bool:
    """Checks if a value is considered 'nothing'.

    Args:
        v: The value to check.

    Returns:
        bool: True if the value is considered 'nothing', False otherwise.

    Examples:
        >>> is_nothing(None)
        True
        >>> is_nothing("")
        True
        >>> is_nothing([None, "", {}])
        True
        >>> is_nothing("text")
        False
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


def are_nothing(*args: Any, **kwargs: Any) -> bool:
    """Checks if all provided values (both args and kwargs) are considered 'nothing'.

    Args:
        *args: Positional arguments to check.
        **kwargs: Keyword arguments to check.

    Returns:
        bool: True if all values are considered 'nothing', False otherwise.

    Examples:
        >>> are_nothing(None, "", [])
        True
        >>> are_nothing(None, "text")
        False
        >>> are_nothing(a=None, b="")
        True
    """
    non_empty = all_non_empty(*args, **kwargs)

    if non_empty is None:
        return True

    if isinstance(non_empty, (list, dict)):
        return len(non_empty) == 0

    if isinstance(non_empty, tuple):
        list_part, dict_part = non_empty
        return len(list_part) == 0 and len(dict_part) == 0

    return False


def is_something(value: Any) -> bool:
    """Check if a value is not considered "nothing".

    Args:
        value: Value to check.

    Returns:
        bool: True if value is not nothing, False otherwise.

    Examples:
        >>> is_something("text")
        True
        >>> is_something(None)
        False
    """
    return not is_nothing(value)


def are_something(*values: Any) -> bool:
    """Check if all values are not considered "nothing".

    Args:
        *values: Values to check.

    Returns:
        bool: True if all values are not nothing, False otherwise.

    Examples:
        >>> are_something("text", [1, 2])
        True
        >>> are_something("text", None)
        False
    """
    return all(is_something(value) for value in values)


def all_non_empty(
    *args: Any, **kwargs: Any
) -> list[Any] | dict[str, Any] | tuple[list[Any], dict[str, Any]] | None:
    """Returns all non-empty values from the provided args and kwargs.

    Args:
        *args: Positional arguments to check.
        **kwargs: Keyword arguments to check.

    Returns:
        One of the following:
            - None if no arguments provided
            - list[Any] of non-empty values if only args provided
            - dict[str, Any] of non-empty values if only kwargs provided
            - tuple[list[Any], dict[str, Any]] if both args and kwargs provided

    Examples:
        >>> all_non_empty("text", None, [1])
        ['text', [1]]
        >>> all_non_empty(a="text", b=None)
        {'a': 'text'}
        >>> all_non_empty("text", b="value")
        (['text'], {'b': 'value'})
    """
    if len(args) == 0 and len(kwargs) == 0:
        return None

    if len(args) == 0:
        return all_non_empty_in_dict(dict(kwargs))

    results = all_non_empty_in_list(list(args))
    if len(kwargs) == 0:
        return results

    return results, all_non_empty_in_dict(dict(kwargs))


def all_non_empty_in_list(input_list: list[Any]) -> list[Any]:
    """Returns a list of all non-empty values from the input list.

    Args:
        input_list: A list of items to check for emptiness.

    Returns:
        list[Any]: A list containing only non-empty values.

    Examples:
        >>> all_non_empty_in_list(["text", None, "", [1]])
        ['text', [1]]
    """
    return [item for item in input_list if not is_nothing(item)]


def all_non_empty_in_dict(input_dict: dict[Any, Any]) -> dict[Any, Any]:
    """Returns a dictionary of all non-empty values from the input dictionary.

    Args:
        input_dict: A dictionary of items to check for emptiness.

    Returns:
        dict[Any, Any]: A dictionary containing only non-empty values.

    Examples:
        >>> all_non_empty_in_dict({"a": "text", "b": None, "c": []})
        {'a': 'text'}
    """
    return {key: value for key, value in input_dict.items() if not is_nothing(value)}


def first_non_empty(*vals: Any) -> Any:
    """Returns the first non-empty value.

    Args:
        *vals: Values to check.

    Returns:
        Any: The first non-empty value, or None if all are 'nothing'.

    Examples:
        >>> first_non_empty(None, "", "text", "more")
        'text'
        >>> first_non_empty(None, "", [])
        None
    """
    non_empty_vals = all_non_empty(*vals)
    return (
        non_empty_vals[0]
        if isinstance(non_empty_vals, list) and non_empty_vals
        else None
    )


def any_non_empty(m: dict[Any, Any], *keys: Any) -> dict[Any, Any]:
    """Returns the first non-empty value from a mapping for the given keys.

    Args:
        m: The mapping to check.
        *keys: The keys to check.

    Returns:
        dict[Any, Any]: A mapping containing the first non-empty value.

    Examples:
        >>> any_non_empty({"a": None, "b": "text"}, "a", "b")
        {'b': 'text'}
        >>> any_non_empty({"a": None}, "a", "b")
        {}
    """
    for k in keys:
        v = m.get(k)
        if not is_nothing(v):
            return {k: v}
    return {}


def yield_non_empty(
    m: dict[Any, Any], *keys: Any
) -> Generator[dict[Any, Any], None, None]:
    """Yields non-empty values from a mapping for the given keys.

    Args:
        m: The mapping to check.
        *keys: The keys to check.

    Yields:
        dict[Any, Any]: A mapping containing each non-empty value.

    Examples:
        >>> list(yield_non_empty({"a": None, "b": "text", "c": [1]}, "a", "b", "c"))
        [{'b': 'text'}, {'c': [1]}]
    """
    for k in keys:
        v = m.get(k)
        if not is_nothing(v):
            yield {k: v}
