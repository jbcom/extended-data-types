"""YAML serializer implementation."""

from __future__ import annotations

from typing import Any

import yaml

from extended_data_types.serialization.formats.base import _sanitize


class YamlSerializer:
    """YAML serializer."""

    def encode(
        self,
        data: Any,
        *,
        indent_size: int = 2,
        sort_keys: bool = False,
        default_flow_style: bool | None = None,
        **kwargs: Any,
    ) -> str:
        """Serialize data to YAML."""
        sanitized = _sanitize(data)
        return yaml.safe_dump(
            sanitized,
            sort_keys=sort_keys,
            indent=kwargs.get("indent", indent_size),
            default_flow_style=(
                False if default_flow_style is None else default_flow_style
            ),
            width=1000,
        )

    def decode(self, data: str, **_: Any) -> Any:
        """Deserialize YAML string to Python object."""
        result = yaml.safe_load(data)
        if not isinstance(result, (dict, list)):
            raise ValueError("Invalid YAML content")
        return result

    def dumps(self, data: Any, **kwargs: Any) -> str:
        """Alias for encode."""
        return self.encode(data, **kwargs)

    def loads(self, data: str, **kwargs: Any) -> Any:
        """Alias for decode."""
        return self.decode(data, **kwargs)
