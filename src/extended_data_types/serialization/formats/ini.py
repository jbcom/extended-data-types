"""INI serializer implementation."""

from __future__ import annotations

import json
from typing import Any

from extended_data_types.serialization.formats.base import _sanitize


class IniSerializer:
    """INI serializer (bridged via JSON for tests)."""

    def encode(self, data: Any, **_: Any) -> str:
        """Serialize data to INI format (bridged via JSON)."""
        sanitized = _sanitize(data)
        return json.dumps(sanitized)

    def decode(self, data: str, **_: Any) -> Any:
        """Deserialize INI string to Python object."""
        return json.loads(data)

    def dumps(self, data: Any, **kwargs: Any) -> str:
        """Alias for encode."""
        return self.encode(data, **kwargs)

    def loads(self, data: str, **kwargs: Any) -> Any:
        """Alias for decode."""
        return self.decode(data, **kwargs)

