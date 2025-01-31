"""Backward compatibility layer for bob validation utilities.

This module provides compatibility with bob's validation_utils while using
the modern Validator internally.
"""

from typing import Any, Type, TypeVar

from ..validation.validators import Validator

T = TypeVar('T')

# Global validator instance for compatibility functions
_validator = Validator(strict=False, coerce_types=True)


def validate_type(value: Any, expected_type: Type[T]) -> bool:
    """Maintains compatibility with bob.validation_utils.validate_type."""
    result = _validator.validate_type(value, expected_type)
    return result.is_valid


def validate_types(values: list[Any], expected_type: Type[T]) -> bool:
    """Maintains compatibility with bob.validation_utils.validate_types."""
    result = _validator.validate_sequence(values, expected_type)
    return result.is_valid 