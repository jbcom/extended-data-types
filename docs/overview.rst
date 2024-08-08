Overview
--------

Extended Data Types extends Python's standard data types with additional methods and utilities to simplify common tasks. It includes features like:

- **Base64 encoding and decoding**: Efficiently encode and decode data to and from Base64 format.
- **Import utilities**: Convert data to and from various formats such as JSON and YAML.
- **Export utilities**: Convert data to and from various formats such as JSON and YAML.
- **File path manipulation and validation**: Manage and validate file paths with ease.
- **Extended string manipulation functions**: Perform advanced string operations.
- **YAML utilities**: Handle custom data structures within YAML.
- **List utilities**: Simplify list operations such as filtering and flattening.
- **Map utilities**: Enhance dictionary operations with additional functionalities.
- **Matcher utilities**: Improve matching capabilities for various use cases.
- **Stack utilities**: Access and filter stack frames.
- **Nothing utilities**: Work with empty and non-empty values seamlessly.

Usage Examples
--------------

Here are a few examples to get you started:

### Base64 Encoding and Decoding

.. code-block:: python

    from extended_data_types import base64_encode

    encoded = base64_encode("Hello, World!")
    print(encoded)  # Encoded Base64 string

### Exporting Data

.. code-block:: python

    from extended_data_types import wrap_raw_data_for_export

    data = {"name": "John", "age": 30}
    wrapped_data = wrap_raw_data_for_export(data)
    print(wrapped_data)  # Wrapped data ready for export

### File Path Validation

.. code-block:: python

    from extended_data_types import is_url

    url = "https://example.com"
    print(is_url(url))  # True

### String Manipulation

.. code-block:: python

    from extended_data_types import sanitize_key, truncate

    key = sanitize_key("Some Key With Spaces")
    truncated = truncate("This is a very long message", 10)
    print(key)        # Output: Some_Key_With_Spaces
    print(truncated)  # Output: This is a...

### YAML Utilities

.. code-block:: python

    from extended_data_types import decode_yaml, encode_yaml

    yaml_data = """
    name: John
    age: 30
    """
    data = decode_yaml(yaml_data)
    print(data)  # Output: {'name': 'John', 'age': 30}

    encoded_yaml = encode_yaml(data)
    print(encoded_yaml)  # Encoded YAML string
