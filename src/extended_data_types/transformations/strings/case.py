"""String case transformation operations."""

from __future__ import annotations

import re

from typing import Literal

from ..core import Transform


CaseStyle = Literal["upper", "lower", "title", "camel", "pascal", "snake", "kebab"]


def to_upper(text: str) -> str:
    """Convert string to uppercase.

    Args:
        text: String to convert

    Returns:
        Uppercase string

    Example:
        >>> to_upper("hello")
        'HELLO'
    """
    return text.upper()


def to_lower(text: str) -> str:
    """Convert string to lowercase.

    Args:
        text: String to convert

    Returns:
        Lowercase string

    Example:
        >>> to_lower("HELLO")
        'hello'
    """
    return text.lower()


def to_title(text: str) -> str:
    """Convert string to title case.

    Args:
        text: String to convert

    Returns:
        Title case string

    Example:
        >>> to_title("hello world")
        'Hello World'
    """
    return text.title()


def to_camel(text: str) -> str:
    """Convert string to camelCase.

    Args:
        text: String to convert

    Returns:
        camelCase string

    Example:
        >>> to_camel("hello_world")
        'helloWorld'
    """
    words = text.replace("-", "_").split("_")
    return words[0].lower() + "".join(w.capitalize() for w in words[1:])


def to_pascal(text: str) -> str:
    """Convert string to PascalCase.

    Args:
        text: String to convert

    Returns:
        PascalCase string

    Example:
        >>> to_pascal("hello_world")
        'HelloWorld'
    """
    return "".join(word.capitalize() for word in text.replace("-", "_").split("_"))


def to_snake(text: str) -> str:
    """Convert string to snake_case.

    Args:
        text: String to convert

    Returns:
        snake_case string

    Example:
        >>> to_snake("helloWorld")
        'hello_world'
    """
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", text)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def to_kebab(text: str) -> str:
    """Convert string to kebab-case.

    Args:
        text: String to convert

    Returns:
        kebab-case string

    Example:
        >>> to_kebab("helloWorld")
        'hello-world'
    """
    return to_snake(text).replace("_", "-")


# Register transforms
upper_transform = Transform(to_upper)
lower_transform = Transform(to_lower)
title_transform = Transform(to_title)
camel_transform = Transform(to_camel)
pascal_transform = Transform(to_pascal)
snake_transform = Transform(to_snake)
kebab_transform = Transform(to_kebab)
