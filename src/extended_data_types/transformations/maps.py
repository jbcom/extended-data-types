"""Map transformation utilities.

This module provides utilities for handling maps (dictionaries), including functions to
manipulate, flatten, filter, and convert dictionary structures.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping, MutableMapping
from typing import Any

import inflection

from sortedcontainers import SortedDict

from ..types import convert_special_types


def first_non_empty_value_from_map(m: Mapping[str, Any], *keys: str) -> Any:
    """Returns the first non-empty value from a map for the given keys.

    Args:
        m: The map to search.
        *keys: The keys to search for.

    Returns:
        Any: The first non-empty value.

    Examples:
        >>> first_non_empty_value_from_map({"a": None, "b": "value"}, "a", "b")
        'value'
    """
    for key in keys:
        if m.get(key):
            return m[key]
    return None


def deduplicate_map(m: Mapping[str, Any]) -> dict[str, Any]:
    """Removes duplicate values from a map.

    Args:
        m: The map to deduplicate.

    Returns:
        dict[str, Any]: The deduplicated map.

    Examples:
        >>> deduplicate_map({"a": [1, 1, 2], "b": {"c": [3, 3]}})
        {'a': [1, 2], 'b': {'c': [3]}}
    """
    deduplicated_map: dict[str, Any] = convert_special_types(m)

    for k, v in m.items():
        if isinstance(v, list):
            deduplicated_map[k] = []
            for elem in v:
                if elem not in deduplicated_map[k]:
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
        m: The map to retrieve values from.

    Returns:
        list[Any]: A list of all values.

    Examples:
        >>> all_values_from_map({"a": 1, "b": {"c": 2}, "d": [3, {"e": 4}]})
        [1, 2, 3, 4]
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
        dictionary: The dictionary to flatten.
        parent_key: The string to prepend to dictionary's keys.
        separator: The string used to separate flattened keys.

    Returns:
        dict[str, Any]: The flattened dictionary.

    Examples:
        >>> flatten_map({"a": {"b": 1}, "c": [2, 3]})
        {'a.b': 1, 'c.0': 2, 'c.1': 3}
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
        a: The first list.
        b: The second list.

    Returns:
        dict[str, str]: The resulting dictionary.

    Examples:
        >>> zipmap(['a', 'b'], ['1', '2'])
        {'a': '1', 'b': '2'}
    """
    return dict(zip(a, b[: len(a)], strict=False))


def get_default_dict(
    use_sorted_dict: bool = False,
    default_type: type[dict[Any, Any]] = dict,
    levels: int = 2,
) -> defaultdict[str, Any] | Any:
    """Create a nested defaultdict with the specified number of levels.

    Args:
        use_sorted_dict: Whether to use a sorted dictionary.
        default_type: The default type for the dictionary.
        levels: The number of levels for nesting.

    Returns:
        defaultdict | Any: A nested defaultdict or a dictionary of the specified type.

    Raises:
        ValueError: If levels is less than 1.

    Examples:
        >>> d = get_default_dict(levels=2)
        >>> d['a']['b'] = 1  # No KeyError
        >>> d['a']['b']
        1
    """
    if levels < 1:
        msg = "The number of levels must be greater than or equal to 1."
        raise ValueError(msg)

    dict_type = SortedDict if use_sorted_dict else default_type

    if levels == 1:
        return dict_type()

    if use_sorted_dict:
        return defaultdict(SortedDefaultDict)

    def nested_dict() -> defaultdict[str, Any]:
        return defaultdict(nested_dict)

    return nested_dict()


def unhump_map(
    m: Mapping[str, Any],
    drop_without_prefix: str | None = None,
) -> dict[str, Any]:
    """Converts keys in a dictionary from camelCase to snake_case.

    Args:
        m: The dictionary to convert.
        drop_without_prefix: Drop keys without this prefix.

    Returns:
        dict[str, Any]: The converted dictionary.

    Examples:
        >>> unhump_map({"camelCase": 1, "anotherKey": {"nestedCamel": 2}})
        {'camel_case': 1, 'another_key': {'nested_camel': 2}}
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
        m: The map to filter.
        allowlist: The list of allowed keys.
        denylist: The list of denied keys.

    Returns:
        tuple[dict[str, Any], dict[str, Any]]: The filtered and remaining maps.

    Examples:
        >>> filter_map({"a": 1, "b": 2, "c": 3}, allowlist=["a", "b"])
        ({'a': 1, 'b': 2}, {'c': 3})
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
