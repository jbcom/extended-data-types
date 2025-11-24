"""Tests for number formatting operations."""

from __future__ import annotations

import pytest

from extended_data_types.transformations.numbers.format import (
    format_binary,
    format_currency,
    format_hex,
    format_number,
    format_percent,
    format_scientific,
)


def test_format_number() -> None:
    """Test number formatting."""
    assert format_number(1234.5678) == "1,234.57"
    assert format_number(1234.5678, decimals=3) == "1,234.568"
    assert format_number(1234, decimals=0) == "1,234"

    # Test with different separators
    assert format_number(1234.56, thousands=".") == "1.234,56"
    assert format_number(1234.56, decimal=",") == "1,234,56"

    # Test with prefix/suffix
    assert format_number(1234.56, prefix="$") == "$1,234.56"
    assert format_number(1234.56, suffix=" USD") == "1,234.56 USD"

    # Test with padding
    assert format_number(123.45, width=10) == "   123.45"
    assert format_number(123.45, width=10, align="left") == "123.45   "

    # Test with negative numbers
    assert format_number(-1234.56) == "-1,234.56"
    assert format_number(-1234.56, parentheses=True) == "(1,234.56)"


def test_format_currency() -> None:
    """Test currency formatting."""
    assert format_currency(1234.56, "USD") == "$1,234.56"
    assert format_currency(1234.56, "EUR") == "€1,234.56"
    assert format_currency(1234.56, "GBP") == "£1,234.56"

    # Test with different locales
    assert format_currency(1234.56, "EUR", locale="de_DE") == "1.234,56 €"
    assert format_currency(1234.56, "JPY", locale="ja_JP") == "¥1,235"

    # Test with decimals
    assert format_currency(1234.56, "USD", decimals=0) == "$1,235"
    assert format_currency(1234.56, "USD", decimals=3) == "$1,234.560"

    # Test with symbols
    assert format_currency(1234.56, "USD", symbol=False) == "1,234.56 USD"

    # Test invalid currency
    with pytest.raises(ValueError):
        format_currency(1234.56, "INVALID")


def test_format_percent() -> None:
    """Test percentage formatting."""
    assert format_percent(0.1234) == "12.34%"
    assert format_percent(0.1234, decimals=1) == "12.3%"
    assert format_percent(0.1234, decimals=0) == "12%"

    # Test with multiplier
    assert format_percent(12.34, multiply=False) == "12.34%"

    # Test with spacing
    assert format_percent(0.1234, space=True) == "12.34 %"

    # Test with prefix/suffix
    assert format_percent(0.1234, prefix="~") == "~12.34%"
    assert format_percent(0.1234, suffix=" (approx)") == "12.34% (approx)"


def test_format_scientific() -> None:
    """Test scientific notation formatting."""
    assert format_scientific(1234.5678) == "1.23E+03"
    assert format_scientific(0.0001234) == "1.23E-04"

    # Test with precision
    assert format_scientific(1234.5678, precision=4) == "1.2346E+03"
    assert format_scientific(1234.5678, precision=1) == "1.2E+03"

    # Test with different notation
    assert format_scientific(1234.5678, notation="e") == "1.23e+03"
    assert format_scientific(1234.5678, notation="E") == "1.23E+03"

    # Test with sign
    assert format_scientific(1234.5678, sign=True) == "+1.23E+03"
    assert format_scientific(-1234.5678) == "-1.23E+03"


def test_format_binary() -> None:
    """Test binary formatting."""
    assert format_binary(42) == "0b101010"
    assert format_binary(42, prefix=False) == "101010"

    # Test with padding
    assert format_binary(42, width=8) == "0b00101010"
    assert format_binary(42, width=8, prefix=False) == "00101010"

    # Test with grouping
    assert format_binary(42, group=True) == "0b10 1010"
    assert format_binary(42, group=True, prefix=False) == "10 1010"

    # Test negative numbers
    assert format_binary(-42) == "-0b101010"

    # Test invalid input
    with pytest.raises(TypeError):
        format_binary(1.23)


def test_format_hex() -> None:
    """Test hexadecimal formatting."""
    assert format_hex(255) == "0xFF"
    assert format_hex(255, prefix=False) == "FF"

    # Test with case
    assert format_hex(255, upper=False) == "0xff"

    # Test with padding
    assert format_hex(15, width=4) == "0x000F"
    assert format_hex(15, width=4, prefix=False) == "000F"

    # Test with grouping
    assert format_hex(65535, group=True) == "0xFF FF"

    # Test negative numbers
    assert format_hex(-255) == "-0xFF"

    # Test invalid input
    with pytest.raises(TypeError):
        format_hex(1.23)
