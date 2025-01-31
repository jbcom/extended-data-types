"""Modern string manipulation utilities with enhanced validation.

This module provides a modern, type-safe approach to string manipulation
with comprehensive validation and Python 3.10+ features.

Typical usage:
    >>> from extended_data_types.strings.manipulation import StringManipulator
    >>> manipulator = StringManipulator()
    >>> result = manipulator.bytes_to_str(b"test")
    >>> print(result)
    'test'
"""

from __future__ import annotations

from typing import Union

import attrs
from validators import url


@attrs.define
class StringManipulator:
    """Modern string manipulation with built-in validation.
    
    This class provides type-safe string manipulation methods with
    comprehensive validation and error handling.
    
    Attributes:
        encoding: Default encoding to use for byte conversions.
    
    Example:
        >>> manipulator = StringManipulator()
        >>> result = manipulator.sanitize_key("test@key")
        >>> print(result)
        'test_key'
    """
    
    encoding: str = attrs.field(default="utf-8")
    
    def bytes_to_str(
        self,
        value: Union[str, memoryview, bytes, bytearray],
        encoding: str | None = None,
    ) -> str:
        """Convert bytes-like object to string with validation.
        
        Args:
            value: The bytes-like object to convert. Can be str, memoryview,
                bytes, or bytearray.
            encoding: Optional encoding to use. Defaults to instance encoding.
        
        Returns:
            The converted string value.
        
        Raises:
            UnicodeDecodeError: If the bytes cannot be decoded.
            TypeError: If the input type is not supported.
        
        Example:
            >>> manipulator = StringManipulator()
            >>> result = manipulator.bytes_to_str(b"test")
            >>> print(result)
            'test'
        """
        if isinstance(value, str):
            return value
        
        actual_encoding = encoding or self.encoding
        
        if isinstance(value, memoryview):
            value = value.tobytes()
        
        if not isinstance(value, (bytes, bytearray)):
            raise TypeError(
                f"Expected bytes-like object, got {type(value).__name__}"
            )
        
        return value.decode(actual_encoding)
    
    def sanitize_key(
        self,
        key: str,
        delimiter: str = "_",
        preserve_case: bool = True,
    ) -> str:
        """Sanitize a key by replacing invalid characters.
        
        Args:
            key: The key to sanitize.
            delimiter: Character to use as delimiter. Defaults to "_".
            preserve_case: Whether to preserve original case. Defaults to True.
        
        Returns:
            The sanitized key string.
        
        Raises:
            ValueError: If delimiter is not a single character.
            TypeError: If key cannot be converted to string.
        
        Example:
            >>> manipulator = StringManipulator()
            >>> result = manipulator.sanitize_key("test@key")
            >>> print(result)
            'test_key'
        """
        if len(delimiter) != 1:
            raise ValueError("Delimiter must be a single character")
        
        try:
            key_str = str(key)
        except Exception as e:
            raise TypeError(f"Cannot convert key to string: {e}") from e
        
        sanitized = "".join(
            c if c.isalnum() or c == delimiter else delimiter
            for c in key_str
        )
        
        return sanitized if preserve_case else sanitized.lower()
    
    def truncate(
        self,
        text: str,
        max_length: int,
        suffix: str = "...",
        preserve_words: bool = False,
    ) -> str:
        """Truncate text to specified length.
        
        Args:
            text: The text to truncate.
            max_length: Maximum length of resulting string.
            suffix: String to append if truncated. Defaults to "...".
            preserve_words: Whether to preserve whole words. Defaults to False.
        
        Returns:
            The truncated string.
        
        Raises:
            ValueError: If max_length is less than length of suffix.
            TypeError: If text cannot be converted to string.
        
        Example:
            >>> manipulator = StringManipulator()
            >>> result = manipulator.truncate("long text", 7)
            >>> print(result)
            'long...'
        """
        if max_length < len(suffix):
            raise ValueError(
                f"max_length ({max_length}) must be >= suffix length ({len(suffix)})"
            )
        
        try:
            text_str = str(text)
        except Exception as e:
            raise TypeError(f"Cannot convert text to string: {e}") from e
        
        if len(text_str) <= max_length:
            return text_str
        
        truncated_length = max_length - len(suffix)
        
        if preserve_words:
            words = text_str[:truncated_length + 1].rsplit(maxsplit=1)
            return words[0] + suffix
        
        return text_str[:truncated_length] + suffix 