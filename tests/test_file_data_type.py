"""
This module contains test functions for verifying the functionality of various file path operations using the
`extended_data_types` package. It includes tests for matching file extensions, determining file encoding, calculating
file path depth, and finding the relative path to the root.

Functions:
    - test_match_file_extensions: Tests matching of file extensions against allowed and denied lists.
    - test_get_encoding_for_file_path: Tests getting the encoding type based on file extension.
    - test_file_path_depth: Tests calculating the depth of a file path.
    - test_file_path_rel_to_root: Tests determining the relative path to the root directory.
"""

from __future__ import annotations

import pytest

from extended_data_types.file_data_type import (
    file_path_depth,
    file_path_rel_to_root,
    get_encoding_for_file_path,
    match_file_extensions,
)


@pytest.mark.parametrize(
    ("file_path", "allowed_extensions", "denied_extensions", "expected"),
    [
        ("test.txt", ["txt"], None, True),
        ("test.txt", ["md"], None, False),
        ("test.txt", None, ["txt"], False),
        ("test.txt", ["txt"], ["md"], True),
        ("test.txt", ["md"], ["txt"], False),
        ("test.txt", None, None, True),
        ("test.", ["txt"], None, False),
        (".hidden", ["hidden"], None, True),
    ],
)
def test_match_file_extensions(
    file_path: str,
    allowed_extensions: list[str] | None,
    denied_extensions: list[str] | None,
    expected: bool,
) -> None:
    """
    Tests matching of file extensions against allowed and denied lists.

    Args:
        file_path (str): The path of the file to check.
        allowed_extensions (list[str] | None): List of allowed file extensions.
        denied_extensions (list[str] | None): List of denied file extensions.
        expected (bool): The expected result of the match.

    Asserts:
        The result of match_file_extensions matches the expected boolean value.
    """
    assert (
        match_file_extensions(file_path, allowed_extensions, denied_extensions)
        == expected
    )


@pytest.mark.parametrize(
    ("file_path", "expected_encoding"),
    [
        ("test.yaml", "yaml"),
        ("test.yml", "yaml"),
        ("test.json", "json"),
        ("test.txt", "raw"),
        ("test", "raw"),
    ],
)
def test_get_encoding_for_file_path(file_path: str, expected_encoding: str) -> None:
    """
    Tests getting the encoding type based on file extension.

    Args:
        file_path (str): The path of the file to check.
        expected_encoding (str): The expected encoding type.

    Asserts:
        The result of get_encoding_for_file_path matches the expected encoding type.
    """
    assert get_encoding_for_file_path(file_path) == expected_encoding


@pytest.mark.parametrize(
    ("file_path", "expected_depth"),
    [
        ("test.txt", 1),
        ("dir/test.txt", 2),
        ("dir/subdir/test.txt", 3),
        ("./test.txt", 1),
        ("./dir/test.txt", 2),
    ],
)
def test_file_path_depth(file_path: str, expected_depth: int) -> None:
    """
    Tests calculating the depth of a file path.

    Args:
        file_path (str): The path of the file to check.
        expected_depth (int): The expected depth of the file path.

    Asserts:
        The result of file_path_depth matches the expected depth.
    """
    assert file_path_depth(file_path) == expected_depth


@pytest.mark.parametrize(
    ("file_path", "expected_rel_to_root"),
    [
        ("test.txt", ".."),
        ("dir/test.txt", "../.."),
        ("dir/subdir/test.txt", "../../.."),
        ("./test.txt", ".."),
        ("./dir/test.txt", "../.."),
    ],
)
def test_file_path_rel_to_root(file_path: str, expected_rel_to_root: str) -> None:
    """
    Tests determining the relative path to the root directory.

    Args:
        file_path (str): The path of the file to check.
        expected_rel_to_root (str): The expected relative path to the root directory.

    Asserts:
        The result of file_path_rel_to_root matches the expected relative path.
    """
    assert file_path_rel_to_root(file_path) == expected_rel_to_root
