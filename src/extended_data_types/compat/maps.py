"""Backward compatibility layer for bob map utilities."""

from collections.abc import Mapping
from typing import Any

from extended_data_types.structures.dict import EnhancedDict


def _flatten(dictionary: Mapping[str, Any], parent_key: str, separator: str) -> dict[str, Any]:
    items: dict[str, Any] = {}
    for key, value in dictionary.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else str(key)
        if isinstance(value, Mapping):
            items.update(_flatten(value, new_key, separator))
        else:
            items[new_key] = value
    return items


def flatten_map(
    dictionary: Mapping[str, Any], parent_key: str = "", separator: str = "."
) -> dict[str, Any]:
    """Maintain bob.map_data_type.flatten_map compatibility."""
    return _flatten(dictionary, parent_key, separator)


def deduplicate_map(m: Mapping[str, Any]) -> dict[str, Any]:
    """Maintain bob.map_data_type.deduplicate_map compatibility."""
    result: dict[str, Any] = {}
    for key, value in m.items():
        if isinstance(value, list):
            seen = []
            for item in value:
                if item not in seen:
                    seen.append(item)
            result[key] = seen
        elif isinstance(value, Mapping):
            result[key] = deduplicate_map(value)
        else:
            result[key] = value
    return result


def unhump_map(
    m: Mapping[str, Any], drop_without_prefix: str | None = None
) -> dict[str, Any]:
    """Maintain bob.map_data_type.unhump_map compatibility."""
    enhanced = EnhancedDict(m)
    return dict(enhanced.keymap_snake_case(drop_without_prefix=drop_without_prefix))
