"""Backward compatibility layer for bob serialization utilities.

This module provides compatibility with bob's export_utils and import_utils,
while using the modern SerializationHandler internally.

Typical usage:
    >>> from extended_data_types.compat.serialization import wrap_raw_data_for_export
    >>> result = wrap_raw_data_for_export({"key": "value"}, "yaml")
"""

import json

from typing import Any

import tomlkit
import yaml

from extended_data_types.serialization.formats.hcl2 import Hcl2Serializer
from extended_data_types.serialization.handlers import (
    SerializationError,
    SerializationHandler,
)


# Global handler instance for compatibility functions
_handler = SerializationHandler()
_hcl2 = Hcl2Serializer()


def wrap_raw_data_for_export(
    raw_data: dict[str, Any] | Any,
    allow_encoding: bool | str = True,
    **format_opts: Any,
) -> str:
    """Maintains compatibility with bob.export_utils.wrap_raw_data_for_export.

    Args:
        raw_data: The raw data to wrap
        allow_encoding: The encoding format or flag (default is True)
        **format_opts: Additional options for formatting

    Returns:
        str: The wrapped and encoded data

    Raises:
        ValueError: If an invalid or unsupported encoding is provided

    Example:
        >>> result = wrap_raw_data_for_export({"key": "value"}, "yaml")
        >>> print(result)
        key: value
    """
    try:
        # Handle boolean allow_encoding
        if isinstance(allow_encoding, bool):
            if allow_encoding:
                # Default to YAML as per original bob behavior
                return _handler.serialize(raw_data, "yaml", **format_opts)
            return _handler.serialize(raw_data, "raw", **format_opts)

        # Handle string format specification
        format_lower = allow_encoding.casefold()
        if format_lower in ["yaml", "json", "toml", "hcl2", "raw"]:
            # Cast to FormatType for type checking
            from typing import cast
            from extended_data_types.serialization.types import FormatType
            return _handler.serialize(raw_data, cast(FormatType, format_lower), **format_opts)

        raise ValueError(f"Invalid allow_encoding value: {allow_encoding}")

    except SerializationError as e:
        raise ValueError(str(e)) from e


def unwrap_raw_data_from_import(
    wrapped_data: str,
    encoding: str = "yaml",
) -> Any:
    """Maintains compatibility with bob.import_utils.unwrap_raw_data_from_import.

    Args:
        wrapped_data: The wrapped data
        encoding: The encoding format (default is 'yaml')

    Returns:
        Any: The unwrapped data

    Raises:
        ValueError: If the encoding format is unsupported

    Example:
        >>> result = unwrap_raw_data_from_import('key: value', 'yaml')
        >>> print(result)
        {'key': 'value'}
    """
    try:
        format_lower = encoding.casefold()
        if format_lower not in ["yaml", "json", "toml", "hcl2", "raw"]:
            raise ValueError(f"Unsupported encoding format: {encoding}")

        if format_lower == "yaml":
            return yaml.safe_load(wrapped_data)
        if format_lower == "json":
            return json.loads(wrapped_data)
        if format_lower == "toml":
            return tomlkit.parse(wrapped_data)
        if format_lower == "hcl2":
            return _hcl2.decode(wrapped_data)
        return wrapped_data

    except Exception as e:
        raise ValueError(str(e)) from e


def detect_format(
    data: str | bytes | None,
    default: str = "raw",
) -> str:
    """Detect the format of the input data.

    Args:
        data: The data to analyze
        default: Default format if detection fails

    Returns:
        str: Detected format name

    Example:
        >>> format = detect_format('{"key": "value"}')
        >>> print(format)
        'json'
    """
    if not data:
        return default

    data_str = data.decode() if isinstance(data, bytes) else str(data)
    data_str = data_str.strip()

    # Try to detect format based on content
    if data_str.startswith("{") and data_str.endswith("}"):
        return "json"
    if data_str.startswith("---") or ":" in data_str:
        return "yaml"
    if "=" in data_str and "[" in data_str:
        return "toml"
    if "resource" in data_str or "variable" in data_str:
        return "hcl2"

    return default
