"""Backward compatibility layer for bob type utilities."""

from typing import Any, TypeVar

from extended_data_types.core.types import TypeSystem
from extended_data_types.type_utils import (
    convert_special_type as _convert_special_type,
)
from extended_data_types.type_utils import (
    convert_special_types as _convert_special_types,
)
from extended_data_types.type_utils import (
    reconstruct_special_type as _reconstruct_special_type,
)
from extended_data_types.type_utils import (
    reconstruct_special_types as _reconstruct_special_types,
)


T = TypeVar("T")

# Local type system for conversions targeting explicit types.
_type_system = TypeSystem()


def convert_special_type(value: Any, target_type: type[T] | None = None) -> T:
    """Maintain bob.type_utils.convert_special_type compatibility."""
    if target_type is None:
        return _convert_special_type(value)
    return _type_system.convert_value(value, target_type)


def convert_special_types(data: Any) -> Any:
    """Maintain bob.type_utils.convert_special_types compatibility."""
    return _convert_special_types(data)


def reconstruct_special_type(converted_obj: str, fail_silently: bool = False) -> Any:
    """Maintain bob.type_utils.reconstruct_special_type compatibility."""
    return _reconstruct_special_type(converted_obj, fail_silently=fail_silently)


def reconstruct_special_types(data: Any, fail_silently: bool = False) -> Any:
    """Maintain bob.type_utils.reconstruct_special_types compatibility."""
    return _reconstruct_special_types(data, fail_silently=fail_silently)
