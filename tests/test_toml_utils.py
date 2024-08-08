"""Tests for TOML Utilities Module.

This module provides unit tests for the `toml_utils` module, verifying the correct
functionality of TOML encoding and decoding using the tomlkit library.
"""

from __future__ import annotations

import datetime
import pathlib

from typing import Any

import pytest
import tomlkit

from extended_data_types.toml_utils import decode_toml, encode_toml


@pytest.mark.parametrize(
    ("toml_string", "expected"),
    [
        ('title = "TOML Example"', {"title": "TOML Example"}),
        (
            """
                [owner]
                name = "Tom Preston-Werner"
                dob = 1979-05-27T07:32:00Z
                """,
            {
                "owner": {
                    "name": "Tom Preston-Werner",
                    "dob": "1979-05-27T07:32:00Z",
                },
            },
        ),
        (
            """
                fruit = ["apple", "orange", "banana"]
                """,
            {"fruit": ["apple", "orange", "banana"]},
        ),
    ],
)
def test_decode_toml(toml_string: str, expected: dict[str, Any]) -> None:
    """Tests the decode_toml function.

    This test verifies that the `decode_toml` function correctly decodes TOML strings
    into their respective Python dictionary representations.

    Args:
        toml_string (str): The TOML string to decode.
        expected (dict[str, Any]): The expected Python dictionary output.
    """
    result = decode_toml(toml_string)
    assert result == expected, f"Expected {expected}, but got {result}"


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        ({"title": "TOML Example"}, 'title = "TOML Example"\n'),
        (
            {"owner": {"name": "Tom Preston-Werner", "dob": "1979-05-27T07:32:00Z"}},
            '[owner]\nname = "Tom Preston-Werner"\ndob = 1979-05-27T07:32:00Z\n',
        ),
        (
            {"fruit": ["apple", "orange", "banana"]},
            'fruit = ["apple", "orange", "banana"]\n',
        ),
    ],
)
def test_encode_toml(data: dict[str, Any], expected: str) -> None:
    """Tests the encode_toml function.

    This test verifies that the `encode_toml` function correctly encodes Python dictionaries
    into their respective TOML string representations.

    Args:
        data (dict[str, Any]): The Python dictionary to encode.
        expected (str): The expected TOML string output.
    """
    result = encode_toml(data)
    assert result == expected, f"Expected {expected}, but got {result}"


def test_decode_toml_invalid_format() -> None:
    """Tests decode_toml with invalid TOML format.

    This test checks that the `decode_toml` function raises a `tomlkit.exceptions.ParseError`
    when provided with an invalid TOML string.
    """
    invalid_toml = "title = 'Unclosed quote"
    with pytest.raises(tomlkit.exceptions.ParseError, match="ParseError"):
        decode_toml(invalid_toml)


def test_encode_toml_with_special_types() -> None:
    """Tests encode_toml with special types that require conversion.

    This test verifies that the `encode_toml` function correctly handles Python types
    that are not directly supported by TOML, such as datetime and pathlib.Path.
    """
    data = {
        "path": pathlib.Path("/some/path"),
        "date": datetime.datetime(2023, 8, 28, 12, 30, tzinfo=datetime.timezone.utc),
    }
    result = encode_toml(data)
    assert 'path = "/some/path"\n' in result, f"Unexpected path encoding: {result}"
    assert (
        "date = 2023-08-28T12:30:00+00:00\n" in result
    ), f"Unexpected date encoding: {result}"
