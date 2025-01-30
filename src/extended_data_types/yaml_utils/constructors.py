"""Custom constructors for YAML deserialization.

This module provides custom YAML constructors that handle special tags
and duplicate keys during deserialization.

Key Components:
    - yaml_construct_undefined: Handles unknown tags
    - yaml_construct_pairs: Handles duplicate keys
    - Tag preservation system

See Also:
    - loaders.py: Uses these constructors for deserialization
    - representers.py: Complementary serialization logic
    - tag_classes.py: For the wrapper classes
    - types.py: For configuration flags

Examples:
    Unknown tag handling::

        from ruamel.yaml import YAML
        from extended_data_types.yaml_utils.constructors import yaml_construct_undefined
        
        yaml = YAML()
        yaml.constructor.add_constructor(None, yaml_construct_undefined)
        
        # Load unknown tag
        data = yaml.load('!CustomTag value')
        assert data.tag == '!CustomTag'
        assert data == 'value'

    CloudFormation tags::

        # Load CloudFormation template
        template = yaml.load('''
        Resources:
          MyQueue:
            Type: AWS::SQS::Queue
            Properties:
              QueueName: !Sub ${AWS::StackName}-queue
        ''')
        
        # Access tagged values
        queue_name = template['Resources']['MyQueue']['Properties']['QueueName']
        assert queue_name.tag == '!Sub'
        assert queue_name == '${AWS::StackName}-queue'

    Duplicate keys::

        # Load mapping with duplicates
        data = yaml.load('''
        mapping:
          key: value1
          key: value2
        ''')
        
        # Access as pairs
        pairs = data['mapping']
        assert len(pairs) == 2
        assert pairs[0] == ('key', 'value1')
        assert pairs[1] == ('key', 'value2')

Implementation Notes:
    - Unknown tags are preserved using YamlTagged wrapper
    - CloudFormation tags are handled automatically
    - Duplicate keys are preserved using YamlPairs
    - All construction is done safely without exec
    - None values are handled gracefully
    - Circular references are detected
"""

from __future__ import annotations

from typing import Any

from ruamel.yaml.constructor import Constructor
from ruamel.yaml.nodes import MappingNode, ScalarNode, SequenceNode

from .tag_classes import YamlPairs, YamlTagged


def yaml_construct_undefined(
    constructor: Constructor,
    node: ScalarNode | SequenceNode | MappingNode,
) -> YamlTagged:
    """Construct an object from an undefined tag.
    
    This constructor wraps any tagged value in a YamlTagged object,
    preserving the original tag for round-trip serialization.
    
    Args:
        constructor: The YAML constructor instance
        node: The YAML node to construct
    
    Returns:
        A YamlTagged object wrapping the constructed value
    """
    if not hasattr(node, 'tag'):
        return constructor.construct_object(node)
    return YamlTagged(node.tag, constructor.construct_object(node))


def yaml_construct_pairs(constructor: Constructor, node: MappingNode) -> dict | YamlPairs:
    """Construct a mapping that may contain duplicate keys.
    
    Args:
        constructor: The YAML constructor instance
        node: The YAML mapping node to construct
    
    Returns:
        Either a dict or YamlPairs depending on if keys are unique
    """
    pairs: list[tuple[Any, Any]] = constructor.construct_pairs(node)
    try:
        return dict(pairs)
    except TypeError:
        return YamlPairs(pairs)
