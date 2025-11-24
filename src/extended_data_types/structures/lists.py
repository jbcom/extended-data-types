"""List manipulation utilities with enhanced validation.

This module provides type-safe list operations with comprehensive
validation and filtering capabilities.

Typical usage:
    >>> from extended_data_types.structures.lists import ListHandler
    >>> handler = ListHandler()
    >>> result = handler.flatten([1, [2, 3], [4, [5]]])
"""

from collections.abc import Sequence
from typing import Any, TypeVar

import attrs


T = TypeVar("T")


@attrs.define
class ListHandler:
    """Handles list operations with validation.

    Attributes:
        recursive: Whether to process nested structures recursively
        maintain_order: Whether to maintain original order in operations
    """

    recursive: bool = True
    maintain_order: bool = True

    def flatten(self, matrix: Sequence[Any]) -> list[Any]:
        """Flatten a nested sequence.

        Args:
            matrix: Sequence to flatten

        Returns:
            Flattened list

        Example:
            >>> handler = ListHandler()
            >>> handler.flatten([1, [2, 3], [4, [5]]])
            [1, 2, 3, 4, 5]
        """
        result = []

        for item in matrix:
            if isinstance(item, (list, tuple)) and self.recursive:
                result.extend(self.flatten(item))
            else:
                result.append(item)

        return result

    def filter_list(
        self,
        items: Sequence[T] | None = None,
        allowlist: Sequence[T] | None = None,
        denylist: Sequence[T] | None = None,
    ) -> list[T]:
        """Filter a list using allowlist and denylist.

        Args:
            items: Items to filter
            allowlist: Items to allow (if empty, all items allowed)
            denylist: Items to deny

        Returns:
            Filtered list

        Example:
            >>> handler = ListHandler()
            >>> handler.filter_list([1, 2, 3], allowlist=[1, 2])
            [1, 2]
        """
        items = items or []
        denylist = denylist or []

        filtered = []
        for item in items:
            # If allowlist is None, allow all items
            # If allowlist is empty [], allow nothing
            # If allowlist has items, only allow items in it
            if allowlist is None:
                allow_item = True
            elif allowlist:
                allow_item = item in allowlist
            else:  # allowlist is empty []
                allow_item = False

            if allow_item and item not in denylist:
                filtered.append(item)

        return filtered

    def deduplicate(
        self,
        items: Sequence[T],
        maintain_order: bool | None = None,
    ) -> list[T]:
        """Remove duplicate items from a sequence.

        Args:
            items: Sequence to deduplicate
            maintain_order: Override order maintenance setting

        Returns:
            Deduplicated list

        Example:
            >>> handler = ListHandler()
            >>> handler.deduplicate([1, 2, 2, 3, 1])
            [1, 2, 3]
        """
        if not items:
            return []

        keep_order = (
            maintain_order if maintain_order is not None else self.maintain_order
        )

        if keep_order:
            return list(dict.fromkeys(items))

        # Try to sort, but fallback to unsorted set if elements are not comparable
        try:
            return sorted(set(items))  # type: ignore[type-var]
        except TypeError:
            return list(set(items))
