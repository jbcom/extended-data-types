"""String formatting transformation operations."""

from __future__ import annotations

import re
import textwrap

from collections.abc import Mapping
from typing import Any, Literal

from extended_data_types.transformations.core import Transform


Alignment = Literal["left", "right", "center"]


def format_template(template: str, values: Mapping[str, Any]) -> str:
    """Format curly-brace templates (legacy behaviour)."""
    try:
        return template.format_map(values)
    except KeyError as exc:
        raise
    except Exception as exc:  # ValueError or formatting errors
        raise ValueError(str(exc)) from exc


def truncate(text: str, length: int, suffix: str = "...") -> str:
    """Truncate text to specified length."""
    if length < 0:
        raise ValueError("Length must be non-negative")
    if len(text) <= length:
        return text
    return text[:length] + suffix


def pad(text: str, length: int, align: Alignment = "center", fill: str = " ") -> str:
    """Pad text to specified length."""
    if length <= len(text):
        return text
    if align not in ("left", "right", "center"):
        raise ValueError("Invalid alignment")
    if not fill:
        fill = " "
    if align == "left":
        return text.ljust(length, fill)
    if align == "right":
        return text.rjust(length, fill)
    # center
    total = length - len(text)
    left = total // 2
    right = total - left
    return f"{fill*left}{text}{fill*right}"


def wrap(
    text: str, width: int = 70, indent: str = "", initial_indent: str | None = None
) -> str:
    """Wrap text to specified width."""
    return textwrap.fill(
        text,
        width=width,
        initial_indent=initial_indent or indent,
        subsequent_indent=indent,
    )


def align(
    text: str, width: int, alignment: Alignment = "left", fill_char: str = " "
) -> str:
    """Align text within specified width."""
    if alignment not in ("left", "right", "center"):
        raise ValueError("Invalid alignment")
    if width <= len(text):
        return text
    if alignment == "left":
        return text.ljust(width, fill_char)
    elif alignment == "right":
        return text.rjust(width, fill_char)
    return text.center(width, fill_char)


def format_align(text: str, width: int, alignment: Alignment = "left", fill: str = " ") -> str:
    """Legacy alias for align."""
    return align(text, width, alignment, fill)


def format_number(text: str, width: int) -> str:
    """Zero-pad any numbers found inside a string."""
    if width < 0:
        raise ValueError("Width must be non-negative")

    def _pad(match: re.Match[str]) -> str:
        return match.group(0).zfill(width)

    return re.sub(r"\d+", _pad, text)


def format_case(text: str, case: str) -> str:
    """Convert text to various casing styles."""
    tokens = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
    parts = [p for p in re.findall(r"[A-Za-z0-9]+", tokens) if p]
    if case == "title":
        return " ".join(p.capitalize() for p in parts)
    if case == "upper":
        return " ".join(parts).upper()
    if case == "lower":
        return " ".join(parts).lower()
    if case == "camel":
        return parts[0].lower() + "".join(p.capitalize() for p in parts[1:]) if parts else ""
    if case == "pascal":
        return "".join(p.capitalize() for p in parts)
    if case == "snake":
        return "_".join(p.lower() for p in parts)
    if case == "kebab":
        return "-".join(p.lower() for p in parts)
    raise ValueError(f"Unsupported case {case}")


def format_slug(text: str) -> str:
    """Legacy helper to slugify text (basic)."""
    return text.lower().replace(" ", "-")


# Register transforms
format_template_transform = Transform(format_template)
truncate_transform = Transform(truncate)
pad_transform = Transform(pad)
wrap_transform = Transform(wrap)
align_transform = Transform(align)
format_slug_transform = Transform(format_slug)
format_align_transform = Transform(format_align)
format_case_transform = Transform(format_case)

# Compatibility aliases
format_truncate = truncate
format_pad = pad
