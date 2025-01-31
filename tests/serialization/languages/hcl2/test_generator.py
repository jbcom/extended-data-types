"""Tests for HCL2 generator functionality."""

from __future__ import annotations

from textwrap import dedent

import pytest

from extended_data_types.serialization.languages.hcl2.generator import \
    HCL2Generator
from extended_data_types.serialization.languages.hcl2.types import (
    Block, BlockType, Expression, Function, HCLFile, MetaArguments, Reference)


def test_generate_basic_block():
    """Test generation of basic block structure."""
    generator = HCL2Generator()
    
    block = Block(
        type=BlockType.RESOURCE,
        labels=["aws_instance", "web"],
        attributes={
            "instance_type": "t2.micro",
            "tags": {"Name": "web-server"}
        }
    )
    
    result = generator.generate(HCLFile(blocks=[block]))
    expected = dedent("""\
        resource "aws_instance" "web" {
          instance_type = "t2.micro"
          tags = {
            Name = "web-server"
          }
        }
        """)
    
    assert result == expected

def test_generate_nested_blocks():
    """Test generation of nested block structures."""
    generator = HCL2Generator()
    
    block = Block(
        type=BlockType.RESOURCE,
        labels=["aws_instance", "web"],
        attributes={"instance_type": "t2.micro"},
        blocks=[
            Block(
                type=BlockType.RESOURCE,
                labels=[],
                attributes={
                    "network_interface_id": Reference("aws_network_interface", "web", "id"),
                    "device_index": 0
                }
            )
        ]
    )
    
    result = generator.generate(HCLFile(blocks=[block]))
    expected = dedent("""\
        resource "aws_instance" "web" {
          instance_type = "t2.micro"
          
          network_interface {
            network_interface_id = aws_network_interface.web.id
            device_index = 0
          }
        }
        """)
    
    assert result.strip() == expected.strip()

def test_generate_meta_arguments():
    """Test generation of meta-arguments."""
    generator = HCL2Generator()
    
    block = Block(
        type=BlockType.RESOURCE,
        labels=["aws_instance", "web"],
        attributes={"instance_type": "t2.micro"},
        meta_args=MetaArguments(
            count=Expression("2"),
            for_each=Expression("var.environments"),
            provider="aws.west",
            depends_on=["aws_vpc.main"],
            lifecycle={"create_before_destroy": True}
        )
    )
    
    result = generator.generate(HCLFile(blocks=[block]))
    expected = dedent("""\
        resource "aws_instance" "web" {
          count = 2
          for_each = var.environments
          provider = "aws.west"
          depends_on = ["aws_vpc.main"]
          lifecycle {
            create_before_destroy = true
          }
          
          instance_type = "t2.micro"
        }
        """)
    
    assert result.strip() == expected.strip()

def test_generate_expressions():
    """Test generation of various expression types."""
    generator = HCL2Generator()
    
    block = Block(
        type=BlockType.LOCALS,
        labels=[],
        attributes={
            "instance_type": Expression('var.environment == "prod" ? "t2.large" : "t2.micro"'),
            "name": Function("format", ["web-%s", Reference("var", "environment")]),
            "ports": [80, 443, Reference("var", "extra_port")]
        }
    )
    
    result = generator.generate(HCLFile(blocks=[block]))
    expected = dedent("""\
        locals {
          instance_type = var.environment == "prod" ? "t2.large" : "t2.micro"
          name = format("web-%s", var.environment)
          ports = [80, 443, var.extra_port]
        }
        """)
    
    assert result.strip() == expected.strip()

def test_generate_heredoc():
    """Test generation of heredoc strings."""
    generator = HCL2Generator()
    
    policy = '''{
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": "*",
          "Resource": "*"
        }
      ]
    }'''
    
    block = Block(
        type=BlockType.RESOURCE,
        labels=["aws_iam_policy", "example"],
        attributes={"policy": policy}
    )
    
    result = generator.generate(HCLFile(blocks=[block]))
    assert "<<-EOT" in result
    assert policy in result
    assert "EOT" in result

def test_generate_terraform_block():
    """Test generation of terraform configuration block."""
    generator = HCL2Generator()
    
    hcl_file = HCLFile(
        terraform_version=">= 1.0.0",
        required_providers={
            "aws": {
                "source": "hashicorp/aws",
                "version": "~> 4.0"
            }
        }
    )
    
    result = generator.generate(hcl_file)
    expected = dedent("""\
        terraform {
          required_version = ">= 1.0.0"
          required_providers {
            aws = {
              source = "hashicorp/aws"
              version = "~> 4.0"
            }
          }
        }
        """)
    
    assert result.strip() == expected.strip()

def test_generator_options():
    """Test generator formatting options."""
    block = Block(
        type=BlockType.RESOURCE,
        labels=["aws_instance", "web"],
        attributes={
            "c": 3,
            "a": 1,
            "b": 2
        }
    )
    
    # Test with default options
    generator = HCL2Generator()
    result = generator.generate(HCLFile(blocks=[block]))
    assert "  c = 3" in result  # Default indentation
    
    # Test with custom indentation
    generator = HCL2Generator(indent_size=4)
    result = generator.generate(HCLFile(blocks=[block]))
    assert "    c = 3" in result
    
    # Test with sorted keys
    generator = HCL2Generator(sort_keys=True)
    result = generator.generate(HCLFile(blocks=[block]))
    lines = result.strip().split("\n")
    assert "  a = 1" in lines[1]
    assert "  b = 2" in lines[2]
    assert "  c = 3" in lines[3] 