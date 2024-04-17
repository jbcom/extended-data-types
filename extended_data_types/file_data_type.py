"""This module provides utilities for handling file paths and extensions.

It includes functions to check file extensions, determine encoding types based on
file extensions, calculate file path depths, and find relative paths to the root
directory.
"""  # noqa: E501

from __future__ import annotations, division, print_function, unicode_literals

import os
from pathlib import Path
from typing import List, Optional, Union

# FilePath is a type alias for file path representations.
FilePath = Union[str, os.PathLike[str]]


def match_file_extensions(
        p: FilePath,
        allowed_extensions: Optional[List[str]],
        denied_extensions: Optional[List[str]] = None,
) -> bool:
    """Checks if the file extension matches the allowed or denied extensions.

    Args:
        p (FilePath): The file path to check.
        allowed_extensions (Optional[List[str]]): List of allowed extensions.
        denied_extensions (Optional[List[str]]): List of denied extensions.

    Returns:
        bool: True if the file extension is allowed and not denied, False otherwise.
    """
    if allowed_extensions is None:
        allowed_extensions = []

    if denied_extensions is None:
        denied_extensions = []

    allowed_extensions = [ext.removeprefix(".") for ext in allowed_extensions]
    denied_extensions = [ext.removeprefix(".") for ext in denied_extensions]

    p = Path(str(p))
    if p.name.startswith("."):
        suffix = p.name.removeprefix(".")
    else:
        suffix = p.suffix.removeprefix(".")

    if (
            len(allowed_extensions) > 0 and suffix not in allowed_extensions
    ) or suffix in denied_extensions:
        return False

    return True


def get_encoding_for_file_path(file_path: FilePath) -> str:
    """Returns the encoding type based on the file extension.

    Args:
        file_path (FilePath): The file path to check.

    Returns:
        str: The encoding type ('yaml', 'json', or 'raw').
    """
    file_path = Path(str(file_path))
    suffix = file_path.suffix
    if suffix in [".yaml", ".yml"]:
        return "yaml"
    elif suffix in [".json"]:
        return "json"
    return "raw"


def file_path_depth(file_path: FilePath) -> int:
    """Calculates the depth of the file path.

    Args:
        file_path (FilePath): The file path to measure.

    Returns:
        int: The depth of the file path.
    """
    depth = [p for p in Path(str(file_path)).parts if p != "."]
    return len(depth)


def file_path_rel_to_root(file_path: FilePath) -> str:
    """Calculates the relative path to the root from the given file path.

    Args:
        file_path (FilePath): The file path to calculate from.

    Returns:
        str: The relative path to the root.
    """
    depth = file_path_depth(file_path)
    path_rel_to_root = [".."] * depth
    return "/".join(path_rel_to_root)
