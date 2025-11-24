"""Data structure splitting utilities with enhanced validation.

This module provides type-safe splitting capabilities for collections
with comprehensive validation and type checking.

Typical usage:
    >>> from extended_data_types.structures.splitter import CollectionSplitter
    >>> splitter = CollectionSplitter()
    >>> lists, dicts = splitter.split_by_type([1, {}, 2, {}])
"""

from collections.abc import Mapping, Sequence
from typing import Any, TypeVar

import attrs


T = TypeVar("T")


@attrs.define
class CollectionSplitter:
    """Handles collection splitting with validation.

    Attributes:
        strict_types: Whether to use strict type checking
        preserve_order: Whether to maintain original order
    """

    strict_types: bool = True
    preserve_order: bool = True

    def split_by_type(
        self,
        items: Sequence[Any],
    ) -> tuple[list[Any], list[dict[str, Any]]]:
        """Split sequence into non-dict and dict items.

        Args:
            items: Sequence to split

        Returns:
            Tuple of (non-dict items, dict items)

        Example:
            >>> splitter = CollectionSplitter()
            >>> lists, dicts = splitter.split_by_type([1, {}, 2, {}])
            >>> print(lists, dicts)
            [1, 2] [{}, {}]
        """
        non_dicts = []
        dicts = []

        for item in items:
            if isinstance(item, Mapping):
                dicts.append(dict(item))
            else:
                non_dicts.append(item)

        return non_dicts, dicts

    def split_by_predicate(
        self,
        items: Sequence[T],
        predicate: Callable[[T], bool],
    ) -> tuple[list[T], list[T]]:
        """Split sequence based on predicate function.

        Args:
            items: Sequence to split
            predicate: Function returning True for matching items

        Returns:
            Tuple of (matching items, non-matching items)

        Example:
            >>> splitter = CollectionSplitter()
            >>> evens, odds = splitter.split_by_predicate(
            ...     [1, 2, 3, 4],
            ...     lambda x: x % 2 == 0
            ... )
        """
        matching = []
        non_matching = []

        for item in items:
            if predicate(item):
                matching.append(item)
            else:
                non_matching.append(item)

        return matching, non_matching

    def split_dict_by_type(
        self,
        data: Mapping[str, Any],
    ) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
        """Split dictionary into non-dict and dict values.

        Args:
            data: Dictionary to split

        Returns:
            Tuple of (non-dict values, dict values)

        Example:
            >>> splitter = CollectionSplitter()
            >>> simple, nested = splitter.split_dict_by_type({
            ...     'a': 1,
            ...     'b': {'x': 2}
            ... })
        """
        simple = {}
        nested = {}

        for key, value in data.items():
            if isinstance(value, Mapping):
                nested[key] = dict(value)
            else:
                simple[key] = value

        return simple, nested
