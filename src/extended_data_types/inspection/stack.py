"""Stack inspection utilities with enhanced validation.

This module provides type-safe stack inspection capabilities with
comprehensive validation for method and class introspection.

Typical usage:
    >>> from extended_data_types.inspection.stack import StackInspector
    >>> inspector = StackInspector()
    >>> caller = inspector.get_caller_name()
"""

import inspect
import re
import sys

from typing import Any, TypeVar

import attrs

from pydantic import BaseModel


T = TypeVar("T")


class MethodInfo(BaseModel):
    """Information about a method.

    Attributes:
        name: Method name
        doc: Method docstring
        signature: Method signature
        is_public: Whether method is public
    """

    name: str
    doc: str | None = None
    signature: inspect.Signature | None = None
    is_public: bool = True

    model_config = {
        "arbitrary_types_allowed": True,
    }


@attrs.define
class StackInspector:
    """Handles stack inspection with validation.

    Attributes:
        skip_private: Whether to skip private methods
        include_docs: Whether to include docstrings
        include_signatures: Whether to include method signatures
    """

    skip_private: bool = True
    include_docs: bool = True
    include_signatures: bool = True

    def get_caller_name(self, depth: int = 2) -> str:
        """Get the name of the calling function.

        Args:
            depth: How many frames up to look

        Returns:
            Name of calling function

        Example:
            >>> inspector = StackInspector()
            >>> caller = inspector.get_caller_name()
        """
        frame = inspect.currentframe()
        try:
            for _ in range(depth):
                if frame is None:
                    return ""
                frame = frame.f_back

            if frame is None:
                return ""

            return frame.f_code.co_name
        finally:
            del frame

    def get_available_methods(
        self,
        obj: Any,
        pattern: str | None = None,
    ) -> dict[str, MethodInfo]:
        """Get available methods of an object.

        Args:
            obj: Object to inspect
            pattern: Optional regex pattern to filter methods

        Returns:
            Dictionary of method names to info

        Example:
            >>> inspector = StackInspector()
            >>> methods = inspector.get_available_methods(obj)
        """
        methods = {}

        for name, method in inspect.getmembers(obj, inspect.ismethod):
            # Skip private methods if configured
            if self.skip_private and name.startswith("_"):
                continue

            # Apply pattern filter if provided
            if pattern and not re.search(pattern, name):
                continue

            info = MethodInfo(
                name=name,
                doc=method.__doc__ if self.include_docs else None,
                signature=(
                    inspect.signature(method) if self.include_signatures else None
                ),
                is_public=not name.startswith("_"),
            )

            methods[name] = info

        return methods

    def current_python_version_is_at_least(
        self,
        minor: int,
        major: int = 3,
    ) -> bool:
        """Check if current Python version meets minimum.

        Args:
            minor: Minimum minor version
            major: Minimum major version

        Returns:
            Whether current version meets minimum

        Example:
            >>> inspector = StackInspector()
            >>> is_valid = inspector.current_python_version_is_at_least(10)
        """
        return sys.version_info.major > major or (
            sys.version_info.major == major and sys.version_info.minor >= minor
        )
