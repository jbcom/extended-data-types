"""Tests for list transformation utilities."""

from __future__ import annotations

from typing import Any

import pytest

from extended_data_types.transformations.lists import filter_list, flatten_list


class TestFlattenList:
    """Tests for flatten_list function."""
    
    def test_empty_list(self):
        """Test flattening an empty list."""
        assert flatten_list([]) == []
    
    def test_flat_list(self):
        """Test flattening an already flat list."""
        items = [1, 2, 3, 4]
        assert flatten_list(items) == items
    
    @pytest.mark.parametrize(
        "nested,expected",
        [
            ([[1, 2], [3, 4]], [1, 2, 3, 4]),
            ([[1], [2], [3]], [1, 2, 3]),
            ([[], [1], [], [2]], [1, 2]),
        ],
    )
    def test_single_level_nesting(self, nested: list[Any], expected: list[Any]):
        """Test flattening single-level nested lists."""
        assert flatten_list(nested) == expected
    
    @pytest.mark.parametrize(
        "nested,expected",
        [
            ([[1, [2, 3]], [4, [5, 6]]], [1, 2, 3, 4, 5, 6]),
            ([1, [2, [3, [4]]]], [1, 2, 3, 4]),
            ([[[[1]]]], [1]),
        ],
    )
    def test_multi_level_nesting(self, nested: list[Any], expected: list[Any]):
        """Test flattening multi-level nested lists."""
        assert flatten_list(nested) == expected
    
    def test_mixed_types(self):
        """Test flattening lists with mixed types."""
        nested = [
            1,
            ["string", 2.0],
            [True, [None, {"key": "value"}]],
        ]
        expected = [1, "string", 2.0, True, None, {"key": "value"}]
        assert flatten_list(nested) == expected
    
    def test_nested_empty_lists(self):
        """Test flattening nested empty lists."""
        assert flatten_list([[], [[]], [], [[[]]]]) == []

class TestFilterList:
    """Tests for filter_list function."""
    
    def test_empty_inputs(self):
        """Test filtering with empty inputs."""
        assert filter_list() == []
        assert filter_list(None) == []
        assert filter_list([]) == []
        assert filter_list([], []) == []
        assert filter_list([], [], []) == []
    
    def test_no_filters(self):
        """Test filtering without any filters applied."""
        items = ["a", "b", "c"]
        assert filter_list(items) == items
        assert filter_list(items, None, None) == items
    
    @pytest.mark.parametrize(
        "items,allowlist,expected",
        [
            (["a", "b", "c"], ["a", "b"], ["a", "b"]),
            (["a", "b", "c"], ["b"], ["b"]),
            (["a", "b", "c"], [], []),
            (["a", "b", "c"], ["d"], []),
        ],
    )
    def test_allowlist(self, items, allowlist, expected):
        """Test filtering with allowlist."""
        assert filter_list(items, allowlist=allowlist) == expected
    
    @pytest.mark.parametrize(
        "items,denylist,expected",
        [
            (["a", "b", "c"], ["b"], ["a", "c"]),
            (["a", "b", "c"], ["a", "b", "c"], []),
            (["a", "b", "c"], ["d"], ["a", "b", "c"]),
            (["a", "b", "c"], [], ["a", "b", "c"]),
        ],
    )
    def test_denylist(self, items, denylist, expected):
        """Test filtering with denylist."""
        assert filter_list(items, denylist=denylist) == expected
    
    def test_combined_filters(self):
        """Test filtering with both allowlist and denylist."""
        items = ["a", "b", "c", "d"]
        
        # Allow a, b, c but deny b
        assert filter_list(
            items,
            allowlist=["a", "b", "c"],
            denylist=["b"]
        ) == ["a", "c"]
        
        # Empty result when item is both allowed and denied
        assert filter_list(
            items,
            allowlist=["a"],
            denylist=["a"]
        ) == []
    
    def test_with_duplicates(self):
        """Test filtering lists with duplicate items."""
        items = ["a", "b", "a", "c", "b"]
        
        # Allowlist
        assert filter_list(items, allowlist=["a", "b"]) == ["a", "b", "a", "b"]
        
        # Denylist
        assert filter_list(items, denylist=["b"]) == ["a", "a", "c"]
    
    def test_type_preservation(self):
        """Test that filtering preserves item types."""
        items = [1, 2, 3, 4]
        filtered = filter_list(items, allowlist=[1, 2])
        assert all(isinstance(x, int) for x in filtered)
        
        items = [1.0, 2.0, 3.0]
        filtered = filter_list(items, denylist=[2.0])
        assert all(isinstance(x, float) for x in filtered) 