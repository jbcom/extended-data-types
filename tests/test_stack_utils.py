import pytest

from extended_data_types.stack_utils import (
    filter_methods,
    get_available_methods,
    get_caller,
)


def dummy_function():
    return get_caller()


class DummyClass:
    def public_method(self):
        """This is a public method."""

    def _private_method(self):
        """This is a private method."""

    def __dunder_method(self):
        """This is a dunder method."""

    def public_method_no_doc(self):
        pass

    def method_with_noparse(self):
        """NOPARSE This method should not be included."""


@pytest.fixture
def methods_list():
    return [
        "public_method",
        "_private_method",
        "__dunder_method",
        "public_method_no_doc",
        "method_with_noparse",
    ]


@pytest.fixture
def dummy_instance():
    return DummyClass()


def test_get_caller():
    assert dummy_function() == "test_get_caller"


def test_filter_methods(methods_list):
    filtered = filter_methods(methods_list)
    assert filtered == ["public_method", "public_method_no_doc", "method_with_noparse"]


def test_get_available_methods(dummy_instance):
    available_methods = get_available_methods(dummy_instance)
    assert "public_method" in available_methods
    assert "method_with_noparse" not in available_methods
    assert available_methods["public_method"] == "This is a public method."
    assert "public_method_no_doc" in available_methods
    assert available_methods["public_method_no_doc"] is None
