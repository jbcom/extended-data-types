"""Core type definitions and conversion utilities.

This module provides the foundational type system and conversion utilities,
leveraging pydantic for validation and cattrs for conversion.

Typical usage:
    >>> from extended_data_types.core.types import TypedDict, convert_special_type
    >>> data = TypedDict({"value": "123"})
    >>> data.set_type("value", int)
    >>> data["value"]
    123
"""

from __future__ import annotations

import datetime
import decimal

from collections.abc import Mapping
from pathlib import Path
from typing import Any, TypeVar, Union

import attrs
import cattrs

from benedict import benedict
from pydantic import BaseModel, ConfigDict, Field, TypeAdapter


T = TypeVar("T")

# Configure cattrs for common conversions
converter = cattrs.Converter()
converter.register_structure_hook(
    datetime.datetime, lambda v, _: datetime.datetime.fromisoformat(v)
)
converter.register_structure_hook(Path, lambda v, _: Path(v))
converter.register_unstructure_hook(datetime.datetime, lambda v: v.isoformat())
converter.register_unstructure_hook(Path, str)


@attrs.define
class SpecialTypes:
    """Container for special type conversion settings.

    This class defines configuration for how special types should be handled
    during conversion operations.

    Attributes:
        datetime_format: Format string for datetime conversion ('iso' or 'rfc')
        preserve_timezone: Whether to preserve timezone information
        path_type: Type to use for path-like objects
        number_types: Tuple of types considered as numbers
    """

    datetime_format: str = "iso"
    preserve_timezone: bool = True
    path_type: type = Path
    number_types: tuple[type, ...] = (int, float, decimal.Decimal)


class DataContainer(BaseModel):
    """Base container for validated data structures.

    This class provides a foundation for data containers with built-in
    validation and type checking.

    Attributes:
        model_config: Pydantic configuration for the model

    Example:
        >>> class UserData(DataContainer):
        ...     name: str
        ...     age: int
        >>> user = UserData(name="John", age=30)
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="allow",
        validate_assignment=True,
    )


class TypedDict(benedict):
    """Enhanced dictionary with type checking and conversion.

    This class extends benedict to provide type-safe dictionary operations
    with automatic type conversion.

    Args:
        *args: Positional arguments passed to benedict
        **kwargs: Keyword arguments passed to benedict

    Example:
        >>> d = TypedDict({"age": "25"})
        >>> d.set_type("age", int)
        >>> d["age"]
        25
    """

    def __init__(self, *args: Any, **kwargs: Any):
        """Initialize TypedDict.

        Args:
            *args: Positional arguments passed to benedict
            **kwargs: Keyword arguments passed to benedict
        """
        super().__init__(*args, **kwargs)
        self._types: dict[str, type] = {}

    def set_type(self, key: str, type_: type) -> None:
        """Set expected type for a key.

        Args:
            key: Dictionary key
            type_: Expected type for the key's value

        Example:
            >>> d = TypedDict({"value": "123"})
            >>> d.set_type("value", int)
            >>> d["value"]
            123
        """
        self._types[key] = type_
        if key in self:
            self[key] = self._convert_value(self[key], type_)

    def __setitem__(self, key: str, value: Any) -> None:
        """Set dictionary item with type checking.

        Args:
            key: Dictionary key
            value: Value to set

        Raises:
            TypeError: If value cannot be converted to expected type
        """
        if key in self._types:
            value = self._convert_value(value, self._types[key])
        super().__setitem__(key, value)

    def _convert_value(self, value: Any, target_type: type) -> Any:
        """Convert value to target type.

        Args:
            value: Value to convert
            target_type: Target type

        Returns:
            Converted value

        Raises:
            TypeError: If conversion fails
        """
        try:
            adapter: TypeAdapter[Any] = TypeAdapter(target_type)
            return adapter.validate_python(value)
        except Exception:
            return converter.structure(value, target_type)


# New Core Layer
@attrs.define
class TypeSystem:
    """Modern type conversion and validation system."""

    def convert_value(self, value: Any, target_type: type[T]) -> T:
        """Convert value with validation."""
        adapter = TypeAdapter(target_type)
        return adapter.validate_python(value)

    def convert_dict(self, data: Mapping[str, Any]) -> benedict:
        """Convert dictionary to enhanced form."""
        return benedict(data)


# Backward Compatibility Layer
def convert_special_type(value: Any, target_type: type[T] = None) -> T:
    """Original bob API for type conversion.

    Args:
        value: Value to convert
        target_type: Optional target type

    Returns:
        Converted value

    Note:
        This maintains the exact same API as bob.type_utils.convert_special_type
        while using the new TypeSystem internally.
    """
    system = TypeSystem()
    if target_type is None:
        return value
    return system.convert_value(value, target_type)


def convert_special_types(data: Any) -> Any:
    """Convert all special types in a data structure.

    This function walks through a data structure and converts all special
    types to their serializable form.

    Args:
        data: Data structure to convert

    Returns:
        Converted data structure

    Example:
        >>> data = {"date": datetime.date(2024, 1, 1)}
        >>> convert_special_types(data)
        {'date': '2024-01-01'}
    """
    return converter.unstructure(data)


def reconstruct_special_type(value: Any, target_type: type[T] = None) -> T:
    """Alias to convert_special_type for compatibility."""
    return convert_special_type(value, target_type)


def reconstruct_special_types(data: Any) -> Any:
    """Alias to convert_special_types for compatibility."""
    return convert_special_types(data)


class TypedData(DataContainer):
    """Container for typed data with validation.

    This class provides a container for data that needs to be converted
    to a specific type with validation.

    Attributes:
        value: The data value
        type_: The target type for conversion

    Example:
        >>> data = TypedData(value="123", type=int)
        >>> data.convert()
        123
    """

    value: Any
    type_: type = Field(default=object, alias="type")

    def convert(self) -> Any:
        """Convert value to specified type.

        Returns:
            Converted value

        Raises:
            TypeError: If conversion fails
        """
        return convert_special_type(self.value, self.type_)


# Common type aliases
JsonPrimitive = Union[str, int, float, bool, None]
JsonValue = Union[JsonPrimitive, list[Any], dict[str, Any]]
JsonDict = dict[str, JsonValue]

# Re-export for convenience
__all__ = [
    "TypedDict",
    "TypedData",
    "convert_special_type",
    "convert_special_types",
    "JsonPrimitive",
    "JsonValue",
    "JsonDict",
]


# --- Legacy compatibility helpers ---
def typeof(obj: Any) -> str:
    """Return a simple string type name."""
    return type(obj).__name__.lower()


def unwrap_object(obj: Any) -> Any:
    """Return underlying object if wrapped."""
    return getattr(obj, "__wrapped__", obj)


def strtobool(value: str, raise_on_error: bool = False) -> bool:
    truthy = {"1", "true", "yes", "y", "on"}
    falsy = {"0", "false", "no", "n", "off"}
    val = str(value).strip().lower()
    if val in truthy:
        return True
    if val in falsy:
        return False
    if raise_on_error:
        raise ValueError(f"Invalid boolean string: {value}")
    return False


def strtodate(value: str) -> datetime.date:
    return datetime.date.fromisoformat(value)


def strtodatetime(value: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(value)


def strtotime(value: str) -> datetime.time:
    return datetime.time.fromisoformat(value)


def strtopath(value: str) -> Path:
    return Path(value)


def strtofloat(value: str) -> float:
    return float(value)


def strtoint(value: str) -> int:
    return int(value)


def coerce_to_type(value: Any, target_type: type[T]) -> T:
    """Lightweight coercion using pydantic TypeAdapter for leniency."""
    adapter: TypeAdapter[T] = TypeAdapter(target_type)
    return adapter.validate_python(value)


def get_primitive_type_for_instance_type(instance_type: type) -> type:
    """Return primitive type (placeholder)."""
    return instance_type
