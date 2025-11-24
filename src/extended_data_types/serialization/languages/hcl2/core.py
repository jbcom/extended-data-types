"""Core HCL2 interface implementation.

This module provides the main interface for working with HCL2 configurations,
combining the parser and generator functionality into a cohesive API.
"""

from __future__ import annotations

from pathlib import Path

try:
    from .generator import HCL2Generator  # type: ignore[attr-defined]
    from .parser import HCL2Parser  # type: ignore[attr-defined]
    from .types import Block, BlockType, HCLFile, MetaArguments  # type: ignore[attr-defined]
except ImportError:
    HCL2Generator = object  # type: ignore
    HCL2Parser = object  # type: ignore
    Block = object  # type: ignore
    BlockType = object  # type: ignore
    HCLFile = object  # type: ignore
    MetaArguments = object  # type: ignore


class HCL2:  # type: ignore
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

    def __init__(self, indent_size: int = 2, sort_keys: bool = False):  # type: ignore
        """Initialize the HCL2 interface.

        Args:
            indent_size: Number of spaces for indentation in generated output
            sort_keys: Whether to sort keys alphabetically in output
        """
        self.parser = HCL2Parser()  # type: ignore
        self.generator = HCL2Generator(indent_size=indent_size, sort_keys=sort_keys)  # type: ignore

    def parse(self, content: str | Path) -> Any:  # type: ignore
        """Parse HCL2 content into a structured format."""
        if isinstance(content, Path):
            if not content.exists():
                raise FileNotFoundError(f"File not found: {content}")
            content = content.read_text()

        return self.parser.parse(content)  # type: ignore

    def generate(self, hcl_file: Any) -> str:  # type: ignore
        """Generate HCL2 content from a file representation."""
        return self.generator.generate(hcl_file)  # type: ignore

    def serializer_to_file(self, data: dict) -> Any:  # type: ignore
        file = HCLFile()  # type: ignore
        if "terraform" in data:
            tf = data["terraform"]
            file.terraform_version = tf.get("required_version")  # type: ignore
            file.required_providers = tf.get("required_providers", {})  # type: ignore
        for block_type, block_data in data.items():
            if block_type == "terraform":
                continue
            try:
                bt = BlockType.from_str(block_type)  # type: ignore
            except ValueError:
                bt = block_type
            if isinstance(block_data, dict):
                for first, maybe_second in block_data.items():
                    if isinstance(maybe_second, dict):
                        for second, attrs in maybe_second.items():
                            block = Block(  # type: ignore
                                type=bt,
                                labels=[first, second],
                                attributes=attrs,
                                meta_args=MetaArguments(),  # type: ignore
                            )
                            file.blocks.append(block)  # type: ignore
                    else:
                        block = Block(  # type: ignore
                            type=bt,
                            labels=[first],
                            attributes={"value": maybe_second},
                            meta_args=MetaArguments(),  # type: ignore
                        )
                        file.blocks.append(block)  # type: ignore
        return file

    def file_to_serializer(self, hcl_file: Any) -> dict:  # type: ignore
        return self.generator.to_dict(hcl_file)  # type: ignore

    def parse_file(self, path: str | Path) -> Any:  # type: ignore
        """Parse HCL2 content from a file."""
        path = Path(path)
        return self.parse(path)

    def generate_file(self, hcl_file: Any, path: str | Path) -> None:  # type: ignore
        """Generate HCL2 content and write to file."""
        path = Path(path)
        content = self.generate(hcl_file)
        path.write_text(content)

    def validate(self, content: str | Path | Any) -> bool:  # type: ignore
        """Validate HCL2 content."""
        try:
            if isinstance(content, HCLFile):  # type: ignore
                self.generate(content)
            else:
                self.parse(content)
            return True
        except (ValueError, FileNotFoundError):
            return False

    def merge_files(self, files: list[str | Path]) -> Any:  # type: ignore
        """Merge multiple HCL2 files into a single configuration."""
        result = HCLFile()  # type: ignore

        for file_path in files:
            config = self.parse_file(file_path)
            result.blocks.extend(config.blocks)  # type: ignore

            # Merge terraform configuration if present
            if config.terraform_version:  # type: ignore
                result.terraform_version = config.terraform_version  # type: ignore
            if config.required_providers:  # type: ignore
                result.required_providers.update(config.required_providers)  # type: ignore

        return result
