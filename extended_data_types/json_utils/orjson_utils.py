"""orjson Utilities Module.

This module provides utilities for encoding and decoding JSON using the `orjson` library.
"""  # noqa: E501

from typing import Any, Dict

import orjson


def decode_json(json_data: str) -> Any:
    """Decodes a JSON string into a Python object using orjson.

    Args:
        json_data (str): The JSON string to decode.

    Returns:
        Any: The decoded Python object.
    """
    return orjson.loads(json_data.encode("utf-8"))


def encode_json(raw_data: Any, **format_opts: Dict[str, Any]) -> str:
    """Encodes a Python object into a JSON string using orjson.

    Args:
        raw_data (Any): The Python object to encode.
        format_opts (Dict[str, Any]): Options for formatting the JSON output.

    Returns:
        str: The encoded JSON string.
    """
    orjson_opts = 0
    if format_opts.get("indent", 2):
        orjson_opts |= orjson.OPT_INDENT_2

    if format_opts.get("sort_keys", True):
        orjson_opts |= orjson.OPT_SORT_KEYS

    return orjson.dumps(raw_data, option=orjson_opts).decode("utf-8")
