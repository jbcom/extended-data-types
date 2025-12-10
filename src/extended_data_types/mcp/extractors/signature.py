"""Type signature extraction utilities for MCP server.

This module provides utilities for extracting and formatting function signatures,
parameter information, and return types from Python callable objects.
"""

from __future__ import annotations

import inspect
import sys

from typing import Any, Callable, Union, get_type_hints

from extended_data_types.mcp.extractors.docstring import DocstringParser
from extended_data_types.mcp.models import ParameterInfo


# Python 3.10+ has get_origin and get_args in typing
if sys.version_info >= (3, 10):
    from typing import get_args, get_origin
else:
    from typing_extensions import get_args, get_origin


def extract_signature(func: Callable[..., Any]) -> str:
    """Extract formatted signature string from a function.

    Args:
        func: The callable to extract signature from.

    Returns:
        Formatted signature string like "func(arg1: str, arg2: int = 5) -> bool".

    Examples:
        >>> def example(name: str, count: int = 1) -> list[str]:
        ...     pass
        >>> extract_signature(example)
        'example(name: str, count: int = 1) -> list[str]'
    """
    try:
        sig = inspect.signature(func)
    except (ValueError, TypeError):
        # Signature not available (e.g., built-in functions)
        return f"{func.__name__}(...)"

    # Get type hints
    try:
        hints = get_type_hints(func)
    except (TypeError, NameError, AttributeError):
        # Type hints not available or invalid
        hints = {}

    # Format parameters
    params = []
    for name, param in sig.parameters.items():
        param_str = _format_parameter(name, param, hints)
        params.append(param_str)

    params_str = ", ".join(params)

    # Format return type
    return_type = hints.get("return", sig.return_annotation)
    if return_type != inspect.Parameter.empty:
        return_str = f" -> {format_type(return_type)}"
    else:
        return_str = ""

    return f"{func.__name__}({params_str}){return_str}"


def extract_parameters(func: Callable[..., Any]) -> list[ParameterInfo]:
    """Extract parameter information from a function.

    Args:
        func: The callable to extract parameters from.

    Returns:
        List of ParameterInfo objects with parameter details.

    Examples:
        >>> def example(name: str, count: int = 1) -> None:
        ...     '''Example function.
        ...
        ...     Args:
        ...         name: The name to use.
        ...         count: How many times.
        ...     '''
        ...     pass
        >>> params = extract_parameters(example)
        >>> params[0].name
        'name'
        >>> params[0].type_hint
        'str'
    """
    try:
        sig = inspect.signature(func)
    except (ValueError, TypeError):
        return []

    # Get type hints
    try:
        hints = get_type_hints(func)
    except (TypeError, NameError, AttributeError):
        hints = {}

    # Parse docstring for parameter descriptions
    parser = DocstringParser()
    try:
        docstring = inspect.getdoc(func) or ""
        parsed = parser.parse(docstring)
        # args is dict[str, tuple[str, str]] where tuple is (type, description)
        param_descriptions = {name: desc for name, (_type, desc) in parsed.args.items()}
    except (AttributeError, ValueError):
        param_descriptions = {}

    # Build parameter info list
    params = []
    for name, param in sig.parameters.items():
        # Get type hint
        if name in hints:
            type_hint = format_type(hints[name])
        elif param.annotation != inspect.Parameter.empty:
            type_hint = format_type(param.annotation)
        else:
            type_hint = "Any"

        # Handle special parameter kinds
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            type_hint = f"*{type_hint}"
        elif param.kind == inspect.Parameter.VAR_KEYWORD:
            type_hint = f"**{type_hint}"

        # Get default value
        default = None
        if param.default != inspect.Parameter.empty:
            default = _safe_repr(param.default)

        # Get description from docstring
        description = param_descriptions.get(name, "No description available")

        params.append(
            ParameterInfo(
                name=name,
                type_hint=type_hint,
                default=default,
                description=description,
            )
        )

    return params


def extract_return_type(func: Callable[..., Any]) -> str:
    """Extract return type annotation as string.

    Args:
        func: The callable to extract return type from.

    Returns:
        Return type as formatted string, or "Any" if not annotated.

    Examples:
        >>> def example() -> list[str]:
        ...     pass
        >>> extract_return_type(example)
        'list[str]'
    """
    try:
        hints = get_type_hints(func)
        if "return" in hints:
            return format_type(hints["return"])
    except (TypeError, NameError, AttributeError):
        # Type hints not available, try signature
        pass

    # Fallback to signature
    try:
        sig = inspect.signature(func)
        if sig.return_annotation != inspect.Parameter.empty:
            return format_type(sig.return_annotation)
    except (ValueError, TypeError):
        pass

    return "Any"


def format_type(type_hint: Any) -> str:
    """Format a type hint as a readable string.

    Handles complex types including Union, Optional, generics, and nested types.

    Args:
        type_hint: The type hint to format.

    Returns:
        Formatted type string.

    Examples:
        >>> from typing import Union, Optional
        >>> format_type(Union[str, int])
        'str | int'
        >>> format_type(Optional[str])
        'str | None'
        >>> format_type(dict[str, list[int]])
        'dict[str, list[int]]'
    """
    # Handle None type
    if type_hint is type(None):
        return "None"

    # Handle Any
    if type_hint is Any:
        return "Any"

    # Get origin and args for generic types
    origin = get_origin(type_hint)
    args = get_args(type_hint)

    # Handle Union types (including Optional)
    if origin is Union:
        # Format as modern union syntax (|)
        arg_strs = [format_type(arg) for arg in args]
        return " | ".join(arg_strs)

    # Handle generic types with arguments
    if origin is not None and args:
        origin_name = _get_type_name(origin)
        args_str = ", ".join(format_type(arg) for arg in args)
        return f"{origin_name}[{args_str}]"

    # Handle simple types
    return _get_type_name(type_hint)


def _format_parameter(
    name: str, param: inspect.Parameter, hints: dict[str, Any]
) -> str:
    """Format a single parameter as string.

    Args:
        name: Parameter name.
        param: Parameter object from signature.
        hints: Type hints dictionary.

    Returns:
        Formatted parameter string.
    """
    # Get type hint
    if name in hints:
        type_str = format_type(hints[name])
    elif param.annotation != inspect.Parameter.empty:
        type_str = format_type(param.annotation)
    else:
        type_str = None

    # Format based on parameter kind
    if param.kind == inspect.Parameter.VAR_POSITIONAL:
        param_str = f"*{name}"
        if type_str:
            param_str += f": {type_str}"
    elif param.kind == inspect.Parameter.VAR_KEYWORD:
        param_str = f"**{name}"
        if type_str:
            param_str += f": {type_str}"
    else:
        param_str = name
        if type_str:
            param_str += f": {type_str}"

        # Add default value
        if param.default != inspect.Parameter.empty:
            default_repr = _safe_repr(param.default)
            param_str += f" = {default_repr}"

    return param_str


def _get_type_name(type_obj: Any) -> str:
    """Get a readable name for a type object.

    Args:
        type_obj: The type object.

    Returns:
        Type name as string.
    """
    # Handle string annotations
    if isinstance(type_obj, str):
        return type_obj

    # Get __name__ attribute if available
    if hasattr(type_obj, "__name__"):
        return type_obj.__name__

    # Get __qualname__ for nested classes
    if hasattr(type_obj, "__qualname__"):
        return type_obj.__qualname__

    # Fallback to repr
    return repr(type_obj)


def _safe_repr(value: Any, max_length: int = 50) -> str:
    """Safely represent a value as string.

    Args:
        value: The value to represent.
        max_length: Maximum length before truncation.

    Returns:
        Safe string representation.
    """
    try:
        result = repr(value)
        if len(result) > max_length:
            result = result[:max_length] + "..."
        return result
    except (TypeError, ValueError, AttributeError):
        return "<repr failed>"
