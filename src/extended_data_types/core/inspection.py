"""Core inspection and introspection utilities.

This module provides utilities for inspecting and analyzing Python objects,
including type checking, attribute inspection, and structural analysis.
"""

from __future__ import annotations

import inspect
from collections.abc import Mapping, Sequence
from typing import Any, TypeVar, cast, get_args, get_origin

from .exceptions import InspectionError
from .types import JsonDict, JsonValue

T = TypeVar("T")

def typeof(obj: Any) -> str:
    """Get a human-readable type name for an object.
    
    Args:
        obj: Object to inspect
        
    Returns:
        Human-readable type name
        
    Examples:
        >>> typeof([1, 2, 3])
        'list'
        >>> typeof({'a': 1})
        'dict'
        >>> typeof(None)
        'null'
    """
    if obj is None:
        return "null"
    if isinstance(obj, bool):
        return "boolean"
    if isinstance(obj, int):
        return "integer"
    if isinstance(obj, float):
        return "float"
    if isinstance(obj, str):
        return "string"
    if isinstance(obj, bytes):
        return "bytes"
    if isinstance(obj, (list, tuple)):
        return "array"
    if isinstance(obj, dict):
        return "object"
    if isinstance(obj, set):
        return "set"
    return obj.__class__.__name__.lower()

def is_dataclass_instance(obj: Any) -> bool:
    """Check if an object is a dataclass instance.
    
    Args:
        obj: Object to check
        
    Returns:
        True if object is a dataclass instance
    """
    return hasattr(obj, "__dataclass_fields__")

def is_json_serializable(obj: Any) -> bool:
    """Check if an object is JSON-serializable.
    
    Args:
        obj: Object to check
        
    Returns:
        True if object can be serialized to JSON
    """
    if isinstance(obj, (str, int, float, bool, type(None))):
        return True
    
    if isinstance(obj, (list, tuple)):
        return all(is_json_serializable(item) for item in obj)
    
    if isinstance(obj, dict):
        return all(
            isinstance(k, str) and is_json_serializable(v)
            for k, v in obj.items()
        )
    
    return False

def is_sequence_not_str(obj: Any) -> bool:
    """Check if an object is a sequence but not a string.
    
    Args:
        obj: Object to check
        
    Returns:
        True if object is a non-string sequence
    """
    return isinstance(obj, Sequence) and not isinstance(obj, (str, bytes))

def is_mapping_type(type_hint: type) -> bool:
    """Check if a type hint represents a mapping type.
    
    Args:
        type_hint: Type to check
        
    Returns:
        True if type is a mapping
    """
    origin = get_origin(type_hint)
    return origin is not None and issubclass(origin, Mapping)

def get_type_args(type_hint: type) -> tuple[type, ...]:
    """Get the type arguments from a generic type hint.
    
    Args:
        type_hint: Type hint to inspect
        
    Returns:
        Tuple of type arguments
        
    Raises:
        InspectionError: If type hint has no arguments
    """
    args = get_args(type_hint)
    if not args:
        raise InspectionError(f"Type {type_hint} has no type arguments")
    return args

def safe_getattr(obj: Any, attr: str, default: Any = None) -> Any:
    """Safely get an attribute from an object.
    
    Args:
        obj: Object to get attribute from
        attr: Attribute name
        default: Default value if attribute doesn't exist
        
    Returns:
        Attribute value or default
    """
    try:
        return getattr(obj, attr)
    except (AttributeError, TypeError):
        return default

def get_public_attributes(obj: Any) -> dict[str, Any]:
    """Get all public attributes of an object.
    
    Args:
        obj: Object to inspect
        
    Returns:
        Dictionary of attribute names and values
    """
    return {
        name: value
        for name, value in inspect.getmembers(obj)
        if not name.startswith("_")
    }

def to_json_dict(obj: Any) -> JsonDict:
    """Convert an object to a JSON-serializable dictionary.
    
    Args:
        obj: Object to convert
        
    Returns:
        JSON-serializable dictionary
        
    Raises:
        InspectionError: If object cannot be converted
    """
    try:
        if isinstance(obj, (str, int, float, bool, type(None))):
            return cast(JsonDict, {"value": obj})
        
        if isinstance(obj, (list, tuple)):
            return cast(JsonDict, {"items": [to_json_dict(item) for item in obj]})
        
        if isinstance(obj, dict):
            return cast(JsonDict, {
                str(k): to_json_dict(v) if not isinstance(v, JsonValue) else v
                for k, v in obj.items()
            })
        
        if is_dataclass_instance(obj):
            return cast(JsonDict, {
                f.name: to_json_dict(getattr(obj, f.name))
                for f in obj.__dataclass_fields__.values()  # type: ignore
            })
        
        # Try to convert object attributes
        return cast(JsonDict, {
            name: to_json_dict(value)
            for name, value in get_public_attributes(obj).items()
            if not callable(value)
        })
        
    except Exception as e:
        raise InspectionError(f"Failed to convert {typeof(obj)} to JSON: {e}") from e 