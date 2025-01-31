"""Extended Data Types - Enhanced Python collections with advanced functionality
"""

from typing import TypeAlias

# CLI utilities
from .cli import ConfigManager, convert_format, format_output, validate_schema

# Compatibility utilities
from .compat import (
    check_compatibility,
    convert_legacy_format,
    flatten_map,
    unflatten_map,
)

# Core types and aliases
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

# Inspection utilities
from .inspection import (
    SchemaValidator,
    StructureInfo,
    TypeInfo,
    get_schema,
    get_type_info,
    inspect_structure,
)

# I/O operations
from .io import StreamReader, StreamWriter, dump, dumps, load, loads

# Pattern matching
from .matching import (
    CompositeRule,
    ExactMatcher,
    RangeMatcher,
    RegexMatcher,
    Rule,
    TypeMatcher,
    compile_pattern,
    match_pattern,
)

# Serialization
from .serialization import (
    JsonSerializer,
    TomlSerializer,
    YamlSerializer,
    get_serializer,
    guess_format,
    register_format,
)


__version__ = "5.0.3"

__all__ = [
    # Version
    "__version__",
    # Core types
    "ExtendedDict",
    "ExtendedList",
    "ExtendedSet",
    "ExtendedFrozenSet",
    "ExtDict",
    "ExtList",
    "ExtSet",
    "ExtFrozenSet",
    "ExtendedBase",
    # I/O
    "load",
    "dump",
    "loads",
    "dumps",
    "StreamReader",
    "StreamWriter",
    # Serialization
    "register_format",
    "get_serializer",
    "guess_format",
    "JsonSerializer",
    "YamlSerializer",
    "TomlSerializer",
    # Inspection
    "get_type_info",
    "TypeInfo",
    "inspect_structure",
    "StructureInfo",
    "get_schema",
    "SchemaValidator",
    # Matching
    "match_pattern",
    "compile_pattern",
    "Rule",
    "CompositeRule",
    "ExactMatcher",
    "RegexMatcher",
    "TypeMatcher",
    "RangeMatcher",
    # CLI
    "convert_format",
    "validate_schema",
    "ConfigManager",
    "format_output",
    # Compat
    "flatten_map",
    "unflatten_map",
    "convert_legacy_format",
    "check_compatibility",
]
