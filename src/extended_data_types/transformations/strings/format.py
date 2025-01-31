"""String formatting transformation operations."""

from __future__ import annotations

import textwrap
from string import Template
from typing import Any, Literal, Mapping

from ..core import Transform

Alignment = Literal['left', 'right', 'center']


def format_template(
    template: str,
    values: Mapping[str, Any],
    default: str | None = None,
    safe: bool = True
) -> str:
    """Format string template with values.
    
    Args:
        template: Template string with placeholders
        values: Values to insert
        default: Default value for missing keys
        safe: Whether to use safe substitution
        
    Returns:
        Formatted string
        
    Example:
        >>> format_template("Hello, ${name}!", {"name": "World"})
        'Hello, World!'
    """
    t = Template(template)
    try:
        if safe:
            return t.safe_substitute(values)
        return t.substitute(values)
    except KeyError:
        if default is not None:
            return default
        raise


def truncate(
    text: str,
    length: int,
    suffix: str = "...",
    word_boundary: bool = True
) -> str:
    """Truncate text to specified length.
    
    Args:
        text: Text to truncate
        length: Maximum length
        suffix: String to append
        word_boundary: Whether to truncate at word boundary
        
    Returns:
        Truncated string
        
    Example:
        >>> truncate("Hello world", 8)
        'Hello...'
    """
    if len(text) <= length:
        return text

    if word_boundary:
        return text[:length].rsplit(' ', 1)[0] + suffix
    return text[:length] + suffix


def pad(
    text: str,
    length: int,
    char: str = " ",
    align: Alignment = "left"
) -> str:
    """Pad text to specified length.
    
    Args:
        text: Text to pad
        length: Desired length
        char: Padding character
        align: Alignment direction
        
    Returns:
        Padded string
        
    Example:
        >>> pad("hello", 10)
        'hello     '
    """
    if align == "left":
        return text.ljust(length, char)
    elif align == "right":
        return text.rjust(length, char)
    return text.center(length, char)


def wrap(
    text: str,
    width: int = 70,
    indent: str = "",
    initial_indent: str | None = None
) -> str:
    """Wrap text to specified width.
    
    Args:
        text: Text to wrap
        width: Maximum line width
        indent: String to use for indentation
        initial_indent: First line indent (defaults to indent)
        
    Returns:
        Wrapped text
        
    Example:
        >>> wrap("A very long text", width=10)
        'A very\\nlong text'
    """
    return textwrap.fill(
        text,
        width=width,
        initial_indent=initial_indent or indent,
        subsequent_indent=indent
    )


def align(
    text: str,
    width: int,
    alignment: Alignment = "left",
    fill_char: str = " "
) -> str:
    """Align text within specified width.
    
    Args:
        text: Text to align
        width: Total width
        alignment: Alignment direction
        fill_char: Character for filling space
        
    Returns:
        Aligned text
        
    Example:
        >>> align("hello", 10, "center")
        '  hello   '
    """
    if alignment == "left":
        return text.ljust(width, fill_char)
    elif alignment == "right":
        return text.rjust(width, fill_char)
    return text.center(width, fill_char)


# Register transforms
format_template_transform = Transform(format_template)
truncate_transform = Transform(truncate)
pad_transform = Transform(pad)
wrap_transform = Transform(wrap)
align_transform = Transform(align) 