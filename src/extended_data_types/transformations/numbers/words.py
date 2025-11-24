"""Number to word conversion operations."""

from __future__ import annotations

import re
from decimal import Decimal
from fractions import Fraction
from typing import Literal

from num2words import num2words

from extended_data_types.transformations.core import Transform


Currency = Literal["USD", "EUR", "GBP", "JPY", "CNY"]


def _parse_integer_words(tokens: list[str]) -> tuple[int, bool]:
    """Parse integer word tokens into a number and negative flag."""
    if not tokens:
        return 0, False

    units = {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "eleven": 11,
        "twelve": 12,
        "thirteen": 13,
        "fourteen": 14,
        "fifteen": 15,
        "sixteen": 16,
        "seventeen": 17,
        "eighteen": 18,
        "nineteen": 19,
    }
    tens = {
        "twenty": 20,
        "thirty": 30,
        "forty": 40,
        "fifty": 50,
        "sixty": 60,
        "seventy": 70,
        "eighty": 80,
        "ninety": 90,
    }
    scales = {"hundred": 100, "thousand": 1000, "million": 1_000_000}

    total = 0
    current = 0
    negative = False

    for token in tokens:
        if token == "minus":
            negative = True
            continue
        if token in ("and", "a", "an"):
            continue
        if token in units:
            current += units[token]
        elif token in tens:
            current += tens[token]
        elif token == "hundred":
            current = (current or 1) * scales[token]
        elif token in ("thousand", "million"):
            current = (current or 1) * scales[token]
            total += current
            current = 0
        else:
            raise ValueError(f"Unrecognized token {token}")

    value = total + current
    return (-value if negative else value), negative


def words_to_number(text: str) -> int | float:
    """Convert english words to a number (limited but test-friendly)."""
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("Empty words")

    normalized = cleaned.replace("-", " ").lower()
    tokens = [t for t in normalized.split() if t]
    if "point" in tokens:
        point_index = tokens.index("point")
        integer_tokens = tokens[:point_index]
        fraction_tokens = tokens[point_index + 1 :]
        if not fraction_tokens:
            raise ValueError("Invalid fractional words")
        integer_value, was_negative = _parse_integer_words(integer_tokens)
        digit_map = {
            "zero": "0",
            "one": "1",
            "two": "2",
            "three": "3",
            "four": "4",
            "five": "5",
            "six": "6",
            "seven": "7",
            "eight": "8",
            "nine": "9",
        }
        try:
            frac_str = "".join(digit_map[token] for token in fraction_tokens)
        except KeyError as exc:
            raise ValueError(f"Invalid fractional token {exc}") from exc
        frac_val = float(f"0.{frac_str}")
        sign = -1 if (integer_value < 0 or was_negative) else 1
        return integer_value + sign * frac_val if integer_value else sign * frac_val

    value, _ = _parse_integer_words(tokens)
    return int(value) if float(value).is_integer() else float(value)


def to_words(
    number: int | float | Decimal,
    lang: str = "en",
    group: bool = True,
    capitalize: bool = False,
) -> str:
    """Convert number to words."""
    # Remove group parameter - not supported in current num2words version
    result = num2words(number, lang=lang)
    if capitalize:
        result = result[:1].upper() + result[1:] if result else result
    return result


def number_to_words(
    number: int | float | Decimal,
    lang: str = "en",
    capitalize: bool = False,
    conjunction: str = " and ",
) -> str:
    """User-facing helper with a couple of legacy options."""
    if isinstance(number, float) and (
        number == float("inf") or number == float("-inf")
    ):
        raise ValueError("Infinite values not supported")

    # Handle negative numbers specially - check sign before calling num2words
    # For negative zero, check the string representation
    number_str = str(number)
    is_negative = number < 0 or (
        isinstance(number, float) and number == 0.0 and number_str.startswith("-")
    )

    if is_negative:
        # Convert to positive for num2words, then add "minus" prefix
        abs_number = abs(number)
        result = num2words(abs_number, lang=lang)
        # Ensure "minus" prefix is present
        if not result.startswith("minus"):
            result = "minus " + result
    else:
        result = num2words(number, lang=lang)

    if conjunction != " and ":
        # Replace " and " with conjunction, preserving spacing
        if conjunction == "":
            # Empty conjunction: replace " and " with a space
            result = result.replace(" and ", " ")
        else:
            result = result.replace(" and ", conjunction)
    if capitalize:
        result = result[:1].upper() + result[1:] if result else result
    return result


def to_ordinal_words(number: int, lang: str = "en", capitalize: bool = False) -> str:
    """Convert number to ordinal words."""
    if number <= 0:
        raise ValueError("Ordinal requires positive integers")
    result = num2words(number, lang=lang, ordinal=True)
    if capitalize:
        result = result[:1].upper() + result[1:]
    return result


ordinal_to_words = to_ordinal_words


def words_to_ordinal(text: str) -> int:
    """Convert ordinal words back to numbers."""
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("Empty words")

    normalized = cleaned.replace("-", " ").lower()
    replacements = {
        "first": "one",
        "second": "two",
        "third": "three",
        "fourth": "four",
        "fifth": "five",
        "sixth": "six",
        "seventh": "seven",
        "eighth": "eight",
        "ninth": "nine",
        "tenth": "ten",
        "eleventh": "eleven",
        "twelfth": "twelve",
        "thirteenth": "thirteen",
        "fourteenth": "fourteen",
        "fifteenth": "fifteen",
        "sixteenth": "sixteen",
        "seventeenth": "seventeen",
        "eighteenth": "eighteen",
        "nineteenth": "nineteen",
        "twentieth": "twenty",
        "thirtieth": "thirty",
        "fortieth": "forty",
        "fiftieth": "fifty",
        "sixtieth": "sixty",
        "seventieth": "seventy",
        "eightieth": "eighty",
        "ninetieth": "ninety",
        "hundredth": "hundred",
        "thousandth": "thousand",
        "millionth": "million",
    }

    converted = []
    for token in normalized.split():
        converted.append(replacements.get(token, token))

    value = words_to_number(" ".join(converted))
    if not float(value).is_integer():
        raise ValueError("Ordinal words must resolve to an integer")
    if value <= 0:
        raise ValueError("Ordinal must be positive")
    return int(value)


def to_currency_words(
    amount: float | Decimal,
    currency: Currency = "USD",
    lang: str = "en",
    cents: bool = True,
) -> str:
    """Convert amount to currency words."""
    return num2words(amount, lang=lang, to="currency", currency=currency, cents=cents)


def _fraction_denominator_name(denominator: int, plural: bool = False) -> str:
    names = {
        2: ("half", "halves"),
        3: ("third", "thirds"),
        4: ("quarter", "quarters"),
    }
    singular, plural_name = names.get(
        denominator, (f"{denominator}th", f"{denominator}ths")
    )
    return plural_name if plural else singular


def fraction_to_words(value: str, capitalize: bool = False) -> str:
    """Convert a fractional string to words."""
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("Empty fraction")

    try:
        if " " in cleaned and "/" in cleaned:
            whole_part, frac_part = cleaned.split(None, 1)
            frac = Fraction(frac_part)
            frac = Fraction(
                int(whole_part) * frac.denominator + frac.numerator, frac.denominator
            )
        else:
            frac = Fraction(cleaned)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"Invalid fraction {value}") from exc

    numerator, denominator = frac.numerator, frac.denominator
    if denominator == 0:
        raise ValueError("Invalid fraction")

    whole = None
    if abs(numerator) >= denominator:
        whole = numerator // denominator
        numerator = abs(numerator % denominator)

    if numerator == 0 and whole is not None:
        result = num2words(whole)
    else:
        denom_word = _fraction_denominator_name(denominator, plural=numerator != 1)
        # Use "a" instead of "one" when there's a whole number part
        if whole is not None and numerator == 1:
            num_word = "a"
        else:
            num_word = "one" if numerator == 1 else num2words(numerator)
        result = f"{num_word} {denom_word}"
        if whole is not None:
            result = f"{num2words(whole)} and {result}"

    if capitalize and result:
        result = result[:1].upper() + result[1:]
    return result


def _parse_fraction_tokens(tokens: list[str]) -> tuple[int, int]:
    if not tokens:
        raise ValueError("Empty fraction words")
    if tokens[0] in ("a", "an"):
        tokens = tokens[1:]
    denom_map = {
        "half": 2,
        "halves": 2,
        "quarter": 4,
        "quarters": 4,
        "third": 3,
        "thirds": 3,
    }
    denom_word = tokens[-1]
    if denom_word not in denom_map:
        raise ValueError("Unrecognized fraction words")
    denominator = denom_map[denom_word]
    numerator_tokens = tokens[:-1] or ["one"]
    numerator = words_to_number(" ".join(numerator_tokens))
    if not float(numerator).is_integer():
        raise ValueError("Fraction numerator must be integer")
    return int(numerator), denominator


def words_to_fraction(text: str) -> str:
    """Convert fractional words to a numeric string."""
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("Empty fraction words")

    normalized = cleaned.replace("-", " ").lower()
    if " and " in normalized:
        whole_part, frac_part = normalized.split(" and ", 1)
        whole = words_to_number(whole_part)
        numerator, denominator = _parse_fraction_tokens(frac_part.split())
        return f"{int(whole)} {numerator}/{denominator}"

    numerator, denominator = _parse_fraction_tokens(normalized.split())
    return f"{numerator}/{denominator}"


def number_to_words_legacy(number: int | float | Decimal, lang: str = "en") -> str:
    """Legacy alias retained for compatibility."""
    return number_to_words(number, lang=lang)


def to_year_words(year: int, lang: str = "en") -> str:
    """Convert year to words."""
    return num2words(year, lang=lang, to="year")


# Register transforms
to_words_transform = Transform(to_words)
to_ordinal_words_transform = Transform(to_ordinal_words)
to_currency_words_transform = Transform(to_currency_words)
to_year_words_transform = Transform(to_year_words)
words_to_number_transform = Transform(words_to_number)
words_to_fraction_transform = Transform(words_to_fraction)
