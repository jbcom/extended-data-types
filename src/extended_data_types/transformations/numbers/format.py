"""Number formatting operations."""

from __future__ import annotations

from decimal import Decimal
from typing import Literal

from ..core import Transform

FormatType = Literal["standard", "scientific", "engineering", "percent"]


def format_number(
    number: int | float | Decimal,
    precision: int = 2,
    thousands_sep: str = ",",
    decimal_sep: str = ".",
    strip_zeros: bool = False
) -> str:
    """Format number with separators.
    
    Args:
        number: Number to format
        precision: Decimal precision
        thousands_sep: Thousands separator
        decimal_sep: Decimal separator
        strip_zeros: Remove trailing zeros
        
    Returns:
        Formatted number string
        
    Example:
        >>> format_number(1234567.89)
        '1,234,567.89'
        >>> format_number(1234.5000, strip_zeros=True)
        '1,234.5'
    """
    format_str = f"{{:,.{precision}f}}"
    result = format_str.format(number)
    
    if thousands_sep != ",":
        result = result.replace(",", thousands_sep)
    if decimal_sep != ".":
        result = result.replace(".", decimal_sep)
        
    if strip_zeros and "." in result:
        result = result.rstrip("0").rstrip(decimal_sep)
    
    return result


def format_currency(
    amount: float | Decimal,
    currency: str = "USD",
    locale: str = "en_US",
    precision: int = 2
) -> str:
    """Format amount as currency.
    
    Args:
        amount: Amount to format
        currency: Currency code
        locale: Locale code
        precision: Decimal precision
        
    Returns:
        Formatted currency string
        
    Example:
        >>> format_currency(1234.56)
        '$1,234.56'
        >>> format_currency(1234.56, currency="EUR", locale="de_DE")
        '1.234,56 €'
    """
    import locale as loc

    import babel.numbers
    
    try:
        loc.setlocale(loc.LC_ALL, locale)
        return babel.numbers.format_currency(
            amount,
            currency,
            locale=locale,
            decimal_quantization=False
        )
    finally:
        loc.setlocale(loc.LC_ALL, '')


def format_percentage(
    number: float | Decimal,
    precision: int = 2,
    strip_zeros: bool = False
) -> str:
    """Format number as percentage.
    
    Args:
        number: Number to format
        precision: Decimal precision
        strip_zeros: Remove trailing zeros
        
    Returns:
        Formatted percentage string
        
    Example:
        >>> format_percentage(0.1234)
        '12.34%'
        >>> format_percentage(0.1200, strip_zeros=True)
        '12%'
    """
    format_str = f"{{:.{precision}%}}"
    result = format_str.format(number)
    
    if strip_zeros and "." in result:
        result = result.rstrip("0").rstrip(".")
        
    return result


def format_scientific(
    number: float | Decimal,
    precision: int = 2,
    upper: bool = False
) -> str:
    """Format number in scientific notation.
    
    Args:
        number: Number to format
        precision: Decimal precision
        upper: Use uppercase E
        
    Returns:
        Scientific notation string
        
    Example:
        >>> format_scientific(1234.56)
        '1.23e+03'
        >>> format_scientific(1234.56, upper=True)
        '1.23E+03'
    """
    format_str = f"{{:.{precision}{'E' if upper else 'e'}}}"
    return format_str.format(number)


def format_engineering(
    number: float | Decimal,
    precision: int = 2,
    upper: bool = True
) -> str:
    """Format number in engineering notation.
    
    Args:
        number: Number to format
        precision: Decimal precision
        upper: Use uppercase E
        
    Returns:
        Engineering notation string
        
    Example:
        >>> format_engineering(1234.56)
        '1.23E+03'
        >>> format_engineering(0.001234)
        '1.23E-03'
    """
    exp = int(f"{number:e}".split('e')[1])
    exp_3 = exp - (exp % 3)
    mantissa = number / (10 ** exp_3)
    format_str = f"{{:.{precision}f}}{'E' if upper else 'e'}{exp_3:+03d}"
    return format_str.format(mantissa)


# Register transforms
format_number_transform = Transform(format_number)
format_currency_transform = Transform(format_currency)
format_percentage_transform = Transform(format_percentage)
format_scientific_transform = Transform(format_scientific)
format_engineering_transform = Transform(format_engineering) 