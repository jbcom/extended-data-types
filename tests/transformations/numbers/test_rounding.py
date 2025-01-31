"""Tests for number rounding operations."""

from __future__ import annotations

import pytest

from extended_data_types.transformations.numbers.rounding import (
    ceiling,
    floor,
    round_number,
    round_significant,
    round_to_fraction,
    round_to_increment,
    truncate,
)


def test_round_number() -> None:
    """Test basic number rounding."""
    assert round_number(3.14159, 2) == 3.14
    assert round_number(3.14159, 0) == 3.0
    assert round_number(3.5, 0) == 4.0
    assert round_number(4.5, 0) == 4.0  # Python 3 rounds to even

    # Test negative decimals
    assert round_number(123.456, -1) == 120.0
    assert round_number(123.456, -2) == 100.0

    # Test rounding modes
    assert round_number(3.5, 0, mode="up") == 4.0
    assert round_number(3.5, 0, mode="down") == 3.0
    assert round_number(3.5, 0, mode="half_up") == 4.0
    assert round_number(3.5, 0, mode="half_down") == 3.0

    # Test invalid input
    with pytest.raises(ValueError):
        round_number(1.23, -10)  # Too many negative decimals


def test_round_to_increment() -> None:
    """Test rounding to specific increments."""
    assert round_to_increment(3.14159, 0.25) == 3.25
    assert round_to_increment(3.14159, 0.5) == 3.0
    assert round_to_increment(3.14159, 1.0) == 3.0

    # Test with different modes
    assert round_to_increment(3.14159, 0.25, mode="up") == 3.25
    assert round_to_increment(3.14159, 0.25, mode="down") == 3.0

    # Test with currency-like values
    assert round_to_increment(1.23, 0.05) == 1.25
    assert round_to_increment(1.22, 0.05) == 1.20

    # Test invalid input
    with pytest.raises(ValueError):
        round_to_increment(1.23, 0)
    with pytest.raises(ValueError):
        round_to_increment(1.23, -0.1)


def test_round_to_fraction() -> None:
    """Test rounding to fractions."""
    assert round_to_fraction(3.14159, 2) == 3.0  # Rounds to 3/1
    assert round_to_fraction(3.14159, 4) == 3.25  # Rounds to 13/4
    assert round_to_fraction(0.33333, 3) == 0.33333  # Rounds to 1/3

    # Test with different denominators
    assert round_to_fraction(0.125, 2) == 0.0  # Rounds to 0/1
    assert round_to_fraction(0.125, 8) == 0.125  # Rounds to 1/8

    # Test invalid input
    with pytest.raises(ValueError):
        round_to_fraction(1.23, 0)
    with pytest.raises(ValueError):
        round_to_fraction(1.23, -2)


def test_round_significant() -> None:
    """Test rounding to significant figures."""
    assert round_significant(3.14159, 3) == 3.14
    assert round_significant(0.0123456, 3) == 0.0123
    assert round_significant(123.456, 3) == 123.0

    # Test with different modes
    assert round_significant(3.14159, 3, mode="up") == 3.15
    assert round_significant(3.14159, 3, mode="down") == 3.14

    # Test with zero
    assert round_significant(0.0, 3) == 0.0

    # Test invalid input
    with pytest.raises(ValueError):
        round_significant(1.23, 0)
    with pytest.raises(ValueError):
        round_significant(1.23, -1)


def test_truncate() -> None:
    """Test number truncation."""
    assert truncate(3.14159, 2) == 3.14
    assert truncate(3.14159, 0) == 3.0
    assert truncate(-3.14159, 2) == -3.14

    # Test negative decimals
    assert truncate(123.456, -1) == 120.0
    assert truncate(123.456, -2) == 100.0

    # Test with zero
    assert truncate(0.0, 2) == 0.0

    # Test invalid input
    with pytest.raises(ValueError):
        truncate(1.23, -10)


def test_ceiling() -> None:
    """Test ceiling operation."""
    assert ceiling(3.14159, 2) == 3.15
    assert ceiling(3.14159, 0) == 4.0
    assert ceiling(-3.14159, 2) == -3.14

    # Test negative decimals
    assert ceiling(123.456, -1) == 130.0
    assert ceiling(123.456, -2) == 200.0

    # Test with zero
    assert ceiling(0.0, 2) == 0.0

    # Test invalid input
    with pytest.raises(ValueError):
        ceiling(1.23, -10)


def test_floor() -> None:
    """Test floor operation."""
    assert floor(3.14159, 2) == 3.14
    assert floor(3.14159, 0) == 3.0
    assert floor(-3.14159, 2) == -3.15

    # Test negative decimals
    assert floor(123.456, -1) == 120.0
    assert floor(123.456, -2) == 100.0

    # Test with zero
    assert floor(0.0, 2) == 0.0

    # Test invalid input
    with pytest.raises(ValueError):
        floor(1.23, -10)
