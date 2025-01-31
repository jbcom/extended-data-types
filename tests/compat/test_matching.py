"""Tests for matching compatibility layer."""

from extended_data_types.compat.matching import is_partial_match, is_value_match


def test_partial_match_compatibility():
    """Test compatibility with bob's is_partial_match."""
    assert is_partial_match("test", "testing")
    assert is_partial_match("TEST", "testing")
    assert not is_partial_match("test", "best")

    # Test prefix only
    assert is_partial_match("test", "testing", check_prefix_only=True)
    assert not is_partial_match("ing", "testing", check_prefix_only=True)


def test_value_match_compatibility():
    """Test compatibility with bob's is_value_match."""
    assert is_value_match({"a": 1}, {"a": 1})
    assert is_value_match([1, 2, 3], [3, 2, 1])
    assert not is_value_match("1", 1)
    assert is_value_match(None, None)
