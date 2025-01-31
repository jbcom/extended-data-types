"""Mapping transformation operations."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import TypeVar, overload

from ..core import Transform


KT = TypeVar("KT")
VT = TypeVar("VT")
T = TypeVar("T")


def pick(
    mapping: Mapping[KT, VT], keys: Sequence[KT], *, strict: bool = True
) -> dict[KT, VT]:
    """Create new mapping with only specified keys.

    Args:
        mapping: Source mapping
        keys: Keys to include
        strict: Raise KeyError for missing keys

    Returns:
        New mapping with picked keys

    Example:
        >>> pick({'a': 1, 'b': 2, 'c': 3}, ['a', 'c'])
        {'a': 1, 'c': 3}
    """
    if strict:
        return {k: mapping[k] for k in keys}
    return {k: mapping[k] for k in keys if k in mapping}


def omit(mapping: Mapping[KT, VT], keys: Sequence[KT]) -> dict[KT, VT]:
    """Create new mapping without specified keys.

    Args:
        mapping: Source mapping
        keys: Keys to exclude

    Returns:
        New mapping without omitted keys

    Example:
        >>> omit({'a': 1, 'b': 2, 'c': 3}, ['b'])
        {'a': 1, 'c': 3}
    """
    return {k: v for k, v in mapping.items() if k not in keys}


def merge_maps(*mappings: Mapping[KT, VT], deep: bool = False) -> dict[KT, VT]:
    """Merge multiple mappings.

    Args:
        *mappings: Mappings to merge
        deep: Perform deep merge of nested mappings

    Returns:
        Merged mapping

    Example:
        >>> merge_maps({'a': 1}, {'b': 2})
        {'a': 1, 'b': 2}
        >>> merge_maps({'a': {'x': 1}}, {'a': {'y': 2}}, deep=True)
        {'a': {'x': 1, 'y': 2}}
    """
    result: dict[KT, VT] = {}

    for mapping in mappings:
        if not deep:
            result.update(mapping)
            continue

        for key, value in mapping.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = merge_maps(result[key], value, deep=True)
            else:
                result[key] = value

    return result


def rename_keys(
    mapping: Mapping[KT, VT], key_map: Mapping[KT, KT], *, strict: bool = True
) -> dict[KT, VT]:
    """Create new mapping with renamed keys.

    Args:
        mapping: Source mapping
        key_map: Old key to new key mapping
        strict: Raise KeyError for missing keys

    Returns:
        New mapping with renamed keys

    Example:
        >>> rename_keys({'old': 1}, {'old': 'new'})
        {'new': 1}
    """
    result = {}
    remaining = dict(mapping)

    for old_key, new_key in key_map.items():
        if strict or old_key in remaining:
            result[new_key] = remaining.pop(old_key)

    result.update(remaining)
    return result


@overload
def transform_keys(
    mapping: Mapping[KT, VT], transform: Callable[[KT], T]
) -> dict[T, VT]: ...


def transform_keys(
    mapping: Mapping[KT, VT], transform: Callable[[KT], T]
) -> dict[T, VT]:
    """Create new mapping with transformed keys.

    Args:
        mapping: Source mapping
        transform: Key transform function

    Returns:
        New mapping with transformed keys

    Example:
        >>> transform_keys({'a': 1}, str.upper)
        {'A': 1}
    """
    return {transform(k): v for k, v in mapping.items()}


@overload
def transform_values(
    mapping: Mapping[KT, VT], transform: Callable[[VT], T]
) -> dict[KT, T]: ...


def transform_values(
    mapping: Mapping[KT, VT], transform: Callable[[VT], T]
) -> dict[KT, T]:
    """Create new mapping with transformed values.

    Args:
        mapping: Source mapping
        transform: Value transform function

    Returns:
        New mapping with transformed values

    Example:
        >>> transform_values({'a': 1}, lambda x: x * 2)
        {'a': 2}
    """
    return {k: transform(v) for k, v in mapping.items()}


# Register transforms
pick_transform = Transform(pick)
omit_transform = Transform(omit)
merge_maps_transform = Transform(merge_maps)
rename_keys_transform = Transform(rename_keys)
transform_keys_transform = Transform(transform_keys)
transform_values_transform = Transform(transform_values)
