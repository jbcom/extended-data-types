"""String transformation operations."""

from .case import to_camel, to_kebab, to_lower, to_pascal, to_snake, to_title, to_upper
from .format import align, format_template, pad, truncate, wrap
from .inflection import ordinalize, parameterize, pluralize, singularize, transliterate
from .pattern import extract_pattern, match_pattern, replace_pattern, split_pattern


__all__ = [
    # Case operations
    "to_upper",
    "to_lower",
    "to_title",
    "to_camel",
    "to_pascal",
    "to_snake",
    "to_kebab",
    # Formatting
    "format_template",
    "truncate",
    "pad",
    "wrap",
    "align",
    # Pattern matching
    "match_pattern",
    "replace_pattern",
    "extract_pattern",
    "split_pattern",
    # Inflection
    "pluralize",
    "singularize",
    "ordinalize",
    "parameterize",
    "transliterate",
]
