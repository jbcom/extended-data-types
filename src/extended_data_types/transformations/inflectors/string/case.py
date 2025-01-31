"""String case transformation utilities."""

from __future__ import annotations

from typing import Literal

CaseStyle = Literal[
    'camel', 'pascal', 'snake', 'kebab', 'title',
    'upper', 'lower', 'dot', 'space', 'constant'
]


def to_camel_case(text: str) -> str:
    """Convert string to camelCase.

    Args:
        text: String to convert

    Returns:
        String in camelCase
    """
    words = text.replace('-', ' ').replace('_', ' ').split()
    return words[0].lower() + ''.join(w.capitalize() for w in words[1:])


def to_pascal_case(text: str) -> str:
    """Convert string to PascalCase.

    Args:
        text: String to convert

    Returns:
        String in PascalCase
    """
    return ''.join(
        word.capitalize()
        for word in text.replace('-', ' ').replace('_', ' ').split()
    ) 