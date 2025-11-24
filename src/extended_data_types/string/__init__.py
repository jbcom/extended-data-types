"""String Operations and Utilities.

This package provides comprehensive string manipulation utilities:

Key Features:
- Case conversion (camel, snake, pascal)
- String inflection
- Pattern matching
- String validation
- Text formatting
- String comparison
- Type conversion
- Text processing
- String operations
- Case detection
- String validation
- Pattern detection
- String transformation
- Text normalization
"""

from .core import (
    camelize,  # type: ignore[attr-defined]
    dasherize,  # type: ignore[attr-defined]
    humanize,  # type: ignore[attr-defined]
    is_url,  # type: ignore[attr-defined]
    pascalize,  # type: ignore[attr-defined]
    removesuffix,  # type: ignore[attr-defined]
    snakeize,  # type: ignore[attr-defined]
    titleize,  # type: ignore[attr-defined]
    underscore,  # type: ignore[attr-defined]
)
from .formatters import format_number, format_size, format_time  # type: ignore[attr-defined]
from .inflection import (
    camelize_all,  # type: ignore[attr-defined]
    dasherize_all,  # type: ignore[attr-defined]
    humanize_all,  # type: ignore[attr-defined]
    inflect,  # type: ignore[attr-defined]
    inflect_mapping,  # type: ignore[attr-defined]
    inflect_sequence,  # type: ignore[attr-defined]
    inflect_value,  # type: ignore[attr-defined]
    pascalize_all,  # type: ignore[attr-defined]
    snakeize_all,  # type: ignore[attr-defined]
    titleize_all,  # type: ignore[attr-defined]
    underscore_all,  # type: ignore[attr-defined]
)
from .matcher import is_non_empty_match, is_partial_match  # type: ignore[attr-defined]
from .validators import is_empty, is_not_empty, is_whitespace  # type: ignore[attr-defined]


__all__ = [
    # Core string operations
    "camelize",
    "dasherize",
    "humanize",
    "is_url",
    "pascalize",
    "removesuffix",
    "snakeize",
    "titleize",
    "underscore",
    # Formatters
    "format_number",
    "format_size",
    "format_time",
    # Inflection utilities
    "camelize_all",
    "dasherize_all",
    "humanize_all",
    "inflect",
    "inflect_mapping",
    "inflect_sequence",
    "inflect_value",
    "pascalize_all",
    "snakeize_all",
    "titleize_all",
    "underscore_all",
    # Matchers
    "is_non_empty_match",
    "is_partial_match",
    # Validators
    "is_empty",
    "is_not_empty",
    "is_whitespace",
]
