"""Compatibility layer for legacy Extended Data Types APIs.

This module provides backward compatibility shims for the v4/v5 API,
allowing existing code to work with the new v6 architecture.
"""

from .legacy import convert_legacy_format, flatten_map, unflatten_map
from .version import check_compatibility


__all__ = [
    "check_compatibility",
    "convert_legacy_format",
    "flatten_map",
    "unflatten_map",
]
