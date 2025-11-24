"""HCL2 type definitions and simple helpers."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, TypeVar, Generic

T = TypeVar('T')


class BlockType(Enum):
    RESOURCE = "resource"
    DATA = "data"
    MODULE = "module"
    OUTPUT = "output"
    PROVIDER = "provider"
    VARIABLE = "variable"
    LOCALS = "locals"
    TERRAFORM = "terraform"

    @classmethod
    def from_str(cls, value: str) -> BlockType:
        for item in cls:
            if item.value == value.casefold():
                return item
        raise ValueError(f"Invalid block type: {value}")


class Expression:
    """Simple wrapper to preserve raw expressions."""

    def __init__(self, raw: str):
        self.raw = raw

    def __str__(self) -> str:
        return self.raw


class Reference:
    """Represents an HCL reference like var.env or aws_instance.web.id."""

    def __init__(self, target: str, name: str, attribute: str | None = None):
        self.target = target
        self.name = name
        self.attribute = attribute

    def __str__(self) -> str:
        parts = [self.target, self.name]
        if self.attribute:
            parts.append(self.attribute)
        return ".".join(parts)


class Function:
    """Represents a function call."""

    def __init__(self, name: str, args: list[Any]):
        self.name = name
        self.args = args

    def __str__(self) -> str:
        def _fmt(arg: Any) -> str:
            if isinstance(arg, str):
                if arg.isidentifier() or "." in arg:
                    return arg
                return f'"{arg}"'
            return str(arg)

        arg_str = ", ".join(_fmt(a) for a in self.args)
        return f"{self.name}({arg_str})"


@dataclass
class MetaArguments:
    """Meta-arguments supported on resource/module blocks."""

    depends_on: list[str] | None = None
    count: Expression | None = None
    for_each: Expression | None = None
    provider: str | None = None
    lifecycle: dict[str, Any] | None = None


@dataclass
class Block(Generic[T]):
    """HCL2 block representation."""

    type: BlockType | str
    labels: list[str] = field(default_factory=list)
    attributes: dict[str, Any] = field(default_factory=dict)
    blocks: list[Block[T]] = field(default_factory=list)
    meta_args: MetaArguments = field(default_factory=MetaArguments)
    data: T | None = None


@dataclass
class HCLFile:
    """Top-level HCL file representation."""

    terraform_version: str | None = None
    required_providers: dict[str, Any] = field(default_factory=dict)
    blocks: list[Block] = field(default_factory=list)

    def __iter__(self) -> Iterator[Block]:
        return iter(self.blocks)


# Convenience aliases for the test suite
ExpressionType = str
CollectionType = str
