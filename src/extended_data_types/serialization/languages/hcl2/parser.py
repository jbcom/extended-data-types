"""Lightweight HCL2 parser built on top of python-hcl2."""

from __future__ import annotations

import hcl2

from .types import Block, BlockType, Expression, HCLFile, MetaArguments


class HCL2Parser:
    """Parse HCL2 strings into simple dataclass structures."""

    def parse(self, content: str) -> HCLFile:
        try:
            parsed = hcl2.loads(content)
        except Exception as exc:
            raise ValueError(f"Invalid HCL2 syntax: {exc}") from exc

        file = HCLFile()

        if "terraform" in parsed:
            tf_raw = parsed.get("terraform") or {}
            tf = tf_raw[0] if isinstance(tf_raw, list) and tf_raw else tf_raw
            file.terraform_version = tf.get("required_version")
            providers = tf.get("required_providers", {})
            if isinstance(providers, list) and providers and isinstance(providers[0], dict):
                providers = providers[0]
            file.required_providers = providers

        for block_type, raw in parsed.items():
            if block_type == "terraform":
                continue
            if block_type not in [
                "resource",
                "module",
                "variable",
                "output",
                "provider",
                "data",
                "locals",
            ]:
                raise ValueError(f"Unsupported block type: {block_type}")
            self._populate_blocks(file, block_type, raw)

        return file

    def _populate_blocks(self, file: HCLFile, block_type: str, raw: object) -> None:
        if block_type == "locals":
            items = raw if isinstance(raw, list) else [raw]
            for item in items:
                if isinstance(item, dict):
                    block = Block(
                        type=BlockType.LOCALS,
                        labels=[],
                        attributes=self._convert_value(item),
                    )
                    file.blocks.append(block)
            return

        items = raw if isinstance(raw, list) else [raw]
        for item in items:
            if not isinstance(item, dict):
                continue
            for first_label, body in item.items():
                if not isinstance(body, dict):
                    continue
                # Two-level blocks
                if any(isinstance(v, dict) for v in body.values()):
                    for second_label, attrs in body.items():
                        block = self._build_block(block_type, [first_label, second_label], attrs)
                        file.blocks.append(block)
                else:
                    block = self._build_block(block_type, [first_label], body)
                    file.blocks.append(block)

    def _build_block(self, block_type: str, labels: list[str], attrs: dict) -> Block:
        try:
            block_type_enum: BlockType | str = BlockType.from_str(block_type)
        except ValueError:
            block_type_enum = block_type

        attributes = {}
        nested_blocks: list[Block] = []
        meta = MetaArguments()

        if isinstance(attrs, dict):
            for key, value in attrs.items():
                if key == "count":
                    meta.count = self._to_expression(value)
                    continue
                if key == "for_each":
                    meta.for_each = self._to_expression(value)
                    continue
                if key == "provider":
                    prov = value if isinstance(value, str) else str(value)
                    if isinstance(prov, str) and prov.startswith("${") and prov.endswith("}"):
                        prov = prov[2:-1]
                    meta.provider = prov
                    continue
                if key == "depends_on":
                    if isinstance(value, list):
                        cleaned = []
                        for item in value:
                            if isinstance(item, str) and item.startswith("${") and item.endswith("}"):
                                cleaned.append(item[2:-1])
                            else:
                                cleaned.append(item)
                        meta.depends_on = cleaned
                    else:
                        meta.depends_on = value
                    continue
                if key == "lifecycle":
                    if isinstance(value, list) and value and isinstance(value[0], dict):
                        value = value[0]
                    meta.lifecycle = value
                    continue

                if isinstance(value, list) and value and all(isinstance(v, dict) for v in value):
                    for entry in value:
                        nested_blocks.append(self._build_block(key, [], entry))
                    continue

                attributes[key] = self._convert_value(value)

        block = Block(
            type=block_type_enum,
            labels=labels,
            attributes=attributes,
            blocks=nested_blocks,
            meta_args=meta,
        )
        return block

    def _convert_value(self, value: Any) -> Any:
        """Convert parsed values into Expressions/References when appropriate."""
        if isinstance(value, str):
            if value.startswith("${") and value.endswith("}"):
                return Expression(value[2:-1])
            if "?" in value or "(" in value or ")" in value:
                return Expression(value)
            return value
        if isinstance(value, list):
            return [self._convert_value(v) for v in value]
        if isinstance(value, dict):
            return {k: self._convert_value(v) for k, v in value.items()}
        return value

    def _to_expression(self, value: Any) -> Expression:
        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            return Expression(value[2:-1])
        return Expression(str(value))
