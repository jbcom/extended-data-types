"""This module provides utilities for handling lists.

It includes functions to flatten lists and to filter lists based on allowlists
and denylists.
"""  # noqa: E501

from __future__ import annotations, division, print_function, unicode_literals

from typing import Any, List, Optional

import numpy as np


def flatten_list(matrix: List[Any]) -> List[Any]:
    """Flattens a list of lists into a single list using numpy.

    Args:
        matrix (List[List[Any]]): The list of lists to flatten.

    Returns:
        List[Any]: The flattened list.
    """
    array = np.array(matrix)
    return list(array.flatten())


def filter_list(
        items: Optional[List[str]],
        allowlist: Optional[List[str]] = None,
        denylist: Optional[List[str]] = None,
) -> List[str]:
    """Filters a list based on allowlist and denylist.

    Args:
        items (Optional[List[str]]): The list to filter.
        allowlist (List[str]): The list of allowed items.
        denylist (List[str]): The list of denied items.

    Returns:
        List[str]: The filtered list.
    """
    if items is None:
        items = []

    if allowlist is None:
        allowlist = []

    if denylist is None:
        denylist = []

    filtered = []

    for elem in items:
        if (len(allowlist) > 0 and elem not in allowlist) or elem in denylist:
            continue

        filtered.append(elem)

    return filtered
