"""Tests for legacy string_data_type helpers."""

from extended_data_types.string_data_type import removeprefix, removesuffix, truncate


def test_truncate_respects_max_length_when_ender_longer() -> None:
    """Ensure truncate never exceeds max_length even when ender is long."""
    assert truncate("Hello", 2, "...") == "."


def test_removeprefix_matches_builtin() -> None:
    original = "prefix_text"
    assert removeprefix(original, "prefix_") == original.removeprefix("prefix_")


def test_removesuffix_matches_builtin() -> None:
    original = "text_suffix"
    assert removesuffix(original, "suffix") == original.removesuffix("suffix")
