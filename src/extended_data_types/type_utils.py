"""Type Utilities.

This module provides utility functions related to Python types, specifically for retrieving
default values based on the type. It includes functions for getting default values for common
types like lists, dictionaries, and strings, and for determining whether to return primitive
or exact types of a given value.

Functions:
    - get_default_value_for_type: Returns the default value for a given type.
    - get_primitive_type_for_instance_type: Returns the primitive type for a given value.
    - typeof: Returns the type (or primitive type) of a given value.
"""

from __future__ import annotations

from typing import Any


def get_default_value_for_type(input_type: type) -> Any:
    """Returns the default value for a given type.

    Args:
        input_type (type): The type to get the default value for.

    Returns:
        Any: The default value for the given type.
    """
    if input_type is list:
        return []
    if input_type is dict:
        return {}
    if input_type is str:
        return ""
    return None


def get_primitive_type_for_instance_type(value: Any) -> type:
    """Gets the primitive type for a given value.

    Args:
        value (Any): The value to match.

    Returns:
        type: The primitive type for the given value.
    """
    if isinstance(value, (bool, int, float, str, bytes, bytearray)):
        return type(value)
    if isinstance(value, (list, tuple)):
        return list
    if isinstance(value, dict):
        return dict
    if isinstance(value, (set, frozenset)):
        return set
    return type(None) if value is None else object


def typeof(item: Any, primitive_only: bool = False) -> type:
    """Determines either the primitive or exact type of a given value.

    Args:
        item (Any): The value to determine the type of.
        primitive_only (bool): Whether to return the primitive type.

    Returns:
        type: The type (or primitive type) of the value.
    """
    return get_primitive_type_for_instance_type(item) if primitive_only else type(item)
