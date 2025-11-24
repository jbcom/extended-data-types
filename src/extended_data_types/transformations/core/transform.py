"""Base transformation functionality."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Generic, TypeVar


T = TypeVar("T")
U = TypeVar("U")
TransformFunc = Callable[[T], U]


class Transform(Generic[T, U]):
    """A transformation operation.

    Encapsulates a transformation function with optional validation and metadata.

    Attributes:
        func: The transformation function
        name: Name of the transformation
        description: Description of what the transformation does
        validate: Optional validation function
    """

    def __init__(
        self,
        func: TransformFunc[T, U],
        name: str | None = None,
        description: str | None = None,
        validate: Callable[[T], bool] | None = None,
    ):
        """Initialize a Transform.

        Args:
            func: The transformation function
            name: Optional name for the transform
            description: Optional description of the transform
            validate: Optional validation function
        """
        self.func = func
        self.name = name or func.__name__
        self.description = description or func.__doc__ or ""
        self.validate = validate

    def __call__(self, value: T) -> U:
        """Apply the transformation."""
        if self.validate and not self.validate(value):  # type: ignore[misc]
            raise ValueError(f"Invalid input for transform {self.name}")
        return self.func(value)  # type: ignore[misc]

    def pipe(self, other: Transform[U, Any]) -> Transform[T, Any]:
        """Chain this transform with another."""
        return Transform(
            lambda x: other(self(x)),
            name=f"{self.name} -> {other.name}",
            description=f"Pipe {self.description} into {other.description}",
        )
