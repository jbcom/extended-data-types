"""Tests for extended collection types."""

from __future__ import annotations

import pytest

from extended_data_types.types.collections import SortedDefaultDict


def test_sorted_default_dict_basic():
    """Test basic SortedDefaultDict functionality."""
    d = SortedDefaultDict(list)
    
    # Test default factory
    assert d["new_key"] == []
    
    # Test sorting
    d["c"] = [3]
    d["a"] = [1]
    d["b"] = [2]
    assert list(d.keys()) == ["a", "b", "c"]

def test_sorted_default_dict_nested():
    """Test nested SortedDefaultDict operations."""
    d = SortedDefaultDict(SortedDefaultDict)
    
    # Test nested default factory
    d["outer"]["inner"] = 1
    assert d["outer"]["inner"] == 1
    assert d["new_outer"]["new_inner"] == {}
    
    # Test sorting at both levels
    d["z"]["c"] = 3
    d["a"]["b"] = 2
    d["m"]["a"] = 1
    assert list(d.keys()) == ["a", "m", "z"]
    assert list(d["z"].keys()) == ["c"]

def test_sorted_default_dict_none_factory():
    """Test SortedDefaultDict with None factory."""
    d = SortedDefaultDict()
    
    # Should raise KeyError for missing keys
    with pytest.raises(KeyError):
        _ = d["missing"]
    
    # But should still maintain sorting
    d["c"] = 3
    d["a"] = 1
    d["b"] = 2
    assert list(d.keys()) == ["a", "b", "c"]

def test_sorted_default_dict_custom_factory():
    """Test SortedDefaultDict with custom factory."""
    def factory():
        return {"default": True}
    
    d = SortedDefaultDict(factory)
    
    # Test custom factory
    assert d["new_key"] == {"default": True}
    
    # Test sorting still works
    d["c"] = {"custom": 3}
    d["a"] = {"custom": 1}
    d["b"] = {"custom": 2}
    assert list(d.keys()) == ["a", "b", "c"] 