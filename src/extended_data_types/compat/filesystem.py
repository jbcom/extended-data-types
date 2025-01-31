"""Backward compatibility layer for bob file utilities.

This module provides compatibility with bob's file_data_type utilities
while using the modern FileHandler internally.
"""

import os
from typing import TypeAlias

from git import Repo

from ..filesystem.operations import FileHandler

FilePath: TypeAlias = str | os.PathLike[str]

# Global handler instance for compatibility functions
_handler = FileHandler()


def get_parent_repository(
    file_path: FilePath | None = None,
    search_parent_directories: bool = True,
) -> Repo | None:
    """Maintains compatibility with bob.file_data_type.get_parent_repository."""
    return _handler.get_parent_repository(
        file_path,
        search_parent_directories
    )


def file_path_depth(file_path: FilePath) -> int:
    """Maintains compatibility with bob.file_data_type.file_path_depth."""
    return _handler.file_path_depth(file_path)


def file_path_rel_to_root(file_path: FilePath) -> str:
    """Maintains compatibility with bob.file_data_type.file_path_rel_to_root."""
    return _handler.file_path_rel_to_root(file_path) 