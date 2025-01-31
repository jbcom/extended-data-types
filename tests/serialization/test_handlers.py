"""Tests for the serialization handlers."""

import pytest

from extended_data_types.serialization.handlers import (SerializationError,
                                                        SerializationHandler)


def test_serialize_json():
    """Test JSON serialization."""
    handler = SerializationHandler()
    data = {"key": "value", "nested": {"list": [1, 2, 3]}}
    
    result = handler.serialize(data, "json")
    assert '"key": "value"' in result
    assert '"nested"' in result
    assert '[1, 2, 3]' in result


def test_serialize_hcl2():
    """Test HCL2 serialization."""
    handler = SerializationHandler()
    data = {
        "resource": {
            "aws_instance": {
                "example": {
                    "instance_type": "t2.micro"
                }
            }
        }
    }
    
    result = handler.serialize(data, "hcl2")
    assert 'resource "aws_instance" "example"' in result
    assert 'instance_type = "t2.micro"' in result


def test_invalid_format():
    """Test handling of invalid formats."""
    handler = SerializationHandler()
    with pytest.raises(ValueError):
        handler.serialize({"key": "value"}, "invalid") 