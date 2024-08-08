"""This module provides utilities for string manipulation and validation.

It includes functions to sanitize keys, truncate messages, manipulate character
cases, validate URLs, convert camelCase to TitleCase, and convert string representations
of truth to boolean values.
"""

from __future__ import annotations

import inflection
import validators

from .stack_utils import current_python_version_is_at_least


def sanitize_key(key: str, delim: str = "_") -> str:
    """Sanitizes a key by replacing non-alphanumeric characters with a delimiter.

    Args:
        key (str): The key to sanitize.
        delim (str): The delimiter to replace non-alphanumeric characters with. Defaults to "_".

    Returns:
        str: The sanitized key.
    """
    return "".join(x if (x.isalnum() or x == delim) else delim for x in key)


def truncate(msg: str, max_length: int, ender: str = "...") -> str:
    """Truncates a message to a maximum length, appending an ender if truncated.

    Args:
        msg (str): The message to truncate.
        max_length (int): The maximum length of the truncated message.
        ender (str): The string to append to the truncated message. Defaults to "...".

    Returns:
        str: The truncated message.
    """
    if len(msg) <= max_length:
        return msg
    return msg[: max_length - len(ender)] + ender


def lower_first_char(inp: str) -> str:
    """Converts the first character of a string to lowercase.

    Args:
        inp (str): The input string.

    Returns:
        str: The string with the first character in lowercase.
    """
    return inp[:1].lower() + inp[1:] if inp else ""


def upper_first_char(inp: str) -> str:
    """Converts the first character of a string to uppercase.

    Args:
        inp (str): The input string.

    Returns:
        str: The string with the first character in uppercase.
    """
    return inp[:1].upper() + inp[1:] if inp else ""


def is_url(url: str) -> bool:
    """Checks if the given string is a valid URL.

    Args:
        url (str): The string to check.

    Returns:
        bool: True if the file path is a valid URL, False otherwise.
    """
    return validators.url(url.strip()) is True


def titleize_name(name: str) -> str:
    """Converts a camelCase name to a TitleCase name.

    Args:
        name (str): The camelCase name.

    Returns:
        str: The TitleCase name.
    """
    return inflection.titleize(inflection.underscore(name))


def strtobool(val: str | bool | None, raise_on_error: bool = False) -> bool | None:
    """Converts a string representation of truth to boolean.

    Args:
        val (str | bool | None): The value to convert.
        raise_on_error (bool): Whether to raise an error on invalid value. Defaults to False.

    Returns:
        bool | None: The converted boolean value, or None if invalid and raise_on_error is False.
    """
    if isinstance(val, bool) or val is None:
        return val

    if isinstance(val, str):
        val = val.lower()
        if val in ("y", "yes", "t", "true", "on", "1"):
            return True
        if val in ("n", "no", "f", "false", "off", "0"):
            return False

    if raise_on_error:
        error_msg = f"invalid truth value {val!r}"
        raise ValueError(error_msg)

    return None


def removeprefix(string: str, prefix: str) -> str:
    """Removes the specified prefix from the string if present.

    For Python versions less than 3.9, the function mimics the behavior of
    str.removeprefix.

    Args:
        string (str): The string from which to remove the prefix.
        prefix (str): The prefix to remove.

    Returns:
        str: The string with the prefix removed if it was present, otherwise the original string.
    """
    if current_python_version_is_at_least(9):
        return string.removeprefix(prefix)

    if prefix and string.startswith(prefix):
        string = string[len(prefix) :]

    return string


def removesuffix(string: str, suffix: str) -> str:
    """Removes the specified suffix from the string if present.

    For Python versions less than 3.9, the function mimics the behavior of
    str.removesuffix.

    Args:
        string (str): The string from which to remove the suffix.
        suffix (str): The suffix to remove.

    Returns:
        str: The string with the suffix removed if it was present, otherwise the original string.
    """
    if current_python_version_is_at_least(9):
        return string.removesuffix(suffix)

    if suffix and string.endswith(suffix):
        string = string[: -len(suffix)]

    return string
