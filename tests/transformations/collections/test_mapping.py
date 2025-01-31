"""Tests for mapping operations."""

from __future__ import annotations

import pytest

from extended_data_types.transformations.collections.mapping import (
    filter_dict, flatten_dict, invert_dict, merge_dicts, transform_dict,
    unflatten_dict)


def test_merge_dicts() -> None:
    """Test dictionary merging."""
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 3, "c": 4}
    
    # Test basic merge
    assert merge_dicts(d1, d2) == {"a": 1, "b": 3, "c": 4}
    
    # Test with nested dictionaries
    d1 = {"a": 1, "b": {"x": 1, "y": 2}}
    d2 = {"b": {"y": 3, "z": 4}, "c": 5}
    assert merge_dicts(d1, d2) == {
        "a": 1,
        "b": {"x": 1, "y": 3, "z": 4},
        "c": 5
    }
    
    # Test with multiple dictionaries
    d3 = {"d": 6}
    assert merge_dicts(d1, d2, d3) == {
        "a": 1,
        "b": {"x": 1, "y": 3, "z": 4},
        "c": 5,
        "d": 6
    }
    
    # Test with empty dictionaries
    assert merge_dicts({}, d1) == d1
    assert merge_dicts(d1, {}) == d1
    assert merge_dicts({}, {}) == {}


def test_flatten_dict() -> None:
    """Test dictionary flattening."""
    # Test basic flattening
    d = {"a": 1, "b": {"x": 2, "y": 3}, "c": 4}
    assert flatten_dict(d) == {
        "a": 1,
        "b.x": 2,
        "b.y": 3,
        "c": 4
    }
    
    # Test with custom separator
    assert flatten_dict(d, separator="/") == {
        "a": 1,
        "b/x": 2,
        "b/y": 3,
        "c": 4
    }
    
    # Test with deeply nested dictionary
    d = {"a": {"b": {"c": {"d": 1}}}}
    assert flatten_dict(d) == {"a.b.c.d": 1}
    
    # Test with lists
    d = {"a": [1, 2, {"b": 3}]}
    assert flatten_dict(d) == {
        "a.0": 1,
        "a.1": 2,
        "a.2.b": 3
    }
    
    # Test empty dictionary
    assert flatten_dict({}) == {}


def test_unflatten_dict() -> None:
    """Test dictionary unflattening."""
    # Test basic unflattening
    d = {
        "a": 1,
        "b.x": 2,
        "b.y": 3,
        "c": 4
    }
    assert unflatten_dict(d) == {
        "a": 1,
        "b": {"x": 2, "y": 3},
        "c": 4
    }
    
    # Test with custom separator
    d = {
        "a": 1,
        "b/x": 2,
        "b/y": 3,
        "c": 4
    }
    assert unflatten_dict(d, separator="/") == {
        "a": 1,
        "b": {"x": 2, "y": 3},
        "c": 4
    }
    
    # Test with array indices
    d = {
        "a.0": 1,
        "a.1": 2,
        "a.2.b": 3
    }
    assert unflatten_dict(d) == {
        "a": [1, 2, {"b": 3}]
    }
    
    # Test empty dictionary
    assert unflatten_dict({}) == {}
    
    # Test invalid keys
    with pytest.raises(ValueError):
        unflatten_dict({"a.": 1})
    with pytest.raises(ValueError):
        unflatten_dict({".a": 1})


def test_filter_dict() -> None:
    """Test dictionary filtering."""
    d = {"a": 1, "b": 2, "c": 3, "d": 4}
    
    # Test with key function
    assert filter_dict(d, key_fn=lambda k: k in ["a", "b"]) == {"a": 1, "b": 2}
    
    # Test with value function
    assert filter_dict(d, value_fn=lambda v: v > 2) == {"c": 3, "d": 4}
    
    # Test with both functions
    assert filter_dict(
        d,
        key_fn=lambda k: k in ["a", "b", "c"],
        value_fn=lambda v: v > 2
    ) == {"c": 3}
    
    # Test with empty result
    assert filter_dict(d, value_fn=lambda v: v > 10) == {}
    
    # Test empty dictionary
    assert filter_dict({}) == {}


def test_transform_dict() -> None:
    """Test dictionary transformation."""
    d = {"a": 1, "b": 2, "c": 3}
    
    # Test key transformation
    assert transform_dict(
        d,
        key_fn=str.upper
    ) == {"A": 1, "B": 2, "C": 3}
    
    # Test value transformation
    assert transform_dict(
        d,
        value_fn=lambda x: x * 2
    ) == {"a": 2, "b": 4, "c": 6}
    
    # Test both transformations
    assert transform_dict(
        d,
        key_fn=str.upper,
        value_fn=lambda x: x * 2
    ) == {"A": 2, "B": 4, "C": 6}
    
    # Test empty dictionary
    assert transform_dict({}) == {}


def test_invert_dict() -> None:
    """Test dictionary inversion."""
    # Test basic inversion
    d = {"a": 1, "b": 2, "c": 3}
    assert invert_dict(d) == {1: "a", 2: "b", 3: "c"}
    
    # Test with duplicate values
    d = {"a": 1, "b": 1, "c": 2}
    assert invert_dict(d) == {1: ["a", "b"], 2: "c"}
    
    # Test with custom handling of duplicates
    assert invert_dict(d, multi=False) == {1: "b", 2: "c"}
    
    # Test with unhashable values
    d = {"a": [1, 2], "b": [3, 4]}
    with pytest.raises(TypeError):
        invert_dict(d)
    
    # Test empty dictionary
    assert invert_dict({}) == {} 