"""Backward compatibility layer for bob type utilities."""

from collections.abc import Mapping
from typing import Any, TypeVar

from extended_data_types.core.types import TypeSystem, convert_special_types as core_convert_special_types


T = TypeVar("T")

# Global instance for compatibility
_type_system = TypeSystem()


def convert_special_type(value: Any, target_type: type[T] = None) -> T:
    """Maintain bob.type_utils.convert_special_type compatibility."""
    return _type_system.convert_value(value, target_type or type(value))


def convert_special_types(data: Any) -> Any:
    """Maintain bob.type_utils.convert_special_types compatibility."""
    try:
        return core_convert_special_types(data)
    except Exception:
        return data


def reconstruct_special_type(converted_obj: str, fail_silently: bool = False) -> Any:
    """Maintain bob.type_utils.reconstruct_special_type compatibility."""
    try:
        return _type_system.reconstruct_value(converted_obj)
    except Exception as e:
        if fail_silently:
            return converted_obj
        raise e
