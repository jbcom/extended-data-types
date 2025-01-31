"""Tests for string pattern operations."""

from __future__ import annotations

import re

import pytest

from extended_data_types.transformations.strings.pattern import (
    extract_pattern, find_boundaries, match_pattern, replace_pattern,
    split_pattern)


def test_match_pattern() -> None:
    """Test pattern matching."""
    # Test with string pattern
    assert match_pattern("hello world", "hello") == [(0, 5)]
    assert match_pattern("hello hello", "hello") == [(0, 5), (6, 11)]
    
    # Test with regex pattern
    pattern = r"\b\w+\b"
    assert match_pattern("hello world", pattern) == [(0, 5), (6, 11)]
    
    # Test with compiled pattern
    pattern = re.compile(r"\b\w+\b")
    assert match_pattern("hello world", pattern) == [(0, 5), (6, 11)]
    
    # Test with flags
    assert match_pattern("Hello", "hello", flags=re.IGNORECASE) == [(0, 5)]
    
    # Test with no matches
    assert match_pattern("hello", "xyz") == []
    
    # Test empty string
    assert match_pattern("", r"\w+") == []


def test_replace_pattern() -> None:
    """Test pattern replacement."""
    # Test simple replacement
    assert replace_pattern("hello world", "hello", "hi") == "hi world"
    
    # Test with regex pattern
    assert replace_pattern("hello 123", r"\d+", "xyz") == "hello xyz"
    
    # Test with callable replacement
    assert replace_pattern(
        "hello 123",
        r"\d+",
        lambda m: str(int(m.group()) * 2)
    ) == "hello 246"
    
    # Test with count limit
    assert replace_pattern("hello hello", "hello", "hi", count=1) == "hi hello"
    
    # Test with flags
    assert replace_pattern(
        "Hello",
        "hello",
        "hi",
        flags=re.IGNORECASE
    ) == "hi"
    
    # Test with no matches
    assert replace_pattern("hello", "xyz", "abc") == "hello"


def test_extract_pattern() -> None:
    """Test pattern extraction."""
    # Test simple extraction
    text = "The price is $12.34 and €5.67"
    pattern = r"\$\d+\.\d+"
    assert extract_pattern(text, pattern) == ["$12.34"]
    
    # Test with groups
    text = "Contact: john@example.com, jane@example.com"
    pattern = r"(\w+)@(\w+)\.(\w+)"
    expected = [
        ("john", "example", "com"),
        ("jane", "example", "com")
    ]
    assert extract_pattern(text, pattern) == expected
    
    # Test with flags
    text = "Hello HELLO"
    assert extract_pattern(text, "hello", flags=re.IGNORECASE) == ["Hello", "HELLO"]
    
    # Test with no matches
    assert extract_pattern("hello", r"\d+") == []
    
    # Test with invalid pattern
    with pytest.raises(re.error):
        extract_pattern("hello", "(invalid")


def test_split_pattern() -> None:
    """Test pattern splitting."""
    # Test simple split
    assert split_pattern("a,b,c", ",") == ["a", "b", "c"]
    
    # Test with regex pattern
    assert split_pattern("a1b2c", r"\d+") == ["a", "b", "c"]
    
    # Test with max splits
    assert split_pattern("a,b,c", ",", maxsplit=1) == ["a", "b,c"]
    
    # Test with flags
    text = "aBcDeFg"
    assert split_pattern(text, "[aeg]", flags=re.IGNORECASE) == ["", "BcD", "F", ""]
    
    # Test with no matches
    assert split_pattern("hello", "xyz") == ["hello"]
    
    # Test empty string
    assert split_pattern("", ",") == [""]


def test_find_boundaries() -> None:
    """Test word boundary finding."""
    # Test basic boundaries
    text = "Hello, World!"
    assert find_boundaries(text) == [(0, 5), (7, 12)]
    
    # Test with custom pattern
    text = "one,two;three"
    assert find_boundaries(text, r"[,;]") == [(3, 4), (7, 8)]
    
    # Test with flags
    text = "Hello WORLD"
    pattern = "hello"
    assert find_boundaries(text, pattern, flags=re.IGNORECASE) == [(0, 5)]
    
    # Test with no boundaries
    assert find_boundaries("hello", ",") == []
    
    # Test empty string
    assert find_boundaries("") == [] 