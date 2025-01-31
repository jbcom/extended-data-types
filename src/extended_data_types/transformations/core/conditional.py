"""Conditional transformation utilities."""

from __future__ import annotations

from typing import Any, Callable, Sequence, TypeVar

from .transform import Transform

T = TypeVar('T')
U = TypeVar('U')


def transform_if(
    condition: bool | Callable[[T], bool],
    func: Transform[T, U]
) -> Transform[T, U | T]:
    """Create a conditional transform.

    Args:
        condition: Boolean or predicate function
        func: Transform to apply conditionally

    Returns:
        Transform that only applies if condition is met
    """
    def conditional(value: T) -> U | T:
        should_transform = condition(value) if callable(condition) else condition
        return func(value) if should_transform else value
    return Transform(conditional)


def transform_any(
    transforms: Sequence[Transform[T, U]]
) -> Transform[T, U | None]:
    """Apply transforms until one succeeds.

    Args:
        transforms: Sequence of transforms to try

    Returns:
        Transform that returns first successful result or None
    """
    def try_all(value: T) -> U | None:
        for t in transforms:
            try:
                return t(value)
            except Exception:
                continue
        return None
    return Transform(try_all)


def transform_all(
    transforms: Sequence[Transform[T, Any]]
) -> Transform[T, list[Any]]:
    """Apply all transforms and collect results.

    Args:
        transforms: Sequence of transforms to apply

    Returns:
        Transform that applies all transforms and returns results
    """
    return Transform(lambda x: [t(x) for t in transforms]) 