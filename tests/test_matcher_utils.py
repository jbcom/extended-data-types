import pytest

from extended_data_types.matcher_utils import is_non_empty_match, is_partial_match


@pytest.mark.parametrize(
    ("a", "b", "check_prefix_only", "expected"),
    [
        ("HelloWorld", "helloworld", False, True),
        ("Hello", "hello world", False, True),
        ("hello", "world", False, False),
        ("prefix", "pre", True, True),
        ("pre", "prefix", True, True),
        ("pre", "suffix", True, False),
    ],
)
def test_is_partial_match(a, b, check_prefix_only, expected):
    assert is_partial_match(a, b, check_prefix_only=check_prefix_only) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        ("Hello", "hello", True),
        ({"key": "value"}, {"key": "value"}, True),
        ({"key": "value"}, {"KEY": "VALUE"}, False),
        ([1, 2, 3], [3, 2, 1], True),
        ([1, 2], [1, 2, 3], False),
        (123, 123, True),
        (123, "123", False),
        (None, None, False),
    ],
)
def test_is_non_empty_match(a, b, expected):
    assert is_non_empty_match(a, b) == expected
