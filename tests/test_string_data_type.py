"""
This module contains test functions for verifying the functionality of various string operations using the
`extended_data_types` package. It includes fixtures for sample keys, and tests for sanitizing keys, truncating strings,
modifying the case of the first character, checking URLs, titleizing names, and converting strings to boolean values.

Fixtures:
    - test_key: Provides a sample key with invalid characters for testing.
    - sanitized_key: Provides the expected sanitized key for testing.

Functions:
    - test_sanitize_key: Tests sanitizing a key by removing invalid characters.
    - test_truncate: Tests truncating a string to a specified length.
    - test_lower_first_char: Tests converting the first character of a string to lowercase.
    - test_upper_first_char: Tests converting the first character of a string to uppercase.
    - test_is_url: Tests checking if a string is a valid URL.
    - test_titleize_name: Tests converting camelCase names to title case.
    - test_strtobool: Tests converting a string to a boolean value.
    - test_removeprefix: Tests removing a prefix from a string.
    - test_removesuffix: Tests removing a suffix from a string.
"""

from __future__ import annotations

import pytest

from extended_data_types.string_data_type import (
    is_url,
    lower_first_char,
    removeprefix,
    removesuffix,
    sanitize_key,
    strtobool,
    titleize_name,
    truncate,
    upper_first_char,
)


@pytest.fixture()
def test_key() -> str:
    """
    Provides a sample key with invalid characters for testing.

    Returns:
        str: A sample key with invalid characters.
    """
    return "key-with*invalid_chars"


@pytest.fixture()
def sanitized_key() -> str:
    """
    Provides the expected sanitized key for testing.

    Returns:
        str: The expected sanitized key.
    """
    return "key_with_invalid_chars"


def test_sanitize_key(test_key: str, sanitized_key: str) -> None:
    """
    Tests sanitizing a key by removing invalid characters.

    Args:
        test_key (str): A sample key provided by the fixture.
        sanitized_key (str): The expected sanitized key provided by the fixture.

    Asserts:
        The result of sanitize_key matches the expected sanitized key.
    """
    assert sanitize_key(test_key) == sanitized_key


def test_truncate() -> None:
    """
    Tests truncating a string to a specified length.

    Asserts:
        The result of truncate matches the expected truncated string.
    """
    assert truncate("This is a long message", 10) == "This is..."
    assert truncate("Short msg", 10) == "Short msg"


def test_lower_first_char() -> None:
    """
    Tests converting the first character of a string to lowercase.

    Asserts:
        The result of lower_first_char matches the expected string with the first character in lowercase.
    """
    assert lower_first_char("Hello") == "hello"
    assert lower_first_char("") == ""


def test_upper_first_char() -> None:
    """
    Tests converting the first character of a string to uppercase.

    Asserts:
        The result of upper_first_char matches the expected string with the first character in uppercase.
    """
    assert upper_first_char("hello") == "Hello"
    assert upper_first_char("") == ""


def test_is_url() -> None:
    """
    Tests checking if a string is a valid URL.

    Asserts:
        The result of is_url is True for valid URLs and False for invalid URLs.
    """
    assert is_url("https://example.com") is True
    assert is_url("not_a_url") is False


def test_titleize_name() -> None:
    """
    Tests converting camelCase names to title case.

    Asserts:
        The result of titleize_name matches the expected title case string.
    """
    assert titleize_name("camelCaseName") == "Camel Case Name"


def test_strtobool() -> None:
    """
    Tests converting a string to a boolean value.

    Asserts:
        The result of strtobool is True for truthy strings, False for falsy strings, and raises a ValueError for invalid strings if specified.
    """
    assert strtobool("yes") is True
    assert strtobool("no") is False
    assert strtobool("invalid") is None
    with pytest.raises(ValueError, match=r"invalid truth value 'invalid'"):
        strtobool("invalid", raise_on_error=True)


def test_removeprefix() -> None:
    """
    Tests removing a prefix from a string.

    Asserts:
        The result of removeprefix matches the expected string with the prefix removed.
    """
    assert removeprefix("test_string", "test_") == "string"
    assert removeprefix("string", "test_") == "string"
    assert removeprefix("test_string", "") == "test_string"


def test_removesuffix() -> None:
    """
    Tests removing a suffix from a string.

    Asserts:
        The result of removesuffix matches the expected string with the suffix removed.
    """
    assert removesuffix("test_string", "_string") == "test"
    assert removesuffix("test", "_string") == "test"
    assert removesuffix("test_string", "") == "test_string"
