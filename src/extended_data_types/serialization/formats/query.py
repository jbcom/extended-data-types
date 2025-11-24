"""Query string serializer implementation."""

from __future__ import annotations

import urllib.parse
from typing import Any


class QuerySerializer:
    """Query string serializer."""

    def encode(self, data: Any, **_: Any) -> str:
        """Serialize data to query string format."""
        if not isinstance(data, dict):
            raise TypeError("Query serializer expects dict")
        return urllib.parse.urlencode(data, doseq=True)

    def decode(self, data: str, **_: Any) -> Any:
        """Deserialize query string to Python object."""
        return {k: v[0] if len(v) == 1 else v for k, v in urllib.parse.parse_qs(data).items()}

    def dumps(self, data: Any, **kwargs: Any) -> str:
        """Alias for encode."""
        return self.encode(data, **kwargs)

    def loads(self, data: str, **kwargs: Any) -> Any:
        """Alias for decode."""
        return self.decode(data, **kwargs)

