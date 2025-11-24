"""HCL2 (HashiCorp Configuration Language) implementation.

This package provides a complete implementation of HCL2 with specific support for
Terraform syntax and semantics, including all modern Terraform features.

Example:
    >>> from extended_data_types.serialization.languages.hcl2 import HCL2
    >>> hcl = HCL2()
    >>> content = '''
    ... resource "aws_instance" "web" {
    ...   instance_type = "t2.micro"
    ...   tags = {
    ...     Name = "web-server"
    ...   }
    ... }
    ... '''
    >>> blocks = hcl.parse(content)
    >>> generated = hcl.generate(blocks)
"""

from .core import HCL2
from .generator import HCL2Generator
from .parser import HCL2Parser
from .serializer import HCL2Serializer
from .types import Block, BlockType, Expression
from extended_data_types.serialization.registry import register_serializer

# Ensure serializer is available in the global registry
register_serializer("hcl2", HCL2Serializer())


__all__ = ["HCL2", "HCL2Parser", "HCL2Generator", "HCL2Serializer", "Block", "BlockType", "Expression"]
