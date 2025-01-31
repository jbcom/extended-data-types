"""Set operations for collections."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from typing import Any, TypeVar

from ..core import Transform

T = TypeVar('T')


def union(*sequences: Sequence[T]) -> list[T]:
    """Combine sequences, removing duplicates.
    
    Args:
        *sequences: Sequences to combine
        
    Returns:
        Combined list without duplicates
        
    Example:
        >>> union([1, 2], [2, 3], [3, 4])
        [1, 2, 3, 4]
    """
    return list(set().union(*map(set, sequences)))


def intersection(*sequences: Sequence[T]) -> list[T]:
    """Get common elements from sequences.
    
    Args:
        *sequences: Sequences to intersect
        
    Returns:
        List of common elements
        
    Example:
        >>> intersection([1, 2, 3], [2, 3, 4], [3, 4, 5])
        [3]
    """
    if not sequences:
        return []
    return list(set(sequences[0]).intersection(*map(set, sequences[1:])))


def difference(
    sequence: Sequence[T],
    *others: Sequence[T]
) -> list[T]:
    """Get elements in first sequence but not in others.
    
    Args:
        sequence: Base sequence
        *others: Sequences to subtract
        
    Returns:
        List of remaining elements
        
    Example:
        >>> difference([1, 2, 3], [2], [3])
        [1]
    """
    return list(set(sequence).difference(*map(set, others)))


def symmetric_difference(
    sequence1: Sequence[T],
    sequence2: Sequence[T]
) -> list[T]:
    """Get elements in either sequence but not both.
    
    Args:
        sequence1: First sequence
        sequence2: Second sequence
        
    Returns:
        List of non-common elements
        
    Example:
        >>> symmetric_difference([1, 2, 3], [2, 3, 4])
        [1, 4]
    """
    return list(set(sequence1).symmetric_difference(sequence2))


def is_subset(
    sequence1: Sequence[T],
    sequence2: Sequence[T]
) -> bool:
    """Check if first sequence is subset of second.
    
    Args:
        sequence1: Potential subset
        sequence2: Potential superset
        
    Returns:
        True if sequence1 is subset of sequence2
        
    Example:
        >>> is_subset([1, 2], [1, 2, 3])
        True
    """
    return set(sequence1).issubset(sequence2)


def is_superset(
    sequence1: Sequence[T],
    sequence2: Sequence[T]
) -> bool:
    """Check if first sequence is superset of second.
    
    Args:
        sequence1: Potential superset
        sequence2: Potential subset
        
    Returns:
        True if sequence1 is superset of sequence2
        
    Example:
        >>> is_superset([1, 2, 3], [1, 2])
        True
    """
    return set(sequence1).issuperset(sequence2)


# Register transforms
union_transform = Transform(union)
intersection_transform = Transform(intersection)
difference_transform = Transform(difference)
symmetric_difference_transform = Transform(symmetric_difference)
is_subset_transform = Transform(is_subset)
is_superset_transform = Transform(is_superset) 