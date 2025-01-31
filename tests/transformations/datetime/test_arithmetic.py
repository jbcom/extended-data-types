"""Tests for datetime arithmetic operations."""

from __future__ import annotations

from datetime import date, datetime, time, timedelta

import pytest

from extended_data_types.transformations.datetime.arithmetic import (
    add_time,
    ceil_time,
    divide_time,
    floor_time,
    multiply_time,
    round_time,
    subtract_time,
)


def test_add_time() -> None:
    """Test time addition."""
    dt = datetime(2024, 1, 15, 14, 30)

    # Test adding various units
    assert add_time(dt, years=1) == datetime(2025, 1, 15, 14, 30)
    assert add_time(dt, months=1) == datetime(2024, 2, 15, 14, 30)
    assert add_time(dt, weeks=1) == datetime(2024, 1, 22, 14, 30)
    assert add_time(dt, days=1) == datetime(2024, 1, 16, 14, 30)
    assert add_time(dt, hours=1) == datetime(2024, 1, 15, 15, 30)
    assert add_time(dt, minutes=30) == datetime(2024, 1, 15, 15, 0)

    # Test adding multiple units
    assert add_time(dt, days=1, hours=2) == datetime(2024, 1, 16, 16, 30)

    # Test month/year rollover
    assert add_time(dt, months=13) == datetime(2025, 2, 15, 14, 30)

    # Test with date object
    d = date(2024, 1, 15)
    assert add_time(d, days=1) == date(2024, 1, 16)

    # Test with time object
    t = time(14, 30)
    assert add_time(t, hours=1) == time(15, 30)

    # Test invalid input
    with pytest.raises(ValueError):
        add_time(dt, invalid_unit=1)


def test_subtract_time() -> None:
    """Test time subtraction."""
    dt = datetime(2024, 1, 15, 14, 30)

    # Test subtracting various units
    assert subtract_time(dt, years=1) == datetime(2023, 1, 15, 14, 30)
    assert subtract_time(dt, months=1) == datetime(2023, 12, 15, 14, 30)
    assert subtract_time(dt, weeks=1) == datetime(2024, 1, 8, 14, 30)
    assert subtract_time(dt, days=1) == datetime(2024, 1, 14, 14, 30)
    assert subtract_time(dt, hours=1) == datetime(2024, 1, 15, 13, 30)
    assert subtract_time(dt, minutes=30) == datetime(2024, 1, 15, 14, 0)

    # Test subtracting multiple units
    assert subtract_time(dt, days=1, hours=2) == datetime(2024, 1, 14, 12, 30)

    # Test month/year rollback
    assert subtract_time(dt, months=13) == datetime(2022, 12, 15, 14, 30)

    # Test with date object
    d = date(2024, 1, 15)
    assert subtract_time(d, days=1) == date(2024, 1, 14)

    # Test with time object
    t = time(14, 30)
    assert subtract_time(t, hours=1) == time(13, 30)

    # Test invalid input
    with pytest.raises(ValueError):
        subtract_time(dt, invalid_unit=1)


def test_multiply_time() -> None:
    """Test time multiplication."""
    td = timedelta(hours=2, minutes=30)

    # Test basic multiplication
    assert multiply_time(td, 2) == timedelta(hours=5)
    assert multiply_time(td, 0.5) == timedelta(hours=1, minutes=15)

    # Test with negative multiplier
    assert multiply_time(td, -1) == timedelta(hours=-2, minutes=-30)

    # Test with zero
    assert multiply_time(td, 0) == timedelta()

    # Test with large numbers
    assert multiply_time(td, 24) == timedelta(days=2, hours=12)

    # Test invalid input
    with pytest.raises(ValueError):
        multiply_time(td, -0.5)  # If negative fractions not allowed


def test_divide_time() -> None:
    """Test time division."""
    td = timedelta(hours=5)

    # Test basic division
    assert divide_time(td, 2) == timedelta(hours=2, minutes=30)

    # Test division by timedelta
    td2 = timedelta(hours=2, minutes=30)
    assert divide_time(td, td2) == 2.0

    # Test with zero
    with pytest.raises(ValueError):
        divide_time(td, 0)

    # Test with very small numbers
    small_td = divide_time(td, 100)
    assert small_td.total_seconds() == 180  # 3 minutes

    # Test invalid input
    with pytest.raises(ValueError):
        divide_time(td, -2)  # If negative divisors not allowed


def test_round_time() -> None:
    """Test time rounding."""
    dt = datetime(2024, 1, 15, 14, 32)

    # Test rounding to different units
    assert round_time(dt, "hour") == datetime(2024, 1, 15, 15, 0)
    assert round_time(dt, "15min") == datetime(2024, 1, 15, 14, 30)
    assert round_time(dt, "day") == datetime(2024, 1, 16)

    # Test with time object
    t = time(14, 32)
    assert round_time(t, "hour") == time(15, 0)

    # Test with different rounding rules
    assert round_time(dt, "hour", rule="up") == datetime(2024, 1, 15, 15, 0)
    assert round_time(dt, "hour", rule="down") == datetime(2024, 1, 15, 14, 0)

    # Test invalid input
    with pytest.raises(ValueError):
        round_time(dt, "invalid")


def test_floor_time() -> None:
    """Test time floor."""
    dt = datetime(2024, 1, 15, 14, 32)

    # Test floor to different units
    assert floor_time(dt, "hour") == datetime(2024, 1, 15, 14, 0)
    assert floor_time(dt, "15min") == datetime(2024, 1, 15, 14, 30)
    assert floor_time(dt, "day") == datetime(2024, 1, 15)

    # Test with time object
    t = time(14, 32)
    assert floor_time(t, "hour") == time(14, 0)

    # Test invalid input
    with pytest.raises(ValueError):
        floor_time(dt, "invalid")


def test_ceil_time() -> None:
    """Test time ceiling."""
    dt = datetime(2024, 1, 15, 14, 32)

    # Test ceil to different units
    assert ceil_time(dt, "hour") == datetime(2024, 1, 15, 15, 0)
    assert ceil_time(dt, "15min") == datetime(2024, 1, 15, 14, 45)
    assert ceil_time(dt, "day") == datetime(2024, 1, 16)

    # Test with time object
    t = time(14, 32)
    assert ceil_time(t, "hour") == time(15, 0)

    # Test invalid input
    with pytest.raises(ValueError):
        ceil_time(dt, "invalid")
