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

from extended_data_types.serialization.registry import register_serializer

from .core import HCL2
from .generator import HCL2Generator
from .parser import HCL2Parser
from .serializer import HCL2Serializer
from .types import Block, BlockType, Expression


# Ensure serializer is available in the global registry
register_serializer("hcl2", HCL2Serializer())


__all__ = [
    "HCL2",
    "Block",
    "BlockType",
    "Expression",
    "HCL2Generator",
    "HCL2Parser",
    "HCL2Serializer",
]
