"""Tests for HCL2 type definitions."""

from __future__ import annotations

import pytest

from extended_data_types.serialization.languages.hcl2.types import (
    Block,
    BlockType,
    Expression,
    Function,
    HCLFile,
    MetaArguments,
    Reference,
)


def test_block_type():
    """Test BlockType enum functionality."""
    # Test valid block types
    assert BlockType.RESOURCE.value == "resource"
    assert BlockType.DATA.value == "data"
    assert BlockType.MODULE.value == "module"

    # Test from_str conversion
    assert BlockType.from_str("resource") == BlockType.RESOURCE
    assert BlockType.from_str("RESOURCE") == BlockType.RESOURCE

    # Test invalid block type
    with pytest.raises(ValueError):
        BlockType.from_str("invalid_type")


def test_reference():
    """Test Reference functionality."""
    # Test basic reference
    ref = Reference("var", "environment")
    assert str(ref) == "var.environment"

    # Test reference with attribute
    ref = Reference("aws_instance", "web", "id")
    assert str(ref) == "aws_instance.web.id"


def test_function():
    """Test Function functionality."""
    # Test simple function
    func = Function("lower", ["Hello"])
    assert str(func) == "lower(Hello)"

    # Test function with multiple arguments
    func = Function("coalesce", ["var.env", "dev"])
    assert str(func) == "coalesce(var.env, dev)"


def test_expression():
    """Test Expression functionality."""
    # Test simple expression
    expr = Expression("var.environment")
    assert str(expr) == "var.environment"

    # Test expression with references
    expr = Expression("var.environment == 'prod'")
    assert str(expr) == "var.environment == 'prod'"


def test_meta_arguments():
    """Test MetaArguments functionality."""
    meta = MetaArguments(
        count=Expression("2"),
        for_each=Expression("var.environments"),
        depends_on=["aws_vpc.main"],
        provider="aws.west",
        lifecycle={"create_before_destroy": True},
    )

    assert meta.count.raw == "2"
    assert meta.for_each.raw == "var.environments"
    assert meta.depends_on == ["aws_vpc.main"]
    assert meta.provider == "aws.west"
    assert meta.lifecycle == {"create_before_destroy": True}


def test_block():
    """Test Block functionality."""
    # Test basic block
    block = Block(
        type=BlockType.RESOURCE,
        labels=["aws_instance", "web"],
        attributes={"instance_type": "t2.micro"},
    )

    assert block.type == BlockType.RESOURCE
    assert block.labels == ["aws_instance", "web"]
    assert block.attributes["instance_type"] == "t2.micro"

    # Test nested blocks
    nested = Block(
        type=BlockType.PROVIDER, labels=["aws"], attributes={"region": "us-west-2"}
    )
    block.blocks.append(nested)

    assert len(block.blocks) == 1
    assert block.blocks[0].type == BlockType.PROVIDER


def test_hcl_file():
    """Test HCLFile functionality."""
    file = HCLFile(terraform_version=">= 1.0.0", required_providers={"aws": "~> 4.0"})

    block = Block(
        type=BlockType.RESOURCE,
        labels=["aws_instance", "web"],
        attributes={"instance_type": "t2.micro"},
    )
    file.blocks.append(block)

    assert file.terraform_version == ">= 1.0.0"
    assert file.required_providers["aws"] == "~> 4.0"
    assert len(file.blocks) == 1
