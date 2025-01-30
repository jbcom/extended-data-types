"""Classes for handling YAML tagged objects and pairs.

This module provides the core classes for handling tagged YAML objects and
mappings with duplicate keys. These classes enable round-trip preservation
of YAML tags and handle special mapping cases.

Key Components:
    - YamlTagged: Wrapper for preserving YAML tags
    - YamlPairs: Container for mappings with duplicate keys

See Also:
    - constructors.py: Uses these classes during deserialization
    - representers.py: Uses these classes during serialization
    - utils.py: High-level interface using these classes
    - types.py: For configuration options

Examples:
    Basic tag handling::

        from extended_data_types.yaml_utils import encode_yaml
        from extended_data_types.yaml_utils.tag_classes import YamlTagged
        
        # Create tagged values
        ref = YamlTagged('!Ref', 'MyResource')
        sub = YamlTagged('!Sub', '${AWS::Region}-${AWS::StackName}')
        
        # Use in data structures
        template = {
            'Resources': {
                'MyBucket': {
                    'Type': 'AWS::S3::Bucket',
                    'Properties': {
                        'BucketName': sub,
                        'Tags': [{
                            'Key': 'Reference',
                            'Value': ref
                        }]
                    }
                }
            }
        }
        
        # Dumps as valid CloudFormation
        yaml_str = encode_yaml(template)
        # Output:
        # Resources:
        #   MyBucket:
        #     Type: AWS::S3::Bucket
        #     Properties:
        #       BucketName: !Sub ${AWS::Region}-${AWS::StackName}
        #       Tags:
        #         - Key: Reference
        #           Value: !Ref MyResource

    Working with duplicate keys::

        from extended_data_types.yaml_utils.tag_classes import YamlPairs
        
        # Create mapping with duplicates
        headers = YamlPairs([
            ('Content-Type', 'application/json'),
            ('X-Header', 'value1'),
            ('X-Header', 'value2')
        ])
        
        # Use in configuration
        config = {
            'http': {
                'headers': headers
            }
        }
        
        # Dumps preserving duplicates
        yaml_str = encode_yaml(config)
        # Output:
        # http:
        #   headers:
        #     Content-Type: application/json
        #     X-Header: value1
        #     X-Header: value2

    Tag inspection and manipulation::

        # Check tag type
        assert isinstance(ref, YamlTagged)
        assert ref.tag == '!Ref'
        assert ref == 'MyResource'  # Transparent wrapper
        
        # Access wrapped value
        original = ref.__wrapped__
        
        # Modify wrapped value
        ref.__wrapped__ = 'NewResource'

Implementation Notes:
    YamlTagged:
        - Uses wrapt.ObjectProxy for transparent wrapping
        - Preserves original object behavior
        - Maintains tag during serialization
        - Handles all Python data types
        - Thread-safe implementation
    
    YamlPairs:
        - Extends list for familiar interface
        - Maintains insertion order
        - Allows duplicate keys
        - Compatible with dict conversion
        - Efficient iteration

Best Practices:
    1. Use YamlTagged for all custom tags
    2. Keep wrapped values immutable when possible
    3. Use YamlPairs only when duplicates are needed
    4. Check tag existence before accessing
    5. Handle None values explicitly
"""

from __future__ import annotations

from typing import Any

import wrapt


class YamlTagged(wrapt.ObjectProxy):  # type: ignore[misc]
    """Wrapper class for YAML tagged objects.
    
    This class wraps any value with its associated YAML tag,
    preserving the tag for round-trip serialization.
    
    Attributes:
        tag: The YAML tag associated with the wrapped value
    """

    def __init__(self, tag: str, wrapped: Any) -> None:
        """Initialize YamlTagged object.
        
        Args:
            tag: The tag for the YAML object
            wrapped: The original object to wrap
        """
        super().__init__(wrapped)
        self._self_tag = tag

    def __repr__(self) -> str:
        """Represent the YamlTagged object as a string.
        
        Returns:
            A string representation of the object
        """
        return f"{type(self).__name__}({self._self_tag!r}, {self.__wrapped__!r})"

    @property
    def tag(self) -> str:
        """Get the tag of the YamlTagged object.
        
        Returns:
            The tag of the object
        """
        return self._self_tag


class YamlPairs(list[tuple[Any, Any]]):
    """Class to represent YAML pairs that preserves duplicates.
    
    This class extends list to store key-value pairs while allowing
    duplicate keys, which standard Python dictionaries don't support.
    """

    def __repr__(self) -> str:
        """Represent the YamlPairs object as a string.
        
        Returns:
            A string representation of the object
        """
        return f"{type(self).__name__}({super().__repr__()})"
