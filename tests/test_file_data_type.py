from __future__ import annotations, division, print_function, unicode_literals

import pytest

from extended_data_types.file_data_type import (
    file_path_depth,
    file_path_rel_to_root,
    get_encoding_for_file_path,
    match_file_extensions,
)


@pytest.mark.parametrize(
    "file_path, allowed_extensions, denied_extensions, expected",
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
    file_path, allowed_extensions, denied_extensions, expected
):
    assert (
        match_file_extensions(file_path, allowed_extensions, denied_extensions)
        == expected
    )


@pytest.mark.parametrize(
    "file_path, expected_encoding",
    [
        ("test.yaml", "yaml"),
        ("test.yml", "yaml"),
        ("test.json", "json"),
        ("test.txt", "raw"),
        ("test", "raw"),
    ],
)
def test_get_encoding_for_file_path(file_path, expected_encoding):
    assert get_encoding_for_file_path(file_path) == expected_encoding


@pytest.mark.parametrize(
    "file_path, expected_depth",
    [
        ("test.txt", 1),
        ("dir/test.txt", 2),
        ("dir/subdir/test.txt", 3),
        ("./test.txt", 1),
        ("./dir/test.txt", 2),
    ],
)
def test_file_path_depth(file_path, expected_depth):
    assert file_path_depth(file_path) == expected_depth


@pytest.mark.parametrize(
    "file_path, expected_rel_to_root",
    [
        ("test.txt", ".."),
        ("dir/test.txt", "../.."),
        ("dir/subdir/test.txt", "../../.."),
        ("./test.txt", ".."),
        ("./dir/test.txt", "../.."),
    ],
)
def test_file_path_rel_to_root(file_path, expected_rel_to_root):
    assert file_path_rel_to_root(file_path) == expected_rel_to_root
