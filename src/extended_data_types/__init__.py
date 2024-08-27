"""Extended Data Types Library.

This library provides extended functionality for handling various data types in Python.
It includes utilities for YAML, JSON, Base64, file paths, strings, lists, maps, and more.
"""

from __future__ import annotations

from .base64_utils import base64_decode, base64_encode
from .export_utils import wrap_raw_data_for_export
from .hcl2_utils import decode_hcl2
from .json_utils import decode_json, encode_json
from .list_data_type import filter_list, flatten_list
from .map_data_type import (
    all_values_from_map,
    deduplicate_map,
    filter_map,
    first_non_empty_value_from_map,
    flatten_map,
    get_default_dict,
    unhump_map,
    zipmap,
)
from .matcher_utils import is_non_empty_match, is_partial_match
from .splitter_utils import split_dict_by_type, split_list_by_type
from .stack_utils import (
    filter_methods,
    get_available_methods,
    get_caller,
    get_unique_signature,
)
from .state_utils import (
    all_non_empty,
    all_non_empty_in_dict,
    all_non_empty_in_list,
    any_non_empty,
    are_nothing,
    first_non_empty,
    is_nothing,
    yield_non_empty,
)
from .string_data_type import (
    is_url,
    lower_first_char,
    sanitize_key,
    strtobool,
    titleize_name,
    truncate,
    upper_first_char,
)
from .yaml_utils import decode_yaml, encode_yaml, is_yaml_data


__version__ = "1.0.2"

__all__ = [
    "base64_decode",
    "base64_encode",
    "wrap_raw_data_for_export",
    "decode_hcl2",
    "decode_json",
    "encode_json",
    "flatten_list",
    "filter_list",
    "first_non_empty_value_from_map",
    "deduplicate_map",
    "all_values_from_map",
    "flatten_map",
    "zipmap",
    "get_default_dict",
    "unhump_map",
    "filter_map",
    "is_partial_match",
    "is_non_empty_match",
    "is_nothing",
    "all_non_empty",
    "all_non_empty_in_list",
    "all_non_empty_in_dict",
    "are_nothing",
    "first_non_empty",
    "any_non_empty",
    "yield_non_empty",
    "split_list_by_type",
    "split_dict_by_type",
    "get_caller",
    "get_unique_signature",
    "filter_methods",
    "get_available_methods",
    "sanitize_key",
    "truncate",
    "lower_first_char",
    "upper_first_char",
    "is_url",
    "titleize_name",
    "strtobool",
    "decode_yaml",
    "encode_yaml",
    "is_yaml_data",
]
