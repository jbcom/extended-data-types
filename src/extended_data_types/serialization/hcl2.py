"""HCL2 (HashiCorp Configuration Language) serialization support.

This module provides serialization support for HCL2, commonly used in
Terraform configurations. It handles both serialization and deserialization
with proper type conversion and formatting.
"""

from __future__ import annotations

import json

from typing import Any, cast

from hcl2 import dumps as hcl2_dumps  # type: ignore[import]
from hcl2 import loads as hcl2_loads  # type: ignore[import]

from extended_data_types.core.exceptions import SerializationError
from extended_data_types.core.types import JsonDict, convert_special_types


class HCL2Serializer:
    """HCL2 format serializer implementation."""

    def loads(self, data: str, **kwargs: Any) -> Any:
        """Deserialize HCL2 string to Python object.

        Args:
            data: HCL2 string to deserialize
            **kwargs: Additional options (passed to hcl2.loads)

        Returns:
            Deserialized object

        Raises:
            SerializationError: If deserialization fails

        Examples:
            >>> serializer = HCL2Serializer()
            >>> serializer.loads('foo = "bar"')
            {'foo': 'bar'}
            >>> serializer.loads('list = [1, 2, 3]')
            {'list': [1, 2, 3]}
        """
        try:
            # Parse HCL2 to Python dict
            result = hcl2_loads(data, **kwargs)

            # HCL2 always returns a dict
            if not isinstance(result, dict):
                raise SerializationError(f"Expected dict from HCL2, got {type(result)}")

            return cast(JsonDict, result)

        except Exception as e:
            raise SerializationError(f"Failed to parse HCL2: {e}") from e

    def dumps(self, obj: Any, **kwargs: Any) -> str:
        """Serialize Python object to HCL2 string.

        Args:
            obj: Object to serialize
            **kwargs: Additional options (passed to hcl2.dumps)

        Returns:
            HCL2 formatted string

        Raises:
            SerializationError: If serialization fails

        Examples:
            >>> serializer = HCL2Serializer()
            >>> print(serializer.dumps({'foo': 'bar'}))
            foo = "bar"
            >>> print(serializer.dumps({'list': [1, 2, 3]}))
            list = [1, 2, 3]
        """
        try:
            # Convert special types to JSON-serializable forms
            converted = convert_special_types(obj)

            # Ensure we have a dict for HCL2
            if not isinstance(converted, dict):
                converted = {"root": converted}

            # Validate with JSON serialization first
            json.dumps(converted)

            # Convert to HCL2
            result = hcl2_dumps(converted, **kwargs)

            if not isinstance(result, str):
                raise SerializationError(
                    f"Expected string from HCL2 dumps, got {type(result)}"
                )

            return result

        except Exception as e:
            raise SerializationError(f"Failed to generate HCL2: {e}") from e

    def validate(self, data: str) -> bool:
        """Validate HCL2 string format.

        Args:
            data: HCL2 string to validate

        Returns:
            True if valid HCL2

        Examples:
            >>> serializer = HCL2Serializer()
            >>> serializer.validate('foo = "bar"')
            True
            >>> serializer.validate('invalid { syntax')
            False
        """
        try:
            self.loads(data)
            return True
        except SerializationError:
            return False


def is_hcl2_data(obj: Any) -> bool:
    """Check if object appears to be HCL2-compatible.

    Args:
        obj: Object to check

    Returns:
        True if object can be serialized as HCL2

    Examples:
        >>> is_hcl2_data({'foo': 'bar'})
        True
        >>> is_hcl2_data([1, 2, 3])
        False
    """
    try:
        HCL2Serializer().dumps(obj)
        return True
    except SerializationError:
        return False
