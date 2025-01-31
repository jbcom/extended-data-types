"""Text transformation utilities.

This module provides utilities for string manipulation and validation, including functions
to sanitize text, truncate messages, manipulate character cases, and convert between
different string formats.
"""

from __future__ import annotations

import sys
from urllib.parse import urlparse

import inflection


def bytestostr(bstr: str | memoryview | bytes | bytearray) -> str:
    """Converts bytes, memoryview, or bytearray to a UTF-8 decoded string.
    
    Args:
        bstr: The input to convert to a string.
            Can be a str, memoryview, bytes, or bytearray.
            
    Returns:
        str: The UTF-8 decoded string representation of the input.
        
    Raises:
        UnicodeDecodeError: If the bytes cannot be decoded into a valid UTF-8 string.
        
    Examples:
        >>> bytestostr(b"hello")
        'hello'
        >>> bytestostr("already string")
        'already string'
    """
    if isinstance(bstr, str):
        return bstr

    if isinstance(bstr, memoryview):
        bstr = bstr.tobytes()

    if isinstance(bstr, (bytes, bytearray)):
        return bstr.decode("utf-8")

    return str(bstr)

def sanitize_key(key: str, delim: str = "_") -> str:
    """Sanitizes a key by replacing non-alphanumeric characters with a delimiter.
    
    Args:
        key: The key to sanitize.
        delim: The delimiter to replace non-alphanumeric characters with.
        
    Returns:
        str: The sanitized key.
        
    Examples:
        >>> sanitize_key("Hello World!")
        'Hello_World_'
        >>> sanitize_key("test@example.com", "-")
        'test-example-com'
    """
    return "".join(x if (x.isalnum() or x == delim) else delim for x in key)

def truncate(msg: str, max_length: int, ender: str = "...") -> str:
    """Truncates a message to a maximum length, appending an ender if truncated.
    
    Args:
        msg: The message to truncate.
        max_length: The maximum length of the truncated message.
        ender: The string to append to the truncated message.
        
    Returns:
        str: The truncated message.
        
    Examples:
        >>> truncate("Hello World", 8)
        'Hello...'
        >>> truncate("Short", 10)
        'Short'
    """
    if len(msg) <= max_length:
        return msg
    return msg[: max_length - len(ender)] + ender

def lower_first_char(inp: str) -> str:
    """Converts the first character of a string to lowercase.
    
    Args:
        inp: The input string.
        
    Returns:
        str: The string with the first character in lowercase.
        
    Examples:
        >>> lower_first_char("Hello")
        'hello'
        >>> lower_first_char("")
        ''
    """
    return inp[:1].lower() + inp[1:] if inp else ""

def upper_first_char(inp: str) -> str:
    """Converts the first character of a string to uppercase.
    
    Args:
        inp: The input string.
        
    Returns:
        str: The string with the first character in uppercase.
        
    Examples:
        >>> upper_first_char("hello")
        'Hello'
        >>> upper_first_char("")
        ''
    """
    return inp[:1].upper() + inp[1:] if inp else ""

def is_url(url: str) -> bool:
    """Checks if the given string is a valid URL using urlparse.
    
    Args:
        url: The string to check.
        
    Returns:
        bool: True if the string is a valid URL, False otherwise.
        
    Examples:
        >>> is_url("https://example.com")
        True
        >>> is_url("not a url")
        False
    """
    parsed = urlparse(url.strip())
    return all([parsed.scheme, parsed.netloc])

def titleize_name(name: str) -> str:
    """Converts a camelCase name to a TitleCase name.
    
    Args:
        name: The camelCase name.
        
    Returns:
        str: The TitleCase name.
        
    Examples:
        >>> titleize_name("camelCaseName")
        'Camel Case Name'
    """
    return inflection.titleize(inflection.underscore(name))

def removeprefix(string: str, prefix: str) -> str:
    """Removes the specified prefix from the string if present.
    
    For Python versions less than 3.9, this function mimics str.removeprefix.
    
    Args:
        string: The string from which to remove the prefix.
        prefix: The prefix to remove.
        
    Returns:
        str: The string with the prefix removed if present.
        
    Examples:
        >>> removeprefix("prefix_text", "prefix_")
        'text'
        >>> removeprefix("text", "other")
        'text'
    """
    if sys.version_info >= (3, 9):
        return string.removeprefix(prefix)

    if prefix and string.startswith(prefix):
        return string[len(prefix):]

    return string

def removesuffix(string: str, suffix: str) -> str:
    """Removes the specified suffix from the string if present.
    
    For Python versions less than 3.9, this function mimics str.removesuffix.
    
    Args:
        string: The string from which to remove the suffix.
        suffix: The suffix to remove.
        
    Returns:
        str: The string with the suffix removed if present.
        
    Examples:
        >>> removesuffix("text_suffix", "_suffix")
        'text'
        >>> removesuffix("text", "other")
        'text'
    """
    if sys.version_info >= (3, 9):
        return string.removesuffix(suffix)

    if suffix and string.endswith(suffix):
        return string[:-len(suffix)]

    return string 