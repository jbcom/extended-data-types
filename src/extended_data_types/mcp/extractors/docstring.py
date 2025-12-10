"""Google-style docstring parser for MCP server.

This module provides utilities for parsing Google-style docstrings
to extract structured documentation information.
"""

from __future__ import annotations

import re

from dataclasses import dataclass, field


@dataclass
class ParsedDocstring:
    """Parsed Google-style docstring structure.

    Attributes:
        short_description: First line/paragraph of docstring.
        long_description: Extended description paragraphs.
        args: Dictionary mapping parameter names to (type, description) tuples.
        returns: Description of return value.
        raises: List of (exception_type, description) tuples.
        examples: List of example code blocks.
    """

    short_description: str = ""
    long_description: str = ""
    args: dict[str, tuple[str, str]] = field(default_factory=dict)
    returns: str = ""
    raises: list[tuple[str, str]] = field(default_factory=list)
    examples: list[str] = field(default_factory=list)


class DocstringParser:
    """Parser for Google-style docstrings.

    This parser extracts structured information from Google-style docstrings,
    including descriptions, parameters, return values, exceptions, and examples.

    Example:
        >>> parser = DocstringParser()
        >>> parsed = parser.parse('''
        ...     Short description.
        ...
        ...     Long description here.
        ...
        ...     Args:
        ...         param: Parameter description.
        ...
        ...     Returns:
        ...         Return value description.
        ... ''')
        >>> parsed.short_description
        'Short description.'
    """

    # Section header patterns
    ARGS_SECTION = re.compile(r"^\s*Args?:\s*$", re.MULTILINE)
    RETURNS_SECTION = re.compile(r"^\s*Returns?:\s*$", re.MULTILINE)
    RAISES_SECTION = re.compile(r"^\s*Raises?:\s*$", re.MULTILINE)
    EXAMPLES_SECTION = re.compile(r"^\s*Examples?:\s*$", re.MULTILINE)
    YIELDS_SECTION = re.compile(r"^\s*Yields?:\s*$", re.MULTILINE)
    ATTRIBUTES_SECTION = re.compile(r"^\s*Attributes?:\s*$", re.MULTILINE)
    NOTE_SECTION = re.compile(r"^\s*Note:\s*$", re.MULTILINE)
    WARNING_SECTION = re.compile(r"^\s*Warning:\s*$", re.MULTILINE)

    # Parameter pattern: "param_name (type): description" or "param_name: description"
    PARAM_PATTERN = re.compile(
        r"^\s*(\w+)\s*(?:\(([^)]+)\))?\s*:\s*(.+?)(?=(?:\n\s*\w+\s*(?:\([^)]+\))?\s*:)|(?:\n\s*\n)|$)",
        re.MULTILINE | re.DOTALL,
    )

    # Exception pattern: "ExceptionType: description"
    EXCEPTION_PATTERN = re.compile(
        r"^\s*(\w+(?:\.\w+)*):\s*(.+?)(?=(?:\n\s*\w+(?:\.\w+)*:)|(?:\n\s*\n)|$)",
        re.MULTILINE | re.DOTALL,
    )

    def parse(self, docstring: str | None) -> ParsedDocstring:
        r"""Parse a Google-style docstring.

        Args:
            docstring: The docstring to parse. Can be None for functions without docstrings.

        Returns:
            ParsedDocstring object with extracted information.

        Example:
            >>> parser = DocstringParser()
            >>> result = parser.parse("Short description.\n\nLong description.")
            >>> result.short_description
            'Short description.'
        """
        if not docstring:
            return ParsedDocstring()

        # Normalize whitespace and remove leading/trailing whitespace
        docstring = self._normalize_docstring(docstring)

        # Split docstring into sections
        sections = self._split_sections(docstring)

        # Parse each section
        result = ParsedDocstring()

        # Parse description (everything before first section)
        if "description" in sections:
            result.short_description, result.long_description = self._parse_description(
                sections["description"]
            )

        # Parse Args section
        if "args" in sections:
            result.args = self._parse_args(sections["args"])

        # Parse Returns section
        if "returns" in sections:
            result.returns = self._clean_text(sections["returns"])

        # Parse Raises section
        if "raises" in sections:
            result.raises = self._parse_raises(sections["raises"])

        # Parse Examples section
        if "examples" in sections:
            result.examples = self._parse_examples(sections["examples"])

        return result

    def _normalize_docstring(self, docstring: str) -> str:
        """Normalize docstring whitespace and indentation.

        Args:
            docstring: Raw docstring text.

        Returns:
            Normalized docstring with consistent indentation.
        """
        # Split into lines
        lines = docstring.split("\n")

        # Remove leading and trailing blank lines
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()

        if not lines:
            return ""

        # Find minimum indentation (excluding blank lines)
        min_indent = float("inf")
        for line in lines:
            if line.strip():
                indent = len(line) - len(line.lstrip())
                min_indent = min(min_indent, indent)

        # Remove minimum indentation from all lines
        if min_indent != float("inf"):
            lines = [line[int(min_indent) :] if line.strip() else "" for line in lines]

        return "\n".join(lines)

    def _split_sections(self, docstring: str) -> dict[str, str]:
        """Split docstring into sections.

        Args:
            docstring: Normalized docstring text.

        Returns:
            Dictionary mapping section names to their content.
        """
        sections: dict[str, str] = {}

        # Find all section headers and their positions
        section_markers = []

        for pattern, name in [
            (self.ARGS_SECTION, "args"),
            (self.RETURNS_SECTION, "returns"),
            (self.RAISES_SECTION, "raises"),
            (self.EXAMPLES_SECTION, "examples"),
            (self.YIELDS_SECTION, "yields"),
            (self.ATTRIBUTES_SECTION, "attributes"),
            (self.NOTE_SECTION, "note"),
            (self.WARNING_SECTION, "warning"),
        ]:
            match = pattern.search(docstring)
            if match:
                section_markers.append((match.start(), match.end(), name))

        # Sort by position
        section_markers.sort()

        # Extract description (everything before first section)
        if section_markers:
            sections["description"] = docstring[: section_markers[0][0]].strip()
        else:
            sections["description"] = docstring.strip()
            return sections

        # Extract each section's content
        for i, (_start, end, name) in enumerate(section_markers):
            # Find the end of this section (start of next section or end of string)
            if i + 1 < len(section_markers):
                section_end = section_markers[i + 1][0]
            else:
                section_end = len(docstring)

            sections[name] = docstring[end:section_end].strip()

        return sections

    def _parse_description(self, text: str) -> tuple[str, str]:
        """Parse description into short and long parts.

        Args:
            text: Description text to parse.

        Returns:
            Tuple of (short_description, long_description).
        """
        if not text:
            return ("", "")

        # Split by double newline or first period followed by newline
        paragraphs = re.split(r"\n\s*\n", text.strip())

        if not paragraphs:
            return ("", "")

        # First paragraph is short description
        short = paragraphs[0].strip()

        # If short description is multiple lines, take only the first line
        short_lines = short.split("\n")
        if len(short_lines) > 1:
            # If first line ends with period, use it
            if short_lines[0].strip().endswith("."):
                short = short_lines[0].strip()
                # Remaining lines become part of long description
                remaining = "\n".join(short_lines[1:])
                long_parts = [remaining, *paragraphs[1:]]
            else:
                # Otherwise use entire first paragraph
                short = paragraphs[0].strip()
                long_parts = paragraphs[1:]
        else:
            long_parts = paragraphs[1:]

        # Remaining paragraphs are long description
        long = "\n\n".join(p.strip() for p in long_parts if p.strip())

        return (short, long)

    def _parse_args(self, text: str) -> dict[str, tuple[str, str]]:
        """Parse Args section.

        Args:
            text: Args section content.

        Returns:
            Dictionary mapping parameter names to (type, description) tuples.
        """
        args: dict[str, tuple[str, str]] = {}

        # Split into lines and process parameter by parameter
        lines = text.split("\n")
        current_param: str | None = None
        current_type = ""
        current_desc_lines: list[str] = []

        for line in lines:
            # Check if this is a new parameter definition
            param_match = re.match(r"^\s*(\w+)\s*(?:\(([^)]+)\))?\s*:\s*(.*)$", line)
            if param_match:
                # Save previous parameter if exists
                if current_param:
                    desc = " ".join(current_desc_lines).strip()
                    args[current_param] = (current_type, desc)

                # Start new parameter
                current_param = param_match.group(1).strip()
                current_type = (
                    param_match.group(2).strip() if param_match.group(2) else ""
                )
                current_desc_lines = [param_match.group(3).strip()]
            elif current_param and line.strip():
                # Continuation of current parameter description
                current_desc_lines.append(line.strip())

        # Save last parameter
        if current_param:
            desc = " ".join(current_desc_lines).strip()
            args[current_param] = (current_type, desc)

        return args

    def _parse_raises(self, text: str) -> list[tuple[str, str]]:
        """Parse Raises section.

        Args:
            text: Raises section content.

        Returns:
            List of (exception_type, description) tuples.
        """
        raises: list[tuple[str, str]] = []

        # Split into lines and process exception by exception
        lines = text.split("\n")
        current_exception: str | None = None
        current_desc_lines: list[str] = []

        for line in lines:
            # Check if this is a new exception definition
            exc_match = re.match(r"^\s*(\w+(?:\.\w+)*):\s*(.*)$", line)
            if exc_match:
                # Save previous exception if exists
                if current_exception:
                    desc = " ".join(current_desc_lines).strip()
                    raises.append((current_exception, desc))

                # Start new exception
                current_exception = exc_match.group(1).strip()
                current_desc_lines = [exc_match.group(2).strip()]
            elif current_exception and line.strip():
                # Continuation of current exception description
                current_desc_lines.append(line.strip())

        # Save last exception
        if current_exception:
            desc = " ".join(current_desc_lines).strip()
            raises.append((current_exception, desc))

        return raises

    def _parse_examples(self, text: str) -> list[str]:
        """Parse Examples section.

        Args:
            text: Examples section content.

        Returns:
            List of example code blocks.
        """
        if not text:
            return []

        # Examples can be:
        # 1. Doctest format (>>> and ...)
        # 2. Code blocks (indented)
        # 3. Plain text descriptions

        # Split by double newline to separate multiple examples
        blocks = re.split(r"\n\s*\n", text.strip())

        return [self._clean_text(block) for block in blocks if block.strip()]

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text.

        Args:
            text: Text to clean.

        Returns:
            Cleaned text with normalized whitespace.
        """
        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text)
        return text.strip()
