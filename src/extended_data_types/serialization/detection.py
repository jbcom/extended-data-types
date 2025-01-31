"""Format detection utilities for serialization.

This module provides utilities for detecting and analyzing serialization formats
from string content and data structures. It supports all registered formats and
provides both strict parsing and heuristic detection.

Typical usage:
    >>> content = '{"key": "value"}'
    >>> is_potential_json(content)
    True
    >>> guess_format(content)
    'json'
"""

from __future__ import annotations

import json

from typing import Any, Final

import yaml

from hcl2 import loads as hcl2_loads

from ..core.inspection import is_json_serializable
from ..core.types import JsonDict


# Format-specific indicators
JSON_INDICATORS: Final = frozenset(["{", "["])
"""JSON structure indicators."""

YAML_INDICATORS: Final = frozenset(["---", ": ", "\n- ", "&", "* "])
"""YAML structure indicators."""

TOML_INDICATORS: Final = frozenset(["[", " = ", "\n[", '"""'])
"""TOML structure indicators."""

XML_INDICATORS: Final = frozenset(["<?xml", "<!DOCTYPE", "<![CDATA["])
"""XML structure indicators."""

INI_INDICATORS: Final = frozenset(["[", "="])
"""INI structure indicators."""

HCL2_INDICATORS: Final = frozenset(
    [
        'resource "',
        'variable "',
        'provider "',
        'module "',
        'data "',
        "locals {",
        "terraform {",
        "<<-",
        "<<~",
        'dynamic "',
        "for_each = ",
    ]
)
"""HCL2 structure indicators."""


def detect_format(data: str) -> str | None:
    """Detect format through strict parsing.

    Args:
        data: String to analyze

    Returns:
        Detected format or None if unknown

    Examples:
        >>> detect_format('{"key": "value"}')
        'json'
        >>> detect_format('key: value')
        'yaml'
    """
    if not data or not data.strip():
        return None

    # Try JSON first (most strict)
    try:
        json.loads(data)
        return "json"
    except ValueError:
        pass

    # Try HCL2 next
    try:
        hcl2_loads(data)
        return "hcl2"
    except ValueError:
        pass

    # Try YAML last (most permissive)
    try:
        result = yaml.safe_load(data)
        if result is not None:  # YAML can parse 'null' as None
            return "yaml"
    except yaml.YAMLError:
        pass

    # Try format-specific detection
    if is_potential_toml(data):
        return "toml"
    if is_potential_xml(data):
        return "xml"
    if is_potential_ini(data):
        return "ini"
    if is_potential_querystring(data):
        return "querystring"

    return None


def is_yaml_compatible(data: Any) -> bool:
    """Check if data is YAML-compatible.

    Args:
        data: Data to check

    Returns:
        True if data can be cleanly represented in YAML
    """
    # Must be JSON-serializable first
    if not is_json_serializable(data):
        return False

    # Check if it's a simple key-value structure
    if isinstance(data, dict):
        return all(
            isinstance(k, str) and not isinstance(v, (dict, list, tuple))
            for k, v in data.items()
        )

    # Non-dict data is usually better in JSON
    return False


def get_optimal_format(data: Any) -> str:
    """Determine optimal format for data structure.

    Args:
        data: Data to analyze

    Returns:
        Recommended format name
    """
    if isinstance(data, JsonDict) and is_yaml_compatible(data):
        return "yaml"
    if is_json_serializable(data):
        return "json"
    return "raw"


def is_potential_json(data: str) -> bool:
    """Check if string is potentially JSON.

    Args:
        data: String to check

    Returns:
        True if string shows JSON indicators
    """
    data = data.strip()
    return (
        data.startswith("{")
        and data.endswith("}")
        or data.startswith("[")
        and data.endswith("]")
    )


def is_potential_yaml(data: str) -> bool:
    """Check if string is potentially YAML.

    Args:
        data: String to check

    Returns:
        True if string shows YAML indicators
    """
    return any(ind in data for ind in YAML_INDICATORS)


def is_potential_toml(data: str) -> bool:
    """Check if string is potentially TOML.

    Args:
        data: String to check

    Returns:
        True if string shows TOML indicators
    """
    return any(ind in data for ind in TOML_INDICATORS) and not data.strip().startswith(
        "{"
    )


def is_potential_xml(data: str) -> bool:
    """Check if string is potentially XML.

    Args:
        data: String to check

    Returns:
        True if string shows XML indicators
    """
    data = data.strip()
    return any(ind in data for ind in XML_INDICATORS) or (
        data.startswith("<") and data.endswith(">")
    )


def is_potential_ini(data: str) -> bool:
    """Check if string is potentially INI.

    Args:
        data: String to check

    Returns:
        True if string shows INI indicators
    """
    return all(ind in data for ind in INI_INDICATORS) and not any(
        c in data for c in "{[<"
    )


def is_potential_querystring(data: str) -> bool:
    """Check if string is potentially a query string.

    Args:
        data: String to check

    Returns:
        True if string shows query string indicators
    """
    return (
        "=" in data
        and "&" in data
        and not any(c in data for c in "{}[]<>")
        and " " not in data.strip()
    )


def is_potential_hcl2(data: str) -> bool:
    """Check if string is potentially HCL2.

    Args:
        data: String to check

    Returns:
        True if string shows HCL2 indicators
    """
    return any(ind in data for ind in HCL2_INDICATORS) and not data.strip().startswith(
        ("{", "[")
    )


def guess_format(data: str) -> str:
    """Guess format using heuristics.

    Args:
        data: String to analyze

    Returns:
        Best guess at format name

    Note:
        Less reliable than detect_format but faster
    """
    if not data or not data.strip():
        return "unknown"

    # Check formats in order of specificity
    if is_potential_json(data):
        return "json"
    if is_potential_hcl2(data):
        return "hcl2"
    if is_potential_yaml(data):
        return "yaml"
    if is_potential_toml(data):
        return "toml"
    if is_potential_xml(data):
        return "xml"
    if is_potential_ini(data):
        return "ini"
    if is_potential_querystring(data):
        return "querystring"

    return "unknown"
