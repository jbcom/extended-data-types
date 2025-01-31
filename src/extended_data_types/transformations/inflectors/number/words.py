"""Number to words transformation utilities."""

from __future__ import annotations

from typing import Literal

from num2words import num2words

Currency = Literal["USD", "EUR", "GBP", "JPY"]


def to_words(
    number: int | float,
    group: bool = True
) -> str:
    """Convert number to words.

    Args:
        number: Number to convert
        group: Whether to group by thousands

    Returns:
        Number in words

    Example:
        >>> to_words(42)
        'forty-two'
    """
    return num2words(number, group=group)


def to_ordinal_words(number: int) -> str:
    """Convert number to ordinal words.

    Args:
        number: Number to convert

    Returns:
        Ordinal number in words

    Example:
        >>> to_ordinal_words(42)
        'forty-second'
    """
    return num2words(number, ordinal=True)


def to_currency_words(
    amount: float,
    currency: Currency = "USD",
    cents: bool = True
) -> str:
    """Convert amount to currency words.

    Args:
        amount: Amount to convert
        currency: Currency type
        cents: Include cents

    Returns:
        Currency amount in words

    Example:
        >>> to_currency_words(42.42)
        'forty-two dollars and forty-two cents'
    """
    return num2words(amount, to='currency', 
                    currency=currency, cents=cents) 