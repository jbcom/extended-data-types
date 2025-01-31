"""Tests for HCL2 serializer integration."""

from __future__ import annotations

from textwrap import dedent

import pytest

from extended_data_types.serialization import get_serializer
from extended_data_types.serialization.languages.hcl2.serializer import HCL2Serializer


def test_serializer_registration():
    """Test HCL2 serializer registration in registry."""
    serializer = get_serializer("hcl2")
    assert isinstance(serializer, HCL2Serializer)


def test_encode_basic_structure():
    """Test encoding basic dictionary to HCL2."""
    serializer = HCL2Serializer()

    data = {
        "resource": {
            "aws_instance": {
                "web": {"instance_type": "t2.micro", "tags": {"Name": "web-server"}}
            }
        }
    }

    result = serializer.encode(data)
    expected = dedent(
        """\
        resource "aws_instance" "web" {
          instance_type = "t2.micro"
          tags = {
            Name = "web-server"
          }
        }
        """
    )

    assert result.strip() == expected.strip()


def test_decode_basic_structure():
    """Test decoding HCL2 to dictionary."""
    serializer = HCL2Serializer()

    content = dedent(
        """\
        resource "aws_instance" "web" {
          instance_type = "t2.micro"
          tags = {
            Name = "web-server"
          }
        }
        """
    )

    result = serializer.decode(content)
    expected = {
        "resource": {
            "aws_instance": {
                "web": {"instance_type": "t2.micro", "tags": {"Name": "web-server"}}
            }
        }
    }

    assert result == expected


def test_terraform_configuration():
    """Test handling of terraform configuration block."""
    serializer = HCL2Serializer()

    data = {
        "terraform": {
            "required_version": ">= 1.0.0",
            "required_providers": {
                "aws": {"source": "hashicorp/aws", "version": "~> 4.0"}
            },
        }
    }

    result = serializer.encode(data)
    decoded = serializer.decode(result)
    assert decoded == data


def test_multiple_resources():
    """Test handling multiple resources and block types."""
    serializer = HCL2Serializer()

    data = {
        "resource": {
            "aws_instance": {
                "web": {"instance_type": "t2.micro"},
                "db": {"instance_type": "t2.medium"},
            }
        },
        "variable": {"environment": {"type": "string", "default": "dev"}},
    }

    result = serializer.encode(data)
    decoded = serializer.decode(result)
    assert decoded == data


def test_serializer_options():
    """Test serializer formatting options."""
    data = {"resource": {"aws_instance": {"web": {"c": 3, "a": 1, "b": 2}}}}

    # Test with default options
    serializer = HCL2Serializer()
    result = serializer.encode(data)
    assert "  c = 3" in result

    # Test with custom indentation
    serializer = HCL2Serializer(indent_size=4)
    result = serializer.encode(data)
    assert "    c = 3" in result

    # Test with sorted keys
    serializer = HCL2Serializer(sort_keys=True)
    result = serializer.encode(data)
    lines = result.strip().split("\n")
    assert "  a = 1" in lines[1]
    assert "  b = 2" in lines[2]
    assert "  c = 3" in lines[3]


def test_error_handling():
    """Test error handling in serializer."""
    serializer = HCL2Serializer()

    # Test invalid input type
    with pytest.raises(TypeError):
        serializer.encode(["not", "a", "dict"])

    # Test invalid HCL syntax
    with pytest.raises(ValueError):
        serializer.decode("invalid { syntax")


def test_complex_structures():
    """Test handling of complex nested structures."""
    serializer = HCL2Serializer()

    data = {
        "module": {
            "vpc": {
                "main": {
                    "source": "terraform-aws-modules/vpc/aws",
                    "version": "3.0.0",
                    "cidr": "10.0.0.0/16",
                    "azs": ["us-west-2a", "us-west-2b", "us-west-2c"],
                    "private_subnets": ["10.0.1.0/24", "10.0.2.0/24"],
                    "public_subnets": ["10.0.101.0/24", "10.0.102.0/24"],
                    "tags": {"Terraform": "true", "Environment": "dev"},
                }
            }
        }
    }

    result = serializer.encode(data)
    decoded = serializer.decode(result)
    assert decoded == data


def test_registry_integration():
    """Test integration with serialization registry."""
    from extended_data_types.serialization import get_serializer, list_serializers

    # Check if hcl2 is in available serializers
    assert "hcl2" in list_serializers()

    # Get serializer from registry
    serializer = get_serializer("hcl2")
    assert isinstance(serializer, HCL2Serializer)

    # Test basic functionality through registry
    data = {"resource": {"aws_instance": {"web": {"instance_type": "t2.micro"}}}}

    encoded = serializer.encode(data)
    decoded = serializer.decode(encoded)
    assert decoded == data
