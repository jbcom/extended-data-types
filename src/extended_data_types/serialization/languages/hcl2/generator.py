"""Generator implementation for HCL2 configuration files.

This module provides a complete generator for HCL2 syntax, with specific support
for Terraform configurations. It handles all modern Terraform constructs and
produces properly formatted output.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from .types import Block, BlockType, Expression, Function, HCLFile, Reference


class HCL2Generator:
    """Generator for HCL2 configuration files.
    
    This generator handles all HCL2 syntax elements including:
    - Blocks and nested blocks
    - Attributes and expressions
    - String literals (including heredocs)
    - Functions and references
    - Meta-arguments
    
    Attributes:
        indent_size: Number of spaces for each indentation level
        sort_keys: Whether to sort keys in maps and blocks
    """
    
    def __init__(self, indent_size: int = 2, sort_keys: bool = False):
        """Initialize the generator.
        
        Args:
            indent_size: Number of spaces to use for each indentation level
            sort_keys: Whether to sort keys alphabetically in output
        """
        self.indent_size = indent_size
        self.sort_keys = sort_keys
    
    def generate(self, hcl_file: HCLFile) -> str:
        """Generate HCL2 content from a file representation.
        
        Args:
            hcl_file: HCLFile object containing the configuration

        Returns:
            str: Generated HCL2 content

        Example:
            >>> generator = HCL2Generator()
            >>> hcl_file = HCLFile(blocks=[...])
            >>> content = generator.generate(hcl_file)
        """
        parts = []
        
        # Generate terraform block if version or providers specified
        if hcl_file.terraform_version or hcl_file.required_providers:
            parts.append(self._generate_terraform_block(
                hcl_file.terraform_version,
                hcl_file.required_providers
            ))
        
        # Generate all blocks
        blocks = sorted(hcl_file.blocks, key=lambda b: str(b)) if self.sort_keys else hcl_file.blocks
        for block in blocks:
            parts.append(self._generate_block(block))
        
        return "\n\n".join(part for part in parts if part) + "\n"
    
    def _generate_terraform_block(
        self, 
        version: Optional[str], 
        providers: Dict[str, str]
    ) -> str:
        """Generate the terraform configuration block.
        
        Args:
            version: Optional terraform version constraint
            providers: Dictionary of provider requirements

        Returns:
            str: Generated terraform block
        """
        parts = []
        parts.append("terraform {")
        
        if version:
            parts.append(f'{self._indent(1)}required_version = "{version}"')
        
        if providers:
            parts.append(f"{self._indent(1)}required_providers {self._generate_map(providers, 2)}")
        
        parts.append("}")
        return "\n".join(parts)
    
    def _generate_block(self, block: Block, level: int = 0) -> str:
        """Generate HCL2 for a single block.
        
        Args:
            block: Block to generate
            level: Current indentation level

        Returns:
            str: Generated block content
        """
        parts = []
        
        # Block header
        header = block.type.value
        if block.labels:
            header += " " + " ".join(f'"{label}"' for label in block.labels)
        parts.append(f"{self._indent(level)}{header} {{")
        
        # Meta arguments first
        if block.meta_args.count is not None:
            parts.append(f'{self._indent(level + 1)}count = {self._generate_expression(block.meta_args.count)}')
        
        if block.meta_args.for_each is not None:
            parts.append(f'{self._indent(level + 1)}for_each = {self._generate_expression(block.meta_args.for_each)}')
        
        if block.meta_args.provider:
            parts.append(f'{self._indent(level + 1)}provider = "{block.meta_args.provider}"')
        
        if block.meta_args.depends_on:
            deps = [f'"{dep}"' for dep in block.meta_args.depends_on]
            parts.append(f'{self._indent(level + 1)}depends_on = [{", ".join(deps)}]')
        
        if block.meta_args.lifecycle:
            parts.append(self._generate_lifecycle_block(block.meta_args.lifecycle, level + 1))
        
        # Regular attributes
        attributes = sorted(block.attributes.items()) if self.sort_keys else block.attributes.items()
        for key, value in attributes:
            parts.append(f"{self._indent(level + 1)}{key} = {self._generate_expression(value)}")
        
        # Nested blocks
        blocks = sorted(block.blocks, key=lambda b: str(b)) if self.sort_keys else block.blocks
        for nested_block in blocks:
            parts.append(self._generate_block(nested_block, level + 1))
        
        parts.append(f"{self._indent(level)}}}")
        return "\n".join(parts)
    
    def _generate_expression(self, value: Any) -> str:
        """Generate HCL2 expression from a value.
        
        Args:
            value: Value to generate expression for

        Returns:
            str: Generated expression
        """
        if isinstance(value, (Expression, Reference, Function)):
            return str(value)
        
        if isinstance(value, bool):
            return str(value).lower()
        
        if isinstance(value, (int, float)):
            return str(value)
        
        if isinstance(value, str):
            if '\n' in value:
                return self._generate_heredoc(value)
            return f'"{self._escape_string(value)}"'
        
        if isinstance(value, list):
            return self._generate_list(value)
        
        if isinstance(value, dict):
            return self._generate_map(value)
        
        if value is None:
            return "null"
        
        return str(value)
    
    def _generate_heredoc(self, value: str) -> str:
        """Generate a heredoc string.
        
        Args:
            value: Multi-line string value

        Returns:
            str: Generated heredoc
        """
        return f"<<-EOT\n{value}\nEOT"
    
    def _generate_list(self, items: List[Any]) -> str:
        """Generate a list expression.
        
        Args:
            items: List of items to generate

        Returns:
            str: Generated list expression
        """
        if not items:
            return "[]"
        
        parts = [self._generate_expression(item) for item in items]
        if len(", ".join(parts)) > 60:  # Line length threshold
            return "[\n" + ",\n".join(self._indent(1) + part for part in parts) + "\n]"
        return f"[{', '.join(parts)}]"
    
    def _generate_map(self, map_data: Dict[str, Any], indent_level: int = 1) -> str:
        """Generate a map expression.
        
        Args:
            map_data: Dictionary to generate
            indent_level: Current indentation level

        Returns:
            str: Generated map expression
        """
        if not map_data:
            return "{}"
        
        parts = []
        items = sorted(map_data.items()) if self.sort_keys else map_data.items()
        
        parts.append("{")
        for key, value in items:
            parts.append(f"{self._indent(indent_level)}{key} = {self._generate_expression(value)}")
        parts.append(self._indent(indent_level - 1) + "}")
        
        return "\n".join(parts)
    
    def _generate_lifecycle_block(self, lifecycle: Dict[str, Any], level: int) -> str:
        """Generate a lifecycle block.
        
        Args:
            lifecycle: Lifecycle configuration
            level: Current indentation level

        Returns:
            str: Generated lifecycle block
        """
        parts = [f"{self._indent(level)}lifecycle {{"]
        
        for key, value in sorted(lifecycle.items()) if self.sort_keys else lifecycle.items():
            parts.append(f"{self._indent(level + 1)}{key} = {self._generate_expression(value)}")
        
        parts.append(f"{self._indent(level)}}}")
        return "\n".join(parts)
    
    def _escape_string(self, s: str) -> str:
        """Escape special characters in a string.
        
        Args:
            s: String to escape

        Returns:
            str: Escaped string
        """
        return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
    
    def _indent(self, level: int) -> str:
        """Generate indentation string.
        
        Args:
            level: Indentation level

        Returns:
            str: Spaces for indentation
        """
        return " " * (level * self.indent_size) 