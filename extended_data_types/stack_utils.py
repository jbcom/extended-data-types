"""This module provides utilities for inspecting the call stack and methods of classes.

It includes functions to get the caller's name, filter methods, and retrieve available
methods and their docstrings for a class.
"""

from __future__ import annotations

import sys

from inspect import getmembers, ismethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing import dict, list, type


def get_caller() -> str:
    """Gets the name of the caller function.

    Returns:
        str: The name of the caller function.
    """
    return sys._getframe(2).f_code.co_name  # noqa: SLF001


def filter_methods(methods: list[str]) -> list[str]:
    """Filters out private methods from a list of method names.

    Args:
        methods (list[str]): The list of method names to filter.

    Returns:
        list[str]: The filtered list of method names.
    """
    return [method for method in methods if not method.startswith("_")]


def get_available_methods(cls: type) -> dict[str, str | None]:
    """Gets available methods and their docstrings for a class.

    An "available method" is a public method that:
    - Does not contain '__' in its name.
    - Belongs to the same module as the class.
    - Does not have 'NOPARSE' in its docstring.

    Args:
        cls (type): The class to inspect.

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
