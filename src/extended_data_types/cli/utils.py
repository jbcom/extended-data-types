"""Utility helpers for CLI compatibility."""

from __future__ import annotations

from typing import Any


def convert_format(data: Any, from_format: str | None = None, to_format: str | None = None) -> Any:
    """Placeholder no-op format converter for compatibility."""
    return data


def validate_schema(data: Any, schema: Any | None = None) -> bool:
    """Placeholder schema validator for compatibility."""
    return True
