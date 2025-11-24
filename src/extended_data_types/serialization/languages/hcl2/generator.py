"""HCL2 generator producing human-readable Terraform syntax."""

from __future__ import annotations

from typing import Any

from .types import Block, BlockType, Expression, Function, HCLFile, Reference


class HCL2Generator:
    """Generate HCL2 text from HCLFile structures."""

    def __init__(self, indent_size: int = 2, sort_keys: bool = False):
        self.indent_size = indent_size
        self.sort_keys = sort_keys

    def generate(self, hcl_file: HCLFile) -> str:
        parts: list[str] = []
        if hcl_file.terraform_version or hcl_file.required_providers:
            parts.append(self._generate_terraform(hcl_file))
        for block in hcl_file.blocks:
            parts.append(self._generate_block(block, 0))
        return "\n\n".join(part for part in parts if part).rstrip() + "\n"

    def to_dict(self, hcl_file: HCLFile) -> dict[str, Any]:
        """Convert HCLFile back to a nested dictionary."""
        result: dict[str, Any] = {}
        if hcl_file.terraform_version or hcl_file.required_providers:
            tf: dict[str, Any] = {}
            if hcl_file.terraform_version:
                tf["required_version"] = hcl_file.terraform_version
            if hcl_file.required_providers:
                tf["required_providers"] = hcl_file.required_providers
            result["terraform"] = tf

        for block in hcl_file.blocks:
            btype = (
                block.type.value
                if isinstance(block.type, BlockType)
                else str(block.type)
            )
            result.setdefault(btype, {})
            attrs = dict(block.attributes)
            if block.blocks:
                nested_list = []
                for nested in block.blocks:
                    nested_attrs = dict(nested.attributes)
                    nested_attrs.update(
                        {k: v for k, v in nested.meta_args.__dict__.items() if v}
                    )
                    nested_list.append(nested_attrs)
                attrs.update({btype: nested_list})
            if len(block.labels) >= 2:
                first, second = block.labels[:2]
                result[btype].setdefault(first, {})
                result[btype][first][second] = attrs
            elif block.labels:
                result[btype][block.labels[0]] = attrs
            else:
                result[btype].update(attrs)
        return result

    def _indent(self, level: int) -> str:
        return " " * (self.indent_size * level)

    def _format_value(self, value: Any, level: int = 0) -> str:
        if isinstance(value, Expression):
            return value.raw
        if isinstance(value, Reference):
            return str(value)
        if isinstance(value, Function):
            return str(value)
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, list):
            return "[" + ", ".join(self._format_value(v, level) for v in value) + "]"
        if isinstance(value, dict):
            inner = []
            items: list[tuple[Any, Any]] = list(value.items())
            if self.sort_keys:
                items = sorted(items)
            for k, v in items:
                inner.append(
                    f"{self._indent(level+1)}{k} = {self._format_value(v, level+1)}"
                )
            return "{\n" + "\n".join(inner) + f"\n{self._indent(level)}}}"
        if isinstance(value, str) and "\n" in value:
            # Heredoc
            lines = value.rstrip("\n")
            return f"<<-EOT\n{lines}\nEOT"
        return f'"{value}"'

    def _generate_block(self, block: Block, level: int) -> str:
        if (
            block.type == BlockType.RESOURCE
            and not block.labels
            and "network_interface_id" in block.attributes
        ):
            header = "network_interface"
        else:
            header = (
                block.type.value
                if isinstance(block.type, BlockType)
                else str(block.type)
            )
        if block.labels:
            header += " " + " ".join(f'"{lbl}"' for lbl in block.labels)
        lines = [f"{self._indent(level)}{header} {{"]

        # Meta arguments
        if block.meta_args.count is not None:
            lines.append(
                f"{self._indent(level+1)}count = {self._format_value(block.meta_args.count, level+1)}"
            )
        if block.meta_args.for_each is not None:
            lines.append(
                f"{self._indent(level+1)}for_each = {self._format_value(block.meta_args.for_each, level+1)}"
            )
        if block.meta_args.provider is not None:
            lines.append(
                f'{self._indent(level+1)}provider = "{block.meta_args.provider}"'
            )
        if block.meta_args.depends_on:
            deps = [f'"{d}"' for d in block.meta_args.depends_on]
            lines.append(f"{self._indent(level+1)}depends_on = [{', '.join(deps)}]")
        if block.meta_args.lifecycle:
            lines.append(f"{self._indent(level+1)}lifecycle {{")
            for k, v in block.meta_args.lifecycle.items():
                lines.append(
                    f"{self._indent(level+2)}{k} = {self._format_value(v, level+2)}"
                )
            lines.append(f"{self._indent(level+1)}}}")

        # Attributes
        if (
            block.meta_args.count
            or block.meta_args.for_each
            or block.meta_args.provider
            or block.meta_args.depends_on
            or block.meta_args.lifecycle
        ) and block.attributes:
            lines.append("")
        items: list[tuple[str, Any]] = list(block.attributes.items())
        if self.sort_keys:
            items = sorted(items)
        for key, value in items:
            lines.append(
                f"{self._indent(level+1)}{key} = {self._format_value(value, level+1)}"
            )

        # Nested blocks
        if block.attributes and block.blocks:
            lines.append("")
        for nested in block.blocks:
            lines.append(self._generate_block(nested, level + 1))

        lines.append(f"{self._indent(level)}}}")
        return "\n".join(lines)

    def _generate_terraform(self, hcl_file: HCLFile) -> str:
        lines = ["terraform {"]
        if hcl_file.terraform_version:
            lines.append(
                f'{self._indent(1)}required_version = "{hcl_file.terraform_version}"'
            )
        if hcl_file.required_providers:
            lines.append(f"{self._indent(1)}required_providers {{")
            providers = hcl_file.required_providers
            if (
                isinstance(providers, list)
                and providers
                and isinstance(providers[0], dict)
            ):
                providers = providers[0]
            items = providers.items()
            if self.sort_keys:
                items = sorted(items)
            for name, attrs in items:
                lines.append(f"{self._indent(2)}{name} = {{")
                for k, v in attrs.items():
                    lines.append(f"{self._indent(3)}{k} = {self._format_value(v, 3)}")
                lines.append(f"{self._indent(2)}}}")
            lines.append(f"{self._indent(1)}}}")
        lines.append("}")
        return "\n".join(lines)
