"""Tests for map transformation utilities."""

from __future__ import annotations

import pytest

from extended_data_types.transformations.maps import (
    all_values_from_map,
    deduplicate_map,
    filter_map,
    first_non_empty_value_from_map,
    flatten_map,
    get_default_dict,
    unhump_map,
    zipmap,
)


def test_first_non_empty_value_from_map():
    """Test first_non_empty_value_from_map function."""
    test_map = {"a": None, "b": "", "c": "value", "d": "another"}
    assert first_non_empty_value_from_map(test_map, "a", "b", "c") == "value"
    assert first_non_empty_value_from_map(test_map, "a", "b") is None
    assert first_non_empty_value_from_map(test_map, "x", "y") is None
    assert first_non_empty_value_from_map({}, "a") is None


def test_deduplicate_map():
    """Test deduplicate_map function."""
    test_map = {
        "list": [1, 1, 2, 2, 3],
        "nested": {"list": [4, 4, 5]},
        "simple": "value",
    }
    result = deduplicate_map(test_map)
    assert result["list"] == [1, 2, 3]
    assert result["nested"]["list"] == [4, 5]
    assert result["simple"] == "value"


def test_all_values_from_map():
    """Test all_values_from_map function."""
    test_map = {"a": 1, "b": {"c": 2}, "d": [3, {"e": 4}], "f": {"g": [5, {"h": 6}]}}
    values = all_values_from_map(test_map)
    assert sorted(values) == [1, 2, 3, 4, 5, 6]


def test_flatten_map():
    """Test flatten_map function."""
    test_map = {"a": {"b": 1, "c": {"d": 2}}, "e": [3, 4], "f": "value"}
    result = flatten_map(test_map)
    assert result == {"a.b": 1, "a.c.d": 2, "e.0": 3, "e.1": 4, "f": "value"}

    # Test with custom separator
    result = flatten_map(test_map, separator="_")
    assert "a_b" in result
    assert "a_c_d" in result


def test_zipmap():
    """Test zipmap function."""
    keys = ["a", "b", "c"]
    values = ["1", "2", "3"]
    result = zipmap(keys, values)
    assert result == {"a": "1", "b": "2", "c": "3"}

    # Test with uneven lists
    assert zipmap(keys, ["1"]) == {"a": "1"}
    assert zipmap(["a"], values) == {"a": "1"}
    assert zipmap([], []) == {}


def test_get_default_dict():
    """Test get_default_dict function."""
    # Test basic defaultdict
    d = get_default_dict(levels=2)
    d["a"]["b"] = 1
    assert d["a"]["b"] == 1
    assert isinstance(d["x"]["y"], dict)

    # Test with sorted dict
    d = get_default_dict(use_sorted_dict=True, levels=1)
    d["c"] = 3
    d["a"] = 1
    d["b"] = 2
    assert list(d.keys()) == ["a", "b", "c"]

    # Test invalid levels
    with pytest.raises(ValueError):
        get_default_dict(levels=0)


def test_unhump_map():
    """Test unhump_map function."""
    test_map = {
        "camelCase": 1,
        "anotherKey": {"nestedCamel": 2, "deeperNesting": {"evenDeeperCamel": 3}},
    }
    result = unhump_map(test_map)
    assert result == {
        "camel_case": 1,
        "another_key": {"nested_camel": 2, "deeper_nesting": {"even_deeper_camel": 3}},
    }

    # Test with prefix dropping
    test_map = {"prefixCamel": 1, "noPrefixCamel": 2}
    result = unhump_map(test_map, drop_without_prefix="prefix")
    assert result == {"prefix_camel": 1}

    # Nested prefix dropping propagates to children
    nested_prefixed = {
        "prefixCamel": {"prefixChild": 2, "noPrefixChild": 3},
        "noPrefixCamel": {"prefixChild": 4},
    }
    result = unhump_map(nested_prefixed, drop_without_prefix="prefix")
    assert result == {"prefix_camel": {"prefix_child": 2}}


def test_filter_map():
    """Test filter_map function."""
    test_map = {"a": 1, "b": 2, "c": 3, "d": 4}

    # Test with allowlist
    filtered, remaining = filter_map(test_map, allowlist=["a", "b"])
    assert filtered == {"a": 1, "b": 2}
    assert remaining == {"c": 3, "d": 4}

    # Test with denylist
    filtered, remaining = filter_map(test_map, denylist=["c", "d"])
    assert filtered == {"a": 1, "b": 2}
    assert remaining == {"c": 3, "d": 4}

    # Test with both lists
    filtered, remaining = filter_map(
        test_map, allowlist=["a", "b", "c"], denylist=["b"]
    )
    assert filtered == {"a": 1, "c": 3}
    assert remaining == {"b": 2, "d": 4}

    # Test with None map
    filtered, remaining = filter_map(None)
    assert filtered == {}
    assert remaining == {}
