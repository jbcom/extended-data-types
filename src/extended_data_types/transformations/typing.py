"""Type-based collection transformations.

This module provides utilities for transforming collections by splitting them based
on their element types. It leverages core type utilities for type detection and
categorization.

Typical usage:
    >>> from extended_data_types.transformations.typing import split_list_by_type
    >>> items = [1, "text", 3.14, True]
    >>> result = split_list_by_type(items)
    >>> result[int]  # [1]
    >>> result[str]  # ["text"]
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, TypeVar

from ..core.types import typeof


K = TypeVar("K")  # Key type for dictionaries
V = TypeVar("V")  # Value type for collections


def split_list_by_type(
    items: list[Any], primitive_only: bool = False
) -> defaultdict[type, list[Any]]:
    """Split a list by the type of its items.

    Args:
        items: The list to split
        primitive_only: If True, use primitive types instead of exact types

    Returns:
        defaultdict[type, list[Any]]: Items grouped by their types

    Examples:
        >>> items = [1, "text", 3.14, True]
        >>> result = split_list_by_type(items)
        >>> dict(result)  # for display
        {int: [1], str: ['text'], float: [3.14], bool: [True]}

        >>> result = split_list_by_type(items, primitive_only=True)
        >>> dict(result)  # for display
        {int: [1, True], str: ['text'], float: [3.14]}
    """
    result: defaultdict[type, list[Any]] = defaultdict(list)
    for item in items:
        result[typeof(item, primitive_only=primitive_only)].append(item)
    return result


def split_dict_by_type(
    items: dict[K, V], primitive_only: bool = False
) -> defaultdict[type, dict[K, V]]:
    """Split a dictionary by the type of its values.

    Args:
        items: The dictionary to split
        primitive_only: If True, use primitive types instead of exact types

    Returns:
        defaultdict[type, dict[K, V]]: Items grouped by value types

    Examples:
        >>> items = {'a': 1, 'b': 'text', 'c': 3.14, 'd': True}
        >>> result = split_dict_by_type(items)
        >>> dict(result)  # for display
        {int: {'a': 1}, str: {'b': 'text'}, float: {'c': 3.14}, bool: {'d': True}}

        >>> result = split_dict_by_type(items, primitive_only=True)
        >>> dict(result)  # for display
        {int: {'a': 1, 'd': True}, str: {'b': 'text'}, float: {'c': 3.14}}
    """
    result: defaultdict[type, dict[K, V]] = defaultdict(dict)
    for key, value in items.items():
        result[typeof(value, primitive_only=primitive_only)][key] = value
    return result
