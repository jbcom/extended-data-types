"""Core utilities for extended data types.

This module provides fundamental utilities for type handling, pattern matching,
and runtime inspection.
"""

from __future__ import annotations

from .exceptions import ConversionError, SerializationError
from .inspection import (get_available_methods, get_caller,
                         get_inputs_from_docstring, get_unique_signature,
                         is_python_version_at_least, update_docstring)
from .patterns import (DATE_PATTERN, DATETIME_PATTERN, FALSY_PATTERN,
                       NUMBER_PATTERN, PATH_PATTERN, TIME_PATTERN,
                       TRUTHY_PATTERN)
from .types import (coerce_to_type, convert_special_type,
                    reconstruct_special_type, reconstruct_special_types,
                    strtobool, strtodate, strtodatetime, strtofloat, strtoint,
                    strtopath, strtotime, typeof, unwrap_object)

__all__ = [
    # Exceptions
    'ConversionError',
    'SerializationError',
    # Inspection
    'get_caller',
    'get_unique_signature',
    'get_available_methods',
    'get_inputs_from_docstring',
    'update_docstring',
    'is_python_version_at_least',
    # Patterns
    'DATE_PATTERN',
    'DATETIME_PATTERN',
    'TIME_PATTERN',
    'PATH_PATTERN',
    'NUMBER_PATTERN',
    'TRUTHY_PATTERN',
    'FALSY_PATTERN',
    # Types
    'typeof',
    'unwrap_object',
    'strtodate',
    'strtodatetime',
    'strtotime',
    'strtopath',
    'strtobool',
    'strtofloat',
    'strtoint',
    'convert_special_type',
    'coerce_to_type',
    'reconstruct_special_type',
    'reconstruct_special_types',
] 