"""Simple serialization registry supporting legacy and new serializers."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from extended_data_types.serialization.types import SerializerProtocol


class SerializationRegistry:
    """Registry for named serializers."""

    def __init__(self) -> None:
        self._serializers: dict[str, SerializerProtocol] = {}

    def register(self, name: str, serializer: SerializerProtocol) -> None:
        key = name.casefold()
        if key in self._serializers:
            raise ValueError(f"Serializer already registered: {name}")
        # Basic protocol validation
        if not (hasattr(serializer, "encode") or hasattr(serializer, "dumps")):
            raise ValueError("Serializer must implement encode/dumps")
        if not (hasattr(serializer, "decode") or hasattr(serializer, "loads")):
            raise ValueError("Serializer must implement decode/loads")
        self._serializers[key] = serializer

    def get(self, name: str) -> SerializerProtocol:
        key = name.casefold()
        if key not in self._serializers:
            raise KeyError(f"Serializer not found: {name}")
        return self._serializers[key]

    def list(self) -> list[str]:
        return sorted(self._serializers.keys())

    def serialize(self, data: Any, name: str, **kwargs: Any) -> str:
        serializer = self.get(name)
        encode: Callable[..., str] = getattr(serializer, "encode", None) or serializer.dumps
        return encode(data, **kwargs)

    def deserialize(self, data: str, name: str, **kwargs: Any) -> Any:
        serializer = self.get(name)
        decode: Callable[..., Any] = getattr(serializer, "decode", None) or serializer.loads
        return decode(data, **kwargs)


registry = SerializationRegistry()


def register_serializer(name: str, serializer: SerializerProtocol) -> None:
    registry.register(name, serializer)


# Backwards-compatible alias
register_format = register_serializer


def get_serializer(name: str) -> SerializerProtocol:
    return registry.get(name)


def list_serializers() -> list[str]:
    return registry.list()


# Backwards-compatible alias expected by tests
list_formats = list_serializers


def serialize(data: Any, format_name: str, **kwargs: Any) -> str:
    return registry.serialize(data, format_name, **kwargs)


def deserialize(data: str, format_name: str, **kwargs: Any) -> Any:
    return registry.deserialize(data, format_name, **kwargs)
