"""Number notation transformation utilities."""

from __future__ import annotations

from typing import Literal

import roman

NotationType = Literal["scientific", "engineering", "percent", "roman"]


def to_scientific(
    number: float,
    precision: int = 2
) -> str:
    """Convert to scientific notation.

    Args:
        number: Number to convert
        precision: Decimal precision

    Returns:
        Scientific notation string

    Example:
        >>> to_scientific(1234.5678)
        '1.23e+3'
    """
    return f"{number:.{precision}e}"


def to_engineering(
    number: float,
    precision: int = 2
) -> str:
    """Convert to engineering notation.

    Args:
        number: Number to convert
        precision: Decimal precision

    Returns:
        Engineering notation string

    Example:
        >>> to_engineering(1234.5678)
        '1.23E+03'
    """
    return f"{number:.{precision}E}"


def to_percent(
    number: float,
    precision: int = 2
) -> str:
    """Convert to percentage.

    Args:
        number: Number to convert
        precision: Decimal precision

    Returns:
        Percentage string

    Example:
        >>> to_percent(0.1234)
        '12.34%'
    """
    return f"{number * 100:.{precision}f}%"


def to_roman(number: int) -> str:
    """Convert to Roman numerals.

    Args:
        number: Number to convert

    Returns:
        Roman numeral string

    Example:
        >>> to_roman(42)
        'XLII'

    Raises:
        ValueError: If number is not in range 1-3999
    """
    return roman.toRoman(number)


def from_roman(numeral: str) -> int:
    """Convert from Roman numerals.

    Args:
        numeral: Roman numeral string

    Returns:
        Integer value

    Example:
        >>> from_roman('XLII')
        42

    Raises:
        ValueError: If invalid Roman numeral
    """
    return roman.fromRoman(numeral) 