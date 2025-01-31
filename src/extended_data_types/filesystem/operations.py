"""File system operations with enhanced validation.

This module provides type-safe file system operations with comprehensive
validation and Git repository handling.

Typical usage:
    >>> from extended_data_types.filesystem.operations import FileHandler
    >>> handler = FileHandler()
    >>> repo = handler.get_parent_repository("path/to/file")
"""

import os
import tempfile
from pathlib import Path
from typing import Any, TypeAlias

import attrs
from git import GitCommandError, InvalidGitRepositoryError, Repo
from pydantic import BaseModel

FilePath: TypeAlias = str | os.PathLike[str]


class FileOperationError(Exception):
    """Raised when file operations fail."""


class GitConfig(BaseModel):
    """Configuration for Git operations.
    
    Attributes:
        search_parent_dirs: Whether to search parent directories for Git repos
        clone_depth: Depth limit for Git clones
        timeout: Timeout for Git operations in seconds
    """
    
    search_parent_dirs: bool = True
    clone_depth: int | None = None
    timeout: int = 30


@attrs.define
class FileHandler:
    """Handles file system operations with validation.
    
    Attributes:
        git_config: Configuration for Git operations
    """
    
    git_config: GitConfig = attrs.field(
        factory=GitConfig,
        converter=lambda x: (
            x if isinstance(x, GitConfig)
            else GitConfig(**x)
        )
    )
    
    def get_parent_repository(
        self,
        file_path: FilePath | None = None,
        search_parent_directories: bool | None = None,
    ) -> Repo | None:
        """Get the parent Git repository for a path.
        
        Args:
            file_path: Path to search from
            search_parent_directories: Override config search behavior
        
        Returns:
            Git repository or None if not found
        
        Example:
            >>> handler = FileHandler()
            >>> repo = handler.get_parent_repository(".")
        """
        if file_path is None:
            file_path = os.getcwd()
        
        search = (
            search_parent_directories
            if search_parent_directories is not None
            else self.git_config.search_parent_dirs
        )
        
        try:
            return Repo(file_path, search_parent_directories=search)
        except (InvalidGitRepositoryError, GitCommandError):
            return None
    
    def clone_repository(
        self,
        url: str,
        path: FilePath | None = None,
        depth: int | None = None,
        **kwargs: Any,
    ) -> Repo:
        """Clone a Git repository.
        
        Args:
            url: Repository URL
            path: Clone destination path
            depth: Override config clone depth
            **kwargs: Additional Git clone options
        
        Returns:
            Cloned repository
        
        Raises:
            FileOperationError: If clone fails
        """
        try:
            clone_path = path or tempfile.mkdtemp()
            clone_depth = depth or self.git_config.clone_depth
            
            return Repo.clone_from(
                url,
                clone_path,
                depth=clone_depth,
                timeout=self.git_config.timeout,
                **kwargs
            )
        except Exception as e:
            raise FileOperationError(f"Failed to clone repository: {e}") from e
    
    def file_path_depth(self, file_path: FilePath) -> int:
        """Calculate the depth of a file path.
        
        Args:
            file_path: Path to analyze
        
        Returns:
            Depth of the path
        
        Example:
            >>> handler = FileHandler()
            >>> depth = handler.file_path_depth("a/b/c")
            >>> print(depth)
            3
        """
        path = Path(file_path)
        parts = [p for p in path.parts if p not in (".", "", "/")]
        return len(parts)
    
    def file_path_rel_to_root(self, file_path: FilePath) -> str:
        """Get relative path to root.
        
        Args:
            file_path: Path to analyze
        
        Returns:
            Relative path string
        
        Example:
            >>> handler = FileHandler()
            >>> rel_path = handler.file_path_rel_to_root("a/b/c")
            >>> print(rel_path)
            ../../..
        """
        depth = self.file_path_depth(file_path)
        if depth == 0:
            return ""
        return "/".join([".."] * depth) 