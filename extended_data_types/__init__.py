"""Extended Data Types Library.

This library provides extended functionality for handling various data types in Python.
It includes utilities for YAML, JSON, Base64, file paths, strings, lists, maps, and more.
"""  # noqa: E501

from .base64_utils import base64_encode
from .export_utils import wrap_raw_data_for_export
from .file_data_type import (
    file_path_depth,
    file_path_rel_to_root,
    get_encoding_for_file_path,
    match_file_extensions,
)
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
from .nothing_utils import (
    all_non_empty,
    any_non_empty,
    are_nothing,
    first_non_empty,
    is_nothing,
    yield_non_empty,
)
from .stack_utils import filter_methods, get_available_methods, get_caller
from .string_data_type import (
    is_url,
    lower_first_char,
    sanitize_key,
    strtobool,
    titleize_name,
    truncate,
    upper_first_char,
)
from .yaml_utils import (
    PureDumper,
    PureLoader,
    YamlPairs,
    YamlTagged,
    decode_yaml,
    encode_yaml,
    is_yaml_data,
    yaml_construct_pairs,
    yaml_construct_undefined,
    yaml_represent_pairs,
    yaml_represent_tagged,
    yaml_str_representer,
)


__all__ = [
    "base64_encode",
    "wrap_raw_data_for_export",
    "match_file_extensions",
    "get_encoding_for_file_path",
    "file_path_depth",
    "file_path_rel_to_root",
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
    "are_nothing",
    "first_non_empty",
    "any_non_empty",
    "yield_non_empty",
    "get_caller",
    "filter_methods",
    "get_available_methods",
    "sanitize_key",
    "truncate",
    "lower_first_char",
    "upper_first_char",
    "is_url",
    "titleize_name",
    "strtobool",
    "YamlTagged",
    "YamlPairs",
    "PureLoader",
    "PureDumper",
    "decode_yaml",
    "encode_yaml",
    "is_yaml_data",
    "yaml_construct_undefined",
    "yaml_construct_pairs",
    "yaml_represent_tagged",
    "yaml_represent_pairs",
    "yaml_str_representer",
]
