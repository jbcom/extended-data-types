"""Compatibility shim for type inspection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class TypeInfo:
    """Placeholder type info."""

    obj: Any | None = None


def get_type_info(obj: Any) -> TypeInfo:
    """Return minimal type info."""
    return TypeInfo(obj=obj)
