"""Backward compatibility layer for bob list utilities.

This module provides compatibility with bob's list_data_type while using
the modern ListHandler internally.
"""

from typing import Any, TypeVar

from ..structures.lists import ListHandler


T = TypeVar("T")

# Global handler instance for compatibility functions
_handler = ListHandler()


def flatten_list(matrix: list[Any]) -> list[Any]:
    """Maintains compatibility with bob.list_data_type.flatten_list."""
    return _handler.flatten(matrix)


def filter_list(
    items: list[T] | None = None,
    allowlist: list[T] | None = None,
    denylist: list[T] | None = None,
) -> list[T]:
    """Maintains compatibility with bob.list_data_type.filter_list."""
    return _handler.filter_list(items, allowlist, denylist)
