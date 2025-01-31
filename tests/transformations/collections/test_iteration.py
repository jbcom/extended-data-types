"""Tests for iteration operations."""

from __future__ import annotations

import pytest

from extended_data_types.transformations.collections.iteration import (
    chain_iterators, consume_iterator, cycle_iterator, peek_iterator,
    skip_iterator, take_iterator)


def test_consume_iterator() -> None:
    """Test iterator consumption."""
    # Test basic consumption
    it = iter([1, 2, 3])
    consume_iterator(it)
    assert list(it) == []  # Iterator should be empty
    
    # Test partial consumption
    it = iter([1, 2, 3, 4, 5])
    consume_iterator(it, n=3)
    assert list(it) == [4, 5]
    
    # Test with n larger than iterator length
    it = iter([1, 2])
    consume_iterator(it, n=5)
    assert list(it) == []
    
    # Test with empty iterator
    it = iter([])
    consume_iterator(it)
    assert list(it) == []
    
    # Test invalid n
    with pytest.raises(ValueError):
        consume_iterator(iter([1, 2]), n=-1)


def test_peek_iterator() -> None:
    """Test iterator peeking."""
    # Test basic peeking
    it = iter([1, 2, 3])
    value = peek_iterator(it)
    assert value == 1
    assert list(it) == [1, 2, 3]  # Iterator should be unchanged
    
    # Test peeking with n items
    it = iter([1, 2, 3, 4])
    values = peek_iterator(it, n=2)
    assert values == [1, 2]
    assert list(it) == [1, 2, 3, 4]
    
    # Test peeking empty iterator
    it = iter([])
    assert peek_iterator(it) is None
    
    # Test peeking with n larger than iterator
    it = iter([1, 2])
    assert peek_iterator(it, n=5) == [1, 2]
    
    # Test invalid n
    with pytest.raises(ValueError):
        peek_iterator(iter([1, 2]), n=-1)


def test_take_iterator() -> None:
    """Test taking from iterator."""
    # Test basic taking
    it = iter([1, 2, 3, 4, 5])
    assert list(take_iterator(it, 3)) == [1, 2, 3]
    assert list(it) == [4, 5]  # Remaining items
    
    # Test taking more than available
    it = iter([1, 2, 3])
    assert list(take_iterator(it, 5)) == [1, 2, 3]
    
    # Test taking zero items
    it = iter([1, 2, 3])
    assert list(take_iterator(it, 0)) == []
    assert list(it) == [1, 2, 3]  # Iterator should be unchanged
    
    # Test taking from empty iterator
    it = iter([])
    assert list(take_iterator(it, 3)) == []
    
    # Test invalid n
    with pytest.raises(ValueError):
        list(take_iterator(iter([1, 2]), -1))


def test_skip_iterator() -> None:
    """Test skipping iterator items."""
    # Test basic skipping
    it = iter([1, 2, 3, 4, 5])
    skip_iterator(it, 2)
    assert list(it) == [3, 4, 5]
    
    # Test skipping more than available
    it = iter([1, 2, 3])
    skip_iterator(it, 5)
    assert list(it) == []
    
    # Test skipping zero items
    it = iter([1, 2, 3])
    skip_iterator(it, 0)
    assert list(it) == [1, 2, 3]
    
    # Test skipping from empty iterator
    it = iter([])
    skip_iterator(it, 3)
    assert list(it) == []
    
    # Test invalid n
    with pytest.raises(ValueError):
        skip_iterator(iter([1, 2]), -1)


def test_chain_iterators() -> None:
    """Test iterator chaining."""
    # Test basic chaining
    it1 = iter([1, 2])
    it2 = iter([3, 4])
    assert list(chain_iterators(it1, it2)) == [1, 2, 3, 4]
    
    # Test with empty iterators
    it1 = iter([])
    it2 = iter([1, 2])
    it3 = iter([])
    it4 = iter([3, 4])
    assert list(chain_iterators(it1, it2, it3, it4)) == [1, 2, 3, 4]
    
    # Test with single iterator
    it = iter([1, 2, 3])
    assert list(chain_iterators(it)) == [1, 2, 3]
    
    # Test with no iterators
    assert list(chain_iterators()) == []


def test_cycle_iterator() -> None:
    """Test iterator cycling."""
    # Test basic cycling
    it = cycle_iterator([1, 2, 3])
    assert next(it) == 1
    assert next(it) == 2
    assert next(it) == 3
    assert next(it) == 1  # Back to start
    assert next(it) == 2
    
    # Test with n cycles
    it = cycle_iterator([1, 2], n=2)
    assert list(it) == [1, 2, 1, 2]
    
    # Test with empty sequence
    it = cycle_iterator([])
    with pytest.raises(StopIteration):
        next(it)
    
    # Test with single item
    it = cycle_iterator([1], n=3)
    assert list(it) == [1, 1, 1]
    
    # Test invalid n
    with pytest.raises(ValueError):
        cycle_iterator([1, 2], n=-1) 