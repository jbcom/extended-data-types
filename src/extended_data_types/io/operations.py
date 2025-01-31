"""File system operations and utilities."""

from __future__ import annotations

import contextlib
import os
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any, TypeVar, cast

import requests
from filelock import FileLock, Timeout

from extended_data_types.core.state import is_nothing
from extended_data_types.log_utils import LoggerProtocol, get_null_logger
from extended_data_types.serialization.decoders import (decode_hcl2,
                                                        decode_json,
                                                        decode_yaml)
from extended_data_types.string.core import is_url

from .types import FilePath, FilePathWrapper

T = TypeVar('T', bound=dict[str, Any])
FileContent = str | dict[str, Any]
ContentType = str | dict[str, Any]
ReturnPathType = ContentType | tuple[ContentType, str]
DecoderFunc = Callable[[str], dict[str, Any]]


@contextlib.contextmanager
def file_lock(file_path: FilePath, timeout: float = 10) -> Iterator[None]:
    """Create a lock file to prevent concurrent access to a file.

    Args:
        file_path: Path to the file to lock
        timeout: Maximum time in seconds to wait for lock acquisition

    Yields:
        None when the lock is acquired

    Raises:
        Timeout: If the lock cannot be acquired within the timeout period
        RuntimeError: If there are issues with the lock file
    """
    path = FilePathWrapper(file_path)
    lock_path = f"{path}.lock"
    try:
        with FileLock(str(lock_path), timeout=timeout):
            yield
    except Timeout as exc:
        msg = f"Could not acquire lock for {path} within {timeout} seconds"
        raise Timeout(msg) from exc
    except Exception as exc:
        msg = f"Error with lock file {lock_path}: {exc}"
        raise RuntimeError(msg) from exc
    finally:
        with contextlib.suppress(Exception):
            Path(str(lock_path)).unlink(missing_ok=True)


def check_file_exists(file_path: FilePath) -> bool:
    """Check if a file exists.

    Args:
        file_path: Path to the file to check

    Returns:
        True if the file exists and is a regular file
    """
    return Path(str(file_path)).is_file()


def check_file_readable(file_path: FilePath) -> bool:
    """Check if a file is readable.

    Args:
        file_path: Path to the file to check

    Returns:
        True if the file exists and is readable
    """
    try:
        path = Path(str(file_path))
        return path.is_file() and os.access(path, os.R_OK)
    except OSError:
        return False


def check_file_writable(file_path: FilePath) -> bool:
    """Check if a file is writable or can be created.

    Args:
        file_path: Path to the file to check

    Returns:
        True if the file is writable or can be created
    """
    path = Path(str(file_path))
    
    # If file exists, check write permission
    if path.exists():
        return os.access(path, os.W_OK)
        
    # If file doesn't exist, check parent directory
    parent = path.parent
    return parent.exists() and os.access(parent, os.W_OK)


def delete_file(file_path: FilePath) -> None:
    """Delete a file if it exists.

    Args:
        file_path: Path to the file to delete

    Raises:
        OSError: If there are issues deleting the file
    """
    Path(str(file_path)).unlink(missing_ok=True)


def get_file(
    file_path: FilePath,
    decode: bool = True,
    charset: str = "utf-8",
    errors: str = "strict",
    raise_on_not_found: bool = False,
    logger: LoggerProtocol | None = None,
) -> ReturnPathType:
    """Get file content, optionally decoding based on file extension.

    Args:
        file_path: Path or URL to the file
        decode: Whether to decode the content based on file extension
        charset: Character encoding to use
        errors: How to handle encoding errors
        raise_on_not_found: Whether to raise FileNotFoundError if file not found
        logger: Logger instance to use

    Returns:
        The file content, optionally decoded based on extension

    Raises:
        FileNotFoundError: If raise_on_not_found is True and file not found
        OSError: If there are issues reading the file
    """
    logger = logger or get_null_logger(__name__)
    path_str = str(file_path)

    # Handle URLs
    if is_url(path_str):
        logger.info("Downloading from URL: %s", path_str)
        response = requests.get(path_str)
        response.raise_for_status()
        content = response.text
    else:
        # Handle local files
        path = Path(path_str)
        if not path.is_file():
            if raise_on_not_found:
                raise FileNotFoundError(f"File not found: {path}")
            return "" if not decode else {}

        logger.info("Reading from file: %s", path)
        content = path.read_text(encoding=charset, errors=errors)

    if not decode:
        return content

    # Decode based on file extension
    suffix = Path(path_str).suffix.lower()
    try:
        if suffix in {".yaml", ".yml"}:
            return decode_yaml(content)
        if suffix == ".json":
            return decode_json(content)
        if suffix == ".hcl":
            return decode_hcl2(content)
        return content
    except Exception as exc:
        logger.error("Failed to decode file %s: %s", path_str, exc)
        raise


def read_file(
    file_path: FilePath,
    encoding: str = "utf-8",
    errors: str = "strict",
    logger: LoggerProtocol | None = None,
) -> str:
    """Read content from a file.

    Args:
        file_path: Path to the file to read
        encoding: Character encoding to use
        errors: How to handle encoding errors
        logger: Logger instance to use

    Returns:
        The file content as a string

    Raises:
        FileNotFoundError: If the file does not exist
        OSError: If there are issues reading the file
    """
    return cast(
        str,
        get_file(
            file_path=file_path,
            decode=False,
            charset=encoding,
            errors=errors,
            raise_on_not_found=True,
            logger=logger,
        ),
    )


def write_file(
    file_path: FilePath,
    content: str,
    encoding: str = "utf-8",
    errors: str = "strict",
    logger: LoggerProtocol | None = None,
) -> None:
    """Write content to a file.

    Args:
        file_path: Path to the file to write
        content: Content to write to the file
        encoding: Character encoding to use
        errors: How to handle encoding errors
        logger: Logger instance to use

    Raises:
        OSError: If there are issues writing to the file
    """
    logger = logger or get_null_logger(__name__)
    logger.info("Writing to file: %s", file_path)

    path = Path(str(file_path))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding=encoding, errors=errors)


def file_path_depth(file_path: FilePath) -> int:
    """Calculate the depth of a file path.

    Args:
        file_path: Path to analyze

    Returns:
        Depth of the path (number of path components)
    """
    path = Path(str(file_path))
    parts = path.parts
    # Remove root component for absolute paths
    if path.is_absolute():
        parts = parts[1:]
    return len(parts)


def file_path_rel_to_root(file_path: FilePath) -> str:
    """Generate relative path to root from given path.

    Args:
        file_path: Path to generate relative path from

    Returns:
        Relative path to root
    """
    depth = file_path_depth(file_path)
    if depth == 0:
        return ""
    return "/".join([".."] * depth)


def match_file_extensions(
    file_path: FilePath,
    allowed: list[str] | None = None,
    denied: list[str] | None = None,
) -> bool:
    """Check if a file matches allowed/denied extensions.

    Args:
        file_path: Path to check
        allowed: List of allowed extensions
        denied: List of denied extensions

    Returns:
        True if file extension matches criteria
    """
    path = Path(str(file_path))
    ext = path.suffix.lower()

    if denied and ext in denied:
        return False
    return not (allowed and ext not in allowed) 