"""HCL2 serializer used by the registry."""

from __future__ import annotations

from typing import Any

from extended_data_types.serialization.formats.hcl2 import Hcl2Serializer


class HCL2Serializer:
    """Bridge serializer that wraps the shared Hcl2Serializer backend."""

    def __init__(self, indent_size: int = 2, sort_keys: bool = False):
        self.backend = Hcl2Serializer(indent_size=indent_size, sort_keys=sort_keys)

    def encode(self, data: Any, **kwargs: Any) -> str:
        return self.backend.encode(data, **kwargs)

    def decode(self, data: str, **kwargs: Any) -> dict[str, Any]:
        return self.backend.decode(data, **kwargs)

    dumps = encode
    loads = decode
