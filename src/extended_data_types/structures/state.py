"""State checking utilities for data structures.

This module provides comprehensive state checking capabilities for Python
data structures, with a focus on emptiness and validation checks.

Typical usage:
    >>> from extended_data_types.structures.state import StateChecker
    >>> checker = StateChecker()
    >>> checker.is_empty("")
    True
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import attrs


@attrs.define
class StateChecker:
    """Modern state checking with comprehensive validation.

    This class provides methods to check the state of various Python
    data structures with type safety and validation.

    Attributes:
        consider_whitespace_empty: Whether to treat whitespace as empty.
        consider_zero_empty: Whether to treat 0/0.0 as empty.
        recursive_check: Whether to check nested structures recursively.

    Example:
        >>> checker = StateChecker()
        >>> checker.is_empty([None, "", {}])
        True
    """

    consider_whitespace_empty: bool = attrs.field(default=True)
    consider_zero_empty: bool = attrs.field(default=False)
    recursive_check: bool = attrs.field(default=True)

    def is_empty(self, value: Any) -> bool:
        """Check if a value is considered empty.

        Args:
            value: The value to check for emptiness.

        Returns:
            bool: True if the value is considered empty, False otherwise.

        Example:
            >>> checker = StateChecker()
            >>> checker.is_empty(None)
            True
            >>> checker.is_empty([1, 2, 3])
            False
        """
        if value is None:
            return True

        if isinstance(value, (str, bytes, bytearray)):
            if self.consider_whitespace_empty and isinstance(value, str):
                return not bool(value.strip())
            return not bool(value)

        if isinstance(value, (int, float)):
            return self.consider_zero_empty and value == 0

        if isinstance(value, (Mapping, Sequence, set)):
            if not value:
                return True
            if self.recursive_check:
                return all(self.is_empty(v) for v in value)
            return False

        return False

    def all_empty(self, *args: Any, **kwargs: Any) -> bool:
        """Check if all provided values are empty.

        Args:
            *args: Positional arguments to check.
            **kwargs: Keyword arguments to check.

        Returns:
            bool: True if all values are empty, False otherwise.

        Example:
            >>> checker = StateChecker()
            >>> checker.all_empty(None, "", [], {})
            True
            >>> checker.all_empty(None, "data")
            False
        """
        all_values = list(args) + list(kwargs.values())
        return all(self.is_empty(value) for value in all_values)

    def get_non_empty(
        self, *args: Any, **kwargs: Any
    ) -> list[Any] | dict[str, Any] | None:
        """Get all non-empty values from provided arguments.

        Args:
            *args: Positional arguments to check.
            **kwargs: Keyword arguments to check.

        Returns:
            Non-empty values as list (for args) or dict (for kwargs),
            or None if all values are empty.

        Example:
            >>> checker = StateChecker()
            >>> checker.get_non_empty(None, "data", "", [1, 2])
            ['data', [1, 2]]
        """
        non_empty_args = [value for value in args if not self.is_empty(value)]

        non_empty_kwargs = {
            key: value for key, value in kwargs.items() if not self.is_empty(value)
        }

        if not non_empty_args and not non_empty_kwargs:
            return None

        if non_empty_args and not non_empty_kwargs:
            return non_empty_args

        if non_empty_kwargs and not non_empty_args:
            return non_empty_kwargs

        return non_empty_args, non_empty_kwargs

    def first_non_empty(self, *values: Any) -> Any:
        """Get the first non-empty value.

        Args:
            *values: Values to check sequentially.

        Returns:
            The first non-empty value found, or None if all empty.

        Example:
            >>> checker = StateChecker()
            >>> checker.first_non_empty(None, "", "data", [])
            'data'
        """
        for value in values:
            if not self.is_empty(value):
                return value
        return None
