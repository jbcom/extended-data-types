"""Documentation indexer for MCP server.

This module provides comprehensive documentation indexing by combining
all extractors to build complete documentation for each function.
"""

from __future__ import annotations

import extended_data_types

from extended_data_types.mcp.extractors.docstring import DocstringParser
from extended_data_types.mcp.extractors.examples import ExampleExtractor
from extended_data_types.mcp.models import Documentation, FunctionInfo
from extended_data_types.mcp.registry import FunctionRegistry, get_registry


class DocumentationIndexer:
    """Builds and indexes comprehensive documentation for all functions."""

    def __init__(
        self,
        registry: FunctionRegistry | None = None,
    ) -> None:
        """Initialize the indexer with a function registry.

        Args:
            registry: Function registry to use. If None, uses the global registry.
        """
        self._registry = registry or get_registry()
        self._docstring_parser = DocstringParser()
        self._example_extractor = ExampleExtractor()
        self._docs_cache: dict[str, Documentation] = {}
        self._indexed = False

    def build_index(self) -> None:
        """Build documentation index for all functions.

        This method is idempotent - calling it multiple times has no effect
        after the first call completes successfully.
        """
        if self._indexed:
            return

        for func_info in self._registry.get_all_functions():
            self._docs_cache[func_info.name] = self._build_documentation(func_info)

        self._indexed = True

    def get_documentation(self, function_name: str) -> Documentation | None:
        """Get documentation for a specific function.

        Args:
            function_name: Name of the function to get documentation for.

        Returns:
            Documentation object if found, None otherwise.
        """
        if not self._indexed:
            self.build_index()
        return self._docs_cache.get(function_name)

    def get_all_documentation(self) -> list[Documentation]:
        """Get documentation for all functions.

        Returns:
            List of all Documentation objects.
        """
        if not self._indexed:
            self.build_index()
        return list(self._docs_cache.values())

    def _build_documentation(self, func_info: FunctionInfo) -> Documentation:
        """Build comprehensive documentation for a function.

        Args:
            func_info: Function information from the registry.

        Returns:
            Complete Documentation object combining all extracted information.
        """
        # Get the actual callable
        func = getattr(extended_data_types, func_info.name, None)

        # Parse docstring
        docstring = func.__doc__ if func and hasattr(func, "__doc__") else None
        parsed = self._docstring_parser.parse(docstring)

        # Extract examples from tests
        examples = self._example_extractor.extract_examples(
            func_info.name,
            func_info.module,
        )

        # Find related functions (same category)
        related = [
            f.name
            for f in self._registry.get_functions_by_category(func_info.category)
            if f.name != func_info.name
        ][:5]  # Limit to 5 related

        return Documentation(
            function_id=func_info.name,
            name=func_info.name,
            module=func_info.module,
            category=func_info.category,
            signature=func_info.signature,
            return_type=func_info.return_type,
            description=parsed.short_description,
            long_description=parsed.long_description,
            parameters=func_info.parameters,
            returns=parsed.returns,
            raises=[{"type": t, "description": d} for t, d in parsed.raises],
            examples=[e.code for e in examples],
            related_functions=related,
        )


class _IndexerSingleton:
    """Singleton container for the documentation indexer."""

    _instance: DocumentationIndexer | None = None

    @classmethod
    def get_instance(cls) -> DocumentationIndexer:
        """Get or create the singleton indexer instance."""
        if cls._instance is None:
            cls._instance = DocumentationIndexer()
        return cls._instance


def get_indexer() -> DocumentationIndexer:
    """Get the global documentation indexer instance.

    Returns:
        The global DocumentationIndexer singleton.
    """
    return _IndexerSingleton.get_instance()
