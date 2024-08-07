"""
This module contains test functions for verifying the functionality of stack and method utilities using the
`extended_data_types` package. It includes tests for filtering methods, retrieving available methods from an instance,
and getting the caller of a function.

Fixtures:
    - methods_list: Provides a list of method names for testing.
    - dummy_instance: Provides an instance of DummyClass for testing.

Functions:
    - test_get_caller: Tests retrieving the caller of a function.
    - test_filter_methods: Tests filtering method names based on visibility and documentation.
    - test_get_available_methods: Tests retrieving available methods from an instance.
"""

from __future__ import annotations

import pytest

from extended_data_types.stack_utils import (
    filter_methods,
    get_available_methods,
    get_caller,
)


def dummy_function() -> str:
    """
    A dummy function to test get_caller.

    Returns:
        str: The name of the caller function.
    """
    return get_caller()


class DummyClass:
    def public_method(self) -> None:
        """This is a public method."""

    def _private_method(self) -> None:
        """This is a private method."""

    def __dunder_method(self) -> None:
        """This is a dunder method."""

    def public_method_no_doc(self) -> None:
        pass

    def method_with_noparse(self) -> None:
        """NOPARSE This method should not be included."""


@pytest.fixture()
def methods_list() -> list[str]:
    """
    Provides a list of method names for testing.

    Returns:
        list[str]: A list of method names.
    """
    return [
        "public_method",
        "_private_method",
        "__dunder_method",
        "public_method_no_doc",
        "method_with_noparse",
    ]


@pytest.fixture()
def dummy_instance() -> DummyClass:
    """
    Provides an instance of DummyClass for testing.

    Returns:
        DummyClass: An instance of DummyClass.
    """
    return DummyClass()


def test_get_caller() -> None:
    """
    Tests retrieving the caller of a function.

    Asserts:
        The result of dummy_function matches the expected caller function name.
    """
    assert dummy_function() == "test_get_caller"


def test_filter_methods(methods_list: list[str]) -> None:
    """
    Tests filtering method names based on visibility and documentation.

    Args:
        methods_list (list[str]): A list of method names provided by the fixture.

    Asserts:
        The result of filter_methods matches the expected filtered list of method names.
    """
    filtered = filter_methods(methods_list)
    assert filtered == ["public_method", "public_method_no_doc", "method_with_noparse"]


def test_get_available_methods(dummy_instance: DummyClass) -> None:
    """
    Tests retrieving available methods from an instance.

    Args:
        dummy_instance (DummyClass): An instance of DummyClass provided by the fixture.

    Asserts:
        The available methods in dummy_instance match the expected methods and documentation.
    """
    available_methods = get_available_methods(dummy_instance)
    assert "public_method" in available_methods
    assert "method_with_noparse" not in available_methods
    assert available_methods["public_method"] == "This is a public method."
    assert "public_method_no_doc" in available_methods
    assert available_methods["public_method_no_doc"] is None
