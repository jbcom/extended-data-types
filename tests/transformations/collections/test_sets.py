"""Tests for set operations."""

from __future__ import annotations

import pytest

from extended_data_types.transformations.collections.sets import (
    find_difference, find_intersection, find_symmetric_difference, find_union,
    is_subset, is_superset)


def test_find_intersection() -> None:
    """Test set intersection."""
    # Test basic intersection
    assert find_intersection({1, 2, 3}, {2, 3, 4}) == {2, 3}
    assert find_intersection({1, 2}, {3, 4}) == set()
    
    # Test with multiple sets
    assert find_intersection({1, 2, 3}, {2, 3, 4}, {3, 4, 5}) == {3}
    
    # Test with empty sets
    assert find_intersection(set(), {1, 2, 3}) == set()
    assert find_intersection({1, 2, 3}, set()) == set()
    
    # Test with identical sets
    assert find_intersection({1, 2, 3}, {1, 2, 3}) == {1, 2, 3}
    
    # Test with single set
    assert find_intersection({1, 2, 3}) == {1, 2, 3}
    
    # Test with no sets
    assert find_intersection() == set()


def test_find_difference() -> None:
    """Test set difference."""
    # Test basic difference
    assert find_difference({1, 2, 3}, {2, 3, 4}) == {1}
    assert find_difference({1, 2}, {3, 4}) == {1, 2}
    
    # Test with multiple sets
    assert find_difference({1, 2, 3, 4}, {2, 3}, {3, 4}) == {1}
    
    # Test with empty sets
    assert find_difference(set(), {1, 2, 3}) == set()
    assert find_difference({1, 2, 3}, set()) == {1, 2, 3}
    
    # Test with identical sets
    assert find_difference({1, 2, 3}, {1, 2, 3}) == set()
    
    # Test with single set
    assert find_difference({1, 2, 3}) == {1, 2, 3}


def test_find_union() -> None:
    """Test set union."""
    # Test basic union
    assert find_union({1, 2}, {3, 4}) == {1, 2, 3, 4}
    assert find_union({1, 2}, {2, 3}) == {1, 2, 3}
    
    # Test with multiple sets
    assert find_union({1, 2}, {2, 3}, {3, 4}) == {1, 2, 3, 4}
    
    # Test with empty sets
    assert find_union(set(), {1, 2, 3}) == {1, 2, 3}
    assert find_union({1, 2, 3}, set()) == {1, 2, 3}
    
    # Test with identical sets
    assert find_union({1, 2, 3}, {1, 2, 3}) == {1, 2, 3}
    
    # Test with single set
    assert find_union({1, 2, 3}) == {1, 2, 3}
    
    # Test with no sets
    assert find_union() == set()


def test_find_symmetric_difference() -> None:
    """Test symmetric difference."""
    # Test basic symmetric difference
    assert find_symmetric_difference({1, 2, 3}, {2, 3, 4}) == {1, 4}
    assert find_symmetric_difference({1, 2}, {3, 4}) == {1, 2, 3, 4}
    
    # Test with multiple sets
    assert find_symmetric_difference({1, 2}, {2, 3}, {3, 4}) == {1, 4}
    
    # Test with empty sets
    assert find_symmetric_difference(set(), {1, 2, 3}) == {1, 2, 3}
    assert find_symmetric_difference({1, 2, 3}, set()) == {1, 2, 3}
    
    # Test with identical sets
    assert find_symmetric_difference({1, 2, 3}, {1, 2, 3}) == set()
    
    # Test with single set
    assert find_symmetric_difference({1, 2, 3}) == {1, 2, 3}


def test_is_subset() -> None:
    """Test subset checking."""
    # Test basic subset
    assert is_subset({1, 2}, {1, 2, 3}) is True
    assert is_subset({1, 4}, {1, 2, 3}) is False
    
    # Test with equal sets
    assert is_subset({1, 2, 3}, {1, 2, 3}) is True
    
    # Test with empty sets
    assert is_subset(set(), {1, 2, 3}) is True
    assert is_subset({1, 2, 3}, set()) is False
    assert is_subset(set(), set()) is True
    
    # Test proper subset
    assert is_subset({1, 2}, {1, 2, 3}, proper=True) is True
    assert is_subset({1, 2, 3}, {1, 2, 3}, proper=True) is False
    
    # Test with multiple supersets
    assert is_subset({1}, {1, 2}, {1, 2, 3}) is True
    assert is_subset({1, 4}, {1, 2}, {1, 2, 3}) is False


def test_is_superset() -> None:
    """Test superset checking."""
    # Test basic superset
    assert is_superset({1, 2, 3}, {1, 2}) is True
    assert is_superset({1, 2, 3}, {1, 4}) is False
    
    # Test with equal sets
    assert is_superset({1, 2, 3}, {1, 2, 3}) is True
    
    # Test with empty sets
    assert is_superset({1, 2, 3}, set()) is True
    assert is_superset(set(), {1, 2, 3}) is False
    assert is_superset(set(), set()) is True
    
    # Test proper superset
    assert is_superset({1, 2, 3}, {1, 2}, proper=True) is True
    assert is_superset({1, 2, 3}, {1, 2, 3}, proper=True) is False
    
    # Test with multiple subsets
    assert is_superset({1, 2, 3}, {1}, {1, 2}) is True
    assert is_superset({1, 2, 3}, {1, 4}, {1, 2}) is False 