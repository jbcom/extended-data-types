"""Serialization type utilities.

This module provides utilities for converting Python objects to and from serializable forms,
building on top of the core type conversion utilities.
"""

from __future__ import annotations

import json

from collections.abc import Mapping
from typing import Any, Protocol

from extended_data_types.core.exceptions import ConversionError
from extended_data_types.core.types import (
    strtobool,
    strtodate,
    strtodatetime,
    strtofloat,
    strtoint,
    strtopath,
    strtotime,
    unwrap_object,
)
from extended_data_types.serialization.detection import is_potential_json


def encode_json(obj: Any, **kwargs: Any) -> str:
    return json.dumps(obj, **kwargs)


def decode_json(data: str) -> Any:
    return json.loads(data)


class SerializerProtocol(Protocol):
    """Minimal serializer protocol."""

    def encode(self, data: Any, **kwargs: Any) -> str: ...
    def decode(self, data: str, **kwargs: Any) -> Any: ...


def convert_to_serializable(obj: Any) -> Any:
    """Convert an object to a serializable form.

    Uses core type conversion utilities to convert special types to their
    serializable string representations.

    Args:
        obj: Object to convert

    Returns:
        Any: Serializable form of the object

    Examples:
        >>> convert_to_serializable(datetime.date(2023, 1, 1))
        '2023-01-01'
        >>> convert_to_serializable({'path': Path('/tmp')})
        {'path': '/tmp'}
    """
    # Use core unwrap_object utility which handles all special types
    return unwrap_object(obj)


def reconstruct_from_serialized(obj: Any, fail_silently: bool = False) -> Any:
    """Reconstruct an object from its serialized form.

    Uses core type conversion utilities to detect and convert strings back
    to their original Python types.

    Args:
        obj: Serialized object to reconstruct
        fail_silently: Whether to return original value on conversion failure

    Returns:
        Any: Reconstructed object with proper Python types

    Examples:
        >>> reconstruct_from_serialized('2023-01-01')
        datetime.date(2023, 1, 1)
        >>> reconstruct_from_serialized({'path': '/tmp'})
        {'path': Path('/tmp')}
    """
    if isinstance(obj, str):
        try:
            # Use core type conversion utilities
            for converter in [
                strtodate,
                strtodatetime,
                strtotime,
                strtopath,
                strtobool,
                strtofloat,
                strtoint,
            ]:
                try:
                    return converter(obj)
                except ValueError:
                    continue

            # Check for JSON/YAML content using core patterns
            if is_potential_json(obj):
                return json.loads(obj)

        except (ValueError, TypeError) as exc:
            if not fail_silently:
                raise ConversionError(type(obj), obj) from exc

        return obj

    if isinstance(obj, Mapping):
        return {
            k: reconstruct_from_serialized(v, fail_silently) for k, v in obj.items()
        }
    if isinstance(obj, (list, set)):
        return type(obj)(reconstruct_from_serialized(v, fail_silently) for v in obj)
    return obj
