"""String Type Definitions and Custom Classes.

This module provides type definitions and custom classes for string operations:

Key Features:
- Extended string functionality
- Type aliases and hints
- Pattern matching
- Format types
- Case types
- Path types
"""

from __future__ import annotations

import re

from collections import UserString
from pathlib import Path
from typing import Literal, Union, overload


# Type aliases
StrOrBytes = Union[str, bytes, bytearray, memoryview]
StrPath = Union[str, Path]
CaseStyle = Literal["camel", "pascal", "snake", "kebab", "title", "upper", "lower"]
FormatPattern = Union[str, re.Pattern[str]]

@overload
def convert_case(text: str, style: CaseStyle) -> str: ...

def convert_case(text: str, style: CaseStyle) -> str:
    """Convert string case."""
    if style == "camel":
        return text.lower().replace(" ", "")
    if style == "pascal":
        return text.title().replace(" ", "")
    if style == "snake":
        return text.lower().replace(" ", "_")
    if style == "kebab":
        return text.lower().replace(" ", "-")
    if style == "title":
        return text.title()
    if style == "upper":
        return text.upper()
    if style == "lower":
        return text.lower()
    raise ValueError(f"Unsupported case style: {style}")


class ExtendedString(UserString):
    """Extended string class with additional operations and safety features.

    Inherits from UserString to provide full string interface with
    additional utility methods for common string operations.
    """

    def truncate(self, max_length: int, ender: str = "...") -> ExtendedString:
        """Truncate the string to a maximum length.

        Args:
            max_length: Maximum length of the resulting string.
            ender: String to append if truncation occurs.

        Returns:
            A new ExtendedString with the truncated result.
        """
        if len(self.data) <= max_length:
            return ExtendedString(self.data)
        return ExtendedString(self.data[: max_length - len(ender)] + ender)

    def sanitize(self, delim: str = "_") -> ExtendedString:
        """Replace non-alphanumeric characters with a delimiter.

        Args:
            delim: Delimiter to use for replacement.

        Returns:
            A new ExtendedString with non-alphanumeric characters replaced.
        """
        return ExtendedString(
            "".join(x if (x.isalnum() or x == delim) else delim for x in self.data)
        )

    def is_url(self) -> bool:
        """Check if the string is a valid URL.

        Returns:
            True if the string is a valid URL.
        """
        try:
            from urllib.parse import urlparse

            result = urlparse(self.data)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def to_path(self) -> Path:
        """Convert the string to a Path object.

        Returns:
            A Path object representing the string.
        """
        return Path(self.data)

    def ensure_prefix(self, prefix: str) -> ExtendedString:
        """Ensure the string starts with the given prefix.

        Args:
            prefix: The prefix to ensure.

        Returns:
            A new ExtendedString with the prefix ensured.
        """
        if not self.data.startswith(prefix):
            return ExtendedString(prefix + self.data)
        return ExtendedString(self.data)

    def ensure_suffix(self, suffix: str) -> ExtendedString:
        """Ensure the string ends with the given suffix.

        Args:
            suffix: The suffix to ensure.

        Returns:
            A new ExtendedString with the suffix ensured.
        """
        if not self.data.endswith(suffix):
            return ExtendedString(self.data + suffix)
        return ExtendedString(self.data)

    def split_and_strip(self, sep: str | None = None) -> list[ExtendedString]:
        """Split the string and strip whitespace from each part.

        Args:
            sep: The separator to split on.

        Returns:
            List of stripped ExtendedString parts.
        """
        return [ExtendedString(part.strip()) for part in self.data.split(sep)]

    def to_bool(self) -> bool:
        """Convert string to boolean value.

        Returns:
            True for 'true', 'yes', '1', 'on' (case-insensitive),
            False for 'false', 'no', '0', 'off' (case-insensitive).

        Raises:
            ValueError: If the string cannot be converted to a boolean.
        """
        normalized = self.data.lower().strip()
        if normalized in ("true", "yes", "1", "on"):
            return True
        if normalized in ("false", "no", "0", "off"):
            return False
        raise ValueError(f"Cannot convert '{self.data}' to boolean")


class Pattern:
    """A compiled regular expression pattern with named operations.

    Attributes:
        pattern: The compiled regular expression pattern.
        flags: The flags used to compile the pattern.
    """

    def __init__(self, pattern: str, flags: int = 0) -> None:
        """Initialize Pattern.

        Args:
            pattern: The regular expression pattern string.
            flags: Regular expression flags.
        """
        self._pattern = re.compile(pattern, flags)
        self._flags = flags

    @property
    def pattern(self) -> re.Pattern[str]:
        """Get the compiled pattern."""
        return self._pattern

    @property
    def flags(self) -> int:
        """Get the pattern flags."""
        return self._flags

    def match(self, string: str) -> bool:
        """Check if the string matches the pattern.

        Args:
            string: The string to check.

        Returns:
            True if the string matches the pattern.
        """
        return bool(self._pattern.match(string))

    def find_all(self, string: str) -> list[str]:
        """Find all matches in the string.

        Args:
            string: The string to search.

        Returns:
            List of all matching strings.
        """
        return self._pattern.findall(string)

    def split(self, string: str, maxsplit: int = 0) -> list[str]:
        """Split the string by the pattern.

        Args:
            string: The string to split.
            maxsplit: Maximum number of splits to perform.

        Returns:
            List of split strings.
        """
        return self._pattern.split(string, maxsplit)

    def __str__(self) -> str:
        return self._pattern.pattern

    def __repr__(self) -> str:
        return f"Pattern({self._pattern.pattern!r}, flags={self._flags})"
