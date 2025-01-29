"""This module contains test functions for verifying file operations functionality using the
`extended_data_types` package. It includes tests for reading, writing, and checking files
with various encodings and formats.

Functions:
    - test_read_file: Tests reading file content with different encodings.
    - test_write_file: Tests writing content to files with different encodings.
    - test_check_file_exists: Tests checking if files exist.
    - test_check_file_empty: Tests checking if files are empty.
    - test_check_file_readable: Tests checking if files are readable.
    - test_check_file_writable: Tests checking if files are writable.
"""

from __future__ import annotations

import tempfile

from pathlib import Path

import pytest

from extended_data_types.file_operations import (
    check_file_empty,
    check_file_exists,
    check_file_readable,
    check_file_writable,
    read_file,
    write_file,
)


@pytest.fixture()
def temp_file() -> Path:
    """Creates a temporary file for testing."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = Path(tmp.name)
    # Clear the file content
    tmp_path.write_text("")
    return tmp_path


@pytest.fixture()
def temp_file_with_content() -> Path:
    """Creates a temporary file with content for testing."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = Path(tmp.name)
    content = "Test content"
    tmp_path.write_text(content)
    return tmp_path


def test_read_file(temp_file_with_content: Path) -> None:
    """Tests reading file content with different encodings.

    Args:
        temp_file_with_content: Path to a temporary file with content.

    Asserts:
        The content read from the file matches the expected content.
    """
    content = read_file(temp_file_with_content)
    assert content == "Test content"

    # Test with explicit encoding
    content = read_file(temp_file_with_content, encoding="utf-8")
    assert content == "Test content"


def test_write_file(temp_file: Path) -> None:
    """Tests writing content to files with different encodings.

    Args:
        temp_file: Path to a temporary file.

    Asserts:
        The content written to the file can be read back correctly.
    """
    content = "Test write content"
    write_file(temp_file, content)

    read_content = temp_file.read_text(encoding="utf-8")
    assert read_content == content

    # Test with explicit encoding
    content = "Test write content with encoding"
    write_file(temp_file, content, encoding="utf-8")

    read_content = temp_file.read_text(encoding="utf-8")
    assert read_content == content


def test_check_file_exists(temp_file: Path) -> None:
    """Tests checking if files exist.

    Args:
        temp_file: Path to a temporary file.

    Asserts:
        The function correctly identifies existing and non-existing files.
    """
    assert check_file_exists(temp_file) is True

    # Test non-existent file
    non_existent = Path("non_existent_file.txt")
    assert check_file_exists(non_existent) is False


def test_check_file_empty(temp_file: Path, temp_file_with_content: Path) -> None:
    """Tests checking if files are empty.

    Args:
        temp_file: Path to an empty temporary file.
        temp_file_with_content: Path to a temporary file with content.

    Asserts:
        The function correctly identifies empty and non-empty files.
    """
    assert check_file_empty(temp_file) is True
    assert check_file_empty(temp_file_with_content) is False


def test_check_file_readable(temp_file_with_content: Path) -> None:
    """Tests checking if files are readable.

    Args:
        temp_file_with_content: Path to a temporary file with content.

    Asserts:
        The function correctly identifies readable and non-readable files.
    """
    assert check_file_readable(temp_file_with_content) is True

    # Make file non-readable
    temp_file_with_content.chmod(0o000)
    assert check_file_readable(temp_file_with_content) is False

    # Restore permissions for cleanup
    temp_file_with_content.chmod(0o666)


def test_check_file_writable(temp_file: Path) -> None:
    """Tests checking if files are writable.

    Args:
        temp_file: Path to a temporary file.

    Asserts:
        The function correctly identifies writable and non-writable files.
    """
    assert check_file_writable(temp_file) is True

    # Make file read-only
    temp_file.chmod(0o444)
    assert check_file_writable(temp_file) is False

    # Restore permissions for cleanup
    temp_file.chmod(0o666)
