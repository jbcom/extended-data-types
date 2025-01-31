"""Tests for backward compatibility with bob type utilities."""

from datetime import datetime
from pathlib import Path

import pytest

from extended_data_types.compat import types


def test_convert_special_type_compatibility():
    """Verify exact compatibility with bob's convert_special_type."""
    # Test basic type conversion
    assert types.convert_special_type("123", int) == 123
    
    # Test datetime conversion
    date_str = "2024-03-14T12:00:00"
    assert isinstance(
        types.convert_special_type(date_str, datetime),
        datetime
    )
    
    # Test path conversion
    path_str = "/tmp/test"
    assert isinstance(
        types.convert_special_type(path_str, Path),
        Path
    )

def test_convert_special_types_compatibility():
    """Verify exact compatibility with bob's convert_special_types."""
    test_data = {
        "number": "123",
        "date": "2024-03-14",
        "nested": {
            "path": "/tmp/test"
        }
    }
    
    result = types.convert_special_types(test_data)
    assert isinstance(result["number"], str)  # Maintains original type when no target specified
    assert isinstance(result["nested"], dict) 