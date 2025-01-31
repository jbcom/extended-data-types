"""Transform composition utilities."""

from __future__ import annotations

from typing import Any, TypeVar

from .chain import TransformChain
from .transform import Transform


T = TypeVar("T")


def pipe(value: T, *transforms: Transform[Any, Any]) -> Any:
    """Pipe a value through transforms.

    Args:
        value: The initial value
        *transforms: Transforms to apply

    Returns:
        The final transformed value
    """
    return TransformChain(transforms)(value)


def compose(*transforms: Transform[Any, Any]) -> Transform[Any, Any]:
    """Compose transforms into a single transform.

    Args:
        *transforms: Transforms to compose

    Returns:
        A single transform that applies all transforms in sequence
    """
    return Transform(lambda x: pipe(x, *transforms))
