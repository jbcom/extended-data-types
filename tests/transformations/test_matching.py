"""Tests for string and value matching utilities."""

from __future__ import annotations

import pytest

from extended_data_types.transformations.matching import (
    is_non_empty_match,
    is_partial_match,
)


class TestPartialMatch:
    """Tests for is_partial_match function."""

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            ("hello", "hell", True),
            ("hello", "lo", True),
            ("hello", "help", False),
            ("HELLO", "hello", True),
            ("hello", "HELL", True),
            ("abc", "def", False),
            ("", "text", False),
            ("text", "", False),
            (None, "text", False),
            ("text", None, False),
            (None, None, False),
        ],
    )
    def test_basic_matching(self, a, b, expected):
        """Test basic partial matching scenarios."""
        assert is_partial_match(a, b) == expected

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            ("hello", "hell", True),
            ("hello", "lo", False),
            ("HELLO", "hell", True),
            ("hello", "HELL", True),
            ("hello", "help", False),
        ],
    )
    def test_prefix_only(self, a, b, expected):
        """Test prefix-only matching."""
        assert is_partial_match(a, b, check_prefix_only=True) == expected

    def test_whitespace_handling(self):
        """Test handling of whitespace in strings."""
        assert is_partial_match("hello world", "world")
        assert is_partial_match("hello  world", "world")
        assert is_partial_match("  hello  ", "hello")
        assert not is_partial_match("  ", "text")


class TestNonEmptyMatch:
    """Tests for is_non_empty_match function."""

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            ("hello", "HELLO", True),
            ("Hello", "hello", True),
            ("hello", "world", False),
            ("", "", True),
            (None, None, False),
            (None, "text", False),
            ("text", None, False),
        ],
    )
    def test_string_matching(self, a, b, expected):
        """Test string matching with case insensitivity."""
        assert is_non_empty_match(a, b) == expected

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            ([1, 2, 3], [3, 2, 1], True),
            ([1, 2], [2, 1], True),
            ([1, 2], [1, 3], False),
            ([], [], True),
            ([1, "2"], [1, "2"], True),
            ([1, 2], [1, "2"], False),  # Different types
        ],
    )
    def test_list_matching(self, a, b, expected):
        """Test list matching with sorting."""
        assert is_non_empty_match(a, b) == expected

    def test_uncomparable_lists(self):
        """Test lists with uncomparable elements."""
        # Lists containing uncomparable elements should return False
        assert not is_non_empty_match(
            [1, {}], [{}, 1]  # dict and int can't be compared
        )
        assert not is_non_empty_match(
            [[], {}], [{}, []]  # list and dict can't be compared
        )

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            ({"a": 1}, {"a": 1}, True),
            ({"a": 1, "b": 2}, {"b": 2, "a": 1}, True),
            ({"a": 1}, {"a": 2}, False),
            ({}, {}, True),
            ({"a": [1, 2]}, {"a": [2, 1]}, True),
            ({"a": {"b": 1}}, {"a": {"b": 1}}, True),
        ],
    )
    def test_dict_matching(self, a, b, expected):
        """Test dictionary matching with JSON encoding."""
        assert is_non_empty_match(a, b) == expected

    def test_type_mismatches(self):
        """Test handling of type mismatches."""
        assert not is_non_empty_match(1, "1")
        assert not is_non_empty_match([1], {"1": 1})
        assert not is_non_empty_match(True, 1)
        assert not is_non_empty_match({}, [])

    def test_nested_structures(self):
        """Test matching of nested data structures."""
        a = {
            "list": [1, 2, 3],
            "dict": {"a": 1, "b": [4, 5, 6]},
            "mixed": [{"x": 1}, {"y": 2}],
        }
        b = {
            "dict": {"b": [6, 5, 4], "a": 1},
            "list": [3, 2, 1],
            "mixed": [{"y": 2}, {"x": 1}],
        }
        assert is_non_empty_match(a, b)
