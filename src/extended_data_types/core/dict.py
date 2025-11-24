"""Dictionary wrapper for backward compatibility."""

from __future__ import annotations

from typing import Any

from .base import ExtendedBase


class ExtendedDict(ExtendedBase, dict[Any, Any]):
    """Legacy ExtendedDict placeholder."""

