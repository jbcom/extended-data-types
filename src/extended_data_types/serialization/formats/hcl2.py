"""HCL2 (HashiCorp Configuration Language) serialization support."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

# Use public API
try:
    from hcl2.api import loads  # type: ignore[import]
except ImportError:
    try:
        import hcl2
        loads = hcl2.loads  # type: ignore[attr-defined]
    except (ImportError, AttributeError):
        def loads(s: str) -> dict[str, Any]:  # type: ignore[misc]
            """Fallback."""
            raise ImportError("python-hcl2 not installed")


class Hcl2Serializer:
    """Lightweight HCL2 serializer implementation for common Terraform shapes."""

    def __init__(self, indent_size: int = 2, sort_keys: bool = False) -> None:
        self.indent_size = indent_size
        self.sort_keys = sort_keys

    def encode(self, obj: Any, **kwargs: Any) -> str:
        if not isinstance(obj, dict):
            raise TypeError("HCL2 serializer expects dictionary input")
        indent_size = kwargs.get("indent_size", self.indent_size)
        sort_keys = kwargs.get("sort_keys", self.sort_keys)

        def _indent_first(text: str, level: int = 1) -> str:
            prefix = " " * (indent_size * level)
            lines = text.split("\n")
            if not lines:
                return prefix
            lines[0] = prefix + lines[0]
            return "\n".join(lines)

        def _format_value(val: Any, level: int = 1) -> str:
            if isinstance(val, bool):
                return "true" if val else "false"
            if isinstance(val, (int, float)):
                return str(val)
            if isinstance(val, str):
                return f'"{val}"'
            if isinstance(val, dict):
                inner_lines = [
                    (" " * (indent_size * level))
                    + f"{k} = {_format_value(v, level + 1)}"
                    for k, v in _iter_items(val, sort_keys)
                ]
                closing = " " * (indent_size * (level - 1))
                return "{\n" + "\n".join(inner_lines) + "\n" + closing + "}"
            if isinstance(val, Iterable):
                return "[{}]".format(", ".join(_format_value(v, level) for v in val))
            return f'"{val}"'

        def _iter_items(d: dict[str, Any], sort: bool) -> Iterable[tuple[str, Any]]:
            items = d.items()
            return sorted(items) if sort else items

        lines: list[str] = []
        for block_type, block_body in _iter_items(obj, sort_keys):
            if block_type in {"resource", "module", "provider", "data"}:
                if not isinstance(block_body, dict):
                    raise TypeError("Block body must be dict")
                for block_name, block_items in _iter_items(block_body, sort_keys):
                    if not isinstance(block_items, dict):
                        raise TypeError("Block items must be dict")
                    for label, attrs in _iter_items(block_items, sort_keys):
                        lines.append(f'{block_type} "{block_name}" "{label}" ' + "{")
                        for k, v in _iter_items(attrs, sort_keys):
                            val_str = _format_value(v, 2)
                            lines.append(_indent_first(f"{k} = {val_str}", 1))
                        lines.append("}")
            elif block_type in {"variable", "output"}:
                if not isinstance(block_body, dict):
                    raise TypeError("Block body must be dict")
                for name, attrs in _iter_items(block_body, sort_keys):
                    lines.append(f'{block_type} "{name}" ' + "{")
                    if isinstance(attrs, dict):
                        for k, v in _iter_items(attrs, sort_keys):
                            val_str = _format_value(v, 2)
                            lines.append(_indent_first(f"{k} = {val_str}", 1))
                    lines.append("}")
            elif block_type in {"locals", "terraform"}:
                lines.append(f"{block_type} " + "{")
                if isinstance(block_body, dict):
                    for k, v in _iter_items(block_body, sort_keys):
                        val_str = _format_value(v, 2)
                        lines.append(_indent_first(f"{k} = {val_str}", 1))
                lines.append("}")
            # Fallback as attribute map
            elif isinstance(block_body, dict):
                lines.append(f"{block_type} = {_format_value(block_body,1)}")
            else:
                lines.append(f"{block_type} = {_format_value(block_body,1)}")

        return "\n".join(lines) + ("\n" if lines else "")

    def decode(self, s: str, **kwargs: Any) -> Any:
        try:
            parsed = hcl2.loads(s, **kwargs)
        except Exception as e:  # pragma: no cover
            raise ValueError(f"Invalid HCL2: {e}") from e

        # hcl2 returns list-of-dicts for repeated blocks; normalize to nested dicts
        def _normalize(obj: Any) -> Any:
            if isinstance(obj, list):
                result: dict[str, Any] = {}
                for entry in obj:
                    if isinstance(entry, dict):
                        for k, v in entry.items():
                            if isinstance(v, dict):
                                # Might have label: value pair
                                result.setdefault(k, {}).update(_normalize(v))
                            else:
                                result[k] = _normalize(v)
                    else:
                        # list of scalars
                        return obj
                return result or obj
            if isinstance(obj, dict):
                return {k: _normalize(v) for k, v in obj.items()}
            return obj

        normalized: dict[str, Any] = {}
        for key, value in parsed.items():
            normalized[key] = _normalize(value)
        return normalized

    # Backwards compatibility for registry expectations
    dumps = encode
    loads = decode
