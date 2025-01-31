"""Tests for collection splitting utilities."""

from extended_data_types.structures.splitter import CollectionSplitter


def test_split_by_type():
    """Test splitting sequences by type."""
    splitter = CollectionSplitter()

    # Test basic splitting
    items = [1, {"a": 1}, 2, {"b": 2}]
    non_dicts, dicts = splitter.split_by_type(items)
    assert non_dicts == [1, 2]
    assert dicts == [{"a": 1}, {"b": 2}]

    # Test empty sequence
    non_dicts, dicts = splitter.split_by_type([])
    assert non_dicts == []
    assert dicts == []

    # Test all dicts
    non_dicts, dicts = splitter.split_by_type([{}, {}])
    assert non_dicts == []
    assert len(dicts) == 2


def test_split_by_predicate():
    """Test splitting by predicate."""
    splitter = CollectionSplitter()

    # Test even/odd splitting
    numbers = [1, 2, 3, 4, 5, 6]
    evens, odds = splitter.split_by_predicate(numbers, lambda x: x % 2 == 0)
    assert evens == [2, 4, 6]
    assert odds == [1, 3, 5]

    # Test empty sequence
    matching, non_matching = splitter.split_by_predicate([], bool)
    assert matching == []
    assert non_matching == []


def test_split_dict_by_type():
    """Test splitting dictionaries by value type."""
    splitter = CollectionSplitter()

    # Test basic splitting
    data = {"a": 1, "b": {"x": 2}, "c": 3, "d": {"y": 4}}
    simple, nested = splitter.split_dict_by_type(data)
    assert simple == {"a": 1, "c": 3}
    assert nested == {"b": {"x": 2}, "d": {"y": 4}}

    # Test empty dict
    simple, nested = splitter.split_dict_by_type({})
    assert simple == {}
    assert nested == {}
