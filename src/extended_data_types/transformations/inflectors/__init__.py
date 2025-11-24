"""Inflector modules for different types.

This package provides specialized inflection utilities for different data types:
- String inflectors (case, format, etc.)
- Number inflectors (words, ordinals, etc.)
- Collection inflectors (coming soon)
- Date inflectors (coming soon)
- Path inflectors (coming soon)
"""

from .number import *
from .string import *

__all__ = [
    # String inflectors
    'pluralize', 'singularize', 'ordinalize', 'parameterize',
    'transliterate', 'underscore_to_camel', 'underscore_to_pascal',
    'humanize', 'titleize', 'dasherize', 'underscore',

    # Number inflectors
    'to_words', 'to_ordinal_words', 'to_currency', 'to_year',
    'to_scientific_notation', 'to_roman_numeral', 'from_roman_numeral',
]
