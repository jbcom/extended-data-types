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
from typeguard import check_type


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
            check_type(value, target_type)
            return value
        except TypeError:
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
