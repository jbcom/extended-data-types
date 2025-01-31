"""Backward compatibility layer for bob map utilities."""

from typing import Any, Mapping

from ..structures.dict import EnhancedDict


def flatten_map(
    dictionary: Mapping[str, Any],
    parent_key: str = "",
    separator: str = "."
) -> dict[str, Any]:
    """Maintain bob.map_data_type.flatten_map compatibility."""
    enhanced = EnhancedDict(dictionary)
    return dict(enhanced.flatten(parent_key=parent_key, separator=separator))

def deduplicate_map(m: Mapping[str, Any]) -> dict[str, Any]:
    """Maintain bob.map_data_type.deduplicate_map compatibility."""
    enhanced = EnhancedDict(m)
    return dict(enhanced.deduplicate())

def unhump_map(
    m: Mapping[str, Any],
    drop_without_prefix: str | None = None
) -> dict[str, Any]:
    """Maintain bob.map_data_type.unhump_map compatibility."""
    enhanced = EnhancedDict(m)
    return dict(enhanced.keymap_snake_case(
        drop_without_prefix=drop_without_prefix
    )) 