"""Fuzzy search engine for function discovery."""

from __future__ import annotations

import difflib

from typing import Any

from extended_data_types.mcp.models import FunctionInfo, SearchResult


# Scoring constants
_MIN_FUZZY_RATIO = 0.6  # Minimum fuzzy match ratio to be considered relevant


class FuzzySearcher:
    """Fuzzy search engine for function discovery."""

    def __init__(self, functions: list[FunctionInfo]) -> None:
        """Initialize with list of functions to search.

        Args:
            functions: List of FunctionInfo objects to index and search.
        """
        self._functions = functions
        self._index: dict[str, Any] = {}
        self._build_index()

    def _build_index(self) -> None:
        """Build search index from functions.

        Creates searchable text combining function name, description,
        and category for efficient lookup.
        """
        for func in self._functions:
            # Create searchable text: name + description words + category
            searchable_text = (
                f"{func.name.lower()} "
                f"{func.description.lower()} "
                f"{func.category.lower()}"
            )
            self._index[func.name] = {
                "function": func,
                "searchable_text": searchable_text,
                "name_lower": func.name.lower(),
                "description_lower": func.description.lower(),
            }

    def search(
        self,
        query: str,
        *,
        category: str | None = None,
        limit: int = 10,
    ) -> list[SearchResult]:
        """Search functions by query string.

        Args:
            query: Search query (function name or description keywords).
            category: Optional category filter.
            limit: Maximum number of results (default 10).

        Returns:
            List of matching functions with scores, sorted by relevance.
        """
        if not query:
            # Empty query: return all functions (optionally filtered by category)
            functions = self._functions
            if category:
                functions = [f for f in functions if f.category == category]
            return [
                self._create_search_result(func, score=0.5)
                for func in functions[:limit]
            ]

        query_lower = query.lower()
        results: list[tuple[float, FunctionInfo]] = []

        for index_data in self._index.values():
            func = index_data["function"]

            # Apply category filter if specified
            if category and func.category != category:
                continue

            score = self._calculate_score(query_lower, func, index_data)

            # Only include results with some relevance
            if score > 0.0:
                results.append((score, func))

        # Sort by score descending, then by name
        results.sort(key=lambda x: (-x[0], x[1].name))

        # Convert to SearchResult objects
        return [
            self._create_search_result(func, score) for score, func in results[:limit]
        ]


    def _calculate_score(
        self, query: str, function: FunctionInfo, index_data: dict[str, Any]  # noqa: ARG002
    ) -> float:
        """Calculate relevance score for a function.

        Scoring criteria:
        - Exact name match: 1.0
        - Name starts with query: 0.9
        - Name contains query: 0.8
        - Fuzzy name match: 0.5-0.7 based on ratio
        - Description contains keywords: 0.3-0.5

        Args:
            query: Search query (lowercase).
            function: FunctionInfo object to score.
            index_data: Pre-computed index data for function.

        Returns:
            Relevance score between 0.0 and 1.0.
        """
        name_lower = index_data["name_lower"]
        description_lower = index_data["description_lower"]

        # Exact name match
        if name_lower == query:
            return 1.0

        # Name starts with query
        if name_lower.startswith(query):
            return 0.9

        # Name contains query
        if query in name_lower:
            return 0.8

        # Fuzzy name match using difflib
        name_ratio = difflib.SequenceMatcher(None, query, name_lower).ratio()
        if name_ratio > _MIN_FUZZY_RATIO:
            # Scale from 0.6-1.0 ratio to 0.5-0.7 score
            return 0.5 + (name_ratio - _MIN_FUZZY_RATIO) * 0.5

        # Description contains query as whole word or substring
        query_words = query.split()
        description_words = description_lower.split()

        # Check for exact word matches in description
        word_matches = sum(1 for word in query_words if word in description_words)
        if word_matches > 0:
            # Score based on proportion of matched words
            return (word_matches / len(query_words)) * 0.5

        # Check if query is a substring of description
        if query in description_lower:
            return 0.3

        # No match
        return 0.0

    def _create_search_result(
        self, function: FunctionInfo, score: float
    ) -> SearchResult:
        """Create SearchResult from FunctionInfo and score.

        Args:
            function: FunctionInfo object.
            score: Relevance score.

        Returns:
            SearchResult object.
        """
        return SearchResult(
            function_id=f"{function.module}.{function.name}",
            name=function.name,
            category=function.category,
            description=function.description,
            score=score,
            signature=function.signature,
        )
