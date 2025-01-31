"""Tests for datetime validation operations."""

from __future__ import annotations

from datetime import date, datetime, time

import pytest

from extended_data_types.transformations.datetime.validation import (
    is_valid_date,
    is_valid_datetime,
    is_valid_format,
    is_valid_time,
    is_valid_timezone,
    normalize_date,
)


def test_is_valid_date() -> None:
    """Test date validation."""
    # Test valid dates
    assert is_valid_date(2024, 1, 15) is True
    assert is_valid_date(2024, 2, 29) is True  # Leap year
    assert is_valid_date(2000, 2, 29) is True  # Leap year

    # Test invalid dates
    assert is_valid_date(2024, 2, 30) is False
    assert is_valid_date(2023, 2, 29) is False  # Not a leap year
    assert is_valid_date(2024, 13, 1) is False
    assert is_valid_date(2024, 1, 32) is False

    # Test with string input
    assert is_valid_date("2024", "01", "15") is True
    assert is_valid_date("2024", "02", "30") is False

    # Test with date object
    d = date(2024, 1, 15)
    assert is_valid_date(d) is True

    # Test with invalid types
    with pytest.raises(TypeError):
        is_valid_date(None, 1, 15)
    with pytest.raises(TypeError):
        is_valid_date("invalid", 1, 15)


def test_is_valid_time() -> None:
    """Test time validation."""
    # Test valid times
    assert is_valid_time(14, 30, 45) is True
    assert is_valid_time(23, 59, 59, 999999) is True
    assert is_valid_time(0, 0, 0) is True

    # Test invalid times
    assert is_valid_time(24, 0, 0) is False
    assert is_valid_time(23, 60, 0) is False
    assert is_valid_time(23, 59, 60) is False
    assert is_valid_time(23, 59, 59, 1000000) is False

    # Test with string input
    assert is_valid_time("14", "30", "45") is True
    assert is_valid_time("24", "00", "00") is False

    # Test with time object
    t = time(14, 30, 45)
    assert is_valid_time(t) is True

    # Test with invalid types
    with pytest.raises(TypeError):
        is_valid_time(None, 30, 45)
    with pytest.raises(TypeError):
        is_valid_time("invalid", 30, 45)


def test_is_valid_datetime() -> None:
    """Test datetime validation."""
    # Test valid datetimes
    assert is_valid_datetime(2024, 1, 15, 14, 30, 45) is True
    assert is_valid_datetime(2024, 2, 29, 23, 59, 59, 999999) is True

    # Test invalid datetimes
    assert is_valid_datetime(2024, 2, 30, 14, 30, 45) is False
    assert is_valid_datetime(2024, 1, 15, 24, 0, 0) is False

    # Test with string input
    assert is_valid_datetime("2024", "01", "15", "14", "30", "45") is True
    assert is_valid_datetime("2024", "02", "30", "14", "30", "45") is False

    # Test with datetime object
    dt = datetime(2024, 1, 15, 14, 30, 45)
    assert is_valid_datetime(dt) is True

    # Test with invalid types
    with pytest.raises(TypeError):
        is_valid_datetime(None, 1, 15, 14, 30, 45)
    with pytest.raises(TypeError):
        is_valid_datetime("invalid", 1, 15, 14, 30, 45)


def test_is_valid_timezone() -> None:
    """Test timezone validation."""
    # Test valid timezones
    assert is_valid_timezone("UTC") is True
    assert is_valid_timezone("US/Eastern") is True
    assert is_valid_timezone("Europe/London") is True

    # Test invalid timezones
    assert is_valid_timezone("Invalid/Timezone") is False
    assert is_valid_timezone("ABC/XYZ") is False
    assert is_valid_timezone("") is False

    # Test with offset format
    assert is_valid_timezone("UTC+01:00") is True
    assert is_valid_timezone("UTC-05:00") is True
    assert is_valid_timezone("UTC+0100") is True
    assert is_valid_timezone("UTC+25:00") is False

    # Test with invalid types
    assert is_valid_timezone(None) is False
    assert is_valid_timezone(123) is False


def test_is_valid_format() -> None:
    """Test datetime format validation."""
    # Test valid formats
    assert is_valid_format("%Y-%m-%d") is True
    assert is_valid_format("%H:%M:%S") is True
    assert is_valid_format("%Y-%m-%d %H:%M:%S") is True

    # Test invalid formats
    assert is_valid_format("%invalid") is False
    assert is_valid_format("") is False
    assert is_valid_format("YYYY-MM-DD") is False

    # Test with sample date
    dt = datetime(2024, 1, 15, 14, 30, 45)
    assert is_valid_format("%Y-%m-%d", dt) is True
    assert is_valid_format("%H:%M:%S", dt) is True

    # Test with invalid types
    assert is_valid_format(None) is False
    assert is_valid_format(123) is False


def test_normalize_date() -> None:
    """Test date normalization."""
    # Test basic normalization
    assert normalize_date(2024, 13, 1) == date(2025, 1, 1)
    assert normalize_date(2024, 1, 32) == date(2024, 2, 1)

    # Test negative values
    assert normalize_date(2024, -1, 1) == date(2023, 11, 1)
    assert normalize_date(2024, 1, -1) == date(2023, 12, 31)

    # Test with large numbers
    assert normalize_date(2024, 1, 366) == date(2025, 1, 1)
    assert normalize_date(2024, 25, 1) == date(2026, 1, 1)

    # Test with string input
    assert normalize_date("2024", "13", "1") == date(2025, 1, 1)

    # Test with date object
    d = date(2024, 1, 15)
    assert normalize_date(d) == date(2024, 1, 15)

    # Test with invalid types
    with pytest.raises(TypeError):
        normalize_date(None, 1, 15)
    with pytest.raises(TypeError):
        normalize_date("invalid", 1, 15)
