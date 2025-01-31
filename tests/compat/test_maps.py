"""Tests for backward compatibility with bob map utilities."""

import pytest

from extended_data_types.compat import maps


def test_flatten_map_compatibility():
    """Verify exact compatibility with bob's flatten_map."""
    test_data = {
        "level1": {
            "level2": {
                "value": 123
            }
        }
    }
    
    result = maps.flatten_map(test_data)
    assert result["level1.level2.value"] == 123

def test_deduplicate_map_compatibility():
    """Verify exact compatibility with bob's deduplicate_map."""
    test_data = {
        "list": [1, 1, 2, 2, 3],
        "nested": {
            "list": [1, 1, 2]
        }
    }
    
    result = maps.deduplicate_map(test_data)
    assert result["list"] == [1, 2, 3]
    assert result["nested"]["list"] == [1, 2] 