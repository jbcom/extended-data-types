"""Transform chain functionality."""

from __future__ import annotations

from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor
from functools import reduce
from typing import Any, Generic, TypeVar

from .transform import Transform


T = TypeVar("T")


class TransformChain(Generic[T]):
    """A chain of transformations.

    Executes multiple transforms in sequence or parallel.

    Attributes:
        transforms: List of transforms to apply
        parallel: Whether to run transforms in parallel
        max_workers: Maximum number of parallel workers
    """

    def __init__(
        self,
        transforms: Sequence[Transform[Any, Any]] | None = None,
        parallel: bool = False,
        max_workers: int | None = None,
    ):
        """Initialize a TransformChain.

        Args:
            transforms: Optional sequence of transforms
            parallel: Whether to run transforms in parallel
            max_workers: Maximum number of parallel workers
        """
        self.transforms = list(transforms or [])
        self.parallel = parallel
        self.max_workers = max_workers

    def add(self, transform: Transform[Any, Any]) -> TransformChain[T]:
        """Add a transform to the chain."""
        self.transforms.append(transform)
        return self

    def __call__(self, value: T) -> Any:
        """Apply all transforms in the chain."""
        if not self.transforms:
            return value

        if not self.parallel:
            return reduce(lambda v, t: t(v), self.transforms, value)

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            return list(executor.map(lambda t: t(value), self.transforms))
