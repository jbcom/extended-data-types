"""Pattern matching utilities with enhanced validation.

This module provides type-safe pattern matching capabilities with
comprehensive validation for strings, mappings, and sequences.

Typical usage:
    >>> from extended_data_types.matching.patterns import Matcher
    >>> matcher = Matcher()
    >>> result = matcher.is_partial_match("test", "testing")
"""

from collections.abc import Mapping
from typing import Any

import attrs

from benedict import benedict


@attrs.define
class Matcher:
    """Handles pattern matching with validation.

    Attributes:
        case_sensitive: Whether string matching is case sensitive
        partial_match: Whether to allow partial string matches
        strict_types: Whether to enforce strict type matching
    """

    case_sensitive: bool = False
    partial_match: bool = True
    strict_types: bool = True

    def is_partial_match(
        self,
        a: str | None,
        b: str | None,
        check_prefix_only: bool = False,
    ) -> bool:
        """Check if strings partially match.

        Args:
            a: First string
            b: Second string
            check_prefix_only: Whether to check only string prefixes

        Returns:
            Whether strings match according to rules

        Example:
            >>> matcher = Matcher()
            >>> matcher.is_partial_match("test", "testing")
            True
        """
        if a is None or b is None:
            return a is b

        if not self.case_sensitive:
            a = a.casefold()
            b = b.casefold()

        if check_prefix_only:
            return a.startswith(b) or b.startswith(a)

        return a in b or b in a

    def is_value_match(
        self,
        a: Any,
        b: Any,
        ignore_case: bool | None = None,
    ) -> bool:
        """Check if values match.

        Args:
            a: First value
            b: Second value
            ignore_case: Override case sensitivity for strings

        Returns:
            Whether values match

        Example:
            >>> matcher = Matcher()
            >>> matcher.is_value_match({"a": 1}, {"a": 1})
            True
        """
        if a is None or b is None:
            return a is b

        if self.strict_types and type(a) is not type(b):
            return False

        case_sensitive = not (ignore_case or not self.case_sensitive)

        if isinstance(a, str):
            return a == b if case_sensitive else a.casefold() == b.casefold()

        if isinstance(a, Mapping):
            return benedict(a) == benedict(b)

        if isinstance(a, (list, tuple, set)):
            try:
                return sorted(a) == sorted(b)
            except TypeError:
                return False

        return a == b
