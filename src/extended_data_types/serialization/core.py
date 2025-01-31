"""Core serialization functionality.

This module provides the base classes and interfaces for serialization operations.
It includes schema validation and type checking capabilities.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from extended_data_types.core.exceptions import (DeserializationError,
                                                 SerializationError)
from extended_data_types.core.types import convert_special_type, typeof

T = TypeVar('T')

class SerializationSchema:
    """Schema for validating serialization/deserialization.
    
    This class provides type validation for data structures being serialized
    or deserialized.
    
    Args:
        type_info: A dictionary mapping field names to their expected types.
        
    Example:
        >>> schema = SerializationSchema({'name': str, 'age': int})
        >>> schema.validate({'name': 'test', 'age': 25})
        True
        >>> schema.validate({'name': 'test', 'age': '25'})
        False
    """
    
    def __init__(self, type_info: dict[str, type]):
        """Initialize the schema with type information.

        Args:
            type_info: Dictionary mapping field names to their expected types.
        """
        self.type_info = type_info
        
    def validate(self, data: Any) -> bool:
        """Validate that data matches the schema.
        
        Args:
            data: The data structure to validate.
            
        Returns:
            bool: True if validation passes, False otherwise.
            
        Example:
            >>> schema = SerializationSchema({'name': str})
            >>> schema.validate({'name': 'test'})
            True
        """
        try:
            self._validate_types(data)
            return True
        except (TypeError, ValueError):
            return False
            
    def _validate_types(self, data: Any) -> None:
        """Recursively validate types in data structure.
        
        Args:
            data: The data structure to validate.
            
        Raises:
            TypeError: If an unexpected type is encountered.
        """
        actual_type = typeof(data)
        if actual_type not in self.type_info:
            raise TypeError(f"Unexpected type: {actual_type}")
            
        if isinstance(data, dict):
            for key, value in data.items():
                self._validate_types(value)
        elif isinstance(data, (list, tuple)):
            for item in data:
                self._validate_types(item)

class Serializer(Generic[T], ABC):
    """Base serializer interface.
    
    This abstract class defines the interface for serializers that convert
    objects to string representations.
    
    Args:
        schema: Optional schema for validating objects before serialization.
        
    Example:
        >>> class MySerializer(Serializer[dict]):
        ...     def serialize(self, obj: dict) -> str:
        ...         return json.dumps(obj)
    """
    
    def __init__(self, schema: SerializationSchema | None = None):
        """Initialize the serializer.

        Args:
            schema: Optional schema for validation.
        """
        self.schema = schema
        
    @abstractmethod
    def serialize(self, obj: T) -> str:
        """Serialize object to string.
        
        Args:
            obj: The object to serialize.
            
        Returns:
            str: The serialized string representation.
            
        Raises:
            SerializationError: If serialization fails.
        """
        pass
        
    def validate(self, obj: T) -> bool:
        """Validate object against schema.
        
        Args:
            obj: The object to validate.
            
        Returns:
            bool: True if validation passes, False otherwise.
        """
        if not self.schema:
            return True
        return self.schema.validate(obj)

class Deserializer(Generic[T], ABC):
    """Base deserializer interface.
    
    This abstract class defines the interface for deserializers that convert
    string representations back into objects.
    
    Args:
        schema: Optional schema for validating deserialized data.
        
    Example:
        >>> class MyDeserializer(Deserializer[dict]):
        ...     def deserialize(self, data: str) -> dict:
        ...         return json.loads(data)
    """
    
    def __init__(self, schema: SerializationSchema | None = None):
        """Initialize the deserializer.

        Args:
            schema: Optional schema for validation.
        """
        self.schema = schema
        
    @abstractmethod 
    def deserialize(self, data: str) -> T:
        """Deserialize string to object.
        
        Args:
            data: The string to deserialize.
            
        Returns:
            T: The deserialized object.
            
        Raises:
            DeserializationError: If deserialization fails.
        """
        pass
        
    def validate(self, data: Any) -> bool:
        """Validate deserialized data against schema.
        
        Args:
            data: The deserialized data to validate.
            
        Returns:
            bool: True if validation passes, False otherwise.
        """
        if not self.schema:
            return True
        return self.schema.validate(data) 