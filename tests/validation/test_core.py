"""Tests for core validation utilities."""

from __future__ import annotations

from extended_data_types.validation.core import (
    all_non_empty,
    all_non_empty_in_dict,
    all_non_empty_in_list,
    any_non_empty,
    are_nothing,
    are_something,
    first_non_empty,
    is_nothing,
    is_something,
    yield_non_empty,
)


def test_is_nothing():
    """Test is_nothing function."""
    # Basic empty values
    assert is_nothing(None)
    assert is_nothing("")
    assert is_nothing([])
    assert is_nothing({})

    # Whitespace strings
    assert is_nothing("   ")
    assert is_nothing("\n\t")

    # Lists/sets with empty values
    assert is_nothing([None, "", {}])
    assert is_nothing({None, "", []})

    # Non-empty values
    assert not is_nothing("text")
    assert not is_nothing([1, 2, 3])
    assert not is_nothing({"key": "value"})
    assert not is_nothing(42)


def test_are_nothing():
    """Test are_nothing function."""
    # All empty values
    assert are_nothing(None, "", [], {})
    assert are_nothing(a=None, b="", c=[])

    # Mixed args and kwargs
    assert are_nothing(None, "", b={}, c=[])

    # Non-empty values
    assert not are_nothing(None, "text")
    assert not are_nothing(a=None, b="text")
    assert not are_nothing("text", b="value")


def test_is_something():
    """Test is_something function."""
    assert is_something("text")
    assert is_something([1])
    assert is_something({"key": "value"})
    assert not is_something(None)
    assert not is_something("")
    assert not is_something([])


def test_are_something():
    """Test are_something function."""
    assert are_something("text", [1], {"key": "value"})
    assert not are_something("text", None)
    assert not are_something("text", "")
    assert not are_something("text", [])


def test_all_non_empty():
    """Test all_non_empty function."""
    # No arguments
    assert all_non_empty() is None

    # Only args
    assert all_non_empty("text", [1]) == ["text", [1]]
    assert all_non_empty(None, "", "text") == ["text"]

    # Only kwargs
    result = all_non_empty(a="text", b=None, c=[1])
    assert isinstance(result, dict)
    assert result == {"a": "text", "c": [1]}

    # Both args and kwargs
    args_result, kwargs_result = all_non_empty("text", [1], a="value", b=None)
    assert args_result == ["text", [1]]
    assert kwargs_result == {"a": "value"}


def test_all_non_empty_in_list():
    """Test all_non_empty_in_list function."""
    assert all_non_empty_in_list([]) == []
    assert all_non_empty_in_list([None, "", []]) == []
    assert all_non_empty_in_list(["text", None, [1]]) == ["text", [1]]


def test_all_non_empty_in_dict():
    """Test all_non_empty_in_dict function."""
    assert all_non_empty_in_dict({}) == {}
    assert all_non_empty_in_dict({"a": None, "b": "", "c": []}) == {}
    assert all_non_empty_in_dict({"a": "text", "b": None, "c": [1]}) == {
        "a": "text",
        "c": [1],
    }


def test_first_non_empty():
    """Test first_non_empty function."""
    assert first_non_empty() is None
    assert first_non_empty(None, "", "text", "more") == "text"
    assert first_non_empty(None, "", []) is None
    assert first_non_empty([1], None, "text") == [1]


def test_any_non_empty():
    """Test any_non_empty function."""
    data = {"a": "text", "b": None, "c": [1]}

    assert any_non_empty(data, "a") == {"a": "text"}
    assert any_non_empty(data, "b") == {}
    assert any_non_empty(data, "d") == {}
    assert any_non_empty(data, "b", "a") == {"a": "text"}
    assert any_non_empty(data, "d", "b", "c") == {"c": [1]}


def test_yield_non_empty():
    """Test yield_non_empty function."""
    data = {"a": "text", "b": None, "c": [1], "d": ""}

    results = list(yield_non_empty(data, "a", "b", "c", "d"))
    assert results == [{"a": "text"}, {"c": [1]}]

    assert list(yield_non_empty(data, "b", "d")) == []
    assert list(yield_non_empty(data, "x", "y")) == []
    assert list(yield_non_empty({}, "a", "b")) == []
