"""Backward compatibility layer for bob stack utilities.

This module provides compatibility with bob's stack_utils while using
the modern StackInspector internally.
"""

from typing import Any

from ..inspection.stack import StackInspector


# Global inspector instance for compatibility functions
_inspector = StackInspector()


def get_caller_name(depth: int = 2) -> str:
    """Maintains compatibility with bob.stack_utils.get_caller_name."""
    return _inspector.get_caller_name(depth)


def get_available_methods(
    obj: Any,
    pattern: str | None = None,
) -> dict[str, Any]:
    """Maintains compatibility with bob.stack_utils.get_available_methods."""
    methods = _inspector.get_available_methods(obj, pattern)
    # Convert to old format for compatibility
    return {
        name: {
            "doc": info.doc,
            "signature": info.signature,
            "is_public": info.is_public,
        }
        for name, info in methods.items()
    }


def current_python_version_is_at_least(
    minor: int,
    major: int = 3,
) -> bool:
    """Maintains compatibility with bob.stack_utils.current_python_version_is_at_least."""
    return _inspector.current_python_version_is_at_least(minor, major)
