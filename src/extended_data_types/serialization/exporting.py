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

from datetime import datetime, date, time
from pathlib import Path
from typing import Any, Literal, cast

from extended_data_types.core.exceptions import SerializationError
from extended_data_types.core.types import typeof
from extended_data_types.serialization.detection import is_yaml_compatible
from extended_data_types.serialization.registry import serialize


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
    allowed_formats = {"yaml", "json", "toml", "hcl2", "raw"}

    # Handle raw format
    if format == "raw":
        return str(data)

    # Handle boolean or string boolean format (auto-detect)
    if isinstance(format, bool):
        if not format:
            return str(data)
        format = cast(
            ExportFormat, "yaml" if is_yaml_compatible(data) else "json"
        )
    elif isinstance(format, str):
        fmt_lower = format.casefold()
        if fmt_lower in ("true", "false"):
            if fmt_lower == "false":
                return str(data)
            format = cast(
                ExportFormat,
                "yaml" if is_yaml_compatible(data) else "json",
            )
        elif fmt_lower not in allowed_formats:
            raise ValueError(f"Invalid format value: {format}")
        else:
            format = cast(ExportFormat, fmt_lower)

    # Convert special types before serializing
    converted_data = _clean_for_export(data)

    try:
        # Serialize to specified format
        return serialize(converted_data, format, **kwargs)

    except Exception as e:
        raise SerializationError(
            f"Failed to serialize {typeof(converted_data)} to {format}: {e}"
        ) from e


def _clean_for_export(obj: Any) -> Any:
    if isinstance(obj, datetime):
        return obj.date().isoformat()
    if isinstance(obj, (date, time)):
        return obj.isoformat()
    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, (bytes, bytearray)):
        try:
            return obj.decode()
        except Exception:
            return str(obj)
    if isinstance(obj, set):
        return [_clean_for_export(v) for v in sorted(obj)]
    if isinstance(obj, list):
        return [_clean_for_export(v) for v in obj]
    if isinstance(obj, dict):
        return {k: _clean_for_export(v) for k, v in obj.items()}
    return obj
