"""Parser implementation for HCL2 configuration files.

This module provides a complete parser for HCL2 syntax, with specific support for
Terraform configurations. It handles all modern Terraform constructs including
blocks, expressions, functions, and meta-arguments.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Tuple

from .types import (Block, BlockType, Expression, Function, HCLFile,
                    MetaArguments, Reference)


@dataclass
class ParserContext:
    """Context for parsing HCL2 content.
    
    Attributes:
        content: The full HCL2 content being parsed
        lines: Content split into lines
        current_line: Current line number being processed
        current_block: Block currently being parsed
        braces_count: Count of open braces for block tracking
    """
    content: str
    lines: List[str]
    current_line: int = 0
    current_block: Optional[Block] = None
    braces_count: int = 0

class HCL2Parser:
    """Parser for HCL2 configuration files.
    
    This parser handles all HCL2 syntax elements including:
    - Blocks and nested blocks
    - Attributes and expressions
    - String literals (including heredocs)
    - Functions and references
    - Meta-arguments
    - Comments (single and multi-line)
    """
    
    # Regular expressions for parsing
    BLOCK_RE = re.compile(r'^\s*(\w+)\s*"([^"]+)"(?:\s*"([^"]+)")?\s*{')
    ATTRIBUTE_RE = re.compile(r'^\s*(\w+)\s*=\s*(.+)')
    REFERENCE_RE = re.compile(r'(\w+)\.([^.\s]+)(?:\.([^.\s]+))?')
    FUNCTION_RE = re.compile(r'(\w+)\((.*)\)')
    STRING_RE = re.compile(r'"([^"\\]*(?:\\.[^"\\]*)*)"')
    HEREDOC_START_RE = re.compile(r'<<-?(\w+)')
    COMMENT_RE = re.compile(r'^\s*(#|//).*$|/\*.*?\*/', re.DOTALL)
    
    def parse(self, content: str) -> HCLFile:
        """Parse HCL2 content into structured format.
        
        Args:
            content: Raw HCL2 configuration content.

        Returns:
            HCLFile: Parsed configuration with all blocks and attributes.

        Raises:
            ValueError: If the content contains invalid HCL2 syntax.
            
        Example:
            >>> parser = HCL2Parser()
            >>> content = '''
            ... resource "aws_instance" "web" {
            ...   instance_type = "t2.micro"
            ... }
            ... '''
            >>> result = parser.parse(content)
        """
        # Remove comments and normalize whitespace
        cleaned_content = self._clean_content(content)
        
        # Initialize parsing context
        ctx = ParserContext(
            content=cleaned_content,
            lines=[line.strip() for line in cleaned_content.splitlines()],
        )
        
        result = HCLFile()
        
        while ctx.current_line < len(ctx.lines):
            line = ctx.lines[ctx.current_line].strip()
            
            # Skip empty lines
            if not line:
                ctx.current_line += 1
                continue
            
            # Parse block or attribute
            if '{' in line:
                block = self._parse_block(ctx)
                if block:
                    result.blocks.append(block)
            elif '=' in line:
                self._parse_attribute(ctx, result)
            
            ctx.current_line += 1
        
        return result

    def _clean_content(self, content: str) -> str:
        """Clean HCL2 content by removing comments and normalizing whitespace.
        
        Args:
            content: Raw content to clean.

        Returns:
            str: Cleaned content with comments removed.
        """
        # Remove multi-line comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        # Remove single-line comments and normalize whitespace
        lines = []
        for line in content.splitlines():
            # Remove single-line comments
            line = re.sub(r'(#|//).*$', '', line)
            # Normalize whitespace
            line = line.strip()
            if line:
                lines.append(line)
        
        return '\n'.join(lines)

    def _parse_block(self, ctx: ParserContext) -> Optional[Block]:
        """Parse a block definition and its contents.
        
        Args:
            ctx: Current parsing context.

        Returns:
            Block: Parsed block with all its contents, or None if invalid.

        Raises:
            ValueError: If block syntax is invalid.
        """
        line = ctx.lines[ctx.current_line]
        match = self.BLOCK_RE.match(line)
        
        if not match:
            raise ValueError(f"Invalid block syntax at line {ctx.current_line + 1}")
        
        block_type = BlockType.from_str(match.group(1))
        labels = [label for label in match.groups()[1:] if label]
        
        block = Block(
            type=block_type,
            labels=labels
        )
        
        # Track brace count for nested blocks
        ctx.braces_count = 1
        ctx.current_line += 1
        
        # Parse block contents
        while ctx.current_line < len(ctx.lines):
            line = ctx.lines[ctx.current_line].strip()
            
            if '{' in line:
                ctx.braces_count += 1
                nested_block = self._parse_block(ctx)
                if nested_block:
                    block.blocks.append(nested_block)
            elif '}' in line:
                ctx.braces_count -= 1
                if ctx.braces_count == 0:
                    break
            elif '=' in line:
                self._parse_attribute(ctx, block)
            
            ctx.current_line += 1
        
        return block

    def _parse_attribute(self, ctx: ParserContext, target: Union[Block, HCLFile]) -> None:
        """Parse an attribute assignment.
        
        Args:
            ctx: Current parsing context.
            target: Block or file to add the attribute to.

        Raises:
            ValueError: If attribute syntax is invalid.
        """
        line = ctx.lines[ctx.current_line]
        match = self.ATTRIBUTE_RE.match(line)
        
        if not match:
            raise ValueError(f"Invalid attribute syntax at line {ctx.current_line + 1}")
        
        name, value = match.groups()
        parsed_value = self._parse_expression(value.strip())
        
        if isinstance(target, Block):
            if name in {'count', 'for_each', 'depends_on', 'provider', 'lifecycle'}:
                self._set_meta_argument(target, name, parsed_value)
            else:
                target.attributes[name] = parsed_value
        else:
            # Top-level attributes (terraform block)
            target.required_providers[name] = parsed_value

    def _parse_expression(self, expr: str) -> Any:
        """Parse an expression into its Python representation.
        
        Args:
            expr: Expression string to parse.

        Returns:
            Any: Python representation of the expression.

        Raises:
            ValueError: If expression syntax is invalid.
        """
        # Handle string literals
        if expr.startswith('"'):
            match = self.STRING_RE.match(expr)
            if match:
                return match.group(1)
        
        # Handle heredoc
        if expr.startswith('<<'):
            match = self.HEREDOC_START_RE.match(expr)
            if match:
                return self._parse_heredoc(expr)
        
        # Handle lists
        if expr.startswith('['):
            return self._parse_list(expr)
        
        # Handle maps
        if expr.startswith('{'):
            return self._parse_map(expr)
        
        # Handle references
        ref_match = self.REFERENCE_RE.match(expr)
        if ref_match:
            return Reference(*ref_match.groups())
        
        # Handle functions
        func_match = self.FUNCTION_RE.match(expr)
        if func_match:
            name, args = func_match.groups()
            return Function(name, self._parse_function_args(args))
        
        # Handle numbers and booleans
        if expr.isdigit():
            return int(expr)
        if expr.lower() in {'true', 'false'}:
            return expr.lower() == 'true'
        
        return Expression(expr)

    def _parse_heredoc(self, expr: str) -> str:
        """Parse a heredoc string.
        
        Args:
            expr: Heredoc expression to parse.

        Returns:
            str: Parsed heredoc content.
        """
        match = self.HEREDOC_START_RE.match(expr)
        if not match:
            raise ValueError("Invalid heredoc syntax")
        
        delimiter = match.group(1)
        lines = []
        current_line = self.current_line + 1
        
        while current_line < len(self.lines):
            line = self.lines[current_line]
            if line.strip() == delimiter:
                break
            lines.append(line)
            current_line += 1
        
        return '\n'.join(lines)

    def _parse_list(self, expr: str) -> List[Any]:
        """Parse a list expression.
        
        Args:
            expr: List expression to parse.

        Returns:
            List[Any]: Parsed list contents.

        Raises:
            ValueError: If list syntax is invalid.
        """
        if not (expr.startswith('[') and expr.endswith(']')):
            raise ValueError("Invalid list syntax")
        
        content = expr[1:-1].strip()
        if not content:
            return []
        
        items = []
        for item in self._split_args(content):
            items.append(self._parse_expression(item.strip()))
        
        return items

    def _parse_map(self, expr: str) -> Dict[str, Any]:
        """Parse a map expression.
        
        Args:
            expr: Map expression to parse.

        Returns:
            Dict[str, Any]: Parsed map contents.

        Raises:
            ValueError: If map syntax is invalid.
        """
        if not (expr.startswith('{') and expr.endswith('}')):
            raise ValueError("Invalid map syntax")
        
        content = expr[1:-1].strip()
        if not content:
            return {}
        
        result = {}
        pairs = self._split_args(content)
        
        for pair in pairs:
            key, value = pair.split('=', 1)
            result[key.strip()] = self._parse_expression(value.strip())
        
        return result

    def _parse_function_args(self, args_str: str) -> List[Any]:
        """Parse function arguments.
        
        Args:
            args_str: String containing function arguments.

        Returns:
            List[Any]: List of parsed arguments.
        """
        if not args_str.strip():
            return []
        
        return [
            self._parse_expression(arg.strip())
            for arg in self._split_args(args_str)
        ]

    def _split_args(self, args_str: str) -> List[str]:
        """Split arguments while respecting nested structures.
        
        Args:
            args_str: String containing arguments to split.

        Returns:
            List[str]: Split arguments.
        """
        args = []
        current_arg = []
        nesting_level = 0
        in_string = False
        escape_next = False
        
        for char in args_str:
            if escape_next:
                current_arg.append(char)
                escape_next = False
                continue
                
            if char == '\\':
                escape_next = True
                current_arg.append(char)
                continue
                
            if char == '"' and not escape_next:
                in_string = not in_string
                current_arg.append(char)
                continue
                
            if in_string:
                current_arg.append(char)
                continue
                
            if char in '[{(':
                nesting_level += 1
                current_arg.append(char)
            elif char in ']})':
                nesting_level -= 1
                current_arg.append(char)
            elif char == ',' and nesting_level == 0:
                args.append(''.join(current_arg).strip())
                current_arg = []
            else:
                current_arg.append(char)
        
        if current_arg:
            args.append(''.join(current_arg).strip())
        
        return args

    def _set_meta_argument(self, block: Block, name: str, value: Any) -> None:
        """Set a meta-argument on a block.
        
        Args:
            block: Block to set meta-argument on.
            name: Name of meta-argument.
            value: Value to set.
        """
        if name == 'count':
            block.meta_args.count = value
        elif name == 'for_each':
            block.meta_args.for_each = value
        elif name == 'depends_on':
            if isinstance(value, list):
                block.meta_args.depends_on = value
            else:
                block.meta_args.depends_on = [value]
        elif name == 'provider':
            block.meta_args.provider = value
        elif name == 'lifecycle':
            if isinstance(value, dict):
                block.meta_args.lifecycle = value 