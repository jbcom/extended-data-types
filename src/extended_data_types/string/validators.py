"""String validation utilities.

This module provides comprehensive validation functions for string formats and patterns:

Key Validators:
- Pattern matching with regular expressions
- Date and time format validation
- URL and email validation
- Numeric string validation
- Path string validation
- Case validation
- Length validation
- Character set validation
- IP address validation
- Domain name validation
- UUID validation
- Credit card validation
- ISBN validation
- MAC address validation
- IBAN validation
- Slug validation

Validation Features:
- Detailed validation results
- Custom error messages
- Validation metadata
- Pattern compilation caching
- Performance optimizations
- Extensible validation rules

Pattern Types:
- Regular expressions
- Glob patterns
- Simple wildcards
- Custom patterns
- Composite patterns

Error Handling:
- Validation context preservation
- Detailed error messages
- Pattern syntax validation
- Performance warnings
- Resource cleanup

Usage Examples:
    >>> result = validate_pattern("test123", r"^[a-z]+\d+$")
    >>> print(result.valid, result.message)
    True None

    >>> result = validate_email("user@example.com")
    >>> print(result.valid, result.message)
    True None

    >>> result = validate_url("https://example.com")
    >>> print(result.valid, result.message)
    True None
"""

from __future__ import annotations

import json
import re
import uuid
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import validators

from extended_data_types.core.patterns import DATE_PATTERN, TIME_PATTERN

from .types import ExtendedString


@dataclass
class ValidationResult:
    """Result of a validation operation.

    Attributes:
        valid: Whether the validation passed
        message: Optional error message if validation failed
        details: Optional dictionary of additional validation details
    """
    valid: bool
    message: str | None = None
    details: dict[str, Any] | None = None


def validate_pattern(text: str, pattern: str | re.Pattern, flags: int = 0) -> ValidationResult:
    """Validate string matches a pattern.

    Args:
        text: The string to validate
        pattern: Regular expression pattern to match against
        flags: Regular expression flags

    Returns:
        ValidationResult containing the validation outcome

    Example:
        >>> result = validate_pattern("test123", r"^[a-z]+\d+$")
        >>> result.valid
        True
    """
    if isinstance(pattern, str):
        pattern = re.compile(pattern, flags)
    
    matches = bool(pattern.match(text))
    return ValidationResult(
        matches,
        None if matches else "String does not match pattern",
        {"pattern": pattern.pattern}
    )


def validate_date(text: str) -> ValidationResult:
    """Validate string is a valid date.

    Args:
        text: The string to validate

    Returns:
        ValidationResult containing the validation outcome

    Example:
        >>> result = validate_date("2024-01-15")
        >>> result.valid
        True
    """
    matches = bool(DATE_PATTERN.match(text))
    return ValidationResult(
        matches,
        None if matches else "Invalid date format"
    )


def validate_time(text: str) -> ValidationResult:
    """Validate string is a valid time.

    Args:
        text: The string to validate

    Returns:
        ValidationResult containing the validation outcome

    Example:
        >>> result = validate_time("14:30:00")
        >>> result.valid
        True
    """
    matches = bool(TIME_PATTERN.match(text))
    return ValidationResult(
        matches,
        None if matches else "Invalid time format"
    )


def validate_length(
    text: str,
    min_length: int | None = None,
    max_length: int | None = None,
) -> ValidationResult:
    """Validate string length is within specified range.

    Args:
        text: String to validate.
        min_length: Minimum allowed length.
        max_length: Maximum allowed length.

    Returns:
        ValidationResult indicating length validity.
    """
    length = len(text)
    if min_length is not None and length < min_length:
        return ValidationResult(
            False,
            f"String length {length} is less than minimum {min_length}",
            {"actual": length, "min": min_length}
        )
    if max_length is not None and length > max_length:
        return ValidationResult(
            False,
            f"String length {length} exceeds maximum {max_length}",
            {"actual": length, "max": max_length}
        )
    return ValidationResult(True)


def validate_url(url: str, public: bool = False) -> ValidationResult:
    """Validate string is a valid URL.

    Args:
        url: The string to validate
        public: If True, requires URL to be publicly accessible

    Returns:
        ValidationResult containing the validation outcome

    Example:
        >>> result = validate_url("https://example.com")
        >>> result.valid
        True
    """
    is_valid = bool(validators.url(url, public=public))
    return ValidationResult(
        is_valid,
        None if is_valid else "Invalid URL format"
    )


def validate_email(email: str) -> ValidationResult:
    """Validate string is a valid email address.

    Args:
        email: The string to validate

    Returns:
        ValidationResult containing the validation outcome

    Example:
        >>> result = validate_email("user@example.com")
        >>> result.valid
        True
    """
    is_valid = bool(validators.email(email))
    return ValidationResult(
        is_valid,
        None if is_valid else "Invalid email format"
    )


def validate_ipv4(ip: str) -> ValidationResult:
    """Validate string is a valid IPv4 address.

    Args:
        ip: The string to validate

    Returns:
        ValidationResult containing the validation outcome

    Example:
        >>> result = validate_ipv4("192.168.1.1")
        >>> result.valid
        True
    """
    is_valid = bool(validators.ipv4(ip))
    return ValidationResult(
        is_valid,
        None if is_valid else "Invalid IPv4 address"
    )


def validate_ipv6(ip: str) -> ValidationResult:
    """Validate string is a valid IPv6 address.

    Args:
        ip: The string to validate

    Returns:
        ValidationResult containing the validation outcome

    Example:
        >>> result = validate_ipv6("2001:db8::1")
        >>> result.valid
        True
    """
    is_valid = bool(validators.ipv6(ip))
    return ValidationResult(
        is_valid,
        None if is_valid else "Invalid IPv6 address"
    )


def validate_domain(domain: str) -> ValidationResult:
    """Validate string is a valid domain name.

    Args:
        domain: The string to validate

    Returns:
        ValidationResult containing the validation outcome

    Example:
        >>> result = validate_domain("example.com")
        >>> result.valid
        True
    """
    is_valid = bool(validators.domain(domain))
    return ValidationResult(
        is_valid,
        None if is_valid else "Invalid domain name"
    )


def validate_mac_address(mac: str) -> ValidationResult:
    """Validate string is a valid MAC address.

    Args:
        mac: The string to validate

    Returns:
        ValidationResult containing the validation outcome

    Example:
        >>> result = validate_mac_address("00:11:22:33:44:55")
        >>> result.valid
        True
    """
    is_valid = bool(validators.mac_address(mac))
    return ValidationResult(
        is_valid,
        None if is_valid else "Invalid MAC address"
    )


def validate_slug(slug: str) -> ValidationResult:
    """Validate string is a valid slug.

    Args:
        slug: The string to validate

    Returns:
        ValidationResult containing the validation outcome

    Example:
        >>> result = validate_slug("this-is-a-slug")
        >>> result.valid
        True
    """
    is_valid = bool(validators.slug(slug))
    return ValidationResult(
        is_valid,
        None if is_valid else "Invalid slug format"
    )


def validate_uuid(text: str, version: int | None = None) -> ValidationResult:
    """Validate string is a valid UUID.

    Args:
        text: String to validate.
        version: Optional UUID version to validate against.

    Returns:
        ValidationResult indicating UUID validity.
    """
    try:
        uuid_obj = uuid.UUID(text)
        if version is not None and uuid_obj.version != version:
            return ValidationResult(
                False,
                f"UUID version {uuid_obj.version} does not match required version {version}",
                {"actual_version": uuid_obj.version, "required_version": version}
            )
        return ValidationResult(True)
    except ValueError as e:
        return ValidationResult(False, str(e))


def validate_json(text: str) -> ValidationResult:
    """Validate string is valid JSON.

    Args:
        text: String to validate.

    Returns:
        ValidationResult indicating JSON validity.
    """
    try:
        json.loads(text)
        return ValidationResult(True)
    except json.JSONDecodeError as e:
        return ValidationResult(False, str(e))


def validate_xml(text: str) -> ValidationResult:
    """Validate string is valid XML.

    Args:
        text: String to validate.

    Returns:
        ValidationResult indicating XML validity.
    """
    try:
        ET.fromstring(text)
        return ValidationResult(True)
    except ET.ParseError as e:
        return ValidationResult(False, str(e))


def validate_path(
    path: str,
    must_exist: bool = False,
    file_only: bool = False,
    dir_only: bool = False,
) -> ValidationResult:
    """Validate string is a valid filesystem path.

    Args:
        path: String to validate.
        must_exist: Whether the path must exist.
        file_only: Whether the path must be a file.
        dir_only: Whether the path must be a directory.

    Returns:
        ValidationResult indicating path validity.
    """
    try:
        path_obj = Path(path)
        if must_exist and not path_obj.exists():
            return ValidationResult(False, "Path does not exist")
        if file_only and not path_obj.is_file():
            return ValidationResult(False, "Path is not a file")
        if dir_only and not path_obj.is_dir():
            return ValidationResult(False, "Path is not a directory")
        return ValidationResult(True)
    except Exception as e:
        return ValidationResult(False, str(e))


def validate_numeric(text: str) -> ValidationResult:
    """Validate string contains only numeric characters.

    Args:
        text: String to validate.

    Returns:
        ValidationResult indicating numeric validity.
    """
    is_numeric = text.isdigit()
    return ValidationResult(
        is_numeric,
        None if is_numeric else "String contains non-numeric characters"
    )


def validate_alphanumeric(
    text: str,
    allow_spaces: bool = False,
) -> ValidationResult:
    """Validate string contains only alphanumeric characters.

    Args:
        text: String to validate.
        allow_spaces: Whether to allow space characters.

    Returns:
        ValidationResult indicating alphanumeric validity.
    """
    if allow_spaces:
        is_valid = all(c.isalnum() or c.isspace() for c in text)
    else:
        is_valid = text.isalnum()
    
    return ValidationResult(
        is_valid,
        None if is_valid else "String contains non-alphanumeric characters"
    )


def validate_printable(text: str) -> ValidationResult:
    """Validate string contains only printable characters.

    Args:
        text: String to validate.

    Returns:
        ValidationResult indicating printable validity.
    """
    is_printable = text.isprintable()
    return ValidationResult(
        is_printable,
        None if is_printable else "String contains non-printable characters"
    ) 