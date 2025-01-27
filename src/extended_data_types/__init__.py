"""Extended Data Types Library.

This library provides extended functionality for handling various data types in Python.
It includes utilities for YAML, JSON, TOML, Base64, file paths, Git repositories, strings,
lists, maps, and more.
"""

from __future__ import annotations

from .base64_utils import base64_decode, base64_encode
from .export_utils import wrap_raw_data_for_export
from .file_data_type import (FilePath, clone_repository_to_temp,
                             file_path_depth, file_path_rel_to_root,
                             get_encoding_for_file_path, get_parent_repository,
                             get_repository_name, get_tld,
                             match_file_extensions)
from .hcl2_utils import decode_hcl2
from .import_utils import unwrap_raw_data_from_import
from .json_utils import decode_json, encode_json
from .list_data_type import filter_list, flatten_list
from .map_data_type import (SortedDefaultDict, all_values_from_map,
                            deduplicate_map, filter_map,
                            first_non_empty_value_from_map, flatten_map,
                            get_default_dict, unhump_map, zipmap)
from .matcher_utils import is_non_empty_match, is_partial_match
from .splitter_utils import split_dict_by_type, split_list_by_type
from .stack_utils import (filter_methods, get_available_methods, get_caller,
                          get_inputs_from_docstring, get_unique_signature,
                          update_docstring)
from .state_utils import (all_non_empty, all_non_empty_in_dict,
                          all_non_empty_in_list, any_non_empty, are_nothing,
                          first_non_empty, is_nothing, yield_non_empty)
from .string_data_type import (bytestostr, is_url, lower_first_char,
                               removeprefix, removesuffix, sanitize_key,
                               titleize_name, truncate, upper_first_char)
from .toml_utils import decode_toml, encode_toml
from .type_utils import (convert_special_type, convert_special_types,
                         get_default_value_for_type,
                         get_primitive_type_for_instance_type,
                         reconstruct_special_type, reconstruct_special_types,
                         strtobool, strtodate, strtodatetime, strtofloat,
                         strtoint, strtopath, strtotime, typeof)
from .yaml_utils import decode_yaml, encode_yaml, is_yaml_data

__version__ = "5.0.0"

__all__ = [
    "FilePath",
    "SortedDefaultDict",
    "all_non_empty",
    "all_non_empty_in_dict",
    "all_non_empty_in_list",
    "all_values_from_map",
    "any_non_empty",
    "are_nothing",
    "base64_decode",
    "base64_encode",
    "bytestostr",
    "clone_repository_to_temp",
    "convert_special_type",
    "convert_special_types",
    "decode_hcl2",
    "decode_json",
    "decode_toml",
    "decode_yaml",
    "deduplicate_map",
    "encode_json",
    "encode_toml",
    "encode_yaml",
    "file_path_depth",
    "file_path_rel_to_root",
    "filter_list",
    "filter_map",
    "filter_methods",
    "first_non_empty",
    "first_non_empty_value_from_map",
    "flatten_list",
    "flatten_map",
    "get_available_methods",
    "get_caller",
    "get_default_dict",
    "get_default_value_for_type",
    "get_encoding_for_file_path",
    "get_inputs_from_docstring",
    "get_parent_repository",
    "get_primitive_type_for_instance_type",
    "get_repository_name",
    "get_tld",
    "get_unique_signature",
    "is_non_empty_match",
    "is_nothing",
    "is_partial_match",
    "is_url",
    "is_yaml_data",
    "lower_first_char",
    "match_file_extensions",
    "reconstruct_special_type",
    "reconstruct_special_types",
    "removeprefix",
    "removesuffix",
    "sanitize_key",
    "split_dict_by_type",
    "split_list_by_type",
    "strtobool",
    "strtodate",
    "strtodatetime",
    "strtofloat",
    "strtoint",
    "strtopath",
    "strtotime",
    "titleize_name",
    "truncate",
    "typeof",
    "unhump_map",
    "unwrap_raw_data_from_import",
    "update_docstring",
    "upper_first_char",
    "wrap_raw_data_for_export",
    "yield_non_empty",
    "zipmap",
]
