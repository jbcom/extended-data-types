"""Tests for core inspection utilities."""

from __future__ import annotations

import pytest

from extended_data_types.core.inspection import (
    filter_methods,
    get_available_methods,
    get_caller,
    get_inputs_from_docstring,
    get_unique_signature,
    is_python_version_at_least,
    update_docstring,
)


def test_get_caller():
    """Test getting caller function name."""

    def wrapper():
        return get_caller()

    def caller():
        return wrapper()

    assert caller() == "caller"


def test_get_unique_signature():
    """Test generating unique signatures for objects."""

    class TestClass:
        pass

    obj = TestClass()

    # Test default delimiter
    assert get_unique_signature(obj) == f"{TestClass.__module__}/TestClass"

    # Test custom delimiter
    assert get_unique_signature(obj, "::") == f"{TestClass.__module__}::TestClass"


def test_filter_methods():
    """Test filtering private methods."""
    methods = [
        "public_method",
        "_private_method",
        "__dunder_method__",
        "_protected_method",
        "another_public_method",
    ]

    filtered = filter_methods(methods)
    assert filtered == ["public_method", "another_public_method"]
    assert all(not method.startswith("_") for method in filtered)


class TestClass:
    """Test class for method inspection."""

    def public_method(self):
        """Public method docstring."""

    def another_public(self):
        """Another public method."""

    def _private(self):
        """Private method."""

    def noparse_method(self):
        """NOPARSE: This should be excluded."""


def test_get_available_methods():
    """Test getting available methods from a class."""
    methods = get_available_methods(TestClass)

    # Should include public methods with their docstrings
    assert "public_method" in methods
    assert methods["public_method"] == "Public method docstring."
    assert "another_public" in methods

    # Should exclude private and NOPARSE methods
    assert "_private" not in methods
    assert "noparse_method" not in methods


@pytest.mark.parametrize(
    "docstring,expected",
    [
        (
            "env=name: API_KEY, required: true, sensitive: false",
            {"api_key": {"required": "true", "sensitive": "false"}},
        ),
        (
            """
            Description
            env=name: DB_PASS, required: true, sensitive: true
            env=name: DEBUG, required: false, sensitive: false
            """,
            {
                "db_pass": {"required": "true", "sensitive": "true"},
                "debug": {"required": "false", "sensitive": "false"},
            },
        ),
        (
            "No inputs here",
            {},
        ),
        (
            None,  # Test None docstring
            {},
        ),
    ],
)
def test_get_inputs_from_docstring(docstring, expected):
    """Test extracting input definitions from docstrings."""
    assert get_inputs_from_docstring(docstring) == expected


@pytest.mark.parametrize(
    "original,new_inputs,expected",
    [
        (
            "Original docstring",
            {"api_key": {"required": "true", "sensitive": "false"}},
            "Original docstring\nenv=name: api_key, required: true, sensitive: false",
        ),
        (
            """Existing inputs:
            env=name: DEBUG, required: false, sensitive: false""",
            {"api_key": {"required": "true", "sensitive": "true"}},
            """Existing inputs:
            env=name: DEBUG, required: false, sensitive: false
            env=name: api_key, required: true, sensitive: true""",
        ),
        (
            """Multiple inputs:
            env=name: DEBUG, required: false, sensitive: false
            env=name: API_KEY, required: true, sensitive: true""",
            {"api_key": {"required": "true", "sensitive": "true"}},
            """Multiple inputs:
            env=name: DEBUG, required: false, sensitive: false
            env=name: API_KEY, required: true, sensitive: true""",  # No duplicate
        ),
    ],
)
def test_update_docstring(original, new_inputs, expected):
    """Test updating docstrings with new input definitions."""
    result = update_docstring(original, new_inputs)
    # Normalize line endings for comparison
    assert result.replace("\r\n", "\n") == expected.replace("\r\n", "\n")


@pytest.mark.parametrize(
    "minor,major,expected",
    [
        (7, 3, True),  # Python >= 3.7
        (99, 3, False),  # Future version
        (0, 4, False),  # Python 4
        (5, 3, True),  # Python >= 3.5
    ],
)
def test_is_python_version_at_least(minor, major, expected):
    """Test Python version checking."""
    assert is_python_version_at_least(minor, major) == expected


def test_is_python_version_at_least_default_major():
    """Test Python version checking with default major version."""
    # Should pass for current Python version
    assert is_python_version_at_least(5)  # Python >= 3.5
