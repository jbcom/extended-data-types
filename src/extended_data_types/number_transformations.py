"""Number transformation utilities.

This module provides functions for converting numbers to/from words,
Roman numerals, and various formatting operations.
"""

from __future__ import annotations

from num2words import num2words


def to_roman(number: int) -> str:
    """Convert integer to Roman numerals.
    
    Args:
        number: Integer between 1 and 3999
        
    Returns:
        Roman numeral string
        
    Example:
        >>> to_roman(42)
        'XLII'
    """
    if not 1 <= number <= 3999:
        raise ValueError("Number must be between 1 and 3999")
    return num2words(number, to='roman').upper()


def from_roman(numeral: str) -> int:
    """Convert Roman numerals to integer.
    
    Args:
        numeral: Roman numeral string
        
    Returns:
        Integer value
        
    Example:
        >>> from_roman('XLII')
        42
    """
    numeral = numeral.upper().strip()
    roman_values = {
        'M': 1000, 'CM': 900, 'D': 500, 'CD': 400,
        'C': 100, 'XC': 90, 'L': 50, 'XL': 40,
        'X': 10, 'IX': 9, 'V': 5, 'IV': 4, 'I': 1
    }
    
    result = 0
    i = 0
    while i < len(numeral):
        # Check for two-character combo
        if i + 1 < len(numeral) and numeral[i:i+2] in roman_values:
            result += roman_values[numeral[i:i+2]]
            i += 2
        elif numeral[i] in roman_values:
            result += roman_values[numeral[i]]
            i += 1
        else:
            raise ValueError(f"Invalid Roman numeral: {numeral}")
    
    if to_roman(result) != numeral:
        raise ValueError(f"Invalid or non-canonical Roman numeral: {numeral}")
    
    return result


def number_to_words(number: int | float, lang: str = "en") -> str:
    """Convert number to words.
    
    Args:
        number: Integer or float to convert. Floats are converted using
            'point' notation (e.g., 3.14 becomes "three point one four")
        lang: Language code (default: 'en')
        
    Returns:
        Number as words
        
    Example:
        >>> number_to_words(42)
        'forty-two'
        >>> number_to_words(3.14)
        'three point one four'
    """
    return num2words(number, lang=lang)


def number_to_ordinal(number: int, lang: str = "en") -> str:
    """Convert number to ordinal words.
    
    Args:
        number: Number to convert
        lang: Language code (default: 'en')
        
    Returns:
        Ordinal as words
        
    Example:
        >>> number_to_ordinal(42)
        'forty-second'
    """
    return num2words(number, ordinal=True, lang=lang)


def number_to_currency(amount: float, currency: str = "USD", lang: str = "en") -> str:
    """Convert number to currency words.
    
    Args:
        amount: Amount to convert
        currency: Currency code (default: 'USD')
        lang: Language code (default: 'en')
        
    Returns:
        Currency as words
        
    Example:
        >>> number_to_currency(42.50)
        'forty-two dollars and fifty cents'
    """
    return num2words(amount, to='currency', currency=currency, lang=lang)
