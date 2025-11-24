"""Collection transformation operations.

This module provides utilities for transforming collections:
- Chunking sequences into groups
- Flattening nested structures
- Grouping by key or predicate
- Sorting by key or predicate
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable, Sequence
from typing import Any, TypeVar

from extended_data_types.transformations.core import Transform


T = TypeVar("T")
K = TypeVar("K")


def chunk(
    items: Sequence[T], size: int, pad: bool = False, fill_value: Any = None
) -> list[list[T]]:
    """Split sequence into chunks of specified size.

    Args:
        items: Sequence to chunk
        size: Chunk size
        pad: Whether to pad last chunk
        fill_value: Value to pad with

    Returns:
        List of chunks

    Example:
        >>> chunk([1, 2, 3, 4, 5], 2)
        [[1, 2], [3, 4], [5]]
        >>> chunk([1, 2, 3, 4, 5], 2, pad=True)
        [[1, 2], [3, 4], [5, None]]
    """
    chunks = [list(items[i : i + size]) for i in range(0, len(items), size)]
    if pad and chunks and len(chunks[-1]) < size:
        chunks[-1].extend([fill_value] * (size - len(chunks[-1])))
    return chunks


def flatten(
    items: Sequence[Any],
    depth: int | None = None,
    types: tuple[type, ...] = (list, tuple),
) -> list[Any]:
    """Flatten nested sequence.

    Args:
        items: Sequence to flatten
        depth: Maximum depth to flatten
        types: Types to consider for flattening

    Returns:
        Flattened list

    Example:
        >>> flatten([1, [2, 3, [4, 5]], 6])
        [1, 2, 3, 4, 5, 6]
        >>> flatten([1, [2, 3, [4, 5]], 6], depth=1)
        [1, 2, 3, [4, 5], 6]
    """
    result = []
    for item in items:
        if isinstance(item, types) and (depth is None or depth > 0):
            result.extend(
                flatten(
                    item, depth=depth - 1 if depth is not None else None, types=types
                )
            )
        else:
            result.append(item)
    return result


def group_by(
    items: Sequence[T],
    key: Callable[[T], K] | str,
) -> dict[K, list[T]]:
    """Group items by key function or attribute.

    Args:
        items: Items to group
        key: Grouping key function or attribute name

    Returns:
        Dictionary of grouped items

    Example:
        >>> group_by([1, 2, 3, 4, 5], lambda x: x % 2)
        {0: [2, 4], 1: [1, 3, 5]}
        >>> group_by(['a', 'ab', 'abc'], len)
        {1: ['a'], 2: ['ab'], 3: ['abc']}
    """
    if isinstance(key, str):
        key_func = lambda x: getattr(x, key)
    else:
        key_func = key

    groups: dict[K, list[T]] = defaultdict(list)
    for item in items:
        groups[key_func(item)].append(item)
    return dict(groups)


def sort_by(
    items: Sequence[T], key: Callable[[T], Any] | str, reverse: bool = False
) -> list[T]:
    """Sort items by key function or attribute.

    Args:
        items: Items to sort
        key: Sorting key function or attribute name
        reverse: Sort in descending order

    Returns:
        Sorted list

    Example:
        >>> sort_by([1, 2, 3, 4, 5], lambda x: -x)
        [5, 4, 3, 2, 1]
        >>> sort_by(['abc', 'a', 'ab'], len)
        ['a', 'ab', 'abc']
    """
    if isinstance(key, str):
        key_func = lambda x: getattr(x, key)
    else:
        key_func = key

    return sorted(items, key=key_func, reverse=reverse)


# Register transforms
chunk_transform = Transform(chunk)
flatten_transform = Transform(flatten)
group_by_transform = Transform(group_by)
sort_by_transform = Transform(sort_by)
