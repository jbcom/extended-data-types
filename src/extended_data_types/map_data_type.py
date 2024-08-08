"""This module provides utilities for handling maps (dictionaries).

It includes functions to manipulate, flatten, and filter dictionaries, and to
convert keys from camelCase to snake_case.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Mapping, MutableMapping

import inflection

from sortedcontainers import SortedDict

from .export_utils import make_raw_data_export_safe


def first_non_empty_value_from_map(m: Mapping[str, Any], *keys: str) -> Any:
    """Returns the first non-empty value from a map for the given keys.

    Args:
        m (Mapping[str, Any]): The map to search.
        keys: The keys to search for.

    Returns:
        Any: The first non-empty value.
    """
    for key in keys:
        if m.get(key):
            return m[key]
    return None


def deduplicate_map(m: Mapping[str, Any]) -> dict[str, Any]:
    """Removes duplicate values from a map.

    Args:
        m (Mapping[str, Any]): The map to deduplicate.

    Returns:
        dict[str, Any]: The deduplicated map.
    """
    deduplicated_map: dict[str, Any] = make_raw_data_export_safe(m)

    for k, v in m.items():
        if isinstance(v, list):
            deduplicated_map[k] = []

            for elem in v:
                if elem in deduplicated_map[k]:
                    continue

                deduplicated_map[k].append(elem)

            continue

        if isinstance(v, Mapping):
            deduplicated_map[k] = deduplicate_map(v)
            continue

        if k not in deduplicated_map:
            deduplicated_map[k] = v

    return deduplicated_map


def all_values_from_map(m: Mapping[str, Any]) -> list[Any]:
    """Returns all values from a nested map.

    Args:
        m (Mapping[str, Any]): The map to retrieve values from.

    Returns:
        List[Any]: A list of all values.
    """
    values = []

    for v in m.values():
        if isinstance(v, Mapping):
            values.extend(all_values_from_map(v))
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, Mapping):
                    values.extend(all_values_from_map(item))
                else:
                    values.append(item)
        else:
            values.append(v)

    return values


def flatten_map(
    dictionary: Mapping[str, Any],
    parent_key: str | None = "",
    separator: str = ".",
) -> dict[str, Any]:
    """Flattens a nested dictionary into a flat dictionary.

    Args:
        dictionary (Mapping[str, Any]): The dictionary to flatten.
        parent_key (Optional[str]): The string to prepend to dictionary's keys.
        separator (str): The string used to separate flattened keys.

    Returns:
        Dict[str, Any]: The flattened dictionary.
    """
    items: list[tuple[str, Any]] = []
    for key, value in dictionary.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key
        if isinstance(value, MutableMapping):
            items.extend(flatten_map(value, new_key, separator).items())
        elif isinstance(value, list):
            for k, v in enumerate(value):
                items.extend(flatten_map({str(k): v}, new_key).items())
        else:
            items.append((new_key, value))
    return dict(items)


def zipmap(a: list[str], b: list[str]) -> dict[str, str]:
    """Creates a dictionary from two lists by zipping them together.

    Args:
        a (List[str]): The first list.
        b (List[str]): The second list.

    Returns:
        Dict[str, str]: The resulting dictionary.
    """
    zipped = {}

    for idx, val in enumerate(a):
        if idx >= len(b):
            break

        zipped[val] = b[idx]

    return zipped


def get_default_dict(
    use_sorted_dict: bool = False,
    default_type: type[dict[str, Any]] = dict,
) -> Any:
    """Returns a default dictionary with nested default dictionaries.

    Args:
        use_sorted_dict (bool): Whether to use SortedDict for sorting keys.
        default_type (Type[Dict[str, Any]]): The type of the default dictionary.

    Returns:
        Any: The default dictionary.
    """

    def default_factory() -> Any:
        return SortedDict() if use_sorted_dict else default_type()

    return defaultdict(default_factory)


def unhump_map(
    m: Mapping[str, Any],
    drop_without_prefix: str | None = None,
) -> dict[str, Any]:
    """Converts keys in a dictionary from camelCase to snake_case.

    Args:
        m (Mapping[str, Any]): The dictionary to convert.
        drop_without_prefix (Optional[str]): Drop keys without this prefix.

    Returns:
        Dict[str, Any]: The converted dictionary.
    """
    unhumped = {}

    for k, v in m.items():
        if drop_without_prefix is not None and not k.startswith(drop_without_prefix):
            continue

        unhumped_key = inflection.underscore(k)

        if isinstance(v, Mapping):
            unhumped[unhumped_key] = unhump_map(v)
            continue

        unhumped[unhumped_key] = v

    return unhumped


def filter_map(
    m: Mapping[str, Any] | None,
    allowlist: list[str] | None = None,
    denylist: list[str] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Filters a map based on allowlist and denylist.

    Args:
        m (Optional[Mapping[str, Any]]): The map to filter.
        allowlist (List[str]): The list of allowed keys.
        denylist (List[str]): The list of denied keys.

    Returns:
        tuple[Dict[str, Any], Dict[str, Any]]: The filtered and remaining maps.
    """
    if m is None:
        m = {}

    if allowlist is None:
        allowlist = []

    if denylist is None:
        denylist = []

    fm = {}
    rm = {}

    for k, v in m.items():
        if (len(allowlist) > 0 and k not in allowlist) or k in denylist:
            rm[k] = v
        else:
            fm[k] = v

    return fm, rm
