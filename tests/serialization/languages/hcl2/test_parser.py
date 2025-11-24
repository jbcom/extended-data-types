"""Tests for HCL2 parser functionality."""

from __future__ import annotations

from textwrap import dedent

import pytest

from extended_data_types.serialization.languages.hcl2.parser import HCL2Parser
from extended_data_types.serialization.languages.hcl2.types import BlockType, Expression


def test_parse_basic_block():
    """Test parsing of basic block structure."""
    parser = HCL2Parser()
    content = dedent(
        """
        resource "aws_instance" "web" {
          instance_type = "t2.micro"
          tags = {
            Name = "web-server"
          }
        }
    """
    )

    result = parser.parse(content)
    assert len(result.blocks) == 1

    block = result.blocks[0]
    assert block.type == BlockType.RESOURCE
    assert block.labels == ["aws_instance", "web"]
    assert block.attributes["instance_type"] == "t2.micro"
    assert block.attributes["tags"] == {"Name": "web-server"}


def test_parse_nested_blocks():
    """Test parsing of nested block structures."""
    parser = HCL2Parser()
    content = dedent(
        """
        resource "aws_instance" "web" {
          instance_type = "t2.micro"

          network_interface {
            network_interface_id = aws_network_interface.web.id
            device_index = 0
          }
        }
    """
    )

    result = parser.parse(content)
    block = result.blocks[0]
    assert len(block.blocks) == 1

    nested = block.blocks[0]
    assert nested.attributes["device_index"] == 0


def test_parse_meta_arguments():
    """Test parsing of meta-arguments."""
    parser = HCL2Parser()
    content = dedent(
        """
        resource "aws_instance" "web" {
          count = 2
          for_each = var.environments
          provider = aws.west
          depends_on = [aws_vpc.main]

          lifecycle {
            create_before_destroy = true
            prevent_destroy = false
          }

          instance_type = "t2.micro"
        }
    """
    )

    result = parser.parse(content)
    block = result.blocks[0]

    assert block.meta_args.count.raw == "2"
    assert block.meta_args.for_each.raw == "var.environments"
    assert block.meta_args.provider == "aws.west"
    assert block.meta_args.depends_on == ["aws_vpc.main"]
    assert block.meta_args.lifecycle == {
        "create_before_destroy": True,
        "prevent_destroy": False,
    }


def test_parse_expressions():
    """Test parsing of various expression types."""
    parser = HCL2Parser()
    content = dedent(
        """
        locals {
          instance_type = var.environment == "prod" ? "t2.large" : "t2.micro"
          tags = {
            Name = "web-${var.environment}"
            Environment = upper(var.environment)
          }
          ports = [80, 443, var.extra_port]
        }
    """
    )

    result = parser.parse(content)
    block = result.blocks[0]

    assert isinstance(block.attributes["instance_type"], Expression)
    assert isinstance(block.attributes["tags"], dict)
    assert isinstance(block.attributes["ports"], list)


def test_parse_heredoc():
    """Test parsing of heredoc strings."""
    parser = HCL2Parser()
    content = dedent(
        """
        resource "aws_iam_policy" "example" {
          policy = <<-EOT
            {
              "Version": "2012-10-17",
              "Statement": [
                {
                  "Effect": "Allow",
                  "Action": "*",
                  "Resource": "*"
                }
              ]
            }
          EOT
        }
    """
    )

    result = parser.parse(content)
    block = result.blocks[0]
    assert "policy" in block.attributes
    assert '"Version": "2012-10-17"' in block.attributes["policy"]


def test_parse_comments():
    """Test parsing with comments."""
    parser = HCL2Parser()
    content = dedent(
        """
        # Single line comment
        resource "aws_instance" "web" {
          /* Multi-line
             comment */
          instance_type = "t2.micro"  // Inline comment
        }
    """
    )

    result = parser.parse(content)
    assert len(result.blocks) == 1
    assert result.blocks[0].attributes["instance_type"] == "t2.micro"


def test_parse_terraform_block():
    """Test parsing of terraform configuration block."""
    parser = HCL2Parser()
    content = dedent(
        """
        terraform {
          required_version = ">= 1.0.0"

          required_providers {
            aws = {
              source = "hashicorp/aws"
              version = "~> 4.0"
            }
          }
        }
    """
    )

    result = parser.parse(content)
    assert result.terraform_version == ">= 1.0.0"
    assert "aws" in result.required_providers


def test_parse_invalid_syntax():
    """Test parsing of invalid HCL2 syntax."""
    parser = HCL2Parser()

    with pytest.raises(ValueError):
        parser.parse("resource aws_instance {")  # Missing quotes

    with pytest.raises(ValueError):
        parser.parse('resource "aws_instance" "web" {')  # Unclosed block
