"""List wrapper for backward compatibility."""

from __future__ import annotations

from typing import Any

from .base import ExtendedBase


class ExtendedList(ExtendedBase, list[Any]):
    """Legacy ExtendedList placeholder."""

    pass
