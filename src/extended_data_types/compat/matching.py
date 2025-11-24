"""Backward compatibility layer for bob matching utilities.

This module provides compatibility with bob's matcher_utils while using
the modern Matcher internally.
"""

from typing import Any

from extended_data_types.matching.patterns import Matcher


# Global matcher instance for compatibility functions
_matcher = Matcher()


def is_partial_match(
    a: str | None,
    b: str | None,
    check_prefix_only: bool = False,
) -> bool:
    """Maintains compatibility with bob.matcher_utils.is_partial_match."""
    return _matcher.is_partial_match(a, b, check_prefix_only)


def is_value_match(
    a: Any,
    b: Any,
    ignore_case: bool = True,
) -> bool:
    """Maintains compatibility with bob.matcher_utils.is_value_match."""
    return _matcher.is_value_match(a, b, ignore_case)
