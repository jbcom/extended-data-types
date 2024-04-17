"""JSON Utilities Initialization.

This module initializes the JSON utilities and provides conditional imports
for encoding and decoding JSON using either the `json` library or the `orjson` library.
"""

try:
    from .orjson_utils import decode_json, encode_json
except ImportError:
    from .json_utils import decode_json, encode_json

__all__ = ["decode_json", "encode_json"]
