"""String transformation utilities.

This module provides functions for string case conversion, inflection,
and formatting operations.
"""

from __future__ import annotations

import inflection


def to_snake_case(text: str) -> str:
    """Convert string to snake_case."""
    return inflection.underscore(text)


def to_camel_case(text: str, uppercase_first: bool = False) -> str:
    """Convert string to camelCase or PascalCase."""
    return inflection.camelize(text, uppercase_first_letter=uppercase_first)


def to_pascal_case(text: str) -> str:
    """Convert string to PascalCase."""
    return inflection.camelize(text, uppercase_first_letter=True)


def to_kebab_case(text: str) -> str:
    """Convert string to kebab-case."""
    return inflection.dasherize(inflection.underscore(text))


def pluralize(text: str) -> str:
    """Convert string to plural form."""
    return inflection.pluralize(text)


def singularize(text: str) -> str:
    """Convert string to singular form."""
    return inflection.singularize(text)


def humanize(text: str) -> str:
    """Convert string to human-readable form."""
    return inflection.humanize(text)


def titleize(text: str) -> str:
    """Convert string to title case."""
    return inflection.titleize(text)


def ordinalize(number: int | str) -> str:
    """Convert number to ordinal string (1 -> 1st, 2 -> 2nd, etc)."""
    return inflection.ordinalize(str(number))
