"""Type definitions for I/O operations.

This module provides type aliases and custom types used across the I/O package
for file paths, encodings, and other I/O-related operations.
"""

from __future__ import annotations

import os
from typing import Literal, TypeAlias, Union

FilePath: TypeAlias = Union[str, os.PathLike[str]]
"""Type alias for file paths that can be represented as strings or os.PathLike objects."""

EncodingType = Literal["yaml", "json", "toml", "hcl", "raw"]
"""Valid encoding types for file content.""" 