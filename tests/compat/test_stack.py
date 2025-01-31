"""Tests for stack compatibility layer."""

from extended_data_types.compat.stack import (
    current_python_version_is_at_least,
    get_available_methods,
    get_caller_name,
)


class TestClass:
    """Test class for method inspection."""

    def test_method(self):
        """Test method."""


def test_get_caller_name_compatibility():
    """Test compatibility with bob's get_caller_name."""

    def wrapper():
        return get_caller_name()

    assert wrapper() == "test_get_caller_name_compatibility"


def test_get_available_methods_compatibility():
    """Test compatibility with bob's get_available_methods."""
    test_obj = TestClass()
    methods = get_available_methods(test_obj)

    assert "test_method" in methods
    assert "doc" in methods["test_method"]
    assert methods["test_method"]["is_public"]


def test_version_check_compatibility():
    """Test compatibility with bob's current_python_version_is_at_least."""
    assert current_python_version_is_at_least(10)
    assert not current_python_version_is_at_least(99)
