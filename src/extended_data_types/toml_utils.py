"""TOML Utilities Module.

This module provides utilities for encoding and decoding TOML data using tomlkit.
"""

from __future__ import annotations

from typing import Any

import tomlkit


def decode_toml(toml_data: str) -> Any:
    """Decodes a TOML string into a Python object using tomlkit.

    Args:
        toml_data (str): The TOML string to decode.

    Returns:
        Any: The decoded Python object.
    """
    return tomlkit.parse(toml_data)


def encode_toml(raw_data: Any) -> str:
    """Encodes a Python object into a TOML string using tomlkit.

    Args:
        raw_data (Any): The Python object to encode.

    Returns:
        str: The encoded TOML string.
    """
    return tomlkit.dumps(raw_data)
