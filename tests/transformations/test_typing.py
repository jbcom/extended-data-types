"""Tests for type-based collection transformations."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import pytest

from extended_data_types.transformations.typing import (
    split_dict_by_type,
    split_list_by_type,
)


class CustomClass:
    """Test class for custom type checking."""


@pytest.fixture
def mixed_list() -> list[Any]:
    """Fixture providing a list with mixed types."""
    return [
        1,  # int
        "text",  # str
        3.14,  # float
        True,  # bool
        [1, 2, 3],  # list
        {"key": "value"},  # dict
        datetime.now(),  # datetime
        Path("/tmp"),  # Path
        CustomClass(),  # custom class
    ]


@pytest.fixture
def mixed_dict() -> dict[str, Any]:
    """Fixture providing a dictionary with mixed value types."""
    return {
        "int": 1,
        "str": "text",
        "float": 3.14,
        "bool": True,
        "list": [1, 2, 3],
        "dict": {"key": "value"},
        "datetime": datetime.now(),
        "path": Path("/tmp"),
        "custom": CustomClass(),
    }


class TestSplitListByType:
    """Tests for split_list_by_type function."""

    def test_empty_list(self):
        """Test splitting an empty list."""
        result = split_list_by_type([])
        assert len(result) == 0
        assert isinstance(result, dict)

    def test_single_type(self):
        """Test splitting a list with single type."""
        items = [1, 2, 3, 4]
        result = split_list_by_type(items)
        assert len(result) == 1
        assert result[int] == items

    def test_mixed_types(self, mixed_list):
        """Test splitting a list with mixed types."""
        result = split_list_by_type(mixed_list)

        # Check each type category
        assert len(result[int]) == 1
        assert len(result[str]) == 1
        assert len(result[float]) == 1
        assert len(result[bool]) == 1
        assert len(result[list]) == 1
        assert len(result[dict]) == 1
        assert len(result[datetime]) == 1
        assert len(result[Path]) == 1
        assert len(result[CustomClass]) == 1

        # Verify contents
        assert result[int] == [1]
        assert result[str] == ["text"]
        assert result[float] == [3.14]
        assert result[bool] == [True]
        assert result[list] == [[1, 2, 3]]
        assert result[dict] == [{"key": "value"}]

    def test_primitive_only(self, mixed_list):
        """Test splitting with primitive_only=True."""
        result = split_list_by_type(mixed_list, primitive_only=True)

        # Bool should be grouped with int
        assert 1 in result[int]
        assert True in result[int]

        # Complex types should use their primitive base
        assert isinstance(result[object][0], (datetime, Path, CustomClass))

        # Basic types remain the same
        assert "text" in result[str]
        assert 3.14 in result[float]


class TestSplitDictByType:
    """Tests for split_dict_by_type function."""

    def test_empty_dict(self):
        """Test splitting an empty dictionary."""
        result = split_dict_by_type({})
        assert len(result) == 0
        assert isinstance(result, dict)

    def test_single_type(self):
        """Test splitting a dictionary with single value type."""
        items = {"a": 1, "b": 2, "c": 3}
        result = split_dict_by_type(items)
        assert len(result) == 1
        assert result[int] == items

    def test_mixed_types(self, mixed_dict):
        """Test splitting a dictionary with mixed value types."""
        result = split_dict_by_type(mixed_dict)

        # Check each type category
        assert len(result[int]) == 1
        assert len(result[str]) == 1
        assert len(result[float]) == 1
        assert len(result[bool]) == 1
        assert len(result[list]) == 1
        assert len(result[dict]) == 1
        assert len(result[datetime]) == 1
        assert len(result[Path]) == 1
        assert len(result[CustomClass]) == 1

        # Verify contents
        assert result[int]["int"] == 1
        assert result[str]["str"] == "text"
        assert result[float]["float"] == 3.14
        assert result[bool]["bool"] is True
        assert result[list]["list"] == [1, 2, 3]
        assert result[dict]["dict"] == {"key": "value"}

    def test_primitive_only(self, mixed_dict):
        """Test splitting with primitive_only=True."""
        result = split_dict_by_type(mixed_dict, primitive_only=True)

        # Bool should be grouped with int
        assert "int" in result[int]
        assert "bool" in result[int]
        assert result[int]["int"] == 1
        assert result[int]["bool"] is True

        # Complex types should use their primitive base
        assert isinstance(result[object]["datetime"], datetime)
        assert isinstance(result[object]["path"], Path)
        assert isinstance(result[object]["custom"], CustomClass)

        # Basic types remain the same
        assert result[str]["str"] == "text"
        assert result[float]["float"] == 3.14

    def test_key_preservation(self):
        """Test that dictionary keys are preserved."""
        items = {"key1": 1, "key2": "text", "key3": True}
        result = split_dict_by_type(items)

        # Check that original keys are preserved
        assert "key1" in result[int]
        assert "key2" in result[str]
        assert "key3" in result[bool]
