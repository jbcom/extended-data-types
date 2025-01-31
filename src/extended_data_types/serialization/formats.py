"""Serialization format handlers with enhanced validation.

This module provides a comprehensive system for handling various serialization
formats with type safety and validation. Supports JSON, YAML, TOML, and HCL2.

Typical usage:
    >>> from extended_data_types.serialization.formats import FormatHandler
    >>> handler = FormatHandler()
    >>> result = handler.serialize({"key": "value"}, "json")
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

import attrs
from marshmallow import Schema, fields
from pydantic import BaseModel, Field

FormatType = Literal["json", "yaml", "toml", "hcl2", "raw"]


class SerializationOptions(BaseModel):
    """Configuration for serialization behavior.
    
    Attributes:
        indent: Number of spaces for indentation
        sort_keys: Whether to sort dictionary keys
        ensure_ascii: Whether to escape non-ASCII characters
    """
    
    indent: int | None = Field(default=2)
    sort_keys: bool = Field(default=True)
    ensure_ascii: bool = Field(default=False)


@attrs.define
class FormatHandler:
    """Handles serialization and deserialization for multiple formats.
    
    Attributes:
        default_format: Default format to use
        options: Serialization options
    """
    
    default_format: FormatType = attrs.field(default="json")
    options: SerializationOptions = attrs.field(
        factory=SerializationOptions,
        converter=lambda x: (
            x if isinstance(x, SerializationOptions)
            else SerializationOptions(**x)
        )
    )
    
    def serialize(
        self,
        data: Any,
        format: FormatType | None = None,
        **options: Any,
    ) -> str:
        """Serialize data to specified format.
        
        Args:
            data: Data to serialize
            format: Target format (json, yaml, toml, hcl2, raw)
            **options: Format-specific options
        
        Returns:
            Serialized string representation
        
        Raises:
            ValueError: If format is invalid
            SerializationError: If serialization fails
        
        Example:
            >>> handler = FormatHandler()
            >>> result = handler.serialize({"key": "value"}, "json")
            >>> print(result)
            {
              "key": "value"
            }
        """
        actual_format = format or self.default_format
        actual_options = {
            **self.options.model_dump(),
            **options
        }
        
        method = getattr(self, f"_to_{actual_format}", None)
        if not method:
            raise ValueError(f"Unsupported format: {actual_format}")
        
        return method(data, **actual_options)
    
    def deserialize(
        self,
        data: str | bytes | Path,
        format: FormatType | None = None,
        **options: Any,
    ) -> Any:
        """Deserialize data from specified format.
        
        Args:
            data: Data to deserialize
            format: Source format (json, yaml, toml, hcl2, raw)
            **options: Format-specific options
        
        Returns:
            Deserialized data structure
        
        Raises:
            ValueError: If format is invalid
            DeserializationError: If deserialization fails
        
        Example:
            >>> handler = FormatHandler()
            >>> result = handler.deserialize('{"key": "value"}', "json")
            >>> print(result)
            {'key': 'value'}
        """
        actual_format = format or self.default_format
        actual_options = {
            **self.options.model_dump(),
            **options
        }
        
        method = getattr(self, f"_from_{actual_format}", None)
        if not method:
            raise ValueError(f"Unsupported format: {actual_format}")
        
        return method(data, **actual_options) 