"""Compatibility shim for structure inspection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class StructureInfo:
    """Placeholder structure info."""

    data: Any | None = None


def inspect_structure(obj: Any) -> StructureInfo:
    """Return minimal structure information."""
    return StructureInfo(data=obj)
