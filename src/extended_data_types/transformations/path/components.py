"""Path component operations."""

from __future__ import annotations

from pathlib import Path
from typing import Union

from ..core import Transform

PathLike = Union[str, Path]


def get_stem(path: PathLike) -> str:
    """Get file name without extension.
    
    Args:
        path: Path to process
        
    Returns:
        File stem
        
    Example:
        >>> get_stem('path/to/file.txt')
        'file'
        >>> get_stem('path/to/archive.tar.gz')
        'archive.tar'
    """
    return Path(path).stem


def get_suffix(
    path: PathLike,
    full: bool = False
) -> str:
    """Get file extension.
    
    Args:
        path: Path to process
        full: Include all extensions for multi-part extensions
        
    Returns:
        File extension
        
    Example:
        >>> get_suffix('file.txt')
        '.txt'
        >>> get_suffix('archive.tar.gz', full=True)
        '.tar.gz'
    """
    p = Path(path)
    if full:
        name = p.name
        if '.' not in name:
            return ''
        return '.' + name.split('.', 1)[1]
    return p.suffix


def get_parent(
    path: PathLike,
    levels: int = 1
) -> Path:
    """Get parent directory.
    
    Args:
        path: Path to process
        levels: Number of levels to go up
        
    Returns:
        Parent path
        
    Example:
        >>> get_parent('a/b/c/file.txt', 2)
        Path('a/b')
    """
    p = Path(path)
    for _ in range(levels):
        p = p.parent
    return p


def split_path(path: PathLike) -> list[str]:
    """Split path into components.
    
    Args:
        path: Path to split
        
    Returns:
        List of path components
        
    Example:
        >>> split_path('/home/user/file.txt')
        ['home', 'user', 'file.txt']
    """
    return [part for part in Path(path).parts if part != '/']


def split_extension(
    path: PathLike,
    full: bool = False
) -> tuple[Path, str]:
    """Split path into stem and extension.
    
    Args:
        path: Path to split
        full: Include all extensions for multi-part extensions
        
    Returns:
        Tuple of (stem path, extension)
        
    Example:
        >>> split_extension('path/to/file.txt')
        (Path('path/to/file'), '.txt')
        >>> split_extension('path/to/archive.tar.gz', full=True)
        (Path('path/to/archive'), '.tar.gz')
    """
    p = Path(path)
    if not full:
        return p.with_suffix(''), p.suffix
    
    name = p.name
    if '.' not in name:
        return p, ''
    
    stem, ext = name.split('.', 1)
    return p.with_name(stem), f'.{ext}'


def get_parts(
    path: PathLike,
    include_root: bool = False
) -> dict[str, str]:
    """Get all path components as dictionary.
    
    Args:
        path: Path to process
        include_root: Include root component
        
    Returns:
        Dictionary of path components
        
    Example:
        >>> get_parts('path/to/file.txt')
        {
            'parent': 'path/to',
            'name': 'file.txt',
            'stem': 'file',
            'suffix': '.txt'
        }
    """
    p = Path(path)
    parts = {
        'parent': str(p.parent),
        'name': p.name,
        'stem': p.stem,
        'suffix': p.suffix
    }
    
    if include_root and p.root:
        parts['root'] = p.root
        
    return parts


def replace_name(
    path: PathLike,
    name: str,
    keep_suffix: bool = True
) -> Path:
    """Replace file name in path.
    
    Args:
        path: Path to modify
        name: New name
        keep_suffix: Keep original extension
        
    Returns:
        Path with new name
        
    Example:
        >>> replace_name('path/to/file.txt', 'newfile')
        Path('path/to/newfile.txt')
        >>> replace_name('path/to/file.txt', 'newfile', keep_suffix=False)
        Path('path/to/newfile')
    """
    p = Path(path)
    if keep_suffix:
        return p.with_name(f"{name}{p.suffix}")
    return p.with_name(name)


def replace_stem(
    path: PathLike,
    stem: str
) -> Path:
    """Replace file stem in path.
    
    Args:
        path: Path to modify
        stem: New stem
        
    Returns:
        Path with new stem
        
    Example:
        >>> replace_stem('path/to/file.txt', 'newfile')
        Path('path/to/newfile.txt')
    """
    return Path(path).with_stem(stem)


# Register transforms
get_stem_transform = Transform(get_stem)
get_suffix_transform = Transform(get_suffix)
get_parent_transform = Transform(get_parent)
split_path_transform = Transform(split_path)
split_extension_transform = Transform(split_extension)
get_parts_transform = Transform(get_parts)
replace_name_transform = Transform(replace_name)
replace_stem_transform = Transform(replace_stem) 