"""Number notation conversion operations."""

from __future__ import annotations

from typing import Literal

import roman

from ..core import Transform

Base = Literal[2, 8, 16]


def to_roman(number: int) -> str:
    """Convert number to Roman numerals.
    
    Args:
        number: Number to convert (1-3999)
        
    Returns:
        Roman numeral string
        
    Example:
        >>> to_roman(42)
        'XLII'
    """
    return roman.toRoman(number)


def from_roman(numeral: str) -> int:
    """Convert Roman numerals to number.
    
    Args:
        numeral: Roman numeral string
        
    Returns:
        Integer value
        
    Example:
        >>> from_roman('XLII')
        42
    """
    return roman.fromRoman(numeral)


def to_binary(
    number: int,
    prefix: bool = True,
    width: int | None = None
) -> str:
    """Convert number to binary string.
    
    Args:
        number: Number to convert
        prefix: Include '0b' prefix
        width: Minimum width (pad with zeros)
        
    Returns:
        Binary string
        
    Example:
        >>> to_binary(42)
        '0b101010'
        >>> to_binary(42, prefix=False, width=8)
        '00101010'
    """
    if width is not None:
        format_str = f"{{:0{width}b}}"
        result = format_str.format(number)
    else:
        result = bin(number)[2:]
    
    return f"0b{result}" if prefix else result


def to_hex(
    number: int,
    prefix: bool = True,
    width: int | None = None,
    upper: bool = False
) -> str:
    """Convert number to hexadecimal string.
    
    Args:
        number: Number to convert
        prefix: Include '0x' prefix
        width: Minimum width (pad with zeros)
        upper: Use uppercase letters
        
    Returns:
        Hexadecimal string
        
    Example:
        >>> to_hex(42)
        '0x2a'
        >>> to_hex(42, prefix=False, upper=True)
        '2A'
    """
    if width is not None:
        format_str = f"{{:0{width}{'X' if upper else 'x'}}}"
        result = format_str.format(number)
    else:
        result = hex(number)[2:]
        if upper:
            result = result.upper()
    
    return f"0x{result}" if prefix else result


def to_octal(
    number: int,
    prefix: bool = True,
    width: int | None = None
) -> str:
    """Convert number to octal string.
    
    Args:
        number: Number to convert
        prefix: Include '0o' prefix
        width: Minimum width (pad with zeros)
        
    Returns:
        Octal string
        
    Example:
        >>> to_octal(42)
        '0o52'
        >>> to_octal(42, prefix=False, width=4)
        '0052'
    """
    if width is not None:
        format_str = f"{{:0{width}o}}"
        result = format_str.format(number)
    else:
        result = oct(number)[2:]
    
    return f"0o{result}" if prefix else result


def from_base(
    text: str,
    base: Base,
    strict: bool = True
) -> int:
    """Convert string from given base to integer.
    
    Args:
        text: String to convert
        base: Number base (2, 8, or 16)
        strict: Require base prefix
        
    Returns:
        Integer value
        
    Example:
        >>> from_base('0b101010', 2)
        42
        >>> from_base('2a', 16, strict=False)
        42
    """
    if strict:
        return int(text, base)
    return int(text.lower().replace('0x', '').replace('0b', '').replace('0o', ''), base)


# Register transforms
to_roman_transform = Transform(to_roman)
from_roman_transform = Transform(from_roman)
to_binary_transform = Transform(to_binary)
to_hex_transform = Transform(to_hex)
to_octal_transform = Transform(to_octal)
from_base_transform = Transform(from_base) 