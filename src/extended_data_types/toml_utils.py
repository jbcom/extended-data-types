"""TOML Utilities Module.

This module provides utilities for encoding and decoding TOML data using tomlkit.
"""

from __future__ import annotations

from typing import Any

import tomlkit

from .type_utils import convert_special_types


def decode_toml(toml_data: str) -> Any:
    """Decodes a TOML string into a Python object using tomlkit.

    Args:
        toml_data (str): The TOML string to decode.

    Returns:
        Any: The decoded Python object with any special types processed.
    """
    return tomlkit.parse(toml_data)


def encode_toml(raw_data: Any) -> str:
    """Encodes a Python object into a TOML string using tomlkit.

    Args:
        raw_data (Any): The Python object to encode.

    Returns:
        str: The encoded TOML string.
    """
    # Convert unsupported types to simpler forms before encoding
    converted_data = convert_special_types(raw_data)
    return tomlkit.dumps(converted_data)
