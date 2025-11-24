"""String format transformation utilities."""

from __future__ import annotations

import string

from collections.abc import Mapping
from typing import Any, Literal


def format_template(
    template: str, values: Mapping[str, Any], default: str | None = None
) -> str:
    """Format string template with values.

    Args:
        template: Template string with placeholders
        values: Values to insert
        default: Default value if key missing

    Returns:
        Formatted string

    Example:
        >>> format_template("Hello, ${name}!", {"name": "World"})
        'Hello, World!'
    """
    try:
        return string.Template(template).substitute(values)
    except KeyError:
        if default is not None:
            return default
        raise


def truncate(
    text: str, length: int, suffix: str = "...", word_boundary: bool = True
) -> str:
    """Truncate text to specified length.

    Args:
        text: Text to truncate
        length: Maximum length
        suffix: String to append
        word_boundary: Whether to truncate at word boundary

    Returns:
        Truncated string
    """
    if len(text) <= length:
        return text

    if word_boundary:
        return text[:length].rsplit(" ", 1)[0] + suffix
    return text[:length] + suffix


def pad(
    text: str,
    length: int,
    char: str = " ",
    align: Literal["left", "right", "center"] = "left",
) -> str:
    """Pad text to specified length.

    Args:
        text: Text to pad
        length: Desired length
        char: Padding character
        align: Alignment direction

    Returns:
        Padded string
    """
    if align == "left":
        return text.ljust(length, char)
    elif align == "right":
        return text.rjust(length, char)
    return text.center(length, char)
