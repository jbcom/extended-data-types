"""Tests for splitter compatibility layer."""

from extended_data_types.compat.splitter import split_by_type, split_dict_by_type


def test_split_by_type_compatibility():
    """Test compatibility with bob's split_by_type."""
    items = [1, {"a": 1}, 2, {"b": 2}]
    non_dicts, dicts = split_by_type(items)
    assert non_dicts == [1, 2]
    assert dicts == [{"a": 1}, {"b": 2}]


def test_split_dict_by_type_compatibility():
    """Test compatibility with bob's split_dict_by_type."""
    data = {"a": 1, "b": {"x": 2}, "c": 3, "d": {"y": 4}}
    simple, nested = split_dict_by_type(data)
    assert simple == {"a": 1, "c": 3}
    assert nested == {"b": {"x": 2}, "d": {"y": 4}}
