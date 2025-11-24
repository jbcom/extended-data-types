"""Backward compatibility layer for bob splitter utilities.

This module provides compatibility with bob's splitter_utils while using
the modern CollectionSplitter internally.
"""

from collections.abc import Mapping, Sequence
from typing import Any

from extended_data_types.structures.splitter import CollectionSplitter


# Global splitter instance for compatibility functions
_splitter = CollectionSplitter()


def split_by_type(
    items: Sequence[Any],
) -> tuple[list[Any], list[dict[str, Any]]]:
    """Maintains compatibility with bob.splitter_utils.split_by_type."""
    return _splitter.split_by_type(items)


def split_dict_by_type(
    data: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    """Maintains compatibility with bob.splitter_utils.split_dict_by_type."""
    return _splitter.split_dict_by_type(data)
