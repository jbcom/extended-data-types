"""Number to word conversion operations."""

from __future__ import annotations

from decimal import Decimal
from typing import Literal

from num2words import num2words

from ..core import Transform

Currency = Literal["USD", "EUR", "GBP", "JPY", "CNY"]


def to_words(
    number: int | float | Decimal,
    lang: str = "en",
    group: bool = True
) -> str:
    """Convert number to words.
    
    Args:
        number: Number to convert
        lang: Language code
        group: Whether to group by thousands
        
    Returns:
        Number in words
        
    Example:
        >>> to_words(42)
        'forty-two'
        >>> to_words(42, lang="es")
        'cuarenta y dos'
    """
    return num2words(number, lang=lang, group=group)


def to_ordinal_words(
    number: int,
    lang: str = "en"
) -> str:
    """Convert number to ordinal words.
    
    Args:
        number: Number to convert
        lang: Language code
        
    Returns:
        Ordinal number in words
        
    Example:
        >>> to_ordinal_words(42)
        'forty-second'
        >>> to_ordinal_words(42, lang="es")
        'cuadragésimo segundo'
    """
    return num2words(number, lang=lang, ordinal=True)


def to_currency_words(
    amount: float | Decimal,
    currency: Currency = "USD",
    lang: str = "en",
    cents: bool = True
) -> str:
    """Convert amount to currency words.
    
    Args:
        amount: Amount to convert
        currency: Currency type
        lang: Language code
        cents: Include cents
        
    Returns:
        Currency amount in words
        
    Example:
        >>> to_currency_words(42.42)
        'forty-two dollars and forty-two cents'
        >>> to_currency_words(42.42, currency="EUR", lang="es")
        'cuarenta y dos euros con cuarenta y dos céntimos'
    """
    return num2words(
        amount,
        lang=lang,
        to='currency',
        currency=currency,
        cents=cents
    )


def to_year_words(
    year: int,
    lang: str = "en"
) -> str:
    """Convert year to words.
    
    Args:
        year: Year to convert
        lang: Language code
        
    Returns:
        Year in words
        
    Example:
        >>> to_year_words(1984)
        'nineteen eighty-four'
        >>> to_year_words(1984, lang="es")
        'mil novecientos ochenta y cuatro'
    """
    return num2words(year, lang=lang, to='year')


# Register transforms
to_words_transform = Transform(to_words)
to_ordinal_words_transform = Transform(to_ordinal_words)
to_currency_words_transform = Transform(to_currency_words)
to_year_words_transform = Transform(to_year_words) 