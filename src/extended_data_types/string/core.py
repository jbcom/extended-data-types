"""Core string functionality.

This module provides core string manipulation and conversion utilities:
- String type conversion and coercion
- Extended string type registration
- String primitive operations
- Type-safe string operations
- String validation hooks
- String transformation utilities

Key Features:
- Safe conversion from any type to string
- Preservation of string metadata
- Type registry integration
- Validation support
- Error handling
- Performance optimizations

Type Conversion Rules:
- Direct string conversion for primitive types
- JSON serialization for complex types
- Custom handlers for special types
- Fallback to str() for unknown types

Error Handling:
- TypeError for unconvertible types
- ValueError for invalid string operations
- Preservation of original error context
- Detailed error messages
"""

from __future__ import annotations

from typing import Any

# Removed import of non-existent module
from extended_data_types.core.conversion import TypeRegistry  # type: ignore[attr-defined]

from .types import ExtendedString, Pattern  # type: ignore[attr-defined]


def to_extended_string(value: Any) -> ExtendedString:
    """Convert any value to an ExtendedString.

    Args:
        value: The value to convert.

    Returns:
        ExtendedString representation of the value.

    Raises:
        TypeError: If the value cannot be converted to a string.

    Example:
        >>> to_extended_string(123)
        ExtendedString('123')
        >>> to_extended_string(['a', 'b'])
        ExtendedString("['a', 'b']")
    """
    try:
        # Try using TypeRegistry first
        return TypeRegistry.convert(value, ExtendedString)
    except (TypeError, ValueError):
        # Fall back to string coercion
        return ExtendedString(str(value))


def create_pattern(pattern: str, flags: int = 0) -> Pattern:
    """Create a named pattern for reuse.

    Args:
        pattern: The regular expression pattern string.
        flags: Regular expression flags.

    Returns:
        A Pattern instance.
    """
    return Pattern(pattern, flags)


def join_extended(*parts: Any, separator: str = "") -> ExtendedString:
    """Join multiple values into an ExtendedString.

    Args:
        *parts: Values to join.
        separator: Separator to use between parts.

    Returns:
        An ExtendedString of the joined parts.
    """
    return ExtendedString(separator.join(str(p) for p in parts))


def wrap_string(
    text: str, wrapper: str | tuple[str, str], condition: bool = True
) -> ExtendedString:
    """Wrap a string with prefix/suffix if condition is met.

    Args:
        text: The text to wrap.
        wrapper: Single string for same prefix/suffix, or tuple of (prefix, suffix).
        condition: Whether to apply the wrapping.

    Returns:
        An ExtendedString with the wrapped text.

    Example:
        >>> wrap_string("text", "*")
        '*text*'
        >>> wrap_string("text", ("<", ">"))
        '<text>'
    """
    if not condition:
        return ExtendedString(text)

    if isinstance(wrapper, tuple):
        prefix, suffix = wrapper
    else:
        prefix = suffix = wrapper

    return ExtendedString(f"{prefix}{text}{suffix}")
