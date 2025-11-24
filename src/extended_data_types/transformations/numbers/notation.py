"""Number notation conversion operations."""

from __future__ import annotations

import re
from fractions import Fraction
from typing import Literal

from num2words import num2words

from extended_data_types.transformations.core import Transform
from extended_data_types.transformations.numbers.words import ordinal_to_words, to_words


Base = Literal[2, 8, 16]


def to_roman(number: int, upper: bool = True) -> str:
    """Convert number to Roman numerals using num2words."""
    if not isinstance(number, int):
        raise TypeError("to_roman requires an integer")
    if number < 1 or number > 3999:
        raise ValueError(f"Number must be between 1 and 3999, got {number}")
    try:
        result = num2words(number, to='roman')
    except (ValueError, OverflowError) as e:
        raise ValueError(f"Invalid number for Roman numeral: {number}") from e
    return result if upper else result.lower()


_ROMAN_VALUES = {
    'M': 1000, 'CM': 900, 'D': 500, 'CD': 400,
    'C': 100, 'XC': 90, 'L': 50, 'XL': 40,
    'X': 10, 'IX': 9, 'V': 5, 'IV': 4, 'I': 1
}


def from_roman(numeral: str) -> int:
    """Convert Roman numerals to number."""
    numeral = numeral.upper().strip()
    if not numeral:
        raise ValueError("Empty Roman numeral")
    
    # Validate characters
    if not all(c in 'MDCLXVI' for c in numeral):
        raise ValueError(f"Invalid Roman numeral: {numeral}")
    
    result = 0
    i = 0
    while i < len(numeral):
        # Check for two-character combo first
        if i + 1 < len(numeral):
            two_char = numeral[i:i+2]
            if two_char in _ROMAN_VALUES:
                result += _ROMAN_VALUES[two_char]
                i += 2
                continue
        # Single character
        if numeral[i] in _ROMAN_VALUES:
            result += _ROMAN_VALUES[numeral[i]]
            i += 1
        else:
            raise ValueError(f"Invalid Roman numeral: {numeral}")
    
    return result


def to_ordinal(number: int, words: bool = False) -> str:
    """Convert integer to ordinal text or suffix form."""
    if not isinstance(number, int):
        raise TypeError("Ordinal requires integer input")
    if number <= 0:
        raise ValueError("Ordinal requires positive integers")
    if words:
        return ordinal_to_words(number)
    suffix = ("th", "st", "nd", "rd", "th")[min(number % 10, 4)]
    if 10 <= number % 100 <= 20:
        suffix = "th"
    return f"{number}{suffix}"


_ORDINAL_WORDS = {
    "first": 1,
    "second": 2,
    "third": 3,
    "fourth": 4,
    "fifth": 5,
    "sixth": 6,
    "seventh": 7,
    "eighth": 8,
    "ninth": 9,
    "tenth": 10,
    "eleventh": 11,
    "twelfth": 12,
    "thirteenth": 13,
    "fourteenth": 14,
    "fifteenth": 15,
    "sixteenth": 16,
    "seventeenth": 17,
    "eighteenth": 18,
    "nineteenth": 19,
    "twentieth": 20,
}


def from_ordinal(value: str) -> int:
    """Convert ordinal text/suffix to integer."""
    cleaned = value.strip().lower()
    if not cleaned:
        raise ValueError("Empty ordinal")

    if cleaned in _ORDINAL_WORDS:
        return _ORDINAL_WORDS[cleaned]

    match = re.match(r"^(-?\d+)(st|nd|rd|th)$", cleaned)
    if not match:
        raise ValueError(f"Invalid ordinal {value}")
    number = int(match.group(1))
    expected = to_ordinal(number)[len(str(number)) :]
    if match.group(2) != expected:
        raise ValueError(f"Invalid ordinal suffix for {value}")
    return number


def _parse_words_to_int(words: str) -> int:
    """Basic english words-to-number converter for compat tests."""
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

    tokens = words.replace("-", " ").split()
    if not tokens:
        raise ValueError("Empty words")

    sign = -1 if tokens and tokens[0].lower() == "minus" else 1
    if sign == -1:
        tokens = tokens[1:]

    total = 0
    current = 0
    for token in tokens:
        part = token.lower()
        if part in units:
            current += units[part]
        elif part in tens:
            current += tens[part]
        elif part == "hundred":
            if current == 0:
                current = 100
            else:
                current *= 100
        elif part == "and":
            continue
        else:
            raise ValueError(f"Unrecognized token {token}")
    total += current
    return sign * total


def from_words(words: str) -> float:
    """Convert simple english words to numbers (limited but test-friendly)."""
    cleaned = words.strip()
    if not cleaned:
        raise ValueError("Empty words")

    lower = cleaned.lower()
    if lower.isdigit() or (lower.startswith("-") and lower[1:].isdigit()):
        return float(int(lower))

    if "point" in lower:
        integer_part, fractional_part = lower.split("point", 1)
        whole = _parse_words_to_int(integer_part.strip()) if integer_part.strip() else 0
        frac_tokens = fractional_part.strip().replace("-", " ").split()
        if not frac_tokens:
            raise ValueError("Invalid fractional words")
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
            frac_str = "".join(digit_map[token] for token in frac_tokens)
        except KeyError as exc:
            raise ValueError(f"Invalid fractional token {exc}") from exc
        sign = -1 if whole < 0 else 1
        return sign * (abs(whole) + float(f"0.{frac_str}"))

    return float(_parse_words_to_int(lower))


def to_fraction(value: float, mixed: bool = False, precision: int | None = None) -> str:
    """Convert float to fractional string."""
    if not isinstance(value, (int, float)):
        raise ValueError("Fraction conversion expects numeric input")
    if value in (float("inf"), float("-inf")):
        raise ValueError("Infinite values not supported")

    if precision is not None:
        scale = 10**precision
        frac = Fraction(int(round(value * scale)), scale)
    else:
        frac = Fraction(value).limit_denominator(1000)
    numerator, denominator = frac.numerator, frac.denominator

    if mixed and abs(numerator) >= denominator:
        whole = numerator // denominator
        remainder = abs(numerator % denominator)
        if remainder == 0:
            return str(whole)
        return f"{whole} {remainder}/{denominator}"

    return f"{numerator}/{denominator}"


def from_fraction(value: str) -> float:
    """Convert fractional string to float."""
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("Empty fraction")

    parts = cleaned.split()
    try:
        if len(parts) == 2:
            whole = Fraction(parts[0])
            frac = Fraction(parts[1])
            return float(whole + frac)
        return float(Fraction(cleaned.replace(" ", "")))
    except (ZeroDivisionError, ValueError) as exc:
        raise ValueError(f"Invalid fraction {value}") from exc


def to_binary(number: int, prefix: bool = True, width: int | None = None) -> str:
    """Convert number to binary string."""
    if width is not None:
        format_str = f"{{:0{width}b}}"
        result = format_str.format(number)
    else:
        result = bin(number)[2:]
    return f"0b{result}" if prefix else result


def to_hex(
    number: int, prefix: bool = True, width: int | None = None, upper: bool = False
) -> str:
    """Convert number to hexadecimal string."""
    if width is not None:
        format_str = f"{{:0{width}{'X' if upper else 'x'}}}"
        result = format_str.format(number)
    else:
        result = hex(number)[2:]
        if upper:
            result = result.upper()
    return f"0x{result}" if prefix else result


def to_octal(number: int, prefix: bool = True, width: int | None = None) -> str:
    """Convert number to octal string."""
    if width is not None:
        format_str = f"{{:0{width}o}}"
        result = format_str.format(number)
    else:
        result = oct(number)[2:]
    return f"0o{result}" if prefix else result


def from_base(text: str, base: Base, strict: bool = True) -> int:
    """Convert string from given base to integer."""
    if strict:
        return int(text, base)
    return int(text.lower().replace("0x", "").replace("0b", "").replace("0o", ""), base)


# Register transforms
to_roman_transform = Transform(to_roman)  # type: ignore[arg-type]
from_roman_transform = Transform(from_roman)  # type: ignore[arg-type]
to_binary_transform = Transform(to_binary)  # type: ignore[arg-type]
to_hex_transform = Transform(to_hex)  # type: ignore[arg-type]
to_octal_transform = Transform(to_octal)  # type: ignore[arg-type]
from_base_transform = Transform(from_base)  # type: ignore[arg-type]
from_words_transform = Transform(from_words)  # type: ignore[arg-type]
from_fraction_transform = Transform(from_fraction)  # type: ignore[arg-type]
from_ordinal_transform = Transform(from_ordinal)  # type: ignore[arg-type]
