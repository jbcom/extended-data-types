"""String inflection utilities.

This module provides comprehensive string inflection operations:
- Case conversion (camel, snake, etc.)
- Pluralization
- Parameterization
- Transliteration
- Humanization
"""

from __future__ import annotations

import inflection
import unidecode


def pluralize(text: str, count: int | None = None) -> str:
    """Convert string to plural form.

    Args:
        text: String to pluralize
        count: Optional count to conditionally pluralize

    Examples:
        >>> pluralize("cat")
        'cats'
        >>> pluralize("cat", 1)
        'cat'
        >>> pluralize("cat", 2)
        'cats'
    """
    if count == 1:
        return text
    return inflection.pluralize(text)


def singularize(text: str) -> str:
    """Convert string to singular form.

    Args:
        text: String to singularize

    Examples:
        >>> singularize("cats")
        'cat'
    """
    return inflection.singularize(text)


def ordinalize(number: int) -> str:
    """Convert number to ordinal string.

    Args:
        number: Number to ordinalize

    Examples:
        >>> ordinalize(1)
        '1st'
        >>> ordinalize(42)
        '42nd'
    """
    return inflection.ordinalize(number)


def parameterize(text: str) -> str:
    """Convert string to URL-safe parameter.

    Args:
        text: String to parameterize

    Examples:
        >>> parameterize("Hello World!")
        'hello-world'
    """
    return inflection.parameterize(text)


def transliterate(text: str) -> str:
    """Convert Unicode string to ASCII.

    Args:
        text: String to transliterate

    Examples:
        >>> transliterate("Café")
        'Cafe'
    """
    return unidecode.unidecode(text)


def underscore_to_camel(text: str) -> str:
    """Convert underscore_case to camelCase.

    Args:
        text: String to convert

    Examples:
        >>> underscore_to_camel("hello_world")
        'helloWorld'
    """
    return inflection.camelize(text, uppercase_first_letter=False)


def underscore_to_pascal(text: str) -> str:
    """Convert underscore_case to PascalCase.

    Args:
        text: String to convert

    Examples:
        >>> underscore_to_pascal("hello_world")
        'HelloWorld'
    """
    return inflection.camelize(text)


def humanize(text: str) -> str:
    """Convert string to human-readable form.

    Args:
        text: String to humanize

    Examples:
        >>> humanize("hello_world")
        'Hello world'
    """
    return inflection.humanize(text)


def titleize(text: str) -> str:
    """Convert string to title case.

    Args:
        text: String to titleize

    Examples:
        >>> titleize("hello world")
        'Hello World'
    """
    return inflection.titleize(text)


def dasherize(text: str) -> str:
    """Convert underscores to dashes.

    Args:
        text: String to dasherize

    Examples:
        >>> dasherize("hello_world")
        'hello-world'
    """
    return inflection.dasherize(text)


def underscore(text: str) -> str:
    """Convert camelCase to underscore_case.

    Args:
        text: String to underscore

    Examples:
        >>> underscore("HelloWorld")
        'hello_world'
    """
    return inflection.underscore(text)
