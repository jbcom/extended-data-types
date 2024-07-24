"""This module provides utilities for decoding and encoding HCL2 data.

It includes functions to decode HCL2 strings into Python objects with appropriate
error handling, and to encode Python objects into HCL2 strings.

Credits:
    The approach for encoding HCL2 data is inspired by Nicolai Antiferov's article:
    https://nklya.medium.com/how-to-write-hcl2-from-python-53ac12e45874
"""

from __future__ import annotations

import json

from io import StringIO
from typing import Any

import hcl2

from lark.exceptions import UnexpectedToken


def decode_hcl2(hcl2_data: str) -> Any:
    """Decodes HCL2 data into a Python object.

    Args:
        hcl2_data (str): The HCL2 data to decode.

    Returns:
        Any: The decoded Python object.

    Raises:
        ValueError: If the HCL2 data cannot be parsed.
    """
    hcl2_data_stream = StringIO(hcl2_data)
    try:
        return hcl2.load(hcl2_data_stream)
    except UnexpectedToken as e:
        error_message = f"Invalid HCL2 data: {e}"
        raise ValueError(error_message) from e


def encode_hcl2(data: Any) -> str:
    """Encodes a Python object into an HCL2 string.

    Args:
        data (Any): The Python object to encode.

    Returns:
        str: The encoded HCL2 string.
    """
    return json.dumps(data, indent=2, separators=(",", " = "))
