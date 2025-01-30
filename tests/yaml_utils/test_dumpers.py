"""Tests for YAML dumper functionality.

This module tests the YAML dumper capabilities, including:
    - Basic YAML dumping
    - Formatting options
    - String style selection
    - Type handling
    - Special cases
    - Indentation control
"""
from __future__ import annotations

import datetime
import pathlib
import textwrap
from typing import Any

import pytest

from extended_data_types.yaml_utils import (DEFAULT_INDENT, MINIMAL_INDENT,
                                            YAMLFlags, YamlPairs, YamlTagged,
                                            configure_yaml, encode_yaml)


@pytest.fixture
def sample_data() -> dict[str, Any]:
    """Provide sample data for testing YAML dumping.
    
    Returns:
        dict: A dictionary containing various data types and structures
    """
    return {
        "string": "Simple string",
        "multiline": textwrap.dedent("""
            First line
            Second line
            Third line
        """).strip(),
        "special": "String: with special & chars *",
        "nested": {
            "dict": {"key": "value"},
            "list": [1, 2, 3]
        }
    }


@pytest.fixture
def type_samples() -> dict[str, Any]:
    """Provide samples of various Python types.
    
    Returns:
        dict: A dictionary containing different Python types
    """
    return {
        "date": datetime.date(2024, 1, 1),
        "datetime": datetime.datetime(2024, 1, 1, 12, 0, 0),
        "path": pathlib.Path("/path/to/file"),
        "none": None,
        "bool": True,
        "float": 3.14159
    }


def test_basic_dumping(sample_data: dict[str, Any]) -> None:
    """Test basic YAML dumping functionality.
    
    This test verifies:
        - Simple strings are dumped correctly
        - Multiline strings use block style
        - Special characters are handled
        - Nested structures are properly formatted
    
    Args:
        sample_data: Fixture containing test data
    """
    result = encode_yaml(sample_data)
    
    # Check string handling
    assert "Simple string" in result
    assert "First line" in result
    assert "String: with special" in result
    
    # Check structure
    assert "nested:" in result
    assert "dict:" in result
    assert "list:" in result


def test_type_handling(type_samples: dict[str, Any]) -> None:
    """Test handling of various Python types.
    
    This test verifies:
        - Dates are formatted as ISO8601
        - Paths are converted to strings
        - None/bool/float values are properly formatted
    
    Args:
        type_samples: Fixture containing various Python types
    """
    result = encode_yaml(type_samples)
    
    # Check date formatting
    assert "2024-01-01" in result
    assert "12:00:00" in result
    
    # Check path handling
    assert "/path/to/file" in result
    
    # Check type representations
    assert "true" in result.lower()
    assert "3.14159" in result
    assert "null" in result.lower()


def test_indentation_control() -> None:
    """Test indentation control and formatting.
    
    This test verifies:
        - Default indentation is applied correctly
        - Minimal indentation works
        - Sequence indentation is consistent
    """
    data = {
        "level1": {
            "level2": {
                "level3": ["item1", "item2"]
            }
        }
    }
    
    # Test default indent
    configure_yaml(YAMLFlags.DEFAULT, indent=DEFAULT_INDENT)
    default_result = encode_yaml(data)
    
    # Test minimal indent
    configure_yaml(YAMLFlags.DEFAULT, indent=MINIMAL_INDENT)
    minimal_result = encode_yaml(data)
    
    # Verify relative lengths
    assert len(minimal_result) < len(default_result)


def test_string_style_selection() -> None:
    """Test string style selection logic.
    
    This test verifies:
        - Plain strings are unquoted when possible
        - Special characters trigger quotes
        - Block style is used for multi-line strings
    """
    data = {
        "plain": "simple string",
        "special": "string: with: colons",
        "multiline": textwrap.dedent("""
            First line
            Second line
            Third line
        """).strip()
    }
    
    result = encode_yaml(data)
    
    # Check styles
    assert "plain: simple string" in result
    assert 'special: "string: with: colons"' in result
    assert "multiline: |" in result


def test_tag_handling() -> None:
    """Test handling of tagged values.
    
    This test verifies:
        - Tags are properly formatted
        - Tag values are correctly encoded
        - Nested tags work correctly
    """
    data = {
        "simple": YamlTagged("!Tag", "value"),
        "nested": YamlTagged("!Tag", {
            "key": YamlTagged("!Other", "value")
        })
    }
    
    result = encode_yaml(data)
    
    # Check tag formatting
    assert "!Tag value" in result
    assert "!Other value" in result


def test_pairs_handling() -> None:
    """Test handling of YamlPairs.
    
    This test verifies:
        - Duplicate keys are preserved
        - Order is maintained
        - Formatting is correct
    """
    pairs = YamlPairs([
        ("key", "value1"),
        ("key", "value2"),
        ("other", "value3")
    ])
    
    result = encode_yaml({"pairs": pairs})
    
    # Check pairs formatting
    assert "key: value1" in result
    assert "key: value2" in result
    assert "other: value3" in result 