"""HCL2 (HashiCorp Configuration Language) serialization support."""

from __future__ import annotations

from typing import Any

import hcl2

from benedict.serializers import AbstractSerializer

from ...core.exceptions import SerializationError


class Hcl2Serializer(AbstractSerializer):
    """HCL2 serializer implementation."""

    def dumps(self, obj: Any, **kwargs: Any) -> str:
        """Serialize object to HCL2 string.

        Args:
            obj: Object to serialize
            **kwargs: Additional arguments for HCL2 serialization

        Returns:
            str: HCL2 string

        Raises:
            SerializationError: If serialization fails
        """
        try:
            return hcl2.dumps(obj, **kwargs)
        except Exception as e:
            raise SerializationError(f"Failed to serialize to HCL2: {e}") from e

    def loads(self, s: str, **kwargs: Any) -> Any:
        """Deserialize HCL2 string to object.

        Args:
            s: HCL2 string to deserialize
            **kwargs: Additional arguments for HCL2 deserialization

        Returns:
            Any: Deserialized object

        Raises:
            SerializationError: If deserialization fails
        """
        try:
            return hcl2.loads(s, **kwargs)
        except Exception as e:
            raise SerializationError(f"Failed to deserialize HCL2: {e}") from e
