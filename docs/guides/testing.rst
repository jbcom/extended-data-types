Testing Guide
============

This guide covers testing strategies and best practices for the Extended Data Types package.

Unit Testing
-----------

Basic unit testing patterns:

.. code-block:: python

    import pytest
    from extended_data_types import yaml_utils, type_utils

    def test_yaml_encoding():
        # Arrange
        data = {"key": "value", "list": [1, 2, 3]}
        
        # Act
        yaml_str = yaml_utils.encode_yaml(data)
        decoded = yaml_utils.decode_yaml(yaml_str)
        
        # Assert
        assert decoded == data
        assert isinstance(decoded["key"], str)
        assert isinstance(decoded["list"], list)

    def test_type_validation():
        # Test valid cases
        assert type_utils.validate_type(42, int)
        assert type_utils.validate_type("test", str)
        
        # Test invalid cases
        assert not type_utils.validate_type("42", int)
        assert not type_utils.validate_type(42, str)

Property-Based Testing
-------------------

Using hypothesis for property-based testing:

.. code-block:: python

    from hypothesis import given, strategies as st

    @given(st.dictionaries(
        keys=st.text(),
        values=st.one_of(st.text(), st.integers())
    ))
    def test_map_roundtrip(data):
        # Test that sorting and filtering preserves data
        sorted_data = map_data_type.sort_map(data)
        assert len(sorted_data) == len(data)
        assert set(sorted_data.items()) == set(data.items())

    @given(st.lists(st.integers()))
    def test_list_operations(data):
        # Test list flattening properties
        flat = list_data_type.flatten_list(data)
        assert len(flat) >= len(data)
        assert all(not isinstance(x, list) for x in flat)

Fixtures and Factories
-------------------

Creating test data:

.. code-block:: python

    import pytest
    from dataclasses import dataclass
    from typing import Any, Dict

    @dataclass
    class TestConfig:
        data: Dict[str, Any]
        expected_result: Any
        should_raise: bool = False

    @pytest.fixture
    def sample_configs():
        return [
            TestConfig(
                data={"key": "value"},
                expected_result={"key": "value"}
            ),
            TestConfig(
                data={"invalid": object()},
                expected_result=None,
                should_raise=True
            )
        ]

    def test_configs(sample_configs):
        for config in sample_configs:
            if config.should_raise:
                with pytest.raises(Exception):
                    process_config(config.data)
            else:
                result = process_config(config.data)
                assert result == config.expected_result

Integration Testing
----------------

Testing integrated components:

.. code-block:: python

    def test_full_pipeline():
        # Setup test data
        input_data = {
            "config": {
                "timeout": "30",
                "retries": "3"
            },
            "data": [1, 2, 3]
        }
        
        # Create pipeline
        pipeline = Pipeline()
        pipeline.add_step(lambda x: type_utils.convert_types(
            x["config"],
            {"timeout": int, "retries": int}
        ))
        pipeline.add_step(map_data_type.sort_map)
        
        # Process data
        result = pipeline.process(input_data)
        
        # Verify results
        assert isinstance(result["config"]["timeout"], int)
        assert isinstance(result["config"]["retries"], int)

Best Practices
------------

1. **Test Organization**:
   
   - Group related tests
   - Use descriptive names
   - Maintain test independence

2. **Test Coverage**:
   
   - Test edge cases
   - Include error cases
   - Test type combinations

3. **Test Performance**:
   
   - Use appropriate fixtures
   - Minimize test duration
   - Profile test suite

4. **Maintenance**:
   
   - Keep tests simple
   - Update with code changes
   - Document test requirements 