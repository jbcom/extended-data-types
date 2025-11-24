"""Data import and deserialization utilities.

This module provides utilities for importing and deserializing data from
various formats, with automatic format detection and validation.

Typical usage:
    >>> from extended_data_types.serialization.importing import unwrap_imported_data
    >>> data = unwrap_imported_data('{"key": "value"}', encoding='json')
    >>> data
    {'key': 'value'}
"""

from __future__ import annotations

from typing import Any

from extended_data_types.core.exceptions import SerializationError
from extended_data_types.core.types import convert_special_types
from extended_data_types.serialization.detection import detect_format
from extended_data_types.serialization.registry import deserialize


def unwrap_imported_data(
    data: str,
    format: str | None = None,
    validate: bool = True,
    **kwargs: Any,
) -> Any:
    """Deserialize imported data string.

    Args:
        data: Data string to deserialize
        format: Format to use (auto-detect if None)
        validate: Whether to validate before parsing
        **kwargs: Format-specific options

    Returns:
        Deserialized data

    Raises:
        SerializationError: If deserialization fails

    Examples:
        >>> data = '{"key": "value"}'
        >>> unwrap_imported_data(data, format="json")
        {'key': 'value'}
        >>> data = 'key: value'
        >>> unwrap_imported_data(data)  # auto-detects YAML
        {'key': 'value'}
    """
    if not data:
        raise SerializationError("Cannot deserialize empty data")

    # Auto-detect format if not specified
    detected_format = format.lower() if format else detect_format(data)
    if not detected_format:
        raise SerializationError("Could not detect data format")
    if detected_format not in ["yaml", "json", "toml", "hcl2", "raw"]:
        raise ValueError("Unsupported encoding format")

    try:
        # Deserialize data
            result = deserialize(data, detected_format, **kwargs)
            if isinstance(result, dict):
                keys = list(result.keys())
                for k in keys:
                    if k is None:
                        result["null"] = result.pop(k)
                        break
            return result

    except Exception as e:
        raise SerializationError(
            f"Failed to deserialize {detected_format} data: {e}"
        ) from e
