"""Custom YAML loaders for deserializing YAML content.

This module provides custom YAML loader classes that handle special YAML features
and CloudFormation templates.

Key Components:
    - PureLoader: Main loader class with CloudFormation support
    - CLOUDFORMATION_TAGS: Mapping of CloudFormation tags

See Also:
    - dumpers.py: For serialization of loaded content
    - constructors.py: For the actual tag construction logic
    - types.py: For configuration flags
    - utils.py: For high-level loading interface

Examples:
    Direct loader usage::

        from ruamel.yaml import YAML
        from extended_data_types.yaml_utils import YAMLFlags
        from extended_data_types.yaml_utils.loaders import PureLoader

        # Configure YAML with custom loader
        yaml = YAML()
        yaml.Constructor = PureLoader
        
        # Load CloudFormation template
        template = yaml.load('''
        Resources:
          MyQueue:
            Type: AWS::SQS::Queue
            Properties:
              QueueName: !Sub ${AWS::StackName}-queue
              VisibilityTimeout: !Ref Timeout
        ''')

    Custom tag handling::

        # All CloudFormation tags are automatically handled
        assert template['Resources']['MyQueue']['Properties']['QueueName'].tag == '!Sub'
        
        # Custom tags are preserved
        data = yaml.load('!CustomTag value')
        assert data.tag == '!CustomTag'
        assert data == 'value'

    Working with duplicate keys::

        # Duplicate keys are preserved when configured
        yaml = YAML()
        yaml.Constructor = lambda stream: PureLoader(
            stream, 
            flags=YAMLFlags.ALLOW_DUPLICATE_KEYS
        )
        
        data = yaml.load('''
        mapping:
          key: value1
          key: value2
        ''')
        
        # Results in YamlPairs instead of dict
        assert len(data['mapping']) == 2

Implementation Notes:
    - CloudFormation tags are automatically converted to their long form
    - Unknown tags are preserved using YamlTagged wrapper
    - Duplicate keys are handled based on configuration flags
    - All loading is done safely without exec or eval
"""

from __future__ import annotations

from typing import Any

from ruamel.yaml import SafeConstructor

from .constructors import yaml_construct_pairs, yaml_construct_undefined
from .types import YAMLFlags


class PureLoader(SafeConstructor):
    """Custom YAML loader with CloudFormation support.
    
    This loader extends ruamel.yaml's SafeConstructor to provide:
        - CloudFormation intrinsic function handling
        - Custom tag support
        - Configurable formatting options
    
    Attributes:
        CLOUDFORMATION_TAGS: Mapping of CloudFormation short tags to long form
    """
    
    CLOUDFORMATION_TAGS = {
        "!Ref": "Ref",
        "!Sub": "Fn::Sub",
        "!GetAtt": "Fn::GetAtt",
        "!Join": "Fn::Join",
        "!Select": "Fn::Select",
        "!Split": "Fn::Split",
        "!FindInMap": "Fn::FindInMap",
        "!GetAZs": "Fn::GetAZs",
        "!ImportValue": "Fn::ImportValue",
        "!Equals": "Fn::Equals",
        "!And": "Fn::And",
        "!Or": "Fn::Or",
        "!Not": "Fn::Not",
        "!If": "Fn::If",
        "!Condition": "Condition",
    }

    def __init__(self, stream: Any, flags: YAMLFlags = YAMLFlags.DEFAULT) -> None:
        """Initialize the custom YAML loader with additional constructors.
        
        Args:
            stream: The input stream containing YAML data
            flags: Configuration flags for the loader
        """
        super().__init__(stream)
        
        # Register CloudFormation tags
        for tag in self.CLOUDFORMATION_TAGS:
            self.add_constructor(tag, yaml_construct_undefined)
        
        # Register other custom constructors
        self.add_constructor("!CustomTag", yaml_construct_undefined)
        self.add_constructor("tag:yaml.org,2002:map", yaml_construct_pairs)
        
        # Configure ruamel.yaml settings based on flags
        self.preserve_quotes = bool(flags & YAMLFlags.PRESERVE_QUOTES)
        self.allow_duplicate_keys = bool(flags & YAMLFlags.ALLOW_DUPLICATE_KEYS)
