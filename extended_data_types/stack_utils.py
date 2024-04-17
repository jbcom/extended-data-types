from __future__ import annotations, division, print_function, unicode_literals

import sys
from inspect import getmembers, ismethod
from typing import Any, Dict, List, Optional


def get_caller() -> str:
    """Gets the name of the caller function.

    Returns:
        str: The name of the caller function.
    """
    return sys._getframe(2).f_code.co_name


def filter_methods(methods: List[str]) -> List[str]:
    """Filters out private methods from a list of method names.

    Args:
        methods (List[str]): The list of method names to filter.

    Returns:
        List[str]: The filtered list of method names.
    """
    return [method for method in methods if not method.startswith("_")]


def get_available_methods(cls: Any) -> Dict[str, Optional[str]]:
    """Gets available methods and their docstrings for a class.

    An "available method" is a public method that:
    - Does not contain '__' in its name.
    - Belongs to the same module as the class.
    - Does not have 'NOPARSE' in its docstring.

    Args:
        cls (Any): The class to inspect.

    Returns:
        Dict[str, Optional[str]]: A dictionary of method names and their docstrings.
    """
    module_name = cls.__class__.__module__
    methods = getmembers(cls, ismethod)

    unique_methods = {
        method_name: method_signature.__doc__
        for method_name, method_signature in methods
        if "__" not in method_name
        and method_signature.__self__.__class__.__module__ == module_name
        and "NOPARSE" not in (method_signature.__doc__ or "")
    }

    return unique_methods
