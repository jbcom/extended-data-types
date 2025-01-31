"""Tests for stack inspection utilities."""

from extended_data_types.inspection.stack import StackInspector


class TestClass:
    """Test class for method inspection."""

    def public_method(self):
        """Test public method."""

    def _private_method(self):
        """Test private method."""


def test_get_caller_name():
    """Test getting caller name."""
    inspector = StackInspector()

    def wrapper():
        return inspector.get_caller_name()

    assert wrapper() == "test_get_caller_name"


def test_get_available_methods():
    """Test method inspection."""
    inspector = StackInspector()
    test_obj = TestClass()

    # Test with default settings
    methods = inspector.get_available_methods(test_obj)
    assert "public_method" in methods
    assert "_private_method" not in methods

    # Test with pattern
    methods = inspector.get_available_methods(test_obj, pattern="public.*")
    assert "public_method" in methods
    assert len(methods) == 1

    # Test with private methods included
    inspector_with_private = StackInspector(skip_private=False)
    methods = inspector_with_private.get_available_methods(test_obj)
    assert "_private_method" in methods


def test_version_check():
    """Test Python version checking."""
    inspector = StackInspector()

    # Should be True for Python 3.10+
    assert inspector.current_python_version_is_at_least(10)

    # Should be False for future versions
    assert not inspector.current_python_version_is_at_least(99)
