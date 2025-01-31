"""Tests for HCL2 core interface."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest

from extended_data_types.serialization.languages.hcl2.core import HCL2
from extended_data_types.serialization.languages.hcl2.types import (Block,
                                                                    BlockType,
                                                                    HCLFile)


def test_parse_and_generate(tmp_path: Path):
    """Test parsing and generating HCL2 content."""
    hcl = HCL2()
    
    content = dedent("""\
        resource "aws_instance" "web" {
          instance_type = "t2.micro"
          tags = {
            Name = "web-server"
          }
        }
        """)
    
    # Test parsing
    config = hcl.parse(content)
    assert len(config.blocks) == 1
    assert config.blocks[0].type == BlockType.RESOURCE
    
    # Test generating
    generated = hcl.generate(config)
    assert generated.strip() == content.strip()

def test_file_operations(tmp_path: Path):
    """Test file-based operations."""
    hcl = HCL2()
    
    # Create test file
    test_file = tmp_path / "test.tf"
    test_file.write_text(dedent("""\
        resource "aws_instance" "web" {
          instance_type = "t2.micro"
        }
        """))
    
    # Test parse_file
    config = hcl.parse_file(test_file)
    assert len(config.blocks) == 1
    
    # Test generate_file
    output_file = tmp_path / "output.tf"
    hcl.generate_file(config, output_file)
    assert output_file.exists()
    assert output_file.read_text().strip() == test_file.read_text().strip()

def test_validation():
    """Test HCL2 validation functionality."""
    hcl = HCL2()
    
    # Test valid content
    valid_content = dedent("""\
        resource "aws_instance" "web" {
          instance_type = "t2.micro"
        }
        """)
    assert hcl.validate(valid_content) is True
    
    # Test invalid content
    invalid_content = "resource aws_instance {"  # Missing quotes
    assert hcl.validate(invalid_content) is False
    
    # Test valid HCLFile
    valid_file = HCLFile(blocks=[
        Block(
            type=BlockType.RESOURCE,
            labels=["aws_instance", "web"],
            attributes={"instance_type": "t2.micro"}
        )
    ])
    assert hcl.validate(valid_file) is True

def test_merge_files(tmp_path: Path):
    """Test merging multiple HCL2 files."""
    hcl = HCL2()
    
    # Create test files
    main_tf = tmp_path / "main.tf"
    main_tf.write_text(dedent("""\
        resource "aws_instance" "web" {
          instance_type = "t2.micro"
        }
        """))
    
    variables_tf = tmp_path / "variables.tf"
    variables_tf.write_text(dedent("""\
        variable "environment" {
          type = string
          default = "dev"
        }
        """))
    
    # Test merging
    merged = hcl.merge_files([main_tf, variables_tf])
    assert len(merged.blocks) == 2
    
    # Verify block types
    block_types = {block.type for block in merged.blocks}
    assert BlockType.RESOURCE in block_types
    assert BlockType.VARIABLE in block_types

def test_error_handling():
    """Test error handling in HCL2 interface."""
    hcl = HCL2()
    
    # Test file not found
    with pytest.raises(FileNotFoundError):
        hcl.parse_file("nonexistent.tf")
    
    # Test invalid syntax
    with pytest.raises(ValueError):
        hcl.parse("invalid { syntax")
    
    # Test invalid block type
    with pytest.raises(ValueError):
        hcl.parse('invalid "type" "label" {}') 