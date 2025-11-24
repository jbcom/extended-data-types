"""Enhanced serialization handlers building on benedict capabilities.

This module extends benedict's serialization capabilities with additional
formats and validation, while reusing its core functionality.

Typical usage:
    >>> from extended_data_types.serialization.handlers import SerializationHandler
    >>> handler = SerializationHandler()
    >>> result = handler.serialize({"key": "value"}, "hcl2")
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

import attrs
import json
import yaml
import tomlkit

from pydantic import BaseModel, Field

from .types import convert_to_serializable, reconstruct_from_serialized
from .languages.hcl2.serializer import HCL2Serializer


FormatType = Literal["json", "yaml", "toml", "hcl2", "raw"]


class SerializationError(Exception):
    """Raised when serialization fails."""


class SerializationOptions(BaseModel):
    """Options specific to formats not handled by benedict."""

    hcl2_compact: bool = Field(default=False)
    raw_formatter: str | None = Field(default=None)


@attrs.define
class SerializationHandler:
    """Handles formats extending benedict's capabilities.

    This handler primarily focuses on formats not natively supported
    by benedict, delegating to benedict for supported formats.

    Attributes:
        options: Options for non-benedict formats
    """

    options: SerializationOptions = attrs.field(
        factory=SerializationOptions,
        converter=lambda x: (
            x if isinstance(x, SerializationOptions) else SerializationOptions(**x)
        ),
    )

    def serialize(
        self,
        data: Any,
        format: FormatType = "json",
        **options: Any,
    ) -> str:
        """Serialize data, delegating to simple safe encoders.

        Args:
            data: Data to serialize
            format: Target format
            **options: Format-specific options

        Returns:
            Serialized string

        Raises:
            SerializationError: If serialization fails

        Example:
            >>> handler = SerializationHandler()
            >>> result = handler.serialize({"key": "value"}, "hcl2")
        """
        try:
            serializable = convert_to_serializable(data)

            if format == "json":
                return json.dumps(
                    serializable,
                    indent=options.get("indent", options.get("indent_size")),
                    sort_keys=options.get("sort_keys", False),
                    default=str,
                )

            if format == "yaml":
                return yaml.safe_dump(
                    serializable,
                    indent=options.get("indent", options.get("indent_size", 2)),
                    sort_keys=options.get("sort_keys", False),
                    default_flow_style=options.get("default_flow_style"),
                )

            if format == "toml":
                return tomlkit.dumps(serializable)

            if format == "hcl2":
                return self._to_hcl2(serializable, **options)

            if format == "raw":
                return self._to_raw(serializable, **options)

            raise ValueError(f"Unsupported format: {format}")

        except Exception as e:
            if isinstance(e, ValueError):
                raise
            raise SerializationError(f"Failed to serialize to {format}: {e}") from e

    def deserialize(
        self,
        data: str | bytes | Path,
        format: FormatType = "json",
        **options: Any,
    ) -> Any:
        """Deserialize data, delegating to simple safe decoders.

        Args:
            data: Data to deserialize
            format: Source format
            **options: Format-specific options

        Returns:
            Deserialized data

        Raises:
            SerializationError: If deserialization fails

        Example:
            >>> handler = SerializationHandler()
            >>> result = handler.deserialize('key = "value"', "hcl2")
        """
        try:
            text = Path(data).read_text() if isinstance(data, Path) else str(data)

            if format == "json":
                return reconstruct_from_serialized(json.loads(text))

            if format == "yaml":
                return reconstruct_from_serialized(yaml.safe_load(text))

            if format == "toml":
                return reconstruct_from_serialized(tomlkit.parse(text))

            if format == "hcl2":
                return reconstruct_from_serialized(self._from_hcl2(text, **options))

            if format == "raw":
                return self._from_raw(text, **options)

            raise ValueError(f"Unsupported format: {format}")

        except Exception as e:
            if isinstance(e, ValueError):
                raise
            raise SerializationError(f"Failed to deserialize from {format}: {e}") from e

    def _to_hcl2(self, data: Any, **options: Any) -> str:
        """Convert data to HCL2 format.

        Args:
            data: Data to convert
            **options: HCL2-specific options

        Returns:
            HCL2 formatted string
        """
        serializer = HCL2Serializer(
            indent_size=options.get("indent_size", 2),
            sort_keys=options.get("sort_keys", False),
        )
        return serializer.encode(data)

    def _from_hcl2(self, data: str | bytes | Path, **options: Any) -> Any:
        """Parse HCL2 format data.

        Args:
            data: Data to parse
            **options: HCL2-specific options

        Returns:
            Parsed data structure
        """
        serializer = HCL2Serializer()
        if isinstance(data, Path):
            data = data.read_text()
        return serializer.decode(str(data))

    def _to_raw(self, data: Any, **options: Any) -> str:
        """Convert data to raw string format.

        Args:
            data: Data to convert
            **options: Formatting options

        Returns:
            String representation
        """
        formatter = options.get("raw_formatter", self.options.raw_formatter)
        if formatter:
            return formatter(data)
        return str(data)

    def _from_raw(self, data: str | bytes | Path, **options: Any) -> str:
        """Parse raw string data.

        Args:
            data: Data to parse
            **options: Parsing options

        Returns:
            String value
        """
        return str(data)
