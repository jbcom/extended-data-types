"""This module provides utilities for inspecting the call stack and methods of classes.

It includes functions to get the caller's name, filter methods, and retrieve available
methods and their docstrings for a class.
"""

from __future__ import annotations

import sys

from inspect import getmembers, ismethod
from typing import Any


def get_caller() -> str:
    """Gets the name of the caller function.

    Returns:
        str: The name of the caller function.
    """
    return sys._getframe(2).f_code.co_name  # noqa: SLF001


def get_unique_signature(obj: Any, delim: str = "/") -> str:
    """Generate a unique signature for an object based on its class and module.

    Args:
        obj (Any): The object to generate a signature for.
        delim (str): The delimiter to use between the module and class names. Defaults to "/".

    Returns:
        str: A unique signature string for the object.
    """
    return str(obj.__class__.__module__) + delim + str(obj.__class__.__name__)


def filter_methods(methods: list[str]) -> list[str]:
    """Filters out private methods from a list of method names.

    Args:
        methods (list[str]): The list of method names to filter.

    Returns:
        list[str]: The filtered list of method names.
    """
    return [method for method in methods if not method.startswith("_")]


def get_available_methods(cls: type[Any]) -> dict[str, str | None]:
    """Gets available methods and their docstrings for a class.

    An "available method" is a public method that:
    - Does not contain '__' in its name.
    - Belongs to the same module as the class.
    - Does not have 'NOPARSE' in its docstring.

    Args:
        cls (type[Any]): The class to inspect.

    Returns:
        dict[str, str | None]: A dictionary of method names and their docstrings.
    """
    module_name = cls.__class__.__module__
    methods = getmembers(cls, ismethod)

    return {
        method_name: method_signature.__doc__
        for method_name, method_signature in methods
        if "__" not in method_name
        and method_signature.__self__.__class__.__module__ == module_name
        and "NOPARSE" not in (method_signature.__doc__ or "")
    }


def current_python_version_is_at_least(minor: int, major: int = 3) -> bool:
    """Checks if the current Python version is at least the specified version.

    Args:
        minor (int): The minimum minor version.
        major (int, optional): The minimum major version. Defaults to 3.

    Returns:
        bool: True if the current Python version is at least the specified version, False otherwise.
    """
    return (sys.version_info.major > major) or (
        sys.version_info.major == major and sys.version_info.minor >= minor
    )
