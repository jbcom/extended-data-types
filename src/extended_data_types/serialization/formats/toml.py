"""TOML serializer implementation."""

from __future__ import annotations

from typing import Any

import tomlkit

from extended_data_types.serialization.formats.base import _sanitize


class TomlSerializer:
    """TOML serializer."""

    def encode(
        self, data: Any, *, indent_size: int = 2, sort_keys: bool = False, **kwargs: Any
    ) -> str:
        """Serialize data to TOML."""

        def _replace_none(obj: Any) -> Any:
            if obj is None:
                return ""
            if isinstance(obj, dict):
                return {k: _replace_none(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [_replace_none(v) for v in obj]
            return obj

        sanitized = _replace_none(_sanitize(data))
        return tomlkit.dumps(sanitized)

    def decode(self, data: str, **_: Any) -> Any:
        """Deserialize TOML string to Python object."""
        return tomlkit.parse(data)

    def dumps(self, data: Any, **kwargs: Any) -> str:
        """Alias for encode."""
        return self.encode(data, **kwargs)

    def loads(self, data: str, **kwargs: Any) -> Any:
        """Alias for decode."""
        return self.decode(data, **kwargs)
