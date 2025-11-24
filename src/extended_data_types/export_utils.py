"""This module provides utilities for exporting raw data in various formats.

It includes functions to make raw data export-safe and to wrap raw data for export
with optional encoding formats such as YAML, JSON, or TOML.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .json_utils import encode_json
from .toml_utils import encode_toml
from .type_utils import convert_special_types, strtobool
from .yaml_utils import encode_yaml, is_yaml_data


def wrap_raw_data_for_export(
    raw_data: Mapping[str, Any] | Any,
    allow_encoding: bool | str = True,
    **format_opts: Any,
) -> str:
    """Wraps raw data for export, optionally encoding it.

    Args:
        raw_data (Mapping[str, Any] | Any): The raw data to wrap.
        allow_encoding (bool | str): The encoding format or flag (default is 'yaml').
        format_opts (Any): Additional options for formatting the output.

    Returns:
        str: The wrapped and encoded data.

    Raises:
        ValueError: If an invalid or unsupported encoding is provided.
    """
    # Convert special types in the raw data to simpler forms
    raw_data = convert_special_types(raw_data)

    # Check if allow_encoding is a string specifying the format
    if isinstance(allow_encoding, str):
        allow_encoding_lower = allow_encoding.casefold()
        if allow_encoding_lower == "yaml":
            return encode_yaml(raw_data)
        if allow_encoding_lower == "json":
            return encode_json(raw_data, **format_opts)
        if allow_encoding_lower == "toml":
            return encode_toml(raw_data)
        if allow_encoding_lower == "raw":
            return str(raw_data)

        # Attempt to convert string-based allow_encoding to a boolean
        try:
            allow_encoding_bool = strtobool(allow_encoding, raise_on_error=True)
            allow_encoding = (
                allow_encoding_bool
                if isinstance(allow_encoding_bool, bool)
                else allow_encoding
            )
        except ValueError as e:
            raise ValueError(f"Invalid allow_encoding value: {allow_encoding}") from e

    # Determine the encoding based on boolean allow_encoding and YAML data check
    if allow_encoding:
        if is_yaml_data(raw_data):
            return encode_yaml(raw_data)
        # Call encode_json with options unpacked to ensure they are correctly passed
        return encode_json(raw_data, **format_opts)

    # If no encoding is allowed, return the string representation of raw_data
    return str(raw_data)


def make_raw_data_export_safe(raw_data: Mapping[str, Any] | Any, **format_opts: Any) -> str:
    """Legacy helper that delegates to wrap_raw_data_for_export."""
    return wrap_raw_data_for_export(raw_data, **format_opts)
