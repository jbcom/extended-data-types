"""Enhanced serialization registry using benedict and marshmallow.

This module provides a comprehensive serialization system that leverages
python-benedict for data handling and marshmallow for schema validation.

Typical usage:
    >>> from extended_data_types.serialization.registry import serialize
    >>> data = {"name": "test", "value": 123}
    >>> json_str = serialize(data, "json")
    >>> yaml_str = serialize(data, "yaml")
"""

from __future__ import annotations

from typing import Any, Protocol

from benedict import benedict
from marshmallow import Schema, fields
from pydantic import BaseModel

from ..core.exceptions import SerializationError


class Serializer(Protocol):
    """Protocol defining the interface for serializers.
    
    This protocol ensures all serializers provide consistent methods for
    serialization and deserialization.
    
    Note:
        Implementations must provide both loads() and dumps() methods.
    """
    
    def loads(self, data: str, **kwargs: Any) -> Any:
        """Deserialize data from string.
        
        Args:
            data: String to deserialize
            **kwargs: Format-specific options
        
        Returns:
            Deserialized data structure
        
        Raises:
            SerializationError: If deserialization fails
        """
        ...
    
    def dumps(self, obj: Any, **kwargs: Any) -> str:
        """Serialize data to string.
        
        Args:
            obj: Data to serialize
            **kwargs: Format-specific options
        
        Returns:
            Serialized string
        
        Raises:
            SerializationError: If serialization fails
        """
        ...

class SerializerSchema(Schema):
    """Schema for serialization metadata.
    
    This schema defines the structure for serializer configuration and
    metadata.
    
    Attributes:
        format: Format identifier
        options: Format-specific options
    
    Example:
        >>> schema = SerializerSchema()
        >>> data = {"format": "json", "options": {"indent": 2}}
        >>> result = schema.load(data)
    """
    
    format = fields.Str(required=True)
    options = fields.Dict(keys=fields.Str(), values=fields.Raw())

class SerializationConfig(BaseModel):
    """Configuration for serialization behavior.
    
    This class defines global configuration options for serialization
    operations.
    
    Attributes:
        default_format: Default serialization format
        preserve_types: Whether to preserve type information
        indent: Indentation level for formatted output
        sort_keys: Whether to sort dictionary keys
    
    Example:
        >>> config = SerializationConfig(default_format="yaml", indent=2)
    """
    
    default_format: str = "json"
    preserve_types: bool = True
    indent: int | None = None
    sort_keys: bool = False

class SerializationRegistry:
    """Enhanced serialization registry.
    
    This class manages serializers and provides high-level serialization
    operations with configuration options.
    
    Attributes:
        _serializers: Dictionary of registered serializers
        _config: Serialization configuration
    
    Example:
        >>> registry = SerializationRegistry()
        >>> registry.register("custom", CustomSerializer())
        >>> result = registry.serialize(data, "custom")
    """
    
    def __init__(self) -> None:
        """Initialize registry with default configuration."""
        self._serializers: dict[str, Serializer] = {}
        self._config = SerializationConfig()
        
        # Register built-in serializers from benedict
        for format_name, serializer in benedict.get_serializers().items():
            self.register(format_name, serializer)
    
    def register(self, format_name: str, serializer: Any) -> None:
        """Register a new serializer.
        
        Args:
            format_name: Name of the format
            serializer: Serializer implementation
        
        Raises:
            ValueError: If serializer is invalid
        
        Example:
            >>> registry.register("custom", CustomSerializer())
        """
        if not isinstance(serializer, Serializer):
            raise ValueError(f"Invalid serializer for {format_name}")
        self._serializers[format_name] = serializer
    
    def serialize(
        self,
        data: Any,
        format_name: str | None = None,
        **options: Any,
    ) -> str:
        """Serialize data to string.
        
        Args:
            data: Data to serialize
            format_name: Target format (uses default if None)
            **options: Format-specific options
        
        Returns:
            Serialized string
        
        Raises:
            SerializationError: If serialization fails
        
        Example:
            >>> result = registry.serialize({"key": "value"}, "json")
        """
        format_name = format_name or self._config.default_format
        try:
            serializer = self._serializers[format_name]
            if self._config.preserve_types:
                data = benedict(data)
            return serializer.dumps(
                data,
                indent=self._config.indent,
                sort_keys=self._config.sort_keys,
                **options,
            )
        except Exception as e:
            raise SerializationError(f"Failed to serialize to {format_name}: {e}")
    
    def deserialize(
        self,
        data: str,
        format_name: str | None = None,
        **options: Any,
    ) -> Any:
        """Deserialize string to data.
        
        Args:
            data: String to deserialize
            format_name: Source format (uses default if None)
            **options: Format-specific options
        
        Returns:
            Deserialized data
        
        Raises:
            SerializationError: If deserialization fails
        
        Example:
            >>> data = registry.deserialize('{"key": "value"}', "json")
        """
        format_name = format_name or self._config.default_format
        try:
            serializer = self._serializers[format_name]
            result = serializer.loads(data, **options)
            return benedict(result) if self._config.preserve_types else result
        except Exception as e:
            raise SerializationError(
                f"Failed to deserialize from {format_name}: {e}"
            )

# Global registry instance
registry = SerializationRegistry()

def serialize(data: Any, format_name: str | None = None, **options: Any) -> str:
    """Serialize data using global registry.
    
    This is a convenience function that uses the global registry instance.
    
    Args:
        data: Data to serialize
        format_name: Target format (uses default if None)
        **options: Format-specific options
    
    Returns:
        Serialized string
    
    Example:
        >>> json_str = serialize({"key": "value"}, "json")
    """
    return registry.serialize(data, format_name, **options)

def deserialize(data: str, format_name: str | None = None, **options: Any) -> Any:
    """Deserialize data using global registry.
    
    This is a convenience function that uses the global registry instance.
    
    Args:
        data: String to deserialize
        format_name: Source format (uses default if None)
        **options: Format-specific options
    
    Returns:
        Deserialized data
    
    Example:
        >>> data = deserialize('{"key": "value"}', "json")
    """
    return registry.deserialize(data, format_name, **options) 