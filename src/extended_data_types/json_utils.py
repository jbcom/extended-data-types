"""JSON Utilities Module.

This module provides utilities for encoding and decoding JSON using the standard `json` library.
"""

from __future__ import annotations

import json

from typing import Any


def decode_json(json_data: str) -> Any:
    """Decodes a JSON string into a Python object using json.

    Args:
        json_data (str): The JSON string to decode.

    Returns:
        Any: The decoded Python object.
    """
    return json.loads(json_data)


def encode_json(raw_data: Any, **format_opts: Any) -> str:
    """Encodes a Python object into a JSON string using json.

    Args:
        raw_data (Any): The Python object to encode.
        format_opts (Any): Options for formatting the JSON output.

    Returns:
        str: The encoded JSON string.
    """
    return json.dumps(raw_data, **format_opts)
