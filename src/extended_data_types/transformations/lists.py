"""List transformation utilities.

This module provides utilities for transforming list structures, including
flattening nested lists and filtering lists based on allow/deny lists.

Typical usage:
    >>> from extended_data_types.transformations.lists import flatten_list
    >>> nested = [[1, 2], [3, [4, 5]]]
    >>> flatten_list(nested)
    [1, 2, 3, 4, 5]
"""

from __future__ import annotations

from typing import Any, TypeVar

T = TypeVar('T')

def flatten_list(matrix: list[Any]) -> list[Any]:
    """Flatten a nested list structure into a single list.
    
    Args:
        matrix: The nested list structure to flatten
        
    Returns:
        list[Any]: The flattened list
        
    Examples:
        >>> flatten_list([[1, 2], [3, [4, 5]]])
        [1, 2, 3, 4, 5]
        >>> flatten_list([1, [2, 3], 4])
        [1, 2, 3, 4]
        >>> flatten_list([])
        []
    """
    def _flatten(lst: list[Any]) -> list[Any]:
        """Recursively flatten a nested list."""
        flattened = []
        for item in lst:
            if isinstance(item, list):
                flattened.extend(_flatten(item))
            else:
                flattened.append(item)
        return flattened

    return _flatten(matrix)

def filter_list(
    items: list[T] | None = None,
    allowlist: list[T] | None = None,
    denylist: list[T] | None = None,
) -> list[T]:
    """Filter a list based on allowlist and denylist.
    
    Args:
        items: The list to filter
        allowlist: List of allowed items
        denylist: List of denied items
        
    Returns:
        list[T]: The filtered list
        
    Examples:
        >>> filter_list(['a', 'b', 'c'], allowlist=['a', 'b'])
        ['a', 'b']
        >>> filter_list(['a', 'b', 'c'], denylist=['b'])
        ['a', 'c']
        >>> filter_list(['a', 'b'], allowlist=['a'], denylist=['a'])
        []
    """
    items = items or []
    allowlist = allowlist or []
    denylist = denylist or []

    return [
        item for item in items
        if (not allowlist or item in allowlist) and item not in denylist
    ] 