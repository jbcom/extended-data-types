"""String inflection operations."""

from __future__ import annotations

import inflection
import unidecode

from ..core import Transform


def pluralize(text: str, count: int | None = None) -> str:
    """Convert string to plural form.

    Args:
        text: String to pluralize
        count: Optional count to conditionally pluralize

    Returns:
        Pluralized string

    Example:
        >>> pluralize("cat")
        'cats'
        >>> pluralize("cat", 1)
        'cat'
    """
    if count == 1:
        return text
    return inflection.pluralize(text)


def singularize(text: str) -> str:
    """Convert string to singular form.

    Args:
        text: String to singularize

    Returns:
        Singular string

    Example:
        >>> singularize("cats")
        'cat'
    """
    return inflection.singularize(text)


def ordinalize(number: int | str) -> str:
    """Convert number to ordinal string.

    Args:
        number: Number to convert

    Returns:
        Ordinal string

    Example:
        >>> ordinalize(1)
        '1st'
    """
    return inflection.ordinalize(str(number))


def parameterize(text: str, separator: str = "-") -> str:
    """Convert string to parameter form.

    Args:
        text: String to convert
        separator: Separator character

    Returns:
        Parameterized string

    Example:
        >>> parameterize("Hello World!")
        'hello-world'
    """
    return inflection.parameterize(text, separator)


def transliterate(text: str) -> str:
    """Convert unicode string to ASCII.

    Args:
        text: String to convert

    Returns:
        ASCII string

    Example:
        >>> transliterate("héllo")
        'hello'
    """
    return unidecode.unidecode(text)


def humanize(text: str) -> str:
    """Convert string to human readable form.

    Args:
        text: String to convert

    Returns:
        Humanized string

    Example:
        >>> humanize("hello_world")
        'Hello world'
    """
    return inflection.humanize(text)


# Register transforms
pluralize_transform = Transform(pluralize)
singularize_transform = Transform(singularize)
ordinalize_transform = Transform(ordinalize)
parameterize_transform = Transform(parameterize)
transliterate_transform = Transform(transliterate)
humanize_transform = Transform(humanize)
