"""String pattern matching and manipulation operations."""

from __future__ import annotations

import re

from collections.abc import Callable
from typing import Any

from extended_data_types.transformations.core import Transform


def match_pattern(
    text: str, pattern: str | re.Pattern[str], flags: int = 0
) -> list[tuple[int, int]]:
    r"""Find all pattern matches in text.

    Args:
        text: Text to search
        pattern: Regular expression pattern
        flags: Regex flags

    Returns:
        List of (start, end) index tuples for each match

    Example:
        >>> match_pattern("hello 123 world", r"\d+")
        [(6, 9)]
    """
    if isinstance(pattern, str):
        pattern = re.compile(pattern, flags)
    return [(m.start(), m.end()) for m in pattern.finditer(text)]


def replace_pattern(
    text: str,
    pattern: str | re.Pattern[str],
    repl: str | Callable[[re.Match[str]], str],
    count: int = 0,
    flags: int = 0,
) -> str:
    r"""Replace pattern matches in text.

    Args:
        text: Text to modify
        pattern: Regular expression pattern
        repl: Replacement string or function
        count: Maximum replacements (0 for all)
        flags: Regex flags

    Returns:
        Modified string

    Example:
        >>> replace_pattern("hello 123 world", r"\d+", "xyz")
        'hello xyz world'
    """
    if isinstance(pattern, str):
        pattern = re.compile(pattern, flags)
    return pattern.sub(repl, text, count)


def extract_pattern(
    text: str,
    pattern: str | re.Pattern[str],
    group: int | str | None = None,
    flags: int = 0,
) -> list[Any]:
    r"""Extract pattern groups from text.

    Args:
        text: Text to search
        pattern: Regular expression pattern
        group: Group index or name to extract
        flags: Regex flags

    Returns:
        List of extracted groups. If pattern has multiple groups and group is None,
        returns list of tuples with all groups.

    Example:
        >>> extract_pattern("age: 25", r"age: (\d+)")
        ['25']
        >>> extract_pattern("x=1, y=2", r"(\w+)=(\d+)", 1)
        ['x', 'y']
        >>> extract_pattern("john@example.com", r"(\w+)@(\w+)\.(\w+)")
        [('john', 'example', 'com')]
    """
    if isinstance(pattern, str):
        pattern = re.compile(pattern, flags)

    matches = pattern.finditer(text)
    if group is None:
        # Check if pattern has groups
        if pattern.groups > 0:
            # Return tuples of all groups
            return [m.groups() for m in matches]
        else:
            # No groups, return matched strings
            return [m.group() for m in matches]
    return [m.group(group) for m in matches]


def split_pattern(
    text: str, pattern: str | re.Pattern[str], maxsplit: int = 0, flags: int = 0
) -> list[str]:
    """Split text by pattern.

    Args:
        text: Text to split
        pattern: Regular expression pattern
        maxsplit: Maximum splits (0 for all)
        flags: Regex flags

    Returns:
        List of split strings

    Example:
        >>> split_pattern("a,b;c", r"[,;]")
        ['a', 'b', 'c']
    """
    if isinstance(pattern, str):
        pattern = re.compile(pattern, flags)
    return pattern.split(text, maxsplit)


def find_boundaries(
    text: str, pattern: str | re.Pattern[str] | None = None, flags: int = 0
) -> list[tuple[int, int]]:
    r"""Find pattern match boundaries in text.

    Args:
        text: Text to search
        pattern: Regular expression pattern (defaults to word boundaries \b\w+\b)
        flags: Regex flags

    Returns:
        List of (start, end) positions

    Example:
        >>> find_boundaries("hello 123 world", r"\d+")
        [(6, 9)]
        >>> find_boundaries("Hello, World!")
        [(0, 5), (7, 12)]
    """
    if pattern is None:
        pattern = r"\b\w+\b"
    if isinstance(pattern, str):
        pattern = re.compile(pattern, flags)
    return [(m.start(), m.end()) for m in pattern.finditer(text)]


# Register transforms
match_pattern_transform = Transform(match_pattern)  # type: ignore[arg-type]
replace_pattern_transform = Transform(replace_pattern)  # type: ignore[arg-type]
extract_pattern_transform = Transform(extract_pattern)  # type: ignore[arg-type]
split_pattern_transform = Transform(split_pattern)  # type: ignore[arg-type]
find_boundaries_transform = Transform(find_boundaries)  # type: ignore[arg-type]
