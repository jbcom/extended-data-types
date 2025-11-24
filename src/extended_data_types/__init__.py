"""Extended Data Types - Enhanced Python collections with advanced functionality
"""

from typing import TypeAlias

# Legacy utilities (v5 API)
from .base64_utils import base64_decode, base64_encode
from .export_utils import make_raw_data_export_safe, wrap_raw_data_for_export
from .file_data_type import (
    FilePath,
    clone_repository_to_temp,
    file_path_depth,
    file_path_rel_to_root,
    get_encoding_for_file_path,
    get_parent_repository,
    get_repository_name,
    get_tld,
    match_file_extensions,
)
from .hcl2_utils import decode_hcl2
from .import_utils import unwrap_raw_data_from_import
from .json_utils import decode_json, encode_json
from .list_data_type import filter_list, flatten_list
from .map_data_type import (
    SortedDefaultDict,
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
    get_inputs_from_docstring,
    get_unique_signature,
    update_docstring,
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
    bytestostr,
    is_url,
    lower_first_char,
    removeprefix,
    removesuffix,
    sanitize_key,
    titleize_name,
    truncate,
    upper_first_char,
)
from .toml_utils import decode_toml, encode_toml
from .type_utils import (
    convert_special_type,
    convert_special_types,
    get_default_value_for_type,
    get_primitive_type_for_instance_type,
    reconstruct_special_type,
    reconstruct_special_types,
    strtobool,
    strtodate,
    strtodatetime,
    strtofloat,
    strtoint,
    strtopath,
    strtotime,
    typeof,
)
from .yaml_utils import decode_yaml, encode_yaml, is_yaml_data

# Compatibility utilities (new compat layer)
from .compat import (
    check_compatibility,
    convert_legacy_format,
    unflatten_map,
)

# Core types and aliases (new architecture)
from .core import (
    ExtDict,
    ExtendedBase,
    ExtendedDict,
    ExtendedFrozenSet,
    ExtendedList,
    ExtendedSet,
    ExtFrozenSet,
    ExtList,
    ExtSet,
)

# Inspection utilities (new architecture)
from .inspection import (
    SchemaValidator,
    StructureInfo,
    TypeInfo,
    get_schema,
    get_type_info,
    inspect_structure,
)

# Pattern matching (new architecture)
from .matching import Matcher

# Serialization (new architecture)
from .serialization import (
    get_serializer,
    guess_format,
    register_format,
)


__version__ = "6.0.0"

__all__ = [
    # Version
    "__version__",
    # Core types (legacy + new)
    "ExtendedDict",
    "ExtendedList",
    "ExtendedSet",
    "ExtendedFrozenSet",
    "ExtDict",
    "ExtList",
    "ExtSet",
    "ExtFrozenSet",
    "ExtendedBase",
    # Serialization
    "register_format",
    "get_serializer",
    "guess_format",
    # Inspection
    "get_type_info",
    "TypeInfo",
    "inspect_structure",
    "StructureInfo",
    "get_schema",
    "SchemaValidator",
    # Matching
    "Matcher",
    # Legacy compatibility utilities
    "base64_decode",
    "base64_encode",
    "make_raw_data_export_safe",
    "wrap_raw_data_for_export",
    "FilePath",
    "clone_repository_to_temp",
    "file_path_depth",
    "file_path_rel_to_root",
    "get_encoding_for_file_path",
    "get_parent_repository",
    "get_repository_name",
    "get_tld",
    "match_file_extensions",
    "decode_hcl2",
    "unwrap_raw_data_from_import",
    "decode_json",
    "encode_json",
    "filter_list",
    "flatten_list",
    "SortedDefaultDict",
    "all_values_from_map",
    "deduplicate_map",
    "filter_map",
    "first_non_empty_value_from_map",
    "flatten_map",
    "get_default_dict",
    "unhump_map",
    "zipmap",
    "is_non_empty_match",
    "is_partial_match",
    "split_dict_by_type",
    "split_list_by_type",
    "filter_methods",
    "get_available_methods",
    "get_caller",
    "get_inputs_from_docstring",
    "get_unique_signature",
    "update_docstring",
    "all_non_empty",
    "all_non_empty_in_dict",
    "all_non_empty_in_list",
    "any_non_empty",
    "are_nothing",
    "first_non_empty",
    "is_nothing",
    "yield_non_empty",
    "bytestostr",
    "is_url",
    "lower_first_char",
    "removeprefix",
    "removesuffix",
    "sanitize_key",
    "titleize_name",
    "truncate",
    "upper_first_char",
    "decode_toml",
    "encode_toml",
    "convert_special_type",
    "convert_special_types",
    "get_default_value_for_type",
    "get_primitive_type_for_instance_type",
    "reconstruct_special_type",
    "reconstruct_special_types",
    "strtobool",
    "strtodate",
    "strtodatetime",
    "strtofloat",
    "strtoint",
    "strtopath",
    "strtotime",
    "typeof",
    "decode_yaml",
    "encode_yaml",
    "is_yaml_data",
    # Compat helpers
    "flatten_map",
    "unflatten_map",
    "convert_legacy_format",
    "check_compatibility",
]
