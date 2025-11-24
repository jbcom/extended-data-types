"""Core inspection and introspection utilities.

This module provides utilities for inspecting and analyzing Python objects,
including type checking, attribute inspection, and structural analysis.
"""

from __future__ import annotations

import inspect
import sys

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
            isinstance(k, str) and is_json_serializable(v) for k, v in obj.items()
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
            return cast(
                JsonDict,
                {
                    str(k): to_json_dict(v) if not isinstance(v, JsonValue) else v
                    for k, v in obj.items()
                },
            )

        if is_dataclass_instance(obj):
            from dataclasses import fields
            return cast(
                JsonDict,
                {
                    f.name: to_json_dict(getattr(obj, f.name))
                    for f in fields(obj)  # type: ignore[arg-type]
                },
            )

        # Try to convert object attributes
        return cast(
            JsonDict,
            {
                name: to_json_dict(value)
                for name, value in get_public_attributes(obj).items()
                if not callable(value)
            },
        )

    except Exception as e:
        raise InspectionError(f"Failed to convert {typeof(obj)} to JSON: {e}") from e


# --- Backwards-compatible helpers expected by tests ---


def filter_methods(methods: list[str]) -> list[str]:
    """Filter out private/dunder methods."""
    return [m for m in methods if not m.startswith("_") and not m.endswith("__")]


def get_caller() -> str:
    """Return caller function name."""
    stack = inspect.stack()
    return stack[2].function  # 0=current,1=get_caller,2=caller


def get_unique_signature(obj: Any, delimiter: str = "/") -> str:
    """Return a module/qualname signature for an object."""
    module = getattr(obj, "__module__", obj.__class__.__module__)
    name = getattr(obj, "__name__", obj.__class__.__name__)
    return f"{module}{delimiter}{name}"


def get_available_methods(obj: Any) -> dict[str, str]:
    """Return public methods with docstrings, skipping NOPARSE."""
    methods: dict[str, str] = {}
    for name, member in inspect.getmembers(obj):
        if not inspect.isfunction(member) and not inspect.ismethod(member):
            continue
        if name.startswith("_") or "NOPARSE" in (member.__doc__ or ""):
            continue
        doc = (member.__doc__ or "").strip()
        methods[name] = doc
    return methods


def get_inputs_from_docstring(docstring: str | None) -> dict[str, dict[str, str]]:
    """Parse env input definitions from docstrings."""
    if not docstring:
        return {}
    inputs: dict[str, dict[str, str]] = {}
    for line in docstring.splitlines():
        line = line.strip()
        if not line.lower().startswith("env=name:"):
            continue
        parts = [part.strip() for part in line.split(",")]
        entry: dict[str, str] = {}
        key = None
        for part in parts:
            if part.lower().startswith("env=name:"):
                key = part.split(":", 1)[1].strip().lower()
            elif ":" in part:
                k, v = part.split(":", 1)
                entry[k.strip().lower()] = v.strip().lower()
        if key:
            inputs[key] = entry
    return inputs


# Compatibility alias
def parse_input_definitions(docstring: str) -> dict[str, dict[str, str]]:
    return get_inputs_from_docstring(docstring)


def update_docstring(obj: Any, new_inputs: dict[str, dict[str, str]]) -> str:
    """Update docstring with new env input metadata (compat helper)."""
    if isinstance(obj, str):
        base_doc = obj
        target = None
    else:
        base_doc = obj.__doc__ or ""
        target = obj

    base_lines = [line for line in base_doc.strip().splitlines() if line.strip()]
    existing_envs = [
        line for line in base_lines if line.strip().lower().startswith("env=name:")
    ]
    text_lines = [
        line for line in base_lines if not line.strip().lower().startswith("env=name:")
    ]

    merged_lines = list(text_lines)
    indent = ""
    if existing_envs:
        # Capture leading whitespace from first env line to reuse
        prefix_len = len(existing_envs[0]) - len(existing_envs[0].lstrip())
        indent = existing_envs[0][:prefix_len]

    for key, meta in new_inputs.items():
        normalized = key.lower()
        already = any(normalized in line.lower() for line in existing_envs)
        if not already:
            existing_envs.append(
                f"{indent}env=name: {key}, required: {meta.get('required','false')}, sensitive: {meta.get('sensitive','false')}"
            )

    merged_lines.extend(existing_envs)
    merged = "\n".join(merged_lines)

    if target is not None:
        try:
            target.__doc__ = merged
        except Exception:
            pass
    return merged


def is_python_version_at_least(minor: int, major: int | None = None) -> bool:
    """Check interpreter version."""
    if major is None:
        major = 3
    current = sys.version_info
    return (current.major, current.minor) >= (major, minor)
