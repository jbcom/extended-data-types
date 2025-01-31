"""Transform validation utilities."""

from __future__ import annotations

from typing import Any, Callable, TypeVar

from .transform import Transform

T = TypeVar('T')
U = TypeVar('U')


def validate_type(expected_type: type[T]) -> Callable[[Any], bool]:
    """Create a type validator.

    Args:
        expected_type: Type to validate against

    Returns:
        Validation function

    Example:
        >>> transform = Transform(str.upper, validate=validate_type(str))
        >>> transform("hello")  # Works
        'HELLO'
        >>> transform(42)  # Raises ValueError
        ValueError: Invalid input type for transform upper
    """
    return lambda x: isinstance(x, expected_type)


def validate_predicate(
    predicate: Callable[[T], bool],
    message: str | None = None
) -> Transform[T, T]:
    """Create a validation transform.

    Args:
        predicate: Validation function
        message: Optional error message

    Returns:
        Transform that validates input

    Example:
        >>> is_positive = validate_predicate(lambda x: x > 0)
        >>> is_positive(5)  # Works
        5
        >>> is_positive(-1)  # Raises ValueError
        ValueError: Validation failed
    """
    def validate(value: T) -> T:
        if not predicate(value):
            raise ValueError(message or "Validation failed")
        return value
    return Transform(validate)


def optional(transform: Transform[T, U]) -> Transform[T | None, U | None]:
    """Make a transform handle None values.

    Args:
        transform: Transform to make optional

    Returns:
        Transform that passes None through

    Example:
        >>> upper = Transform(str.upper)
        >>> optional_upper = optional(upper)
        >>> optional_upper("hello")
        'HELLO'
        >>> optional_upper(None)
        None
    """
    def handle_none(value: T | None) -> U | None:
        if value is None:
            return None
        return transform(value)
    return Transform(handle_none)


def fallback(
    transform: Transform[T, U],
    default: U
) -> Transform[T, U]:
    """Add fallback value to transform.

    Args:
        transform: Transform to add fallback to
        default: Default value if transform fails

    Returns:
        Transform with fallback

    Example:
        >>> to_int = Transform(int)
        >>> safe_int = fallback(to_int, 0)
        >>> safe_int("42")
        42
        >>> safe_int("not a number")
        0
    """
    def with_fallback(value: T) -> U:
        try:
            return transform(value)
        except Exception:
            return default
    return Transform(with_fallback) 