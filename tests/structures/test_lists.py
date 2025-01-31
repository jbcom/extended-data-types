"""Tests for list manipulation utilities."""

from extended_data_types.structures.lists import ListHandler


def test_flatten():
    """Test list flattening."""
    handler = ListHandler()

    # Test basic flattening
    assert handler.flatten([1, [2, 3], [4, [5]]]) == [1, 2, 3, 4, 5]

    # Test empty lists
    assert handler.flatten([]) == []
    assert handler.flatten([[], []]) == []

    # Test mixed types
    assert handler.flatten([1, "a", [2, "b"]]) == [1, "a", 2, "b"]

    # Test with recursive disabled
    non_recursive = ListHandler(recursive=False)
    assert non_recursive.flatten([1, [2, [3]]]) == [1, [2, [3]]]


def test_filter_list():
    """Test list filtering."""
    handler = ListHandler()

    # Test allowlist
    assert handler.filter_list([1, 2, 3], allowlist=[1, 2]) == [1, 2]

    # Test denylist
    assert handler.filter_list([1, 2, 3], denylist=[2]) == [1, 3]

    # Test both lists
    assert handler.filter_list([1, 2, 3, 4], allowlist=[1, 2, 3], denylist=[2]) == [
        1,
        3,
    ]

    # Test empty lists
    assert handler.filter_list() == []
    assert handler.filter_list([1, 2, 3]) == [1, 2, 3]


def test_deduplicate():
    """Test list deduplication."""
    handler = ListHandler()

    # Test with order maintenance
    assert handler.deduplicate([1, 2, 2, 3, 1]) == [1, 2, 3]

    # Test without order maintenance
    no_order = ListHandler(maintain_order=False)
    assert no_order.deduplicate([3, 1, 2, 1, 2]) == [1, 2, 3]

    # Test empty list
    assert handler.deduplicate([]) == []
