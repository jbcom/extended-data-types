"""Tests for list compatibility layer."""

import pytest

from extended_data_types.compat.lists import filter_list, flatten_list


def test_flatten_list_compatibility():
    """Test compatibility with bob's flatten_list."""
    assert flatten_list([1, [2, 3], [4, [5]]]) == [1, 2, 3, 4, 5]
    assert flatten_list([]) == []
    assert flatten_list([[], []]) == []


def test_filter_list_compatibility():
    """Test compatibility with bob's filter_list."""
    assert filter_list([1, 2, 3], allowlist=[1, 2]) == [1, 2]
    assert filter_list([1, 2, 3], denylist=[2]) == [1, 3]
    assert filter_list() == [] 