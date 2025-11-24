"""Compatibility shim for schema inspection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class SchemaValidator:
    """Placeholder validator."""

    schema: dict[str, Any] | None = None

    def validate(self, data: Any) -> bool:  # pragma: no cover
        return True


def get_schema(obj: Any | None = None) -> dict[str, Any]:
    """Return an empty schema placeholder."""
    return {}
