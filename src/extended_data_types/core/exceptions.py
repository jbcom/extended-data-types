"""Custom exceptions for extended data types."""

from typing import Any


class TransformError(Exception):
    """Base class for transformation errors."""

class ValidationError(Exception):
    """Raised when validation fails."""

class SerializationError(Exception):
    """Base class for serialization errors."""

class DeserializationError(SerializationError):
    """Raised when deserialization fails."""

class ConversionError(ValueError):
    """Raised when type conversion fails.
    
    Args:
        expected_type: The expected Python type
        value: The actual value that failed conversion
    """
    
    def __init__(self, expected_type: type, value: Any) -> None:
        self.expected_type = expected_type
        self.value = value
        
        # Special handling for Path type to ensure consistent messages
        type_str = "<class 'pathlib.Path'>" if expected_type == Path else str(self.expected_type)
        super().__init__(f"Invalid {type_str} value: {self.value!r}") 