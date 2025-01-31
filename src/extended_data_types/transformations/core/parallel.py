"""Parallel transformation utilities."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Any, Sequence, TypeVar

from .transform import Transform

T = TypeVar('T')
U = TypeVar('U')


def batch_transform(
    values: Sequence[T],
    transform: Transform[T, U],
    max_workers: int | None = None
) -> list[U]:
    """Transform multiple values in parallel.

    Args:
        values: Sequence of values to transform
        transform: Transform to apply
        max_workers: Maximum number of parallel workers

    Returns:
        List of transformed values
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(transform, values))


def parallel_transform(
    value: T,
    transforms: Sequence[Transform[T, Any]],
    max_workers: int | None = None
) -> list[Any]:
    """Apply transforms in parallel.

    Args:
        value: Value to transform
        transforms: Transforms to apply
        max_workers: Maximum number of parallel workers

    Returns:
        List of transformed values
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(lambda t: t(value), transforms)) 