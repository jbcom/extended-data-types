# Test Suite Guidelines

This directory contains the test suite for `extended_data_types`.

## Test Organization

Tests mirror the source structure:

```
tests/
├── __init__.py
├── test_*.py                    # Top-level module tests
├── compat/                      # Compatibility tests
├── core/                        # Core functionality tests
├── inspection/                  # Introspection tests
├── io/                          # I/O operation tests
├── matching/                    # Pattern matching tests
├── serialization/               # Serialization tests
├── structures/                  # Data structure tests
├── transformations/             # Transformation tests
├── types/                       # Type utility tests
└── validation/                  # Validation tests
```

## Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=src/ --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_type_utils.py -v

# Run specific test function
uv run pytest tests/test_type_utils.py::test_strtobool -v

# Run tests matching pattern
uv run pytest tests/ -k "yaml" -v
```

## Test File Conventions

### Naming

- Test files: `test_<module_name>.py`
- Test functions: `test_<function_name>_<scenario>`
- Test classes: `Test<ClassName>`

### Required Headers

```python
"""Test suite for extended_data_types.<module_name> module."""

from __future__ import annotations

import pytest
from extended_data_types.<module> import function_to_test
```

### Test Structure

```python
class TestFunctionName:
    """Tests for function_name."""

    def test_basic_usage(self) -> None:
        """Test basic functionality."""
        result = function_name(input_value)
        assert result == expected_value

    def test_edge_case(self) -> None:
        """Test edge case handling."""
        result = function_name(edge_input)
        assert result == edge_expected

    def test_error_handling(self) -> None:
        """Test error conditions."""
        with pytest.raises(ValueError, match="expected message"):
            function_name(invalid_input)
```

### Fixtures

Use pytest fixtures for reusable test data:

```python
@pytest.fixture
def sample_data() -> dict[str, Any]:
    """Provide sample test data."""
    return {"key": "value", "nested": {"inner": 1}}

@pytest.fixture(params=[("input1", "expected1"), ("input2", "expected2")])
def parametrized_data(request: Any) -> tuple[str, str]:
    """Provide parametrized test data."""
    return request.param
```

### Parametrization

Use `@pytest.mark.parametrize` for multiple test cases:

```python
@pytest.mark.parametrize(
    "input_value,expected",
    [
        ("yes", True),
        ("no", False),
        ("1", True),
        ("0", False),
    ],
)
def test_strtobool(input_value: str, expected: bool) -> None:
    """Test string to boolean conversion."""
    assert strtobool(input_value) == expected
```

## Coverage Requirements

- Minimum 75% coverage for new code
- All public functions must have tests
- Edge cases and error conditions must be tested

## Test Quality

- Tests must be deterministic (no flaky tests)
- Use meaningful assertion messages
- Mock external dependencies (file system, network, time)
- Clean up any temporary files/state after tests
