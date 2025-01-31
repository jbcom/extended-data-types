"""Tests for sequence operations."""

from __future__ import annotations

import pytest

from extended_data_types.transformations.collections.sequence import (
    chunk_sequence,
    interleave_sequences,
    partition_sequence,
    remove_duplicates,
    rotate_sequence,
    sliding_window,
)


def test_chunk_sequence() -> None:
    """Test sequence chunking."""
    # Test basic chunking
    assert list(chunk_sequence([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]
    assert list(chunk_sequence([1, 2, 3, 4], 2)) == [[1, 2], [3, 4]]

    # Test with different sizes
    assert list(chunk_sequence([1, 2, 3, 4, 5], 3)) == [[1, 2, 3], [4, 5]]
    assert list(chunk_sequence([1, 2, 3, 4, 5], 1)) == [[1], [2], [3], [4], [5]]
    assert list(chunk_sequence([1, 2, 3], 5)) == [[1, 2, 3]]

    # Test with fill value
    assert list(chunk_sequence([1, 2, 3, 4, 5], 2, fill=0)) == [[1, 2], [3, 4], [5, 0]]
    assert list(chunk_sequence([1, 2, 3], 2, fill=None)) == [[1, 2], [3, None]]

    # Test with empty sequence
    assert list(chunk_sequence([], 2)) == []

    # Test invalid chunk size
    with pytest.raises(ValueError):
        list(chunk_sequence([1, 2, 3], 0))
    with pytest.raises(ValueError):
        list(chunk_sequence([1, 2, 3], -1))


def test_rotate_sequence() -> None:
    """Test sequence rotation."""
    # Test positive rotation
    assert rotate_sequence([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]
    assert rotate_sequence([1, 2, 3], 1) == [3, 1, 2]

    # Test negative rotation
    assert rotate_sequence([1, 2, 3, 4, 5], -2) == [3, 4, 5, 1, 2]
    assert rotate_sequence([1, 2, 3], -1) == [2, 3, 1]

    # Test rotation larger than sequence length
    assert rotate_sequence([1, 2, 3], 5) == [2, 3, 1]  # Same as rotating by 2
    assert rotate_sequence([1, 2, 3], -5) == [2, 3, 1]  # Same as rotating by -2

    # Test with empty sequence
    assert rotate_sequence([], 2) == []

    # Test with single element
    assert rotate_sequence([1], 5) == [1]


def test_interleave_sequences() -> None:
    """Test sequence interleaving."""
    # Test basic interleaving
    assert list(interleave_sequences([1, 2, 3], [4, 5, 6])) == [1, 4, 2, 5, 3, 6]

    # Test with sequences of different lengths
    assert list(interleave_sequences([1, 2, 3], [4, 5])) == [1, 4, 2, 5, 3]
    assert list(interleave_sequences([1, 2], [3, 4, 5])) == [1, 3, 2, 4, 5]

    # Test with multiple sequences
    assert list(interleave_sequences([1, 2], [3, 4], [5, 6])) == [1, 3, 5, 2, 4, 6]

    # Test with empty sequences
    assert list(interleave_sequences([], [1, 2])) == [1, 2]
    assert list(interleave_sequences([1, 2], [])) == [1, 2]
    assert list(interleave_sequences([], [])) == []

    # Test with single sequence
    assert list(interleave_sequences([1, 2, 3])) == [1, 2, 3]


def test_partition_sequence() -> None:
    """Test sequence partitioning."""
    # Test basic partitioning
    assert partition_sequence([1, 2, 3, 4], lambda x: x % 2 == 0) == ([2, 4], [1, 3])
    assert partition_sequence([1, 2, 3], lambda x: x > 2) == ([3], [1, 2])

    # Test with all elements matching
    assert partition_sequence([2, 4, 6], lambda x: x % 2 == 0) == ([2, 4, 6], [])
    assert partition_sequence([1, 3, 5], lambda x: x % 2 == 0) == ([], [1, 3, 5])

    # Test with empty sequence
    assert partition_sequence([], lambda x: x > 0) == ([], [])

    # Test with custom key function
    assert partition_sequence(["a", "bb", "ccc"], lambda x: len(x) > 1) == (
        ["bb", "ccc"],
        ["a"],
    )


def test_sliding_window() -> None:
    """Test sliding window."""
    # Test basic sliding window
    assert list(sliding_window([1, 2, 3, 4], 2)) == [(1, 2), (2, 3), (3, 4)]
    assert list(sliding_window([1, 2, 3], 3)) == [(1, 2, 3)]

    # Test with step size
    assert list(sliding_window([1, 2, 3, 4], 2, step=2)) == [(1, 2), (3, 4)]
    assert list(sliding_window([1, 2, 3, 4, 5], 2, step=2)) == [(1, 2), (3, 4), (5,)]

    # Test with window size larger than sequence
    assert list(sliding_window([1, 2], 3)) == []

    # Test with empty sequence
    assert list(sliding_window([], 2)) == []

    # Test invalid window size or step
    with pytest.raises(ValueError):
        list(sliding_window([1, 2, 3], 0))
    with pytest.raises(ValueError):
        list(sliding_window([1, 2, 3], 2, step=0))


def test_remove_duplicates() -> None:
    """Test duplicate removal."""
    # Test basic duplicate removal
    assert remove_duplicates([1, 2, 2, 3, 3, 3]) == [1, 2, 3]
    assert remove_duplicates([1, 1, 1]) == [1]

    # Test with key function
    assert remove_duplicates(["a", "A", "b", "B"], key=str.lower) == ["a", "b"]

    # Test with custom comparison
    assert remove_duplicates([(1, 2), (2, 1)], key=lambda x: tuple(sorted(x))) == [
        (1, 2)
    ]

    # Test order preservation
    assert remove_duplicates([3, 2, 1, 2, 3]) == [3, 2, 1]

    # Test with empty sequence
    assert remove_duplicates([]) == []

    # Test with all unique elements
    assert remove_duplicates([1, 2, 3]) == [1, 2, 3]
