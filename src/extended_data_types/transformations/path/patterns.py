"""Path pattern matching operations."""

from __future__ import annotations

import fnmatch
import re
from pathlib import Path
from typing import Iterator, Union

from ..core import Transform

PathLike = Union[str, Path]


def match_pattern(
    path: PathLike,
    pattern: str,
    case_sensitive: bool = True
) -> bool:
    """Check if path matches pattern.
    
    Args:
        path: Path to check
        pattern: Glob pattern
        case_sensitive: Use case-sensitive matching
        
    Returns:
        True if path matches pattern
        
    Example:
        >>> match_pattern('file.txt', '*.txt')
        True
        >>> match_pattern('File.TXT', '*.txt', case_sensitive=False)
        True
    """
    if not case_sensitive:
        return fnmatch.fnmatch(str(path), pattern)
    return fnmatch.fnmatchcase(str(path), pattern)


def find_files(
    directory: PathLike,
    pattern: str = "*",
    recursive: bool = True,
    follow_links: bool = False
) -> Iterator[Path]:
    """Find files matching pattern.
    
    Args:
        directory: Directory to search
        pattern: Glob pattern
        recursive: Search subdirectories
        follow_links: Follow symbolic links
        
    Yields:
        Matching file paths
        
    Example:
        >>> list(find_files('docs', '*.md', recursive=True))
        [Path('docs/readme.md'), Path('docs/api/guide.md')]
    """
    path = Path(directory)
    if recursive:
        glob = "**/" + pattern
    else:
        glob = pattern
        
    yield from path.glob(glob)


def find_dirs(
    directory: PathLike,
    pattern: str = "*",
    recursive: bool = True,
    follow_links: bool = False
) -> Iterator[Path]:
    """Find directories matching pattern.
    
    Args:
        directory: Directory to search
        pattern: Glob pattern
        recursive: Search subdirectories
        follow_links: Follow symbolic links
        
    Yields:
        Matching directory paths
        
    Example:
        >>> list(find_dirs('src', '*_test'))
        [Path('src/unit_test'), Path('src/integration_test')]
    """
    for path in find_files(directory, pattern, recursive, follow_links):
        if path.is_dir():
            yield path


def replace_extension(
    path: PathLike,
    new_ext: str,
    full: bool = False
) -> Path:
    """Replace file extension.
    
    Args:
        path: Path to modify
        new_ext: New extension
        full: Replace full extension for multi-part extensions
        
    Returns:
        Path with new extension
        
    Example:
        >>> replace_extension('file.txt', '.md')
        Path('file.md')
        >>> replace_extension('archive.tar.gz', '.zip', full=True)
        Path('archive.zip')
    """
    p = Path(path)
    if not full:
        if not new_ext.startswith('.'):
            new_ext = '.' + new_ext
        return p.with_suffix(new_ext)
    
    name = p.name
    if '.' not in name:
        if not new_ext.startswith('.'):
            new_ext = '.' + new_ext
        return p.with_name(name + new_ext)
    
    stem = name.split('.')[0]
    if not new_ext.startswith('.'):
        new_ext = '.' + new_ext
    return p.with_name(stem + new_ext)


def filter_paths(
    paths: Iterator[PathLike] | list[PathLike],
    include: list[str] | None = None,
    exclude: list[str] | None = None,
    case_sensitive: bool = True
) -> Iterator[Path]:
    """Filter paths by patterns.
    
    Args:
        paths: Paths to filter
        include: Patterns to include
        exclude: Patterns to exclude
        case_sensitive: Use case-sensitive matching
        
    Yields:
        Filtered paths
        
    Example:
        >>> paths = ['a.txt', 'b.md', 'c.txt']
        >>> list(filter_paths(paths, include=['*.txt'], exclude=['b*']))
        [Path('a.txt'), Path('c.txt')]
    """
    for path in paths:
        path = Path(path)
        
        if exclude:
            if any(match_pattern(path, p, case_sensitive) for p in exclude):
                continue
                
        if include:
            if not any(match_pattern(path, p, case_sensitive) for p in include):
                continue
                
        yield path


# Register transforms
match_pattern_transform = Transform(match_pattern)
find_files_transform = Transform(find_files)
find_dirs_transform = Transform(find_dirs)
replace_extension_transform = Transform(replace_extension)
filter_paths_transform = Transform(filter_paths) 