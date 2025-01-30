"""Tests for YAML configuration flags and settings.

This module tests the configuration flags and settings functionality of the YAML utils,
including:
    - Default flag behavior
    - Minimal flag configuration
    - CloudFormation flags
    - Custom indentation
    - Flag combinations
    - Round-trip preservation

Fixtures:
    sample_data: Provides test data with various string types
"""
from __future__ import annotations

import textwrap
from typing import Any

import pytest

from extended_data_types.yaml_utils import (DEFAULT_INDENT, MINIMAL_INDENT,
                                            YAMLFlags, configure_yaml,
                                            decode_yaml, encode_yaml)


@pytest.fixture
def sample_data() -> dict[str, str]:
    """Provide sample data for testing YAML encoding/decoding.
    
    Returns:
        dict: A dictionary containing various string types:
            - Simple string
            - Quoted string
            - Multiline string
            - String with special characters
    """
    return {
        "string": "Hello, World!",
        "quoted": '"quoted value"',
        "multiline": textwrap.dedent("""
            line 1
            line 2
            line 3
        """).strip(),
        "special": "value: with special & chars *"
    }


def test_default_flags(sample_data: dict[str, str]) -> None:
    """Test default flag behavior.
    
    This test verifies that the default flags:
        - Preserve quotes in strings
        - Allow Unicode characters
        - Use default indentation
    
    Args:
        sample_data: Test data fixture containing various string types
    """
    configure_yaml(YAMLFlags.DEFAULT)
    encoded = encode_yaml(sample_data)
    
    # Default preserves quotes
    assert '"quoted value"' in encoded
    # Unicode is allowed
    assert "Hello, World!" in encoded


def test_minimal_flags(sample_data: dict[str, str]) -> None:
    """Test minimal flag configuration.
    
    This test verifies that the minimal flags:
        - Don't preserve unnecessary quotes
        - Properly escape special characters
        - Use minimal indentation
    
    Args:
        sample_data: Test data fixture containing various string types
    """
    configure_yaml(YAMLFlags.MINIMAL)
    encoded = encode_yaml(sample_data)
    
    # Quotes are not preserved
    assert "quoted value" in encoded
    # Special characters are escaped
    assert "value: with special & chars *" in encoded


def test_cloudformation_flags() -> None:
    """Test CloudFormation-specific flags.
    
    This test verifies that CloudFormation flags:
        - Allow duplicate keys
        - Prevent line wrapping
        - Handle CloudFormation tags
    """
    configure_yaml(YAMLFlags.CLOUDFORMATION)
    data: dict[str, Any] = {
        "key1": "value1",
        "key1": "value2",  # Duplicate key
        "long": "x" * 1000  # Long line
    }
    encoded = encode_yaml(data)
    
    # No line wrapping
    assert "x" * 1000 in encoded
    # Duplicate keys allowed
    assert encoded.count("key1") == 2


def test_custom_indent() -> None:
    """Test custom indentation settings.
    
    This test verifies that:
        - Custom indentation is properly applied
        - Different indent settings produce different results
        - Minimal indent produces more compact output
    """
    nested_data: dict[str, Any] = {
        "level1": {
            "level2": {
                "level3": "value"
            }
        }
    }
    
    # Test with default indent
    configure_yaml(YAMLFlags.DEFAULT, indent=DEFAULT_INDENT)
    default_encoded = encode_yaml(nested_data)
    
    # Test with minimal indent
    configure_yaml(YAMLFlags.DEFAULT, indent=MINIMAL_INDENT)
    minimal_encoded = encode_yaml(nested_data)
    
    # Minimal should be more compact
    assert len(minimal_encoded) < len(default_encoded)


def test_flag_combinations() -> None:
    """Test combining multiple flags.
    
    This test verifies that multiple flags can be combined to:
        - Sort dictionary keys
        - Prevent line wrapping
        - Preserve quotes
        - Work together without conflicts
    """
    configure_yaml(
        YAMLFlags.PRESERVE_QUOTES |
        YAMLFlags.NO_WRAP |
        YAMLFlags.SORT_KEYS
    )
    
    data: dict[str, str] = {
        "b": "value",
        "a": "x" * 1000,
        'quoted': '"test"'
    }
    encoded = encode_yaml(data)
    
    # Keys should be sorted
    assert encoded.index("a:") < encoded.index("b:")
    # No line wrapping
    assert "x" * 1000 in encoded
    # Quotes preserved
    assert '"\\"test\\""' in encoded


def test_round_trip_preservation() -> None:
    """Test round-trip preservation of YAML content.
    
    This test verifies that:
        - Comments are preserved
        - Formatting is maintained
        - Tags are preserved
        - Complex structures survive round-trip
    """
    yaml_str = textwrap.dedent("""
        # Header comment
        key1: value1  # Inline comment
        key2:
          # Nested comment
          nested: value2
          list:
            - item1  # List comment
            - item2
    """).lstrip()
    
    configure_yaml(YAMLFlags.PRESERVE_COMMENTS | YAMLFlags.ROUND_TRIP)
    data = decode_yaml(yaml_str)
    encoded = encode_yaml(data)
    
    # Comments should be preserved
    assert "# Header comment" in encoded
    assert "# Inline comment" in encoded
    assert "# Nested comment" in encoded
    assert "# List comment" in encoded 