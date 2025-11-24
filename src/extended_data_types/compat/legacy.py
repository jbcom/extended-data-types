"""Compatibility helpers mirroring the pre-5.x API surface."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from extended_data_types.map_data_type import flatten_map as _flatten_map


def flatten_map(
    dictionary: Mapping[str, Any], parent_key: str = "", separator: str = "."
) -> dict[str, Any]:
    """Backwards compatible wrapper for map flattening."""
    return _flatten_map(dictionary, parent_key=parent_key, separator=separator)


def unflatten_map(flat_map: Mapping[str, Any], separator: str = ".") -> dict[str, Any]:
    """Reconstruct nested structures from a flattened mapping."""
    root: dict[str, Any] = {}

    for flat_key, value in flat_map.items():
        if flat_key.startswith(separator) or flat_key.endswith(separator):
            raise ValueError(f"Invalid key: {flat_key}")

        parts = flat_key.split(separator) if flat_key else [flat_key]
        cursor: Any = root

        for idx, part in enumerate(parts):
            is_last = idx == len(parts) - 1
            is_index = part.isdigit()
            key: Any = int(part) if is_index else part

            if is_last:
                _assign(cursor, key, value)
                continue

            next_part = parts[idx + 1]
            next_is_index = next_part.isdigit()
            container = [] if next_is_index else {}
            cursor = _ensure(cursor, key, container)

    return root


def convert_legacy_format(data: Any) -> Any:
    """Placeholder compatibility shim. Kept to satisfy imports."""
    return data


def _ensure(container: Any, key: Any, default: Any) -> Any:
    if isinstance(container, list):
        _pad_list(container, key)
        if container[key] is None:
            container[key] = default
        return container[key]

    if key not in container:
        container[key] = default
    return container[key]


def _assign(container: Any, key: Any, value: Any) -> None:
    if isinstance(container, list):
        _pad_list(container, key)
        container[key] = value
    else:
        container[key] = value


def _pad_list(lst: list[Any], index: int) -> None:
    if index < 0:
        raise ValueError(f"Negative index not supported: {index}")
    while len(lst) <= index:
        lst.append(None)
