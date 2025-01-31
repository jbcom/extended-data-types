"""String utility transformations."""

from __future__ import annotations

import re

from collections.abc import Sequence


def split_words(text: str) -> list[str]:
    """Split text into words.

    Args:
        text: Text to split

    Returns:
        List of words
    """
    return re.findall(r"[A-Za-z][a-z]*", text)


def join_words(words: Sequence[str], separator: str = " ") -> str:
    """Join words with separator.

    Args:
        words: Words to join
        separator: Separator to use

    Returns:
        Joined string
    """
    return separator.join(words)


def clean_whitespace(text: str) -> str:
    """Normalize whitespace in text.

    Args:
        text: Text to clean

    Returns:
        Text with normalized whitespace
    """
    return " ".join(text.split())
