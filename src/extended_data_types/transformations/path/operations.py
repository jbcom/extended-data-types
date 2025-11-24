"""Path operation transformations."""

from __future__ import annotations

from pathlib import Path
from typing import Union

from extended_data_types.transformations.core import Transform


PathLike = Union[str, Path]


def join_paths(*paths: PathLike) -> Path:
    """Join path components.

    Args:
        *paths: Path components to join

    Returns:
        Joined path

    Example:
        >>> join_paths('dir', 'subdir', 'file.txt')
        Path('dir/subdir/file.txt')
    """
    return Path(*paths)


def resolve_path(path: PathLike) -> Path:
    """Resolve path to absolute with symlinks resolved.

    Args:
        path: Path to resolve

    Returns:
        Resolved absolute path

    Example:
        >>> resolve_path('~/documents/../downloads')
        Path('/home/user/downloads')
    """
    return Path(path).expanduser().resolve()


def normalize_path(
    path: PathLike, collapse_user: bool = True, collapse_relative: bool = True
) -> Path:
    """Normalize path format.

    Args:
        path: Path to normalize
        collapse_user: Replace home dir with ~
        collapse_relative: Collapse .. and . components

    Returns:
        Normalized path

    Example:
        >>> normalize_path('/home/user/./docs/../downloads')
        Path('~/downloads')
    """
    p = Path(path)

    if collapse_relative:
        p = p.resolve()

    if collapse_user:
        try:
            p = Path("~") / p.relative_to(Path.home())
        except ValueError:
            pass

    return p


def make_relative(path: PathLike, start: PathLike | None = None) -> Path:
    """Make path relative to start path.

    Args:
        path: Path to convert
        start: Start path (default: current directory)

    Returns:
        Relative path

    Example:
        >>> make_relative('/home/user/file.txt', '/home')
        Path('user/file.txt')
    """
    p = Path(path)
    if start is None:
        start = Path.cwd()
    else:
        start = Path(start)

    try:
        return p.relative_to(start)
    except ValueError:
        # If paths don't share a prefix, return original
        return p


def make_absolute(path: PathLike, base: PathLike | None = None) -> Path:
    """Make path absolute using optional base.

    Args:
        path: Path to convert
        base: Base path (default: current directory)

    Returns:
        Absolute path

    Example:
        >>> make_absolute('file.txt', '/home/user')
        Path('/home/user/file.txt')
    """
    p = Path(path)
    if p.is_absolute():
        return p

    if base is None:
        base = Path.cwd()
    else:
        base = Path(base)

    return (base / p).resolve()


def ensure_parent(path: PathLike) -> Path:
    """Ensure parent directories exist.

    Args:
        path: Path to check

    Returns:
        Path with parents created

    Example:
        >>> ensure_parent('new_dir/subdir/file.txt')
        Path('new_dir/subdir/file.txt')
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def is_subpath(path: PathLike, parent: PathLike) -> bool:
    """Check if path is subpath of parent.

    Args:
        path: Path to check
        parent: Potential parent path

    Returns:
        True if path is subpath

    Example:
        >>> is_subpath('/home/user/file.txt', '/home')
        True
    """
    try:
        Path(path).relative_to(Path(parent))
        return True
    except ValueError:
        return False


# Register transforms
join_paths_transform = Transform(join_paths)
resolve_path_transform = Transform(resolve_path)
normalize_path_transform = Transform(normalize_path)
make_relative_transform = Transform(make_relative)
make_absolute_transform = Transform(make_absolute)
ensure_parent_transform = Transform(ensure_parent)
is_subpath_transform = Transform(is_subpath)
