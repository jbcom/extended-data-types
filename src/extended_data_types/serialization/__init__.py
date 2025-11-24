"""Serialization utilities for extended data types.

This package provides serialization capabilities building on core type handling.
It includes format detection, type conversion, and a registry system for different
serialization formats.

Typical usage:
    >>> from extended_data_types.serialization import serialize, deserialize
    >>> data = {'date': datetime.date(2023, 1, 1)}
    >>> serialized = serialize(data, 'json')
    >>> deserialized = deserialize(serialized, 'json')
"""

from __future__ import annotations

from typing import Any

from extended_data_types.core.exceptions import SerializationError
from extended_data_types.core.types import unwrap_object
from extended_data_types.serialization.detection import (
    guess_format,
    is_potential_hcl2,
    is_potential_ini,
    is_potential_json,
    is_potential_querystring,
    is_potential_toml,
    is_potential_xml,
    is_potential_yaml,
)
from extended_data_types.serialization.formats import JsonSerializer, TomlSerializer, YamlSerializer
from extended_data_types.serialization.registry import (
    deserialize as registry_deserialize,
    get_serializer,
    list_serializers,
    register_format,
    register_serializer,
    serialize as registry_serialize,
)
from extended_data_types.serialization.types import convert_to_serializable, reconstruct_from_serialized


def serialize(obj: Any, format_name: str | None = None) -> str:
    """Serialize an object to a string.

    Args:
        obj: Object to serialize
        format_name: Target format (auto-detected if None)

    Returns:
        str: Serialized representation

    Raises:
        SerializationError: If format is unsupported or serialization fails
    """
    serializable = convert_to_serializable(obj)
    fmt = format_name or guess_format(str(obj))
    return registry_serialize(serializable, fmt)


def deserialize(content: str, format_name: str | None = None) -> Any:
    """Deserialize a string to an object.

    Args:
        content: String to deserialize
        format_name: Source format (auto-detected if None)

    Returns:
        Any: Deserialized object

    Raises:
        SerializationError: If format is unsupported or deserialization fails
    """
    if not format_name:
        format_name = guess_format(content)

    fmt = format_name or guess_format(content)
    raw = registry_deserialize(content, fmt)
    return reconstruct_from_serialized(raw)


__all__ = [
    # Detection
    "guess_format",
    "is_potential_json",
    "is_potential_yaml",
    "is_potential_toml",
    "is_potential_xml",
    "is_potential_ini",
    "is_potential_querystring",
    "is_potential_hcl2",
    # Registry
    "get_serializer",
    "register_serializer",
    "list_serializers",
    "register_format",
    # Types
    "convert_to_serializable",
    "reconstruct_from_serialized",
    "SerializationError",
    "serialize",
    "deserialize",
    "wrap_for_export",
    "unwrap_imported_data",
    # Formats
    "JsonSerializer",
    "YamlSerializer",
    "TomlSerializer",
]
