"""Mapping transformation operations."""

from __future__ import annotations

from collections.abc import Callable, Mapping, MutableMapping, Sequence
from typing import Any, TypeVar, overload

from extended_data_types.transformations.core import Transform


KT = TypeVar("KT")
VT = TypeVar("VT")
T = TypeVar("T")
U = TypeVar("U")


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


def flatten_dict(
    dictionary: Mapping[str, Any], parent_key: str | None = None, separator: str = "."
) -> dict[str, Any]:
    """Legacy helper to flatten nested dict."""
    items: list[tuple[str, Any]] = []
    for key, value in dictionary.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key
        if isinstance(value, MutableMapping):
            items.extend(flatten_dict(value, new_key, separator).items())
        elif isinstance(value, list):
            for idx, item in enumerate(value):
                items.extend(flatten_dict({str(idx): item}, new_key, separator).items())
        else:
            items.append((new_key, value))
    return dict(items)


def invert_dict(
    mapping: Mapping[KT, VT], *, multi: bool = True
) -> dict[VT, KT | list[KT]]:
    """Legacy helper to invert a mapping."""
    result: dict[VT, KT | list[KT]] = {}
    for key, value in mapping.items():
        try:
            hash(value)
        except Exception as exc:
            raise TypeError("Values must be hashable to invert mapping") from exc
        if not multi:
            result[value] = key
            continue
        if value in result:
            existing = result[value]
            if isinstance(existing, list):
                existing.append(key)
            else:
                result[value] = [existing, key]
        else:
            result[value] = key
    return result


def merge_dicts(*mappings: Mapping[KT, VT]) -> dict[KT, VT]:
    """Legacy helper to merge dictionaries (later overrides earlier)."""

    def _merge(a: Mapping[KT, VT], b: Mapping[KT, VT]) -> dict[KT, VT]:
        merged: dict[KT, VT] = dict(a)
        for key, value in b.items():
            if (
                key in merged
                and isinstance(merged[key], dict)
                and isinstance(value, dict)
            ):
                merged[key] = _merge(merged[key], value)  # type: ignore[arg-type]
            else:
                merged[key] = value
        return merged

    result: dict[KT, VT] = {}
    for m in mappings:
        result = _merge(result, m)
    return result


def transform_dict(
    mapping: Mapping[KT, VT],
    *,
    key_fn: Callable[[KT], KT] | None = None,
    value_fn: Callable[[VT], U] | None = None,
) -> dict[KT, VT] | dict[KT, U] | dict[KT, Any]:
    """Apply a function to all values."""
    key_transform = key_fn or (lambda x: x)
    value_transform = value_fn or (lambda x: x)
    return {key_transform(k): value_transform(v) for k, v in mapping.items()}


def unflatten_dict(flat_map: Mapping[str, Any], separator: str = ".") -> dict[str, Any]:
    """Reconstruct nested dict from flattened keys."""
    root: dict[str, Any] = {}
    for flat_key, value in flat_map.items():
        parts = flat_key.split(separator) if flat_key else [flat_key]
        if any(part == "" for part in parts):
            raise ValueError(f"Invalid key segment in '{flat_key}'")
        cursor: Any = root
        for idx, part in enumerate(parts):
            is_last = idx == len(parts) - 1
            next_part = parts[idx + 1] if not is_last else None
            is_index = part.isdigit()

            if is_index:
                index = int(part)
                if not isinstance(cursor, list):
                    raise ValueError(f"List index '{part}' not under a list")
                while len(cursor) <= index:
                    cursor.append(None)
                if is_last:
                    cursor[index] = value
                else:
                    expected_list = next_part is not None and next_part.isdigit()
                    if cursor[index] is None or (
                        expected_list and not isinstance(cursor[index], list)
                    ):
                        cursor[index] = [] if expected_list else {}
                    cursor = cursor[index]
            else:
                if not isinstance(cursor, dict):
                    raise ValueError(f"Cannot nest key '{part}' into non-dict")
                if is_last:
                    cursor[part] = value
                else:
                    expected_list = next_part is not None and next_part.isdigit()
                    if part not in cursor or (
                        expected_list and not isinstance(cursor[part], list)
                    ):
                        cursor[part] = [] if expected_list else {}
                    cursor = cursor[part]
    return root


def filter_dict(
    mapping: Mapping[KT, VT],
    *,
    key_fn: Callable[[KT], bool] | None = None,
    value_fn: Callable[[VT], bool] | None = None,
) -> dict[KT, VT]:
    """Legacy helper to filter dict by predicate."""
    key_pred = key_fn or (lambda _: True)
    value_pred = value_fn or (lambda _: True)
    return {k: v for k, v in mapping.items() if key_pred(k) and value_pred(v)}


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
