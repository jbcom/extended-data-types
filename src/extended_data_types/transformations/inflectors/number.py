"""Number inflection utilities.

This module provides comprehensive number inflection operations:
- Word conversion
- Ordinal numbers
- Currency formatting
- Scientific notation
- Roman numerals
"""

from __future__ import annotations

import roman
from num2words import num2words
from typing import Any

from extended_data_types.core.types import convert_special_types
from extended_data_types.number.types import ExtendedNumber


def to_words(number: int | float) -> str:
    """Convert number to words.

    Args:
        number: Number to convert

    Examples:
        >>> to_words(42)
        'forty-two'
        >>> to_words(3.14)
        'three point one four'
    """
    return num2words(number)


def to_ordinal_words(number: int) -> str:
    """Convert number to ordinal words.

    Args:
        number: Number to convert

    Examples:
        >>> to_ordinal_words(1)
        'first'
        >>> to_ordinal_words(42)
        'forty-second'
    """
    return num2words(number, ordinal=True)


def to_currency(amount: float, currency: str = "USD") -> str:
    """Format number as currency.

    Args:
        amount: Amount to format
        currency: Currency code

    Examples:
        >>> to_currency(42.50)
        'forty-two point five zero dollars'
    """
    return num2words(amount, to="currency", currency=currency)


def to_year(number: int) -> str:
    """Convert number to year format.

    Args:
        number: Year number

    Examples:
        >>> to_year(1984)
        'nineteen eighty-four'
    """
    return num2words(number, to="year")


def to_scientific_notation(number: float) -> str:
    """Format number in scientific notation.

    Args:
        number: Number to format

    Examples:
        >>> to_scientific_notation(1234.56)
        '1.23456e+03'
    """
    return f"{number:e}"


def to_roman_numeral(number: int) -> str:
    """Convert number to Roman numeral.

    Args:
        number: Number to convert (1-3999)

    Examples:
        >>> to_roman_numeral(42)
        'XLII'
    """
    return roman.toRoman(number)


def from_roman_numeral(numeral: str) -> int:
    """Convert Roman numeral to number.

    Args:
        numeral: Roman numeral string

    Examples:
        >>> from_roman_numeral('XLII')
        42
    """
    return roman.fromRoman(numeral)
