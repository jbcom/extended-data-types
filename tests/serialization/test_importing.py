"""Tests for serialization import utilities."""

from __future__ import annotations

import pytest

from extended_data_types.core.exceptions import SerializationError
from extended_data_types.serialization.importing import unwrap_imported_data


class TestUnwrapImportedData:
    """Tests for unwrap_imported_data function."""

    def test_json_import(self):
        """Test importing JSON data."""
        # Simple JSON
        assert unwrap_imported_data('{"key": "value"}', "json") == {"key": "value"}

        # Complex JSON
        complex_json = """
        {
            "string": "value",
            "number": 42,
            "float": 3.14,
            "boolean": true,
            "null": null,
            "array": [1, 2, 3],
            "object": {
                "nested": "value"
            }
        }
        """
        result = unwrap_imported_data(complex_json, "json")
        assert result["string"] == "value"
        assert result["number"] == 42
        assert result["float"] == 3.14
        assert result["boolean"] is True
        assert result["null"] is None
        assert result["array"] == [1, 2, 3]
        assert result["object"]["nested"] == "value"

    def test_yaml_import(self):
        """Test importing YAML data."""
        # Simple YAML
        assert unwrap_imported_data("key: value", "yaml") == {"key": "value"}

        # Complex YAML
        complex_yaml = """
        string: value
        number: 42
        float: 3.14
        boolean: true
        null: null
        array:
          - 1
          - 2
          - 3
        object:
          nested: value
        """
        result = unwrap_imported_data(complex_yaml, "yaml")
        assert result["string"] == "value"
        assert result["number"] == 42
        assert result["float"] == 3.14
        assert result["boolean"] is True
        assert result["null"] is None
        assert result["array"] == [1, 2, 3]
        assert result["object"]["nested"] == "value"

    def test_toml_import(self):
        """Test importing TOML data."""
        # Simple TOML
        assert unwrap_imported_data('key = "value"', "toml") == {"key": "value"}

        # Complex TOML
        complex_toml = """
        string = "value"
        number = 42
        float = 3.14
        boolean = true

        array = [1, 2, 3]

        [object]
        nested = "value"
        """
        result = unwrap_imported_data(complex_toml, "toml")
        assert result["string"] == "value"
        assert result["number"] == 42
        assert result["float"] == 3.14
        assert result["boolean"] is True
        assert result["array"] == [1, 2, 3]
        assert result["object"]["nested"] == "value"

    def test_default_yaml(self):
        """Test that YAML is the default format."""
        data = "key: value"
        assert unwrap_imported_data(data) == {"key": "value"}

    def test_case_insensitive_format(self):
        """Test that format specification is case-insensitive."""
        data = '{"key": "value"}'
        assert unwrap_imported_data(data, "JSON") == {"key": "value"}
        assert unwrap_imported_data(data, "json") == {"key": "value"}
        assert unwrap_imported_data(data, "JsOn") == {"key": "value"}

    def test_invalid_format(self):
        """Test handling of invalid format specifications."""
        with pytest.raises(ValueError, match="Unsupported encoding format"):
            unwrap_imported_data("data", "invalid_format")

    def test_invalid_data(self):
        """Test handling of invalid data for each format."""
        # Invalid JSON
        with pytest.raises(SerializationError):
            unwrap_imported_data("{invalid json}", "json")

        # Invalid YAML
        with pytest.raises(SerializationError):
            unwrap_imported_data("{{invalid: yaml}}", "yaml")

        # Invalid TOML
        with pytest.raises(SerializationError):
            unwrap_imported_data("invalid toml", "toml")

    def test_empty_data(self):
        """Test handling of empty data."""
        with pytest.raises(SerializationError):
            unwrap_imported_data("", "json")

        with pytest.raises(SerializationError):
            unwrap_imported_data("", "yaml")

        with pytest.raises(SerializationError):
            unwrap_imported_data("", "toml")
