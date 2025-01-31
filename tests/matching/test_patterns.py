"""Tests for pattern matching utilities."""

import pytest

from extended_data_types.matching.patterns import Matcher


def test_partial_string_matching():
    """Test partial string matching."""
    matcher = Matcher()
    
    assert matcher.is_partial_match("test", "testing")
    assert matcher.is_partial_match("TEST", "testing")
    assert not matcher.is_partial_match("test", "best")
    
    # Test prefix only
    assert matcher.is_partial_match("test", "testing", check_prefix_only=True)
    assert not matcher.is_partial_match("ing", "testing", check_prefix_only=True)
    
    # Test case sensitivity
    matcher_sensitive = Matcher(case_sensitive=True)
    assert not matcher_sensitive.is_partial_match("TEST", "test")


def test_value_matching():
    """Test value matching."""
    matcher = Matcher()
    
    # Test dictionaries
    assert matcher.is_value_match({"a": 1}, {"a": 1})
    assert not matcher.is_value_match({"a": 1}, {"a": 2})
    
    # Test lists
    assert matcher.is_value_match([1, 2, 3], [3, 2, 1])
    assert not matcher.is_value_match([1, 2], [1, 2, 3])
    
    # Test mixed types
    assert not matcher.is_value_match("1", 1)
    
    # Test None
    assert matcher.is_value_match(None, None)
    assert not matcher.is_value_match(None, "") 