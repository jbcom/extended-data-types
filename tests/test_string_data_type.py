import pytest

from extended_data_types.string_data_type import (
    is_url,
    lower_first_char,
    sanitize_key,
    strtobool,
    titleize_name,
    truncate,
    upper_first_char,
)


@pytest.fixture
def test_key():
    return "key-with*invalid_chars"


@pytest.fixture
def sanitized_key():
    return "key_with_invalid_chars"


def test_sanitize_key(test_key, sanitized_key):
    assert sanitize_key(test_key) == sanitized_key


def test_truncate():
    assert truncate("This is a long message", 10) == "This is..."
    assert truncate("Short msg", 10) == "Short msg"


def test_lower_first_char():
    assert lower_first_char("Hello") == "hello"
    assert lower_first_char("") == ""


def test_upper_first_char():
    assert upper_first_char("hello") == "Hello"
    assert upper_first_char("") == ""


def test_is_url():
    assert is_url("https://example.com") is True
    assert is_url("not_a_url") is False


def test_titleize_name():
    assert titleize_name("camelCaseName") == "Camel Case Name"


def test_strtobool():
    assert strtobool("yes") is True
    assert strtobool("no") is False
    assert strtobool("invalid") is None
    with pytest.raises(ValueError):
        strtobool("invalid", raise_on_error=True)
