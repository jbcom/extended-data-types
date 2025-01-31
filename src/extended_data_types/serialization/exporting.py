"""Data export and serialization utilities.

This module provides utilities for exporting and serializing data to
various formats, with automatic format selection and validation.

Typical usage:
    >>> from extended_data_types.serialization.exporting import wrap_for_export
    >>> data = {"key": "value"}
    >>> result = wrap_for_export(data, format="json")
    >>> print(result)
    {"key": "value"}
"""

from __future__ import annotations

from typing import Any, Literal, cast

from ..core.exceptions import SerializationError
from ..core.types import typeof
from .detection import is_yaml_compatible
from .registry import serialize


ExportFormat = Literal["yaml", "json", "toml", "hcl2", "raw"]


def wrap_for_export(
    data: Any,
    format: ExportFormat | bool = "yaml",
    **kwargs: Any,
) -> str:
    """Prepare and serialize data for export.

    Args:
        data: Data to export
        format: Target format or auto-detect flag
        **kwargs: Format-specific options

    Returns:
        Serialized data string

    Raises:
        SerializationError: If serialization fails

    Examples:
        >>> data = {"key": "value"}
        >>> wrap_for_export(data, format="json")
        '{"key": "value"}'
        >>> wrap_for_export(data, format="yaml")
        'key: value\\n'
        >>> wrap_for_export(data)  # defaults to YAML
        'key: value\\n'
    """
    # Convert special types first
    converted_data = convert_special_types(data)

    # Handle raw format
    if format == "raw":
        return str(converted_data)

    # Handle boolean format (auto-detect)
    if isinstance(format, bool):
        if not format:
            return str(converted_data)
        # Auto-detect best format
        format = cast(
            ExportFormat, "yaml" if is_yaml_compatible(converted_data) else "json"
        )

    try:
        # Serialize to specified format
        return serialize(converted_data, format, **kwargs)

    except Exception as e:
        raise SerializationError(
            f"Failed to serialize {typeof(converted_data)} to {format}: {e}"
        ) from e
