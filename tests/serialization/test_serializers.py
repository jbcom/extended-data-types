"""Tests for serialization formats and serializers."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest

from extended_data_types.serialization.formats.base import _sanitize
from extended_data_types.serialization.registry import (
    deserialize,
    get_serializer,
    list_formats,
    register_serializer,
    serialize,
)


class MockSerializer:
    """Mock serializer for testing."""

    def loads(self, data: str, **kwargs: Any) -> Any:
        return {"mock": data}

    def dumps(self, obj: Any, **kwargs: Any) -> str:
        return f"mock:{obj}"


@pytest.fixture
def complex_data() -> dict[str, Any]:
    """Fixture providing complex test data."""
    return {
        "string": "value",
        "number": 42,
        "float": 3.14,
        "boolean": True,
        "none": None,
        "list": [1, 2, 3],
        "nested": {
            "key": "value",
            "date": datetime(2024, 1, 1),
            "path": Path("/test/path"),
        },
    }


def test_sanitize_datetime_preserves_time() -> None:
    """Ensure datetime serialization retains time and timezone components."""
    dt = datetime(2024, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
    assert _sanitize(dt) == "2024-01-02T03:04:05+00:00"


class TestSerializerRegistry:
    """Tests for serializer registry."""

    def test_register_serializer(self):
        """Test registering new serializer."""
        register_serializer("mock", MockSerializer())
        assert "mock" in list_formats()

        # Test duplicate registration
        with pytest.raises(ValueError):
            register_serializer("mock", MockSerializer())

    def test_invalid_serializer(self):
        """Test registering invalid serializer."""
        with pytest.raises(ValueError):
            register_serializer("invalid", object())

    def test_get_serializer(self):
        """Test getting registered serializer."""
        serializer = get_serializer("json")
        assert hasattr(serializer, "loads")
        assert hasattr(serializer, "dumps")

        with pytest.raises(KeyError):
            get_serializer("nonexistent")

    def test_list_formats(self):
        """Test listing registered formats."""
        formats = list_formats()
        assert isinstance(formats, list)
        assert all(isinstance(f, str) for f in formats)
        assert "json" in formats
        assert "yaml" in formats
        assert "toml" in formats
        assert "hcl2" in formats


@pytest.mark.parametrize(
    "format_name",
    [
        "json",
        "yaml",
        "toml",
        "hcl2",
        "xml",
        "ini",
    ],
)
class TestSerializers:
    """Tests for individual serializers."""

    def test_serialize_deserialize(
        self, format_name: str, complex_data: dict[str, Any]
    ):
        """Test serialization and deserialization roundtrip."""
        # Serialize
        serialized = serialize(complex_data, format_name)
        assert isinstance(serialized, str)

        # Deserialize
        deserialized = deserialize(serialized, format_name)

        # Check basic structure
        assert isinstance(deserialized, dict)
        assert "string" in deserialized
        assert "number" in deserialized
        assert "list" in deserialized
        assert "nested" in deserialized

        # Check values
        assert deserialized["string"] == "value"
        assert deserialized["number"] == 42
        assert deserialized["list"] == [1, 2, 3]

    def test_special_types(self, format_name: str):
        """Test handling of special types."""
        special_data = {
            "date": datetime(2024, 1, 1),
            "path": Path("/test/path"),
            "bytes": b"test",
            "set": {1, 2, 3},
        }

        # Serialize
        serialized = serialize(special_data, format_name)
        assert isinstance(serialized, str)

        # Deserialize
        deserialized = deserialize(serialized, format_name)
        assert isinstance(deserialized, dict)

    def test_nested_structures(self, format_name: str):
        """Test handling of nested structures."""
        nested_data = {
            "level1": {
                "level2": {
                    "level3": {
                        "key": "value",
                        "list": [1, [2, [3]]],
                    }
                }
            }
        }

        # Serialize
        serialized = serialize(nested_data, format_name)
        assert isinstance(serialized, str)

        # Deserialize
        deserialized = deserialize(serialized, format_name)
        assert isinstance(deserialized, dict)
        assert "level1" in deserialized

    def test_error_handling(self, format_name: str):
        """Test error handling."""
        # Invalid input
        with pytest.raises(Exception):
            serialize(object(), format_name)

        # Invalid serialized data
        with pytest.raises(Exception):
            deserialize("invalid data", format_name)


class TestJSONSerializer:
    """Specific tests for JSON serializer."""

    def test_json_options(self):
        """Test JSON-specific options."""
        data = {"b": 2, "a": 1}

        # Test indentation
        serialized = serialize(data, "json", indent=4)
        assert "    " in serialized

        # Test sorting
        serialized = serialize(data, "json", sort_keys=True)
        assert serialized.index('"a"') < serialized.index('"b"')


class TestYAMLSerializer:
    """Specific tests for YAML serializer."""

    def test_yaml_options(self):
        """Test YAML-specific options."""
        data = {"key": "value"}

        # Test default_flow_style
        serialized = serialize(data, "yaml", default_flow_style=True)
        assert "{" in serialized

        serialized = serialize(data, "yaml", default_flow_style=False)
        assert "key:" in serialized


class TestTOMLSerializer:
    """Specific tests for TOML serializer."""

    def test_toml_structure(self):
        """Test TOML structure handling."""
        data = {
            "table": {
                "key": "value",
                "list": [1, 2, 3],
            }
        }
        serialized = serialize(data, "toml")
        assert "[table]" in serialized
        assert "key =" in serialized
        assert "list =" in serialized


class TestHCL2Serializer:
    """Specific tests for HCL2 serializer."""

    def test_hcl2_structure(self):
        """Test HCL2 structure handling."""
        data = {
            "resource": {
                "aws_instance": {
                    "example": {
                        "ami": "ami-123",
                        "instance_type": "t2.micro",
                    }
                }
            }
        }
        serialized = serialize(data, "hcl2")
        assert "resource" in serialized
        assert "aws_instance" in serialized
        assert "example" in serialized
