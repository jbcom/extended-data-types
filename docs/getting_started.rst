Getting Started
=============

This guide will help you get started with Extended Data Types and showcase its main features.

Basic Usage
----------

YAML Handling
~~~~~~~~~~~

.. code-block:: python

    from extended_data_types.yaml_utils import encode_yaml, decode_yaml

    # Handle YAML with custom tags
    data = {
        "Resources": {
            "MyBucket": {
                "Type": "AWS::S3::Bucket",
                "Properties": {
                    "BucketName": "!Sub ${AWS::StackName}-bucket"
                }
            }
        }
    }

    yaml_str = encode_yaml(data)
    decoded = decode_yaml(yaml_str)

JSON Processing
~~~~~~~~~~~~

.. code-block:: python

    from extended_data_types.json_utils import encode_json, decode_json

    # High-performance JSON handling
    data = {"key": "value", "numbers": [1, 2, 3]}
    json_str = encode_json(data)
    decoded = decode_json(json_str)

Base64 Operations
~~~~~~~~~~~~~~

.. code-block:: python

    from extended_data_types.base64_utils import encode_base64, decode_base64

    # Encode/decode with wrapping
    encoded = encode_base64(b"binary data", wrap=True)
    decoded = decode_base64(encoded)

Advanced Features
--------------

Type Safety
~~~~~~~~~

.. code-block:: python

    from extended_data_types.type_utils import validate_type, convert_type

    # Type validation
    is_valid = validate_type(42, int)

    # Type conversion
    value = convert_type("42", int)  # Returns 42

Pattern Matching
~~~~~~~~~~~~~

.. code-block:: python

    from extended_data_types.matcher_utils import match_pattern

    # Pattern matching
    pattern = "*.txt"
    filename = "document.txt"
    matches = match_pattern(filename, pattern)

State Management
~~~~~~~~~~~~~

.. code-block:: python

    from extended_data_types.state_utils import StateManager

    # State management
    state = StateManager({
        "environment": "production",
        "features": ["feature1", "feature2"]
    })

Best Practices
------------

1. **Type Safety**

   - Always use type hints
   - Validate input types
   - Handle conversion errors

2. **Error Handling**

   - Use try/except blocks
   - Validate input data
   - Provide meaningful errors

3. **Performance**

   - Use appropriate data structures
   - Consider memory usage
   - Cache when necessary

Next Steps
---------

- Review the :doc:`api/index` for detailed documentation
- Check out the :doc:`guides/advanced_usage` guide
- See :doc:`guides/performance` for optimization tips
