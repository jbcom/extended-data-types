"""Number rounding operations."""

from __future__ import annotations

import math
from decimal import ROUND_HALF_DOWN, ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal
from typing import Literal, TypeVar, overload

from ..core import Transform

N = TypeVar('N', int, float, Decimal)
RoundingMode = Literal["up", "down", "nearest", "floor", "ceil"]


@overload
def round_to(
    number: N,
    precision: int = 0,
    mode: RoundingMode = "nearest"
) -> N: ...

def round_to(
    number: N,
    precision: int = 0,
    mode: RoundingMode = "nearest"
) -> N:
    """Round number to specified precision.
    
    Args:
        number: Number to round
        precision: Decimal places
        mode: Rounding mode
        
    Returns:
        Rounded number
        
    Example:
        >>> round_to(3.14159, 2)
        3.14
        >>> round_to(3.5, mode="up")
        4
    """
    if isinstance(number, Decimal):
        exp = Decimal(f"1e-{precision}")
        if mode == "up":
            return number.quantize(exp, rounding=ROUND_HALF_UP)
        elif mode == "down":
            return number.quantize(exp, rounding=ROUND_HALF_DOWN)
        return number.quantize(exp, rounding=ROUND_HALF_EVEN)
    
    factor = 10 ** precision
    if mode == "up":
        return type(number)(math.ceil(number * factor) / factor)
    elif mode == "down":
        return type(number)(math.floor(number * factor) / factor)
    elif mode == "floor":
        return type(number)(math.floor(number))
    elif mode == "ceil":
        return type(number)(math.ceil(number))
    return type(number)(round(number * factor) / factor)


def ceil_to(
    number: N,
    step: N = 1
) -> N:
    """Round number up to nearest multiple of step.
    
    Args:
        number: Number to round
        step: Step size
        
    Returns:
        Rounded number
        
    Example:
        >>> ceil_to(42.3, 5)
        45
        >>> ceil_to(41, 10)
        50
    """
    return type(number)(math.ceil(number / step) * step)


def floor_to(
    number: N,
    step: N = 1
) -> N:
    """Round number down to nearest multiple of step.
    
    Args:
        number: Number to round
        step: Step size
        
    Returns:
        Rounded number
        
    Example:
        >>> floor_to(42.3, 5)
        40
        >>> floor_to(41, 10)
        40
    """
    return type(number)(math.floor(number / step) * step)


def clamp(
    number: N,
    minimum: N | None = None,
    maximum: N | None = None
) -> N:
    """Clamp number between minimum and maximum.
    
    Args:
        number: Number to clamp
        minimum: Minimum value
        maximum: Maximum value
        
    Returns:
        Clamped number
        
    Example:
        >>> clamp(42, minimum=0, maximum=10)
        10
        >>> clamp(-42, minimum=0)
        0
    """
    if minimum is not None and number < minimum:
        return minimum
    if maximum is not None and number > maximum:
        return maximum
    return number


def quantize(
    number: N,
    step: N,
    mode: RoundingMode = "nearest"
) -> N:
    """Quantize number to nearest multiple of step.
    
    Args:
        number: Number to quantize
        step: Quantization step
        mode: Rounding mode
        
    Returns:
        Quantized number
        
    Example:
        >>> quantize(42.3, 5)
        40
        >>> quantize(42.3, 5, mode="up")
        45
    """
    if mode == "up":
        return ceil_to(number, step)
    elif mode == "down":
        return floor_to(number, step)
    elif mode == "floor":
        return floor_to(number, step)
    elif mode == "ceil":
        return ceil_to(number, step)
    
    # Nearest mode
    lower = floor_to(number, step)
    upper = ceil_to(number, step)
    return lower if number - lower <= upper - number else upper


# Register transforms
round_to_transform = Transform(round_to)
ceil_to_transform = Transform(ceil_to)
floor_to_transform = Transform(floor_to)
clamp_transform = Transform(clamp)
quantize_transform = Transform(quantize) 