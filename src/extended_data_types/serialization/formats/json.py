"""JSON serializer implementation."""

from __future__ import annotations

import json
import re

from typing import Any

from extended_data_types.serialization.formats.base import _sanitize


class JsonSerializer:
    """JSON serializer with compact list formatting."""

    def encode(
        self, data: Any, *, indent_size: int = 2, sort_keys: bool = False, **kwargs: Any
    ) -> str:
        """Serialize data to JSON with compact list formatting."""
        sanitized = _sanitize(data)
        indent = kwargs.get("indent", indent_size)

        # Generate JSON with indent
        result = json.dumps(
            sanitized,
            indent=indent,
            sort_keys=sort_keys or kwargs.get("sort_keys", False),
            default=str,
        )

        # Post-process: compact simple lists that were formatted across lines
        # Match patterns like: "key": [\n    1,\n    2,\n    3\n  ]
        def compact_simple_list(match: re.Match[str]) -> str:
            key_part = match.group(1)  # "key"
            colon = match.group(2)  # ":"
            content = match.group(3)  # the list content
            # Check if content is just numbers/strings/booleans (simple list)
            if not re.search(r"[\[\{]", content):  # No nested arrays/objects
                # Extract values and compact
                values = re.findall(r"[^,\n\[\]]+", content)
                values = [v.strip() for v in values if v.strip()]
                compacted = ", ".join(values)
                return f'"{key_part}"{colon} [{compacted}]'
            return match.group(0)

        # Pattern: "key": [\n    values\n  ]
        result = re.sub(
            r'"([\w]+)"(\s*:\s*)\[\s*\n\s*([^\]]+)\s*\n\s*\]',
            compact_simple_list,
            result,
            flags=re.MULTILINE,
        )
        # Fix any double spaces after colon
        result = re.sub(r":\s+\[", ": [", result)
        return result

    def decode(self, data: str, **_: Any) -> Any:
        """Deserialize JSON string to Python object."""
        return json.loads(data)

    # Provide json-like compatibility attributes
    def dumps(self, data: Any, **kwargs: Any) -> str:
        """Alias for encode."""
        return self.encode(data, **kwargs)

    def loads(self, data: str, **kwargs: Any) -> Any:
        """Alias for decode."""
        return self.decode(data, **kwargs)
