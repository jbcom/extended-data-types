"""Metadata extraction utilities for MCP server."""

from __future__ import annotations

from extended_data_types.mcp.extractors.docstring import (
    DocstringParser,
    ParsedDocstring,
)
from extended_data_types.mcp.extractors.examples import Example, ExampleExtractor
from extended_data_types.mcp.extractors.signature import (
    extract_parameters,
    extract_return_type,
    extract_signature,
    format_type,
)


__all__ = [
    "DocstringParser",
    "Example",
    "ExampleExtractor",
    "ParsedDocstring",
    "extract_parameters",
    "extract_return_type",
    "extract_signature",
    "format_type",
]
