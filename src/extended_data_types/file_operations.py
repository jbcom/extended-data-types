"""This module provides utilities for file operations including reading, writing, and deleting files.

It includes functions to handle both local and remote files, with support for locking mechanisms
to prevent concurrent access issues.
"""

from __future__ import annotations

import contextlib
import os
from pathlib import Path
from typing import Any, Dict, Mapping, TypeVar, Union, cast

import requests
from filelock import FileLock, Timeout
from requests.models import Response

from .export_utils import wrap_raw_data_for_export
from .file_data_type import FilePath, get_encoding_for_file_path
from .hcl2_utils import decode_hcl2
from .json_utils import decode_json
from .log_utils import LoggerProtocol, get_null_logger
from .state_utils import is_nothing
from .string_data_type import is_url
from .yaml_utils import decode_yaml

T = TypeVar("T", str, Dict[str, Any])
FileContent = Union[str, Dict[str, Any]]
ReturnType = Union[FileContent, tuple[FileContent, FilePath]]


@contextlib.contextmanager
def file_lock(file_path: FilePath, timeout: float = 10) -> None:
    """Create a lock file to prevent concurrent access.

    Args:
        file_path: Path to the file to lock.
        timeout: Maximum time to wait for lock in seconds.

    Yields:
        None when lock is acquired.

    Raises:
        Timeout: If lock cannot be acquired within timeout period.
        RuntimeError: If there are issues with the lock file.
    """
    lock_path = f"{file_path}.lock"
    try:
        with FileLock(lock_path, timeout=timeout):
            yield
    except Timeout as exc:
        msg = f"Could not acquire lock for {file_path} within {timeout} seconds"
        raise Timeout(msg) from exc
    except Exception as exc:
        msg = f"Error with lock file {lock_path}: {exc}"
        raise RuntimeError(msg) from exc
    finally:
        with contextlib.suppress(Exception):
            Path(lock_path).unlink(missing_ok=True)


def check_file_exists(file_path: FilePath) -> bool:
    """Check if a file exists.

    Args:
        file_path: Path to the file to check.

    Returns:
        True if the file exists, False otherwise.
    """
    return Path(file_path).is_file()


def check_file_readable(file_path: FilePath) -> bool:
    """Check if a file is readable.

    Args:
        file_path: Path to the file to check.

    Returns:
        True if the file exists and is readable, False otherwise.
    """
    try:
        path = Path(file_path)
        return path.is_file() and os.access(path, os.R_OK)
    except (OSError, IOError):
        return False


def check_file_writable(file_path: FilePath) -> bool:
    """Check if a file is writable.

    Args:
        file_path: Path to the file to check.

    Returns:
        True if the file exists and is writable or can be created, False otherwise.
    """
    try:
        path = Path(file_path)
        if path.exists():
            return os.access(path, os.W_OK)
        
        # Check if the parent directory is writable
        parent = path.parent
        try:
            return parent.exists() and os.access(parent, os.W_OK)
        except OSError:
            return False
    except (OSError, IOError):
        return False


def check_file_empty(file_path: FilePath) -> bool:
    """Check if a file is empty.

    Args:
        file_path: Path to the file to check.

    Returns:
        True if the file is empty or does not exist, False otherwise.
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return True
        return path.stat().st_size == 0
    except (OSError, IOError):
        return True


def decode_file_content(content: str, file_path: FilePath) -> Dict[str, Any]:
    """Decode file content based on file extension.

    Args:
        content: Raw file content to decode.
        file_path: Path to the file, used to determine format.

    Returns:
        Decoded content as a dictionary.

    Raises:
        ValueError: If the file format is not supported.
    """
    if is_nothing(content):
        return {}

    path = str(file_path).lower()
    if path.endswith((".yml", ".yaml")):
        return decode_yaml(content)
    if path.endswith(".json"):
        return decode_json(content)
    if path.endswith((".hcl", ".tf")):
        return decode_hcl2(content)
    
    raise ValueError(f"Unsupported file format for {file_path}")


def get_file(
    file_path: FilePath,
    decode: bool = True,
    return_path: bool = False,
    charset: str = "utf-8",
    errors: str = "strict",
    headers: Mapping[str, str] | None = None,
    raise_on_not_found: bool = False,
    logger: LoggerProtocol | None = None,
) -> ReturnType:
    """Get file content from either a local path or URL.

    Args:
        file_path: Path to the file or URL.
        decode: Whether to decode the file content.
        return_path: Whether to return the file path with the content.
        charset: Character encoding to use.
        errors: How to handle encoding errors.
        headers: Headers to use for URL requests.
        raise_on_not_found: Whether to raise an error if file not found.
        logger: Logger instance to use. If None, uses a null logger.

    Returns:
        The file content and optionally the path.

    Raises:
        FileNotFoundError: If the file is not found and raise_on_not_found is True.
    """
    logger = logger or get_null_logger(__name__)
    headers = headers or {}
    file_data: str = ""

    def state_negative_result(result: str) -> None:
        logger.warning(result)
        if raise_on_not_found:
            raise FileNotFoundError(result)

    try:
        if is_url(str(file_path)):
            logger.info("Getting remote URL: %s", file_path)
            response: Response = requests.get(
                str(file_path), headers=headers, timeout=30
            )
            if response.ok:
                file_data = response.content.decode(charset, errors)
            else:
                state_negative_result(
                    f"URL {file_path} could not be read: {response.status_code}"
                )
        else:
            logger.info("Getting local file: %s", file_path)
            path = Path(file_path)
            if path.is_file():
                file_data = path.read_text(encoding=charset, errors=errors)
            else:
                state_negative_result(f"File {file_path} does not exist")

        if decode and file_data:
            file_data = decode_file_content(file_data, file_path)

    except (OSError, IOError) as exc:
        state_negative_result(f"Error reading {file_path}: {exc}")

    retval: list[FileContent | FilePath] = [file_data]
    if return_path:
        retval.append(file_path)

    return tuple(retval) if return_path else retval[0]


def decode_file(
    file_data: str,
    file_path: FilePath | None = None,
    suffix: str | None = None,
    logger: LoggerProtocol | None = None,
) -> Any:
    """Decode file content based on file extension.

    Args:
        file_data: The file content to decode.
        file_path: Path to the file.
        suffix: File suffix to use for decoding.
        logger: Logger instance to use. If None, uses a null logger.

    Returns:
        The decoded data.

    Raises:
        RuntimeError: If file parsing fails.
    """
    logger = logger or get_null_logger(__name__)

    def _raise_decode_error(msg: str, exc: Exception | None = None) -> None:
        if exc is not None:
            raise RuntimeError(msg) from exc
        raise RuntimeError(msg)

    if suffix is None and file_path is not None:
        logger.info("Decoding file %s", file_path)
        suffix = Path(file_path).suffix.lstrip(".").lower()

    try:
        if suffix in ("yml", "yaml"):
            logger.info("Data is being loaded from YAML")
            return decode_yaml(file_data)
        if suffix == "json":
            logger.info("Data is being loaded from JSON")
            return decode_json(file_data)
        if suffix == "tf":
            logger.info("Data is being loaded from HCL2")
            return decode_hcl2(file_data)

        # Move decoders outside loop to avoid try-except performance overhead
        decoders = (decode_yaml, decode_json, decode_hcl2)
        decoder_errors = []

        for decoder in decoders:
            logger.debug("Attempting to decode with %s", decoder.__name__)
            try:
                return decoder(file_data)
            except (ValueError, TypeError, SyntaxError) as e:
                decoder_errors.append(f"{decoder.__name__}: {e!s}")
                continue

        error_details = "; ".join(decoder_errors)
        _raise_decode_error(
            f"Failed to decode data with any known decoder: {error_details}"
        )
    except (ValueError, TypeError, SyntaxError) as exc:
        _raise_decode_error(f"Failed to parse file {file_path}", exc)


def update_file(
    file_path: FilePath,
    file_data: Any,
    allow_encoding: bool | str | None = None,
    allow_empty: bool = False,
    max_lock_wait: int = 10,
    logger: LoggerProtocol | None = None,
    **format_opts: Any,
) -> int | None:
    """Update a file with the given data.

    Args:
        file_path: Path to the file to update.
        file_data: Data to write to the file.
        allow_encoding: Encoding to use.
        allow_empty: Whether to allow empty data.
        max_lock_wait: Maximum time to wait for file lock in seconds.
        logger: Logger instance to use. If None, uses a null logger.
        **format_opts: Additional formatting options.

    Returns:
        Number of bytes written, or None if no update performed.

    Raises:
        RuntimeError: If file cannot be updated due to lock timeout.
    """
    logger = logger or get_null_logger(__name__)

    if is_nothing(file_data) and not allow_empty:
        logger.warning("Empty file data for %s not allowed", file_path)
        return None

    if allow_encoding is None:
        allow_encoding = get_encoding_for_file_path(file_path)
        logger.debug("Detected encoding for %s: %s", file_path, allow_encoding)

    file_data = wrap_raw_data_for_export(
        file_data, allow_encoding=allow_encoding, **format_opts
    )

    if not isinstance(file_data, str):
        file_data = str(file_data)

    logger.info("Updating local file %s", file_path)

    try:
        with file_lock(file_path, timeout=max_lock_wait):
            local_file = Path(file_path)
            logger.info("Updating local file: %s", local_file)
            local_file.parent.mkdir(parents=True, exist_ok=True)
            return local_file.write_text(file_data)
    except Timeout as e:
        msg = (
            f"Cannot update file path {file_path}, "
            "another instance of this application currently holds the lock."
        )
        raise RuntimeError(msg) from e


def delete_file(
    file_path: FilePath,
    logger: LoggerProtocol | None = None,
) -> bool:
    """Delete a file.

    Args:
        file_path: Path to the file to delete.
        logger: Logger instance to use. If None, uses a null logger.

    Returns:
        True if file was deleted or did not exist, False otherwise.
    """
    logger = logger or get_null_logger(__name__)
    logger.warning("Deleting local file %s", file_path)
    try:
        Path(file_path).unlink(missing_ok=True)
        return True
    except OSError:
        logger.exception("Failed to delete file %s", file_path)
        return False


def read_file(
    file_path: FilePath,
    encoding: str = "utf-8",
    errors: str = "strict",
    logger: LoggerProtocol | None = None,
) -> str:
    """Read content from a file.

    Args:
        file_path: Path to the file to read.
        encoding: Character encoding to use.
        errors: How to handle encoding errors.
        logger: Logger instance to use. If None, uses a null logger.

    Returns:
        The file content as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
        OSError: If there are issues reading the file.
    """
    return cast(
        str,
        get_file(
            file_path=file_path,
            decode=False,  # We want raw text
            charset=encoding,
            errors=errors,
            raise_on_not_found=True,  # Match read_file behavior
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
        file_path: Path to the file to write.
        content: Content to write to the file.
        encoding: Character encoding to use.
        errors: How to handle encoding errors.
        logger: Logger instance to use. If None, uses a null logger.

    Raises:
        OSError: If there are issues writing to the file.
    """
    logger = logger or get_null_logger(__name__)
    logger.info("Writing to file: %s", file_path)

    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding=encoding, errors=errors)
