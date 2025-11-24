"""Number utility transformations."""

from __future__ import annotations

from decimal import ROUND_DOWN, ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal
from typing import Literal


RoundingMode = Literal["up", "down", "nearest"]


def round_number(
    number: float, precision: int = 0, mode: RoundingMode = "nearest"
) -> float:
    """Round number to specified precision.

    Args:
        number: Number to round
        precision: Decimal places
        mode: Rounding mode

    Returns:
        Rounded number

    Example:
        >>> round_number(3.14159, 2)
        3.14
    """
    decimal = Decimal(str(number))
    if mode == "up":
        return float(
            decimal.quantize(Decimal(f"0.{'0' * precision}"), rounding=ROUND_HALF_UP)
        )
    elif mode == "down":
        return float(
            decimal.quantize(Decimal(f"0.{'0' * precision}"), rounding=ROUND_DOWN)
        )
    return float(
        decimal.quantize(Decimal(f"0.{'0' * precision}"), rounding=ROUND_HALF_EVEN)
    )


def format_thousands(number: float, separator: str = ",") -> str:
    """Format number with thousand separators.

    Args:
        number: Number to format
        separator: Thousand separator

    Returns:
        Formatted string

    Example:
        >>> format_thousands(1234567)
        '1,234,567'
    """
    return f"{number:,}".replace(",", separator)


def clamp(number: float, minimum: float, maximum: float) -> float:
    """Clamp number between minimum and maximum.

    Args:
        number: Number to clamp
        minimum: Minimum value
        maximum: Maximum value

    Returns:
        Clamped number

    Example:
        >>> clamp(5, 0, 10)
        5
        >>> clamp(-1, 0, 10)
        0
    """
    return max(minimum, min(number, maximum))
