"""Tests for data export utilities."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import pytest

from extended_data_types.serialization.exporting import wrap_for_export


class TestWrapForExport:
    """Tests for wrap_for_export function."""

    @pytest.fixture()
    def complex_data(self) -> dict[str, Any]:
        """Fixture providing complex test data."""
        return {
            "string": "value",
            "number": 42,
            "float": 3.14,
            "boolean": True,
            "none": None,
            "list": [1, 2, 3],
            "dict": {"nested": "value"},
            "date": datetime(2024, 1, 1),
            "path": Path("/test/path"),
        }

    def test_yaml_export(self, complex_data):
        """Test YAML export format."""
        result = wrap_for_export(complex_data, format="yaml")
        assert isinstance(result, str)
        assert "string: value" in result
        assert "number: 42" in result
        assert "float: 3.14" in result
        assert "boolean: true" in result
        assert "none: null" in result
        assert "list:" in result
        assert "dict:" in result
        assert "nested: value" in result
        assert "2024-01-01T00:00:00" in result
        assert "/test/path" in result

    def test_json_export(self, complex_data):
        """Test JSON export format."""
        result = wrap_for_export(complex_data, format="json")
        assert isinstance(result, str)
        assert '"string": "value"' in result
        assert '"number": 42' in result
        assert '"float": 3.14' in result
        assert '"boolean": true' in result
        assert '"none": null' in result
        assert '"list": [1, 2, 3]' in result
        assert '"dict": {' in result
        assert '"nested": "value"' in result
        assert '"2024-01-01T00:00:00"' in result
        assert '"/test/path"' in result

    def test_toml_export(self, complex_data):
        """Test TOML export format."""
        result = wrap_for_export(complex_data, format="toml")
        assert isinstance(result, str)
        assert 'string = "value"' in result
        assert "number = 42" in result
        assert "float = 3.14" in result
        assert "boolean = true" in result
        assert "list = [1, 2, 3]" in result
        assert "[dict]" in result
        assert 'nested = "value"' in result

    def test_raw_export(self, complex_data):
        """Test raw string export."""
        result = wrap_for_export(complex_data, format="raw")
        assert isinstance(result, str)
        assert str(complex_data) == result

    def test_auto_format_detection(self):
        """Test automatic format detection."""
        # Simple data should use YAML
        simple_data = {"key": "value"}
        result = wrap_for_export(simple_data, format=True)
        assert "key: value" in result

        # Complex nested data should use JSON
        complex_data = {"key": {"nested": [1, 2, {"deep": "value"}]}}
        result = wrap_for_export(complex_data, format=True)
        assert '"key":' in result
        assert '"nested":' in result

    def test_boolean_format_handling(self, complex_data):
        """Test boolean format specifications."""
        # True should auto-detect
        result_true = wrap_for_export(complex_data, format=True)
        assert isinstance(result_true, str)

        # False should return raw string
        result_false = wrap_for_export(complex_data, format=False)
        assert isinstance(result_false, str)
        assert result_false == str(complex_data)

    def test_string_boolean_format(self, complex_data):
        """Test string boolean format specifications."""
        # "true" should auto-detect
        result_true = wrap_for_export(complex_data, format="true")
        assert isinstance(result_true, str)

        # "false" should return raw string
        result_false = wrap_for_export(complex_data, format="false")
        assert isinstance(result_false, str)
        assert result_false == str(complex_data)

    def test_format_options(self):
        """Test format-specific options."""
        data = {"key": "value"}

        # Test JSON indentation
        result = wrap_for_export(data, format="json", indent=4)
        assert "    " in result

        # Test JSON sorting
        data = {"b": 2, "a": 1}
        result = wrap_for_export(data, format="json", sort_keys=True)
        assert result.index('"a"') < result.index('"b"')

    @pytest.mark.parametrize(
        "invalid_format",
        [
            "invalid",
            "xml",  # Not supported for export
            "123",
            "",
            "yaml2",
        ],
    )
    def test_invalid_formats(self, invalid_format):
        """Test handling of invalid format specifications."""
        with pytest.raises(ValueError, match="Invalid format value"):
            wrap_for_export({"key": "value"}, format=invalid_format)

    def test_special_types_conversion(self):
        """Test conversion of special types."""
        special_data = {
            "date": datetime(2024, 1, 1),
            "path": Path("/test/path"),
            "set": {1, 2, 3},
            "bytes": b"test",
        }

        result = wrap_for_export(special_data, format="json")
        assert isinstance(result, str)
        assert "2024-01-01" in result
        assert "/test/path" in result
        assert "[1, 2, 3]" in result
        assert "test" in result
