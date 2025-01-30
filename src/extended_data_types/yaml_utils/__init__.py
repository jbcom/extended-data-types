"""YAML handling utilities with enhanced configuration and CloudFormation support.

This package provides a comprehensive set of utilities for handling YAML data with
features like:
    - Type-safe configuration using flags
    - CloudFormation template support
    - Enhanced string formatting
    - Customizable indentation
    - Comment preservation
    - Round-trip support

Key Components:
    - YAMLFlags: Configuration flags for customizing behavior
    - YAMLHandler: Main class for YAML operations
    - YamlTagged: Wrapper for tagged YAML objects
    - YamlPairs: Container for mappings with duplicate keys

Example:
    Basic usage::

        from extended_data_types.yaml_utils import decode_yaml, encode_yaml
        
        # Load YAML data
        data = decode_yaml("key: value")
        
        # Dump YAML data
        yaml_str = encode_yaml({"key": "value"})

    Advanced configuration::

        from extended_data_types.yaml_utils import YAMLFlags, configure_yaml
        
        # Configure with flags
        configure_yaml(
            YAMLFlags.PRESERVE_QUOTES | YAMLFlags.NO_WRAP,
            indent={"mapping": 2, "sequence": 4, "offset": 2}
        )

    CloudFormation support::

        template = '''
        Resources:
          MyBucket:
            Type: AWS::S3::Bucket
            Properties:
              BucketName: !Sub ${AWS::StackName}-bucket
        '''
        cf_data = decode_yaml(template)

    Working with tags::

        from extended_data_types.yaml_utils import YamlTagged
        
        # Create tagged data
        tagged = YamlTagged('!MyTag', 'value')
        
        # Dump with custom tag
        yaml_str = encode_yaml(tagged)
        # Output: !MyTag value

See Also:
    - types.py: For configuration flags and type definitions
    - utils.py: For the main YAML handling functionality
    - loaders.py: For custom YAML loading behavior
    - dumpers.py: For custom YAML dumping behavior
"""

from __future__ import annotations

from typing import Any, Literal

from .constructors import yaml_construct_pairs, yaml_construct_undefined
from .dumpers import PureDumper
from .loaders import PureLoader
from .representers import (yaml_represent_pairs, yaml_represent_tagged,
                           yaml_str_representer)
from .tag_classes import YamlPairs, YamlTagged
from .types import (DEFAULT_INDENT, MINIMAL_INDENT, YAMLFlags, YAMLIndent,
                    YAMLVersion)
from .utils import configure_yaml, decode_yaml, encode_yaml, is_yaml_data

# Export configuration types for better IDE support
YAMLVersion = tuple[Literal[1], Literal[1] | Literal[2]]
YAMLConfig = dict[str, Any]

__all__ = [
    "PureDumper",
    "PureLoader",
    "YamlPairs",
    "YamlTagged",
    "decode_yaml",
    "encode_yaml",
    "is_yaml_data",
    "configure_yaml",
    "yaml_construct_pairs",
    "yaml_construct_undefined",
    "yaml_represent_pairs",
    "yaml_represent_tagged",
    "yaml_str_representer",
    "YAMLVersion",
    "YAMLConfig",
    "DEFAULT_CONFIG",
    "CLOUDFORMATION_CONFIG",
    "MINIMAL_CONFIG",
    "YAMLFlags",
    "YAMLIndent",
    "DEFAULT_INDENT",
    "MINIMAL_INDENT",
]

# Common configuration presets
DEFAULT_CONFIG: YAMLConfig = {
    "indent_mapping": 2,
    "indent_sequence": 4,
    "indent_offset": 2,
    "width": 4096,
    "preserve_quotes": True,
    "allow_unicode": True,
    "sort_keys": False,
    "explicit_start": False,
    "explicit_end": False,
    "version": (1, 2),
}

CLOUDFORMATION_CONFIG: YAMLConfig = {
    **DEFAULT_CONFIG,
    "allow_duplicate_keys": True,
    "width": None,  # Don't wrap lines
}

MINIMAL_CONFIG: YAMLConfig = {
    "indent_mapping": 2,
    "indent_sequence": 2,
    "indent_offset": 0,
    "width": None,
    "preserve_quotes": False,
    "sort_keys": True,
}
