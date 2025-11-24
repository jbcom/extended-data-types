"""Core HCL2 interface implementation.

This module provides the main interface for working with HCL2 configurations,
combining the parser and generator functionality into a cohesive API.
"""

from __future__ import annotations

from pathlib import Path

from .generator import HCL2Generator
from .parser import HCL2Parser
from .types import Block, BlockType, HCLFile, MetaArguments


class HCL2:
    """Main interface for HCL2 operations.

    This class provides a high-level interface for working with HCL2 configurations,
    including parsing, generating, and manipulating Terraform configurations.

    Attributes:
        parser: HCL2Parser instance for parsing configurations
        generator: HCL2Generator instance for generating HCL2 content

    Example:
        >>> hcl = HCL2()
        >>> with open('main.tf', 'r') as f:
        ...     config = hcl.parse(f.read())
        >>> config.blocks.append(new_resource_block)
        >>> with open('output.tf', 'w') as f:
        ...     f.write(hcl.generate(config))
    """

    def __init__(self, indent_size: int = 2, sort_keys: bool = False):
        """Initialize the HCL2 interface.

        Args:
            indent_size: Number of spaces for indentation in generated output
            sort_keys: Whether to sort keys alphabetically in output
        """
        self.parser = HCL2Parser()
        self.generator = HCL2Generator(indent_size=indent_size, sort_keys=sort_keys)

    def parse(self, content: str | Path) -> HCLFile:
        """Parse HCL2 content into a structured format.

        Args:
            content: HCL2 content as string or Path to file

        Returns:
            HCLFile: Parsed configuration

        Raises:
            ValueError: If content contains invalid HCL2 syntax
            FileNotFoundError: If provided Path doesn't exist

        Example:
            >>> hcl = HCL2()
            >>> config = hcl.parse('''
            ...     resource "aws_instance" "web" {
            ...         instance_type = "t2.micro"
            ...     }
            ... ''')
        """
        if isinstance(content, Path):
            if not content.exists():
                raise FileNotFoundError(f"File not found: {content}")
            content = content.read_text()

        return self.parser.parse(content)

    def generate(self, hcl_file: HCLFile) -> str:
        """Generate HCL2 content from a file representation.

        Args:
            hcl_file: HCLFile object containing the configuration

        Returns:
            str: Generated HCL2 content

        Example:
            >>> hcl = HCL2()
            >>> config = HCLFile(blocks=[...])
            >>> content = hcl.generate(config)
        """
        return self.generator.generate(hcl_file)

    # Convenience helpers for the serializer wrapper
    def serializer_to_file(self, data: dict) -> HCLFile:
        file = HCLFile()
        if "terraform" in data:
            tf = data["terraform"]
            file.terraform_version = tf.get("required_version")
            file.required_providers = tf.get("required_providers", {})
        for block_type, block_data in data.items():
            if block_type == "terraform":
                continue
            try:
                bt: BlockType | str = BlockType.from_str(block_type)
            except ValueError:
                bt = block_type
            if isinstance(block_data, dict):
                for first, maybe_second in block_data.items():
                    if isinstance(maybe_second, dict):
                        for second, attrs in maybe_second.items():
                            block = Block(type=bt, labels=[first, second], attributes=attrs, meta_args=MetaArguments())
                            file.blocks.append(block)
                    else:
                        block = Block(type=bt, labels=[first], attributes={"value": maybe_second}, meta_args=MetaArguments())
                        file.blocks.append(block)
        return file

    def file_to_serializer(self, hcl_file: HCLFile) -> dict:
        return self.generator.to_dict(hcl_file)

    def parse_file(self, path: str | Path) -> HCLFile:
        """Parse HCL2 content from a file.

        Args:
            path: Path to the HCL2 file

        Returns:
            HCLFile: Parsed configuration

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file contains invalid HCL2 syntax

        Example:
            >>> hcl = HCL2()
            >>> config = hcl.parse_file('main.tf')
        """
        path = Path(path)
        return self.parse(path)

    def generate_file(self, hcl_file: HCLFile, path: str | Path) -> None:
        """Generate HCL2 content and write to file.

        Args:
            hcl_file: HCLFile object containing the configuration
            path: Path where to write the generated content

        Raises:
            OSError: If unable to write to the specified path

        Example:
            >>> hcl = HCL2()
            >>> config = HCLFile(blocks=[...])
            >>> hcl.generate_file(config, 'output.tf')
        """
        path = Path(path)
        content = self.generate(hcl_file)
        path.write_text(content)

    def validate(self, content: str | Path | HCLFile) -> bool:
        """Validate HCL2 content.

        Args:
            content: Content to validate (string, Path, or HCLFile)

        Returns:
            bool: True if content is valid HCL2, False otherwise

        Example:
            >>> hcl = HCL2()
            >>> is_valid = hcl.validate('''
            ...     resource "aws_instance" "web" {
            ...         instance_type = "t2.micro"
            ...     }
            ... ''')
        """
        try:
            if isinstance(content, HCLFile):
                self.generate(content)
            else:
                self.parse(content)
            return True
        except (ValueError, FileNotFoundError):
            return False

    def merge_files(self, files: list[str | Path]) -> HCLFile:
        """Merge multiple HCL2 files into a single configuration.

        Args:
            files: List of file paths to merge

        Returns:
            HCLFile: Combined configuration

        Raises:
            FileNotFoundError: If any file doesn't exist
            ValueError: If any file contains invalid HCL2 syntax

        Example:
            >>> hcl = HCL2()
            >>> config = hcl.merge_files(['main.tf', 'variables.tf'])
        """
        result = HCLFile()

        for file_path in files:
            config = self.parse_file(file_path)
            result.blocks.extend(config.blocks)

            # Merge terraform configuration if present
            if config.terraform_version:
                result.terraform_version = config.terraform_version
            if config.required_providers:
                result.required_providers.update(config.required_providers)

        return result
