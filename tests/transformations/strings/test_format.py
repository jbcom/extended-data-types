"""Tests for string formatting operations."""

from __future__ import annotations

import pytest

from extended_data_types.transformations.strings.format import (
    format_align, format_case, format_number, format_pad, format_template,
    format_truncate)


def test_format_case() -> None:
    """Test case formatting."""
    assert format_case("hello world", "title") == "Hello World"
    assert format_case("hello world", "upper") == "HELLO WORLD"
    assert format_case("Hello World", "lower") == "hello world"
    assert format_case("hello_world", "camel") == "helloWorld"
    assert format_case("hello_world", "pascal") == "HelloWorld"
    assert format_case("helloWorld", "snake") == "hello_world"
    assert format_case("HelloWorld", "kebab") == "hello-world"
    
    # Test with special characters
    assert format_case("hello-world_123", "camel") == "helloWorld123"
    assert format_case("$hello@world", "snake") == "hello_world"
    
    # Test empty string
    assert format_case("", "title") == ""
    
    # Test invalid case
    with pytest.raises(ValueError):
        format_case("hello", "invalid")


def test_format_align() -> None:
    """Test text alignment."""
    assert format_align("hello", 10) == "hello     "
    assert format_align("hello", 10, "right") == "     hello"
    assert format_align("hello", 10, "center") == "  hello   "
    
    # Test with fill character
    assert format_align("hello", 10, fill="-") == "hello-----"
    assert format_align("hello", 10, "right", "-") == "-----hello"
    
    # Test with width smaller than text
    assert format_align("hello world", 5) == "hello world"
    
    # Test empty string
    assert format_align("", 5) == "     "
    
    # Test invalid alignment
    with pytest.raises(ValueError):
        format_align("hello", 10, "invalid")


def test_format_truncate() -> None:
    """Test text truncation."""
    assert format_truncate("hello world", 5) == "hello..."
    assert format_truncate("hello world", 5, suffix="") == "hello"
    assert format_truncate("hello", 10) == "hello"
    
    # Test with custom suffix
    assert format_truncate("hello world", 5, suffix="...more") == "hello...more"
    
    # Test with unicode characters
    assert format_truncate("hello 👋", 5) == "hello..."
    
    # Test empty string
    assert format_truncate("", 5) == ""
    
    # Test invalid length
    with pytest.raises(ValueError):
        format_truncate("hello", -1)


def test_format_pad() -> None:
    """Test text padding."""
    assert format_pad("hello", 10) == "  hello   "
    assert format_pad("hello", 10, "left") == "hello     "
    assert format_pad("hello", 10, "right") == "     hello"
    
    # Test with fill character
    assert format_pad("hello", 10, fill="-") == "--hello---"
    
    # Test with width smaller than text
    assert format_pad("hello world", 5) == "hello world"
    
    # Test empty string
    assert format_pad("", 5, fill="-") == "-----"
    
    # Test invalid position
    with pytest.raises(ValueError):
        format_pad("hello", 10, "invalid")


def test_format_template() -> None:
    """Test template formatting."""
    template = "Hello, {name}!"
    data = {"name": "World"}
    assert format_template(template, data) == "Hello, World!"
    
    # Test with multiple replacements
    template = "{greeting}, {name}!"
    data = {"greeting": "Hello", "name": "World"}
    assert format_template(template, data) == "Hello, World!"
    
    # Test with missing keys
    template = "Hello, {name}!"
    data = {}
    with pytest.raises(KeyError):
        format_template(template, data)
    
    # Test with invalid template
    template = "Hello, {name!"
    data = {"name": "World"}
    with pytest.raises(ValueError):
        format_template(template, data)


def test_format_number() -> None:
    """Test number formatting in strings."""
    assert format_number("File-123.txt", 5) == "File-00123.txt"
    assert format_number("Chapter 1", 2) == "Chapter 01"
    
    # Test with multiple numbers
    assert format_number("File-123-456.txt", 5) == "File-00123-00456.txt"
    
    # Test with no numbers
    assert format_number("hello.txt", 5) == "hello.txt"
    
    # Test with invalid width
    with pytest.raises(ValueError):
        format_number("123", -1) 