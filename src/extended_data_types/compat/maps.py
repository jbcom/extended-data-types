"""Compatibility wrappers for legacy map utilities."""

from collections.abc import Mapping
from typing import Any

from extended_data_types.map_data_type import (
    deduplicate_map as _deduplicate_map,
)
from extended_data_types.map_data_type import (
    flatten_map as _flatten_map,
)
from extended_data_types.map_data_type import (
    unhump_map as _unhump_map,
)


def flatten_map(
    dictionary: Mapping[str, Any], parent_key: str = "", separator: str = "."
) -> dict[str, Any]:
    """Maintain bob.map_data_type.flatten_map compatibility."""
    return _flatten_map(dictionary, parent_key=parent_key, separator=separator)


def deduplicate_map(m: Mapping[str, Any]) -> dict[str, Any]:
    """Maintain bob.map_data_type.deduplicate_map compatibility."""
    return _deduplicate_map(m)


def unhump_map(
    m: Mapping[str, Any], drop_without_prefix: str | None = None
) -> dict[str, Any]:
    """Maintain bob.map_data_type.unhump_map compatibility."""
    return _unhump_map(m, drop_without_prefix=drop_without_prefix)
