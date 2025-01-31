Overview
========

Extended Data Types enhances Python's standard data types with additional functionality and utilities to simplify common tasks.

Key Features
-----------

Data Type Extensions
~~~~~~~~~~~~~~~~~~

- **List Operations**: Advanced list manipulation including flattening, filtering, and type-safe operations
- **Map Operations**: Enhanced dictionary operations with sorting, filtering, and type validation
- **String Operations**: Comprehensive string manipulation and validation utilities
- **Type Utilities**: Robust type checking, conversion, and validation

Format Support
~~~~~~~~~~~~

- **YAML**: Enhanced YAML handling with custom tags and advanced features
- **JSON**: High-performance JSON operations using orjson
- **Base64**: Flexible encoding/decoding with wrapping options
- **TOML**: Comprehensive TOML format support
- **HCL2**: HashiCorp Configuration Language parsing

File and Path Handling
~~~~~~~~~~~~~~~~~~~

- **Path Operations**: Safe path manipulation and validation
- **File Type Detection**: Automatic file type detection
- **Encoding Support**: Automatic encoding detection and handling

Pattern Matching
~~~~~~~~~~~~~~

- **Type Patterns**: Advanced type-based pattern matching
- **String Matching**: Flexible string matching with wildcards
- **Custom Matchers**: Extensible matcher framework

State Management
~~~~~~~~~~~~~~

- **State Tracking**: Type-safe state management
- **Configuration**: Environment-aware configuration
- **Validation**: Comprehensive state validation

Quick Examples
------------

List Operations
~~~~~~~~~~~~~

.. code-block:: python

    from extended_data_types import list_data_type

    # Flatten nested lists
    nested = [[1, 2], [3, [4, 5]]]
    flat = list_data_type.flatten_list(nested)  # [1, 2, 3, 4, 5]

Map Operations
~~~~~~~~~~~~

.. code-block:: python

    from extended_data_types import map_data_type

    # Sort dictionary
    unsorted = {"c": 3, "a": 1, "b": 2}
    sorted_map = map_data_type.sort_map(unsorted)  # {"a": 1, "b": 2, "c": 3}

YAML Operations
~~~~~~~~~~~~~

.. code-block:: python

    from extended_data_types import yaml_utils

    # Parse YAML with custom tags
    yaml_str = """
    name: !ref ${USER}
    config: !include config.yaml
    """
    data = yaml_utils.decode_yaml(yaml_str)

Next Steps
---------

- Check out the :doc:`installation` guide to get started
- Review the :doc:`api/index` for detailed documentation
- See the :doc:`guides/advanced_usage` for advanced features
