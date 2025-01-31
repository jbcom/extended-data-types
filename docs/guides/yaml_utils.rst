YAML Utilities Guide
==================

The ``yaml_utils`` module provides enhanced YAML handling capabilities with support for
CloudFormation templates, custom tags, and advanced formatting options.

Configuration
-----------

The module provides flexible configuration through flags:

.. code-block:: python

    from extended_data_types.yaml_utils import YAMLFlags, configure_yaml

    # Configure for CloudFormation
    configure_yaml(YAMLFlags.CLOUDFORMATION)

    # Configure for minimal output
    configure_yaml(
        YAMLFlags.MINIMAL |
        YAMLFlags.NO_WRAP |
        YAMLFlags.SORT_KEYS
    )

Available Flags
~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Flag
     - Description
   * - ``DEFAULT``
     - Standard YAML handling
   * - ``PRESERVE_QUOTES``
     - Keep original string quoting
   * - ``PRESERVE_COMMENTS``
     - Maintain comments in round-trip
   * - ``NO_WRAP``
     - Disable line wrapping
   * - ``ALLOW_DUPLICATE_KEYS``
     - Allow duplicate dictionary keys
   * - ``ROUND_TRIP``
     - Preserve format during encode/decode
   * - ``MINIMAL``
     - Minimize output formatting
   * - ``SORT_KEYS``
     - Sort dictionary keys
   * - ``CLOUDFORMATION``
     - Optimize for CloudFormation templates

CloudFormation Support
-------------------

Special support for AWS CloudFormation templates:

.. code-block:: python

    from extended_data_types.yaml_utils import YamlTagged

    template = {
        "Resources": {
            "MyBucket": {
                "Type": "AWS::S3::Bucket",
                "Properties": {
                    "BucketName": YamlTagged(
                        "!Sub",
                        "${AWS::StackName}-bucket"
                    )
                }
            }
        }
    }

    yaml_str = encode_yaml(template)

Supported CloudFormation Tags
~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``!Ref``
- ``!Sub``
- ``!GetAtt``
- ``!Join``
- ``!Select``
- ``!Split``
- ``!FindInMap``
- ``!GetAZs``
- ``!ImportValue``
- ``!Equals``
- ``!And``
- ``!Or``
- ``!Not``
- ``!If``
- ``!Condition``

Advanced Features
--------------

Custom Indentation
~~~~~~~~~~~~~~~

.. code-block:: python

    from extended_data_types.yaml_utils import configure_yaml

    configure_yaml(
        YAMLFlags.DEFAULT,
        indent={
            "mapping": 2,
            "sequence": 4,
            "offset": 2
        }
    )

Comment Preservation
~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Configure for comment preservation
    configure_yaml(YAMLFlags.PRESERVE_COMMENTS)

    yaml_str = '''
    # Header comment
    key: value  # Inline comment
    nested:
      # Nested comment
      key: value
    '''

    data = decode_yaml(yaml_str)
    result = encode_yaml(data)  # Comments are preserved

Error Handling
~~~~~~~~~~~~

.. code-block:: python

    from ruamel.yaml.error import YAMLError

    try:
        data = decode_yaml(yaml_str)
    except YAMLError as e:
        print(f"YAML parsing error: {e}")
    except ValueError as e:
        print(f"Validation error: {e}")

Best Practices
------------

1. **Configuration**:

   - Always configure explicitly
   - Use appropriate flags for your use case
   - Set consistent indentation

2. **Error Handling**:

   - Catch specific exceptions
   - Validate input/output
   - Provide meaningful error messages

3. **Type Safety**:

   - Use type hints
   - Validate data structures
   - Handle edge cases

4. **Performance**:

   - Configure for specific needs
   - Handle large files appropriately
   - Use memory efficiently
