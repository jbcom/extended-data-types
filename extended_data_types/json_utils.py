from __future__ import annotations, division, print_function, unicode_literals

from typing import Any, Dict

import orjson


def decode_json(json_data: str) -> Any:
    """Decodes a JSON string into a Python object.

    Args:
        json_data (str): The JSON string to decode.

    Returns:
        Any: The decoded Python object.
    """
    raw_data = orjson.loads(json_data.encode("utf-8"))
    return raw_data


def encode_json(raw_data: Any, **format_opts: Dict[str, Any]) -> str:
    """Encodes a Python object into a JSON string.

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
