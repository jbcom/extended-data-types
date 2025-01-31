"""Core transformation functionality.

This module provides the foundation for all transformations:
- Transform class for encapsulating transformations
- TransformChain for composing transforms
- Registry for managing transforms
- Utilities for parallel processing and composition
"""

from .chain import TransformChain
from .composition import compose, pipe
from .conditional import transform_all, transform_any, transform_if
from .parallel import batch_transform, parallel_transform
from .transform import Transform, TransformFunc
from .validation import fallback, optional, validate_type


__all__ = [
    # Base classes
    "Transform",
    "TransformChain",
    # Type hints
    "TransformFunc",
    # Composition
    "compose",
    "pipe",
    # Parallel processing
    "batch_transform",
    "parallel_transform",
    # Conditional execution
    "transform_if",
    "transform_all",
    "transform_any",
    # Validation
    "validate_type",
    "optional",
    "fallback",
]
