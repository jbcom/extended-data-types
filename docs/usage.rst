Usage
=====

Here are some usage examples for the Extended Data Types library:

Base64 Utilities
----------------

.. code-block:: python

    from extended_data_types import base64_utils

    encoded = base64_utils.base64_encode("example")
    decoded = base64_utils.base64_decode(encoded)

YAML Utilities
--------------

.. code-block:: python

    from extended_data_types.yaml_utils import decode_yaml, encode_yaml

    data = decode_yaml('key: value')
    yaml_str = encode_yaml(data)

File Path Utilities
-------------------

.. code-block:: python

    from extended_data_types.file_data_type import match_file_extensions

    is_match = match_file_extensions("example.txt", ["txt", "md"])
