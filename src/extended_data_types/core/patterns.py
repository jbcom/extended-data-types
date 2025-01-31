"""Core pattern matching and validation utilities.

This module provides regular expression patterns and validation utilities for
common string formats, including:
- File paths and extensions
- URLs and URIs
- Email addresses
- Version strings
- UUIDs
- Common data formats (dates, numbers, etc.)
"""

from __future__ import annotations

import re

from typing import Final


# File path patterns
WINDOWS_PATH_PATTERN: Final = re.compile(
    r'^[a-zA-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*$'
)
"""Pattern matching valid Windows file paths."""

UNIX_PATH_PATTERN: Final = re.compile(r"^(/[^/\0]+)*/?$")
"""Pattern matching valid Unix file paths."""

FILE_EXTENSION_PATTERN: Final = re.compile(r"\.([^./\\]+)$")
"""Pattern matching file extensions."""

# URL and URI patterns
URL_PATTERN: Final = re.compile(
    r"^(?:http[s]?://)?"  # protocol
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain
    r"localhost|"  # localhost
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # IP
    r"(?::\d+)?"  # port
    r"(?:/?|[/?]\S+)$",  # path
    re.IGNORECASE,
)
"""Pattern matching URLs including optional protocol."""

URI_PATTERN: Final = re.compile(
    r"^[a-z][a-z0-9+.-]*:"  # scheme
    r'[^"\s<>{}|\\^[\]`]*$',  # remainder
    re.IGNORECASE,
)
"""Pattern matching URIs."""

# Email patterns
EMAIL_PATTERN: Final = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
"""Pattern matching email addresses."""

# Version patterns
SEMVER_PATTERN: Final = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)
"""Pattern matching semantic version strings."""

PEP440_VERSION_PATTERN: Final = re.compile(
    r"^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|c|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?$"
)
"""Pattern matching PEP 440 version strings."""

# UUID patterns
UUID_PATTERN: Final = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE
)
"""Pattern matching UUIDs."""

# Data format patterns
DATE_ISO_PATTERN: Final = re.compile(
    r"^\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)?$"
)
"""Pattern matching ISO format dates and datetimes."""

NUMBER_PATTERN: Final = re.compile(r"^[+-]?(\d*\.)?\d+([eE][+-]?\d+)?$")
"""Pattern matching numeric strings including scientific notation."""

BOOLEAN_PATTERN: Final = re.compile(
    r"^(?:true|false|yes|no|1|0|on|off)$", re.IGNORECASE
)
"""Pattern matching common boolean string representations."""


# Validation functions
def is_valid_path(path: str) -> bool:
    """Check if string is a valid file path.

    Args:
        path: String to check

    Returns:
        True if string is a valid path
    """
    return bool(WINDOWS_PATH_PATTERN.match(path) or UNIX_PATH_PATTERN.match(path))


def is_valid_url(url: str) -> bool:
    """Check if string is a valid URL.

    Args:
        url: String to check

    Returns:
        True if string is a valid URL
    """
    return bool(URL_PATTERN.match(url))


def is_valid_email(email: str) -> bool:
    """Check if string is a valid email address.

    Args:
        email: String to check

    Returns:
        True if string is a valid email
    """
    return bool(EMAIL_PATTERN.match(email))


def is_valid_version(version: str, pep440: bool = False) -> bool:
    """Check if string is a valid version string.

    Args:
        version: String to check
        pep440: Whether to check PEP 440 format

    Returns:
        True if string is a valid version
    """
    pattern = PEP440_VERSION_PATTERN if pep440 else SEMVER_PATTERN
    return bool(pattern.match(version))


def is_valid_uuid(uuid: str) -> bool:
    """Check if string is a valid UUID.

    Args:
        uuid: String to check

    Returns:
        True if string is a valid UUID
    """
    return bool(UUID_PATTERN.match(uuid))


def is_valid_date(date: str) -> bool:
    """Check if string is a valid ISO format date.

    Args:
        date: String to check

    Returns:
        True if string is a valid date
    """
    return bool(DATE_ISO_PATTERN.match(date))


def is_valid_number(number: str) -> bool:
    """Check if string is a valid number.

    Args:
        number: String to check

    Returns:
        True if string is a valid number
    """
    return bool(NUMBER_PATTERN.match(number))


def is_valid_boolean(value: str) -> bool:
    """Check if string is a valid boolean representation.

    Args:
        value: String to check

    Returns:
        True if string is a valid boolean
    """
    return bool(BOOLEAN_PATTERN.match(value))
