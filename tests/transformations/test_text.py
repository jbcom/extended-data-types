"""Tests for text transformation utilities."""

from __future__ import annotations

import pytest

from extended_data_types.transformations.text import (
    bytestostr,
    is_url,
    lower_first_char,
    removeprefix,
    removesuffix,
    sanitize_key,
    titleize_name,
    truncate,
    upper_first_char,
)


def test_bytestostr():
    """Test bytestostr function."""
    # Test with different input types
    assert bytestostr("already string") == "already string"
    assert bytestostr(b"bytes string") == "bytes string"
    assert bytestostr(bytearray(b"bytearray string")) == "bytearray string"
    assert bytestostr(memoryview(b"memoryview string")) == "memoryview string"

    # Test with special characters
    assert bytestostr("hello 世界".encode()) == "hello 世界"

    # Test with empty inputs
    assert bytestostr("") == ""
    assert bytestostr(b"") == ""

    # Test with non-UTF8 should raise error
    with pytest.raises(UnicodeDecodeError):
        bytestostr(b"\xff\xfe")


def test_sanitize_key():
    """Test sanitize_key function."""
    # Test basic sanitization
    assert sanitize_key("Hello World!") == "Hello_World_"
    assert sanitize_key("test@example.com") == "test_example_com"

    # Test with custom delimiter
    assert sanitize_key("Hello World!", "-") == "Hello-World-"
    assert sanitize_key("test@example.com", ".") == "test.example.com"

    # Test with special characters
    assert sanitize_key("!@#$%^&*()") == "__________"

    # Test with empty string
    assert sanitize_key("") == ""


def test_truncate():
    """Test truncate function."""
    # Test no truncation needed
    assert truncate("short", 10) == "short"

    # Test truncation
    assert truncate("Hello World", 8) == "Hello..."

    # Test custom ender
    assert truncate("Hello World", 8, "!") == "Hello W!"

    # Test exact length
    assert truncate("Hello", 5) == "Hello"

    # Test empty string
    assert truncate("", 5) == ""

    # Test ender longer than max_length
    assert truncate("Hello", 2, "...") == "."


def test_lower_first_char():
    """Test lower_first_char function."""
    assert lower_first_char("Hello") == "hello"
    assert lower_first_char("HELLO") == "hELLO"
    assert lower_first_char("already lowercase") == "already lowercase"
    assert lower_first_char("") == ""
    assert lower_first_char("a") == "a"
    assert lower_first_char("A") == "a"


def test_upper_first_char():
    """Test upper_first_char function."""
    assert upper_first_char("hello") == "Hello"
    assert upper_first_char("HELLO") == "HELLO"
    assert upper_first_char("already uppercase") == "Already uppercase"
    assert upper_first_char("") == ""
    assert upper_first_char("a") == "A"
    assert upper_first_char("A") == "A"


def test_is_url():
    """Test is_url function."""
    # Valid URLs
    assert is_url("https://example.com")
    assert is_url("http://localhost:8080")
    assert is_url("ftp://files.example.com")

    # Invalid URLs
    assert not is_url("not a url")
    assert not is_url("http://")
    assert not is_url("example.com")
    assert not is_url("")

    # URLs with whitespace
    assert is_url("  https://example.com  ")


def test_titleize_name():
    """Test titleize_name function."""
    assert titleize_name("camelCaseName") == "Camel Case Name"
    assert titleize_name("simpletext") == "Simpletext"
    assert titleize_name("already_snake_case") == "Already Snake Case"
    assert titleize_name("") == ""
    assert titleize_name("UPPERCASE") == "Uppercase"
    assert titleize_name("mixedCASeText") == "Mixed Ca Se Text"


def test_removeprefix():
    """Test removeprefix function."""
    # Basic prefix removal
    assert removeprefix("prefix_text", "prefix_") == "text"
    assert removeprefix("prefixtext", "prefix") == "text"

    # No prefix match
    assert removeprefix("text", "prefix") == "text"
    assert removeprefix("different_prefix_text", "prefix") == "different_prefix_text"

    # Empty strings
    assert removeprefix("", "") == ""
    assert removeprefix("text", "") == "text"
    assert removeprefix("", "prefix") == ""

    # Prefix same as string
    assert removeprefix("prefix", "prefix") == ""


def test_removesuffix():
    """Test removesuffix function."""
    # Basic suffix removal
    assert removesuffix("text_suffix", "_suffix") == "text"
    assert removesuffix("text_suffix", "suffix") == "text_"
    assert removesuffix("textsuffix", "suffix") == "text"
    assert removesuffix("text_different_suffix", "suffix") == "text_different_"

    # No suffix match
    assert removesuffix("text", "suffix") == "text"

    # Empty strings
    assert removesuffix("", "") == ""
    assert removesuffix("text", "") == "text"
    assert removesuffix("", "suffix") == ""

    # Suffix same as string
    assert removesuffix("suffix", "suffix") == ""

    # Aligns with built-in removesuffix when available (Python >= 3.9)
    if hasattr(str, "removesuffix"):
        cases = [
            ("text_suffix", "_suffix"),
            ("text_suffix", "suffix"),
            ("textsuffix", "suffix"),
            ("text_different_suffix", "suffix"),
            ("text", "suffix"),
        ]
        for original, suffix in cases:
            assert removesuffix(original, suffix) == original.removesuffix(suffix)
