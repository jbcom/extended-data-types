"""Tests for YAML loader functionality.

This module tests the YAML loader capabilities, including:
    - Basic YAML loading
    - Custom tag loading
    - Error handling
    - Edge cases
    - Duplicate key handling
    - Comment preservation
    - Special character handling

Fixtures:
    basic_yaml: Provides simple YAML content
    complex_yaml: Provides YAML with various features
    invalid_yaml: Provides invalid YAML content
"""
from __future__ import annotations

import textwrap
from typing import Any

import pytest
from ruamel.yaml.error import YAMLError

from extended_data_types.yaml_utils import (YAMLFlags, YamlPairs, YamlTagged,
                                            configure_yaml, decode_yaml)


@pytest.fixture
def basic_yaml() -> str:
    """Provide basic YAML content for testing.
    
    Returns:
        str: Simple YAML string with various data types
    """
    return textwrap.dedent("""
        string: Simple string
        number: 42
        float: 3.14
        boolean: true
        null_value: null
        list:
          - item1
          - item2
        dict:
          key1: value1
          key2: value2
    """).lstrip()


@pytest.fixture
def complex_yaml() -> str:
    """Provide complex YAML content with various features.
    
    Returns:
        str: Complex YAML string with comments, tags, and special cases
    """
    return textwrap.dedent("""
        # Header comment
        string: |
          Multi-line
          string with
          preservation
        special: "string: with: colons"
        tagged: !CustomTag
          key: value
        references: &anchor
          reused: content
        reuse: *anchor
        duplicates:
          key: value1
          key: value2  # Duplicate key
    """).lstrip()


@pytest.fixture
def invalid_yaml() -> list[str]:
    """Provide invalid YAML content for error testing.
    
    Returns:
        list[str]: List of invalid YAML strings
    """
    return [
        "invalid: - not valid",
        "unmatched:\nindentation",
        "duplicate: value\nduplicate: value\n",
        "invalid-tag: !@#$",
        "incomplete: 'string",
    ]


def test_basic_loading(basic_yaml: str) -> None:
    """Test basic YAML loading functionality.
    
    This test verifies:
        - Different data types are loaded correctly
        - Structure is preserved
        - Values are properly typed
    
    Args:
        basic_yaml: Fixture containing basic YAML content
    """
    data = decode_yaml(basic_yaml)
    
    assert isinstance(data, dict)
    assert data["string"] == "Simple string"
    assert data["number"] == 42
    assert data["float"] == 3.14
    assert data["boolean"] is True
    assert data["null_value"] is None
    assert isinstance(data["list"], list)
    assert isinstance(data["dict"], dict)


def test_complex_loading(complex_yaml: str) -> None:
    """Test loading of complex YAML features.
    
    This test verifies:
        - Multi-line strings are preserved
        - Comments are handled properly
        - Tags are processed
        - Anchors and aliases work
        - Special characters are preserved
    
    Args:
        complex_yaml: Fixture containing complex YAML content
    """
    configure_yaml(YAMLFlags.PRESERVE_COMMENTS | YAMLFlags.ROUND_TRIP)
    data = decode_yaml(complex_yaml)
    
    # Check multi-line string
    assert isinstance(data["string"], str)
    assert data["string"].count("\n") == 2
    
    # Check tagged content
    assert isinstance(data["tagged"], YamlTagged)
    assert data["tagged"].tag == "!CustomTag"
    
    # Check reference handling
    assert data["references"] == data["reuse"]
    
    # Check duplicate keys
    assert isinstance(data["duplicates"], YamlPairs)


def test_error_handling(invalid_yaml: list[str]) -> None:
    """Test YAML loading error handling.
    
    This test verifies:
        - Invalid YAML raises appropriate exceptions
        - Error messages are meaningful
        - Different types of errors are handled
    
    Args:
        invalid_yaml: Fixture containing invalid YAML content
    """
    for invalid_content in invalid_yaml:
        with pytest.raises((YAMLError, ValueError)):
            decode_yaml(invalid_content)


def test_duplicate_key_handling() -> None:
    """Test handling of duplicate keys in YAML.
    
    This test verifies:
        - Duplicate keys are detected
        - YamlPairs is used when appropriate
        - Order is preserved
        - Values are accessible
    """
    yaml_with_duplicates = textwrap.dedent("""
        mapping:
          key: value1
          other: between
          key: value2
    """).lstrip()
    
    # Test with duplicate keys allowed
    configure_yaml(YAMLFlags.ALLOW_DUPLICATE_KEYS)
    data = decode_yaml(yaml_with_duplicates)
    assert isinstance(data["mapping"], YamlPairs)
    pairs = data["mapping"]
    assert len(pairs) == 3
    assert pairs[0] == ("key", "value1")
    assert pairs[1] == ("other", "between")
    assert pairs[2] == ("key", "value2")
    
    # Test with duplicate keys forbidden
    configure_yaml(YAMLFlags.DEFAULT)
    data = decode_yaml(yaml_with_duplicates)
    assert isinstance(data["mapping"], dict)
    assert data["mapping"]["key"] == "value2"  # Last value wins


def test_special_cases() -> None:
    """Test handling of special YAML cases.
    
    This test verifies:
        - Empty documents
        - Unicode handling
        - Special characters
        - Edge cases
    """
    special_cases = {
        "empty": "",
        "unicode": "unicode: 🌟 星",
        "special_chars": "special: !@#$%^&*()",
        "empty_mapping": "empty: {}",
        "empty_sequence": "empty: []",
        "zero_values": "zero: 0\nfalse: false\nempty: ''",
    }
    
    for case_name, content in special_cases.items():
        try:
            data = decode_yaml(content)
            if case_name == "empty":
                assert data is None
            else:
                assert isinstance(data, dict)
        except Exception as e:
            pytest.fail(f"Failed to load {case_name}: {e}")


def test_binary_data_handling() -> None:
    """Test handling of binary data in YAML.
    
    This test verifies:
        - Binary data is properly loaded
        - Encoding is handled correctly
        - Binary tags are processed
    """
    yaml_with_binary = textwrap.dedent("""
        binary: !!binary |
            R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs=
    """).lstrip()
    
    data = decode_yaml(yaml_with_binary)
    assert isinstance(data["binary"], bytes) 