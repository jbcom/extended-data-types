"""Set wrappers for backward compatibility."""

from __future__ import annotations

from typing import Any

from .base import ExtendedBase


class ExtendedSet(ExtendedBase, set[Any]):
    """Legacy ExtendedSet placeholder."""



class ExtendedFrozenSet(ExtendedBase, frozenset[Any]):
    """Legacy ExtendedFrozenSet placeholder."""

