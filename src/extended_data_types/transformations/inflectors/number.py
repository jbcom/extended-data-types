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

[... continue with number inflectors ...]
