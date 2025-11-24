"""Base serializer utilities."""

from __future__ import annotations

from datetime import date, datetime, time
from pathlib import Path
from typing import Any

from extended_data_types.serialization.types import convert_to_serializable


def _sanitize(data: Any) -> Any:
    """Convert special types to serializable primitives."""
    # Basic gate: reject unknown objects early
    if not isinstance(
        data,
        (
            dict,
            list,
            tuple,
            set,
            str,
            int,
            float,
            bool,
            type(None),
            Path,
            bytes,
            bytearray,
            datetime,
            date,
            time,
        ),
    ):
        raise TypeError(f"Unsupported type for serialization: {type(data)}")

    converted = convert_to_serializable(data)
    if converted is None:
        return None
    if isinstance(converted, Path):
        return str(converted)
    if isinstance(converted, datetime):
        return converted.date().isoformat()
    if isinstance(converted, (date, time)):
        return converted.isoformat()
    if isinstance(converted, (bytes, bytearray)):
        try:
            return converted.decode()
        except Exception:
            return str(converted)
    if isinstance(converted, set):
        return [_sanitize(v) for v in sorted(converted)]
    if isinstance(converted, list):
        return [_sanitize(v) for v in converted]
    if isinstance(converted, dict):
        return {k: _sanitize(v) for k, v in converted.items()}
    return converted

