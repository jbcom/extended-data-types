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

from .core import (camelize, dasherize, humanize, is_url, pascalize,
                   removesuffix, snakeize, titleize, underscore)
from .formatters import format_number, format_size, format_time
from .inflection import (camelize_all, dasherize_all, humanize_all, inflect,
                         inflect_mapping, inflect_sequence, inflect_value,
                         pascalize_all, snakeize_all, titleize_all,
                         underscore_all)
from .matcher import is_non_empty_match, is_partial_match
from .validators import is_empty, is_not_empty, is_whitespace

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