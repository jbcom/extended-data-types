"""Function registry for the MCP server.

This module discovers and catalogs all public functions and classes from
extended_data_types, organizing them by category and providing metadata
for efficient lookup and searching.
"""

from __future__ import annotations

import inspect
import logging

from typing import Any

import extended_data_types

from extended_data_types.mcp.models import FunctionInfo, ParameterInfo


logger = logging.getLogger(__name__)

# Constants
MIN_MODULE_PARTS = 2
MAX_DEFAULT_LENGTH = 50
MAX_DEFAULT_DISPLAY = 47

# Mapping of module names to functional categories
CATEGORY_MAP = {
    "base64_utils": "Serialization",
    "json_utils": "Serialization",
    "yaml_utils": "Serialization",
    "toml_utils": "Serialization",
    "hcl2_utils": "Serialization",
    "file_data_type": "File Operations",
    "string_data_type": "String Utilities",
    "string_transformations": "String Transformations",
    "list_data_type": "List Operations",
    "map_data_type": "Map Operations",
    "state_utils": "State Utilities",
    "type_utils": "Type Utilities",
    "matcher_utils": "Matcher Utilities",
    "stack_utils": "Stack Utilities",
    "export_utils": "Export/Import",
    "import_utils": "Export/Import",
    "splitter_utils": "Data Types",
}


class FunctionRegistry:
    """Registry of all public functions and classes from extended_data_types.

    This class provides lazy loading of function metadata and efficient
    lookup by name or category.
    """

    def __init__(self) -> None:
        """Initialize the registry."""
        self._functions: dict[str, FunctionInfo] | None = None
        self._categories_cache: list[str] | None = None

    def _ensure_loaded(self) -> None:  # noqa: PLR0912
        """Ensure the registry is populated."""
        if self._functions is not None:
            return

        self._functions = {}

        # Iterate through all public exports
        for name in extended_data_types.__all__:
            try:
                obj = getattr(extended_data_types, name)

                # Get the module where the object is defined
                module = inspect.getmodule(obj)
                if module is None:
                    continue

                module_name = module.__name__

                # Special handling for type aliases from typing module
                # Check if this is imported from a specific extended_data_types module
                if module_name == "typing":
                    # Try to find where it's defined by checking the imports
                    for submodule_name in [
                        "file_data_type",
                        "base64_utils",
                        "json_utils",
                        "yaml_utils",
                    ]:
                        try:
                            submodule = __import__(
                                f"extended_data_types.{submodule_name}",
                                fromlist=[name],
                            )
                            if hasattr(submodule, name):
                                module_name = submodule.__name__
                                break
                        except (ImportError, AttributeError):
                            continue

                # Extract the base module name for categorization
                # e.g., "extended_data_types.yaml_utils" -> "yaml_utils"
                if "." in module_name:
                    base_module = module_name.split(".")[-1]
                else:
                    base_module = module_name

                # Handle subpackages (e.g., yaml_utils.utils -> yaml_utils)
                if base_module in ["utils", "core"]:
                    parts = module_name.split(".")
                    if len(parts) >= MIN_MODULE_PARTS:
                        base_module = parts[-2]

                # Determine category
                category = CATEGORY_MAP.get(base_module, "Utilities")

                # Extract function info
                function_info = self._extract_function_info(
                    name, obj, module_name, category
                )
                if function_info:
                    self._functions[name] = function_info

            except Exception as e:  # noqa: BLE001
                # Skip any functions that can't be introspected
                # Broad exception is appropriate for introspection code
                logger.debug("Failed to introspect %s: %s", name, e)
                continue

    def _extract_function_info(  # noqa: PLR0912
        self, name: str, obj: Any, module_name: str, category: str
    ) -> FunctionInfo | None:
        """Extract metadata from a function or class.

        Args:
            name: Name of the function/class.
            obj: The function or class object.
            module_name: Full module path.
            category: Functional category.

        Returns:
            FunctionInfo object or None if extraction fails.
        """
        try:
            # Handle type aliases (like FilePath)
            if hasattr(obj, "__origin__") and hasattr(obj, "__args__"):
                # This is a type alias (Union, etc.)
                doc = inspect.getdoc(obj) or ""
                description = doc.split("\n")[0] if doc else f"Type alias: {name}"

                # Format the type alias
                type_str = str(obj).replace("typing.", "")

                return FunctionInfo(
                    name=name,
                    module=module_name,
                    category=category,
                    signature=f"{name}: {type_str}",
                    return_type=type_str,
                    description=description,
                    parameters=[],
                    related_functions=[],
                )

            # Handle both functions and classes
            elif inspect.isclass(obj):
                # For classes, extract the __init__ signature
                sig = inspect.signature(obj.__init__)
                # Get the class docstring
                doc = inspect.getdoc(obj) or ""
                description = doc.split("\n")[0] if doc else f"Class: {name}"

                # Build signature string
                params = []
                for param_name, param in sig.parameters.items():
                    if param_name == "self":
                        continue
                    params.append(self._format_parameter(param_name, param))

                signature = f"{name}({', '.join(params)})"
                return_type = name  # Classes return instances of themselves

            elif inspect.isfunction(obj) or inspect.isbuiltin(obj):
                # For functions
                try:
                    sig = inspect.signature(obj)
                except (ValueError, TypeError):
                    # Some builtins don't have signatures we can inspect
                    doc = inspect.getdoc(obj) or ""
                    description = doc.split("\n")[0] if doc else f"Function: {name}"
                    return FunctionInfo(
                        name=name,
                        module=module_name,
                        category=category,
                        signature=f"{name}(...)",
                        return_type="Any",
                        description=description,
                        parameters=[],
                        related_functions=[],
                    )

                doc = inspect.getdoc(obj) or ""
                description = doc.split("\n")[0] if doc else f"Function: {name}"

                # Build signature string
                params = []
                param_infos = []
                for param_name, param in sig.parameters.items():
                    params.append(self._format_parameter(param_name, param))
                    param_infos.append(
                        self._extract_parameter_info(param_name, param, doc)
                    )

                signature = f"{name}({', '.join(params)})"

                # Extract return type
                return_type = "Any"
                if sig.return_annotation != inspect.Parameter.empty:
                    return_type = self._format_annotation(sig.return_annotation)

                return FunctionInfo(
                    name=name,
                    module=module_name,
                    category=category,
                    signature=signature,
                    return_type=return_type,
                    description=description,
                    parameters=param_infos,
                    related_functions=[],
                )
            else:
                return None

            # Create FunctionInfo for classes
            if inspect.isclass(obj):
                param_infos = []
                for param_name, param in sig.parameters.items():
                    if param_name == "self":
                        continue
                    param_infos.append(
                        self._extract_parameter_info(param_name, param, doc)
                    )

                return FunctionInfo(
                    name=name,
                    module=module_name,
                    category=category,
                    signature=signature,
                    return_type=return_type,
                    description=description,
                    parameters=param_infos,
                    related_functions=[],
                )

        except Exception as e:  # noqa: BLE001
            # Broad exception is appropriate for introspection code
            logger.debug("Failed to extract info for %s: %s", name, e)
            return None

        return None

    def _format_parameter(self, name: str, param: inspect.Parameter) -> str:
        """Format a parameter for signature display.

        Args:
            name: Parameter name.
            param: Parameter object.

        Returns:
            Formatted parameter string.
        """
        parts = []

        # Handle *args and **kwargs
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            parts.append(f"*{name}")
        elif param.kind == inspect.Parameter.VAR_KEYWORD:
            parts.append(f"**{name}")
        else:
            parts.append(name)

        # Add type annotation if present
        if param.annotation != inspect.Parameter.empty:
            annotation = self._format_annotation(param.annotation)
            if param.kind in (
                inspect.Parameter.VAR_POSITIONAL,
                inspect.Parameter.VAR_KEYWORD,
            ):
                # For *args and **kwargs, include annotation
                parts[-1] = f"{parts[-1]}: {annotation}"
            else:
                parts.append(f": {annotation}")

        # Add default value if present
        if param.default != inspect.Parameter.empty:
            default_str = repr(param.default)
            # Truncate long defaults
            if len(default_str) > MAX_DEFAULT_LENGTH:
                default_str = default_str[:MAX_DEFAULT_DISPLAY] + "..."
            parts.append(f" = {default_str}")

        return "".join(parts)

    def _format_annotation(self, annotation: Any) -> str:
        """Format a type annotation as a string.

        Args:
            annotation: Type annotation object.

        Returns:
            String representation of the annotation.
        """
        if hasattr(annotation, "__name__"):
            return annotation.__name__
        else:
            # Handle complex annotations like list[str], dict[str, Any], etc.
            return str(annotation).replace("typing.", "")

    def _extract_parameter_info(
        self, name: str, param: inspect.Parameter, docstring: str
    ) -> ParameterInfo:
        """Extract parameter information.

        Args:
            name: Parameter name.
            param: Parameter object.
            docstring: Function docstring.

        Returns:
            ParameterInfo object.
        """
        # Format type hint
        type_hint = "Any"
        if param.annotation != inspect.Parameter.empty:
            type_hint = self._format_annotation(param.annotation)

        # Format default value
        default = None
        if param.default != inspect.Parameter.empty:
            default_str = repr(param.default)
            if len(default_str) > MAX_DEFAULT_LENGTH:
                default_str = default_str[:MAX_DEFAULT_DISPLAY] + "..."
            default = default_str

        # Try to extract description from docstring
        description = f"Parameter: {name}"
        if docstring:
            # Simple extraction - look for "name:" or "name (type):" patterns
            lines = docstring.split("\n")
            for i, raw_line in enumerate(lines):
                line = raw_line.strip()
                if line.startswith((f"{name}:", f"{name} (")):
                    # Get description from same line or next line
                    desc_parts = line.split(":", 1)
                    if len(desc_parts) > 1 and desc_parts[1].strip():
                        description = desc_parts[1].strip()
                    elif i + 1 < len(lines):
                        description = lines[i + 1].strip()
                    break

        return ParameterInfo(
            name=name, type_hint=type_hint, default=default, description=description
        )

    def get_all_functions(self) -> list[FunctionInfo]:
        """Get all registered functions.

        Returns:
            List of all FunctionInfo objects.
        """
        self._ensure_loaded()
        if self._functions is None:
            return []
        return list(self._functions.values())

    def get_function(self, name: str) -> FunctionInfo | None:
        """Get a specific function by name.

        Args:
            name: Function name to look up.

        Returns:
            FunctionInfo object or None if not found.
        """
        self._ensure_loaded()
        if self._functions is None:
            return None
        return self._functions.get(name)

    def get_functions_by_category(self, category: str) -> list[FunctionInfo]:
        """Get all functions in a specific category.

        Args:
            category: Category name to filter by.

        Returns:
            List of FunctionInfo objects in the category.
        """
        self._ensure_loaded()
        if self._functions is None:
            return []

        return [
            func_info
            for func_info in self._functions.values()
            if func_info.category == category
        ]

    def get_categories(self) -> list[str]:
        """Get all available categories.

        Returns:
            Sorted list of unique category names.
        """
        if self._categories_cache is not None:
            return self._categories_cache

        self._ensure_loaded()
        if self._functions is None:
            return []

        categories = {func_info.category for func_info in self._functions.values()}
        self._categories_cache = sorted(categories)
        return self._categories_cache


class _RegistrySingleton:
    """Singleton wrapper for FunctionRegistry."""

    _instance: FunctionRegistry | None = None

    @classmethod
    def get_instance(cls) -> FunctionRegistry:
        """Get the singleton FunctionRegistry instance.

        Returns:
            The singleton FunctionRegistry instance.
        """
        if cls._instance is None:
            cls._instance = FunctionRegistry()
        return cls._instance


def get_registry() -> FunctionRegistry:
    """Get the global function registry instance.

    Returns:
        The singleton FunctionRegistry instance.
    """
    return _RegistrySingleton.get_instance()
