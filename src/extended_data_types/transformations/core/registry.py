"""Transform registry functionality."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeVar

from typing import Any, Callable, TypeVar, cast, overload

from extended_data_types.core.conversion import TypeRegistry

from .transform import Transform


T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")


class TransformRegistry:
    """Registry for transform operations.

    Manages registration and lookup of transforms by type.
    """

    @staticmethod
    def register(
        transform: Transform[T, U], input_type: type[T], output_type: type[U]
    ) -> None:
        """Register a transform with the type registry.

        Args:
            transform: Transform to register
            input_type: Expected input type
            output_type: Expected output type
        """
        TypeRegistry.register_converter(
            input_type, output_type, transform, transform.validate  # type: ignore[arg-type]
        )

    @staticmethod
    @overload
    def create(
        func: Callable[[T], U], input_type: type[T], output_type: type[U], **kwargs: Any
    ) -> Transform[T, U]: ...

    @staticmethod
    @overload
    def create(
        func: Callable[[T, V], U], input_type: type[T], output_type: type[U], **kwargs: Any
    ) -> Transform[T, U]: ...

    @staticmethod
    def create(
        func: Callable[..., U], input_type: type[T], output_type: type[U], **kwargs: Any
    ) -> Transform[T, U]:
        """Create and register a new transform.

        Args:
            func: Function to transform into a Transform
            input_type: Expected input type
            output_type: Expected output type
            **kwargs: Additional configuration for the transform

        Returns:
            Registered transform
        """
        transform = Transform(func, name=func.__name__, description=func.__doc__)
        TransformRegistry.register(transform, input_type, output_type)  # type: ignore[arg-type]
        return transform

    @staticmethod
    def create(
        func: Callable[[T], U], input_type: type[T], output_type: type[U], **kwargs: Any
    ) -> Transform[T, U]:
        """Create and register a new transform.

        Args:
            func: Function to transform into a Transform
            input_type: Expected input type
            output_type: Expected output type
            **kwargs: Additional configuration for the transform

        Returns:
            Registered transform
        """
        transform = Transform(func, name=func.__name__, description=func.__doc__)
        TransformRegistry.register(transform, input_type, output_type)  # type: ignore[arg-type]
        return transform
