from __future__ import annotations, division, print_function, unicode_literals

from collections import defaultdict
from typing import Any, Dict, List, Mapping, MutableMapping, Optional, Tuple

import inflection
from sortedcontainers import SortedDict

from extended_data_types.export_utils import make_raw_data_export_safe


def first_non_empty_value_from_map(m: Mapping, *keys: str) -> Any:
    """Returns the first non-empty value from a map for the given keys.

    Args:
        m (Mapping): The map to search.
        keys: The keys to search for.

    Returns:
        Any: The first non-empty value.
    """
    for key in keys:
        if key in m and m[key]:
            return m[key]
    return None


def deduplicate_map(m: Mapping) -> Dict[str, Any]:
    """Removes duplicate values from a map.

    Args:
        m (Mapping): The map to deduplicate.

    Returns:
        Dict[str, Any]: The deduplicated map.
    """
    deduplicated_map = make_raw_data_export_safe(m)

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


def all_values_from_map(m: Mapping) -> List[Any]:
    """Returns all values from a nested map.

    Args:
        m (Mapping): The map to retrieve values from.

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
    dictionary: Mapping, parent_key: Optional[str] = "", separator: str = "."
) -> Dict[str, Any]:
    """Flattens a nested dictionary into a flat dictionary.

    Args:
        dictionary (Mapping): The dictionary to flatten.
        parent_key (Optional[str]): The string to prepend to dictionary's keys.
        separator (str): The string used to separate flattened keys.

    Returns:
        Dict[str, Any]: The flattened dictionary.
    """
    items: List[Tuple[str, Any]] = []
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


def zipmap(a: List[str], b: List[str]) -> Dict[str, str]:
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


def get_default_dict(sorted: bool = False, default_type=dict) -> Any:
    """Returns a default dictionary with nested default dictionaries.

    Args:
        sorted (bool): Whether to use SortedDict for sorting keys.
        default_type: The type of the default dictionary.

    Returns:
        Any: The default dictionary.
    """

    def default_factory():
        return SortedDict() if sorted else default_type()

    return defaultdict(default_factory)


def unhump_map(
    m: Mapping[str, Any], drop_without_prefix: Optional[str] = None
) -> Dict[str, Any]:
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
    m: Optional[Mapping[str, Any]],
    allowlist: Optional[List[str]] = None,
    denylist: Optional[List[str]] = None,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Filters a map based on allowlist and denylist.

    Args:
        m (Optional[Mapping[str, Any]]): The map to filter.
        allowlist (List[str]): The list of allowed keys.
        denylist (List[str]): The list of denied keys.

    Returns:
        Tuple[Dict[str, Any], Dict[str, Any]]: The filtered and remaining maps.
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
