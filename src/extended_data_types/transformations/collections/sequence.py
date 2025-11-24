"""Sequence transformation operations."""

from __future__ import annotations

import random

from collections.abc import Callable, Sequence
from typing import Any, TypeVar

from extended_data_types.transformations.core import Transform


T = TypeVar("T")
U = TypeVar("U")


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
        >>> chunk([1, 2, 3], 2, pad=True)
        [[1, 2], [3, None]]
    """
    # Convert to list to ensure mutable chunks
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
        >>> flatten([1, [2, [3]], 4], depth=1)
        [1, 2, [3], 4]
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
    key: Callable[[T], U] | str,
) -> dict[U, list[T]]:
    """Group items by key function or attribute.

    Args:
        items: Items to group
        key: Grouping key function or attribute name

    Returns:
        Dictionary of grouped items

    Example:
        >>> group_by([1, 2, 3, 4], lambda x: x % 2)
        {0: [2, 4], 1: [1, 3]}
    """
    if isinstance(key, str):
        key_func = lambda x: getattr(x, key)
    else:
        key_func = key

    groups: dict[U, list[T]] = {}
    for item in items:
        k = key_func(item)
        if k not in groups:
            groups[k] = []
        groups[k].append(item)
    return groups


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
        >>> sort_by(['abc', 'a', 'ab'], len)
        ['a', 'ab', 'abc']
    """
    if isinstance(key, str):
        key_func = lambda x: getattr(x, key)
    else:
        key_func = key

    return sorted(items, key=key_func, reverse=reverse)


_NO_FILL = object()


def chunk_sequence(
    seq: Sequence[T], size: int, fill: Any | object = _NO_FILL
) -> list[list[T]]:
    """Legacy helper to chunk sequences."""
    if size <= 0:
        raise ValueError("size must be positive")
    chunks = [list(seq[i : i + size]) for i in range(0, len(seq), size)]
    if fill is not _NO_FILL and chunks and len(chunks[-1]) < size:
        chunks[-1].extend([fill] * (size - len(chunks[-1])))
    return chunks


def interleave_sequences(*sequences: Sequence[T]) -> list[T]:
    """Legacy helper to interleave sequences."""
    result: list[T] = []
    max_len = max((len(seq) for seq in sequences), default=0)
    for i in range(max_len):
        for seq in sequences:
            if i < len(seq):
                result.append(seq[i])
    return result


def partition_sequence(
    seq: Sequence[T], predicate: Callable[[T], bool]
) -> tuple[list[T], list[T]]:
    """Legacy helper to partition a sequence based on predicate."""
    true_part, false_part = [], []
    for item in seq:
        (true_part if predicate(item) else false_part).append(item)
    return true_part, false_part


def remove_duplicates(
    seq: Sequence[T], key: Callable[[T], Any] | None = None
) -> list[T]:
    """Legacy helper to remove duplicates preserving order."""
    seen = set()
    result: list[T] = []
    for item in seq:
        marker = key(item) if key else item
        if marker in seen:
            continue
        seen.add(marker)
        result.append(item)
    return result


def rotate_sequence(seq: Sequence[T], positions: int = 1) -> list[T]:
    """Rotate sequence by positions."""
    if not seq:
        return []
    length = len(seq)
    if positions < 0:
        mod = (-positions) % length
        offset = mod if mod > (length / 2) else (length - mod)
    else:
        offset = positions % length
    if offset == 0:
        return list(seq)
    return list(seq[-offset:] + seq[:-offset])


def sliding_window(seq: Sequence[T], size: int, step: int = 1) -> list[tuple[T, ...]]:
    """Legacy helper to produce sliding windows."""
    if size <= 0:
        raise ValueError("size must be positive")
    windows: list[tuple[T, ...]] = []
    for i in range(0, len(seq), step):
        window = tuple(seq[i : i + size])
        if not window:
            break
        if len(window) < size:
            if step > 1:
                windows.append(window)
            break
        windows.append(window)
    return windows


def unique(items: Sequence[T], key: Callable[[T], Any] | None = None) -> list[T]:
    """Get unique items from sequence.

    Args:
        items: Source sequence
        key: Optional key function for uniqueness

    Returns:
        List of unique items

    Example:
        >>> unique([1, 2, 2, 3, 1])
        [1, 2, 3]
        >>> unique(['a', 'A', 'b'], key=str.lower)
        ['a', 'b']
    """
    seen = set()
    result = []

    for item in items:
        k = key(item) if key else item
        if k not in seen:
            seen.add(k)
            result.append(item)
    return result


def shuffle(items: Sequence[T], seed: int | None = None) -> list[T]:
    """Randomly shuffle sequence.

    Args:
        items: Sequence to shuffle
        seed: Random seed

    Returns:
        Shuffled list

    Example:
        >>> shuffle([1, 2, 3, 4], seed=42)
        [2, 4, 1, 3]
    """
    result = list(items)
    rng = random.Random(seed)
    rng.shuffle(result)
    return result


def rotate(items: Sequence[T], steps: int = 1) -> list[T]:
    """Rotate sequence by specified steps.

    Args:
        items: Sequence to rotate
        steps: Number of steps (positive=right, negative=left)

    Returns:
        Rotated list

    Example:
        >>> rotate([1, 2, 3, 4], 1)
        [4, 1, 2, 3]
        >>> rotate([1, 2, 3, 4], -1)
        [2, 3, 4, 1]
    """
    if not items:
        return list(items)
    steps = steps % len(items)
    return list(items[-steps:] + items[:-steps])


def partition(
    items: Sequence[T], predicate: Callable[[T], bool]
) -> tuple[list[T], list[T]]:
    """Split sequence into two groups based on predicate.

    Args:
        items: Sequence to partition
        predicate: Function returning True for first group

    Returns:
        Tuple of (matching, non-matching) lists

    Example:
        >>> partition([1, 2, 3, 4], lambda x: x % 2 == 0)
        ([2, 4], [1, 3])
    """
    matches = []
    non_matches = []

    for item in items:
        if predicate(item):
            matches.append(item)
        else:
            non_matches.append(item)

    return matches, non_matches


# Register transforms
chunk_transform = Transform(chunk)
flatten_transform = Transform(flatten)
group_by_transform = Transform(group_by)
sort_by_transform = Transform(sort_by)
unique_transform = Transform(unique)
shuffle_transform = Transform(shuffle)
rotate_transform = Transform(rotate)
partition_transform = Transform(partition)
