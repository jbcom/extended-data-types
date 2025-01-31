Advanced Usage Guide
==================

This guide covers advanced usage patterns and integration strategies for the Extended Data Types package.

Complex Data Transformations
--------------------------

Combining multiple utilities for complex transformations:

.. code-block:: python

    from extended_data_types import (
        yaml_utils,
        json_utils,
        type_utils,
        map_data_type
    )

    # Load and transform configuration
    def process_config(config_path: str) -> dict:
        # Load YAML configuration
        with open(config_path) as f:
            config = yaml_utils.decode_yaml(f)
        
        # Convert types and validate
        config = type_utils.convert_types(config, {
            "timeout": int,
            "retries": int,
            "enabled": bool
        })
        
        # Sort and filter configuration
        config = map_data_type.sort_map(config)
        config = map_data_type.filter_map(
            config,
            exclude_keys=["_internal", "_temp"]
        )
        
        # Export as JSON
        return json_utils.encode_json(config)

Type Safety Patterns
------------------

Advanced type safety patterns:

.. code-block:: python

    from typing import TypeVar, Generic, Dict, Any
    from dataclasses import dataclass

    T = TypeVar('T')

    @dataclass
    class ValidationResult(Generic[T]):
        is_valid: bool
        value: T
        errors: list[str]

    def validate_config(
        data: Dict[str, Any],
        schema: Dict[str, type]
    ) -> ValidationResult[Dict[str, Any]]:
        errors = []
        result = {}
        
        for key, expected_type in schema.items():
            if key not in data:
                errors.append(f"Missing key: {key}")
                continue
                
            value = data[key]
            if not isinstance(value, expected_type):
                errors.append(
                    f"Invalid type for {key}: "
                    f"expected {expected_type.__name__}, "
                    f"got {type(value).__name__}"
                )
                continue
                
            result[key] = value
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            value=result,
            errors=errors
        )

Performance Optimization
---------------------

Optimizing for performance:

.. code-block:: python

    from functools import lru_cache
    from typing import Any

    # Cache type validation results
    @lru_cache(maxsize=1000)
    def validate_type_cached(value: Any, type_name: str) -> bool:
        return type_utils.validate_type(value, type_name)

    # Batch processing for large datasets
    def process_large_dataset(items: list[Any], batch_size: int = 1000):
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            process_batch(batch)

    # Memory-efficient YAML processing
    def process_large_yaml(file_path: str):
        for document in yaml_utils.decode_yaml_stream(file_path):
            process_document(document)

Integration Patterns
-----------------

Common integration patterns:

.. code-block:: python

    # Configuration management
    class Config:
        def __init__(self, path: str):
            self.path = path
            self._config = None
        
        def load(self):
            with open(self.path) as f:
                self._config = yaml_utils.decode_yaml(f)
        
        def get(self, key: str, default: Any = None) -> Any:
            if self._config is None:
                self.load()
            return self._config.get(key, default)
        
        def save(self):
            with open(self.path, 'w') as f:
                yaml_utils.encode_yaml(self._config, f)

    # Data transformation pipeline
    class Pipeline:
        def __init__(self):
            self.steps = []
        
        def add_step(self, func):
            self.steps.append(func)
            return self
        
        def process(self, data: Any) -> Any:
            result = data
            for step in self.steps:
                result = step(result)
            return result

Best Practices
------------

1. **Error Handling**:
   
   - Use specific exceptions
   - Provide context in error messages
   - Handle all error cases

2. **Type Safety**:
   
   - Use type hints consistently
   - Validate input types
   - Document type requirements

3. **Performance**:
   
   - Cache expensive operations
   - Use batch processing
   - Monitor memory usage

4. **Testing**:
   
   - Write comprehensive tests
   - Test edge cases
   - Use property-based testing

5. **Documentation**:
   
   - Document assumptions
   - Provide examples
   - Keep docs updated 