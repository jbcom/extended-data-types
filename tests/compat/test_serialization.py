"""Tests for serialization compatibility layer."""

import pytest

from extended_data_types.compat.serialization import (
    detect_format, unwrap_raw_data_from_import, wrap_raw_data_for_export)


def test_wrap_raw_data_compatibility():
    """Test compatibility with bob's wrap_raw_data_for_export."""
    data = {"key": "value"}
    
    # Test boolean allow_encoding
    result_true = wrap_raw_data_for_export(data, True)
    assert "key:" in result_true
    assert "value" in result_true
    
    result_false = wrap_raw_data_for_export(data, False)
    assert str(data) == result_false
    
    # Test string format
    result_json = wrap_raw_data_for_export(data, "json")
    assert '"key":' in result_json
    assert '"value"' in result_json


def test_unwrap_raw_data_compatibility():
    """Test compatibility with bob's unwrap_raw_data_from_import."""
    yaml_data = "key: value"
    result = unwrap_raw_data_from_import(yaml_data, "yaml")
    assert result == {"key": "value"}


def test_format_detection():
    """Test format detection."""
    assert detect_format('{"key": "value"}') == "json"
    assert detect_format("key: value") == "yaml"
    assert detect_format("[section]\nkey = value") == "toml"
    assert detect_format("resource aws_instance") == "hcl2" 