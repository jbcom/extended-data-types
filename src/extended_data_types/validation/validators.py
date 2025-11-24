"""Enhanced validation utilities with type checking.

This module provides comprehensive validation capabilities with
type safety and detailed error reporting.

Typical usage:
    >>> from extended_data_types.validation.validators import Validator
    >>> validator = Validator()
    >>> validator.validate_type(123, int)
"""

from collections.abc import Sequence
from typing import Any, TypeVar

import attrs

from pydantic import BaseModel, TypeAdapter


T = TypeVar("T")


class ValidationResult(BaseModel):
    """Result of a validation operation.

    Attributes:
        is_valid: Whether validation passed
        errors: List of validation errors
        value: Validated value (if successful)
    """

    is_valid: bool
    errors: list[str] = []
    value: Any | None = None


@attrs.define
class Validator:
    """Handles validation with comprehensive type checking.

    Attributes:
        strict: Whether to use strict type checking
        coerce_types: Whether to attempt type coercion
    """

    strict: bool = True
    coerce_types: bool = False

    def validate_type(
        self,
        value: Any,
        expected_type: type[T],
    ) -> ValidationResult:
        """Validate value against expected type.

        Args:
            value: Value to validate
            expected_type: Expected type

        Returns:
            Validation result

        Example:
            >>> validator = Validator()
            >>> result = validator.validate_type(123, int)
            >>> print(result.is_valid)
            True
        """
        try:
            adapter: TypeAdapter[T] = TypeAdapter(expected_type)
            validated = adapter.validate_python(value)
            return ValidationResult(is_valid=True, value=validated)

        except Exception as e:
            return ValidationResult(is_valid=False, errors=[str(e)])

    def validate_sequence(
        self,
        values: Sequence[Any],
        expected_type: type[T],
    ) -> ValidationResult:
        """Validate sequence of values against type.

        Args:
            values: Values to validate
            expected_type: Expected type for all values

        Returns:
            Validation result

        Example:
            >>> validator = Validator()
            >>> result = validator.validate_sequence([1, 2, 3], int)
        """
        errors = []
        valid_values = []

        for i, value in enumerate(values):
            result = self.validate_type(value, expected_type)
            if not result.is_valid:
                errors.extend(f"Index {i}: {err}" for err in result.errors)
            else:
                valid_values.append(result.value)

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            value=valid_values if not errors else None,
        )
