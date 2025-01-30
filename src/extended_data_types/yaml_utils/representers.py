"""Custom representers for YAML serialization.

This module provides custom YAML representers that handle special formatting
and tag preservation during serialization.

Key Components:
    - yaml_str_representer: Smart string formatting
    - yaml_represent_tagged: Tag preservation
    - yaml_represent_pairs: Duplicate key handling

See Also:
    - dumpers.py: Uses these representers for serialization
    - constructors.py: Complementary deserialization logic
    - tag_classes.py: For the wrapped object types
    - types.py: For configuration flags

Examples:
    String representation::

        from ruamel.yaml import YAML
        from extended_data_types.yaml_utils.representers import yaml_str_representer
        
        yaml = YAML()
        yaml.representer.add_representer(str, yaml_str_representer)
        
        # Multi-line strings use block style
        data = {
            'block': '''
                First line
                Second line
                Third line
            '''
        }
        # Dumps as:
        # block: |
        #   First line
        #   Second line
        #   Third line

    Tagged values::

        from extended_data_types.yaml_utils.tag_classes import YamlTagged
        
        # Create and dump tagged value
        tagged = YamlTagged('!Custom', 'value')
        yaml.dump({'key': tagged})
        # Dumps as:
        # key: !Custom value

    Duplicate keys::

        from extended_data_types.yaml_utils.tag_classes import YamlPairs
        
        # Create and dump pairs
        pairs = YamlPairs([
            ('key', 'value1'),
            ('key', 'value2')
        ])
        yaml.dump({'mapping': pairs})
        # Dumps as:
        # mapping:
        #   key: value1
        #   key: value2

Implementation Notes:
    - String style selection is context-aware:
        - '|' for multi-line blocks
        - '>' for folded text
        - '"' for special characters
        - plain for simple strings
    - Tags are preserved exactly as specified
    - Pairs maintain order and duplicates
    - All representers handle None values safely
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ruamel.yaml import MappingNode, Node, SafeDumper, ScalarNode

from .tag_classes import YamlPairs, YamlTagged
from .types import YAMLFlags


def yaml_str_representer(dumper: SafeDumper, data: str) -> ScalarNode:
    """Represent a YAML string with appropriate formatting.
    
    Chooses the appropriate YAML string style based on content:
        - Literal block style (|) for multi-line strings > 2 lines
        - Folded style (>) for shorter multi-line strings
        - Double-quoted style (") for strings with special characters
        - Plain style for simple strings
    
    Args:
        dumper: The YAML dumper instance
        data: The string to represent
    
    Returns:
        A YAML scalar node with appropriate style
    """
    if "\n" in data:
        if data.count('\n') > 2:
            return dumper.represent_scalar(
                "tag:yaml.org,2002:str",
                data,
                style="|"
            )
        return dumper.represent_scalar(
            "tag:yaml.org,2002:str",
            data,
            style=">"
        )
    
    if any(char in data for char in ":{}[],&*#?|-><!%@`"):
        return dumper.represent_scalar(
            "tag:yaml.org,2002:str",
            data,
            style='"'
        )
    
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


def yaml_represent_tagged(dumper: SafeDumper, data: YamlTagged) -> Node:
    """Represent a YAML tagged object.
    
    Args:
        dumper: The YAML dumper instance
        data: The tagged object to represent
    
    Returns:
        A YAML node with the appropriate tag
    
    Raises:
        TypeError: If data is not a YamlTagged instance
    """
    if not isinstance(data, YamlTagged):
        message = f"Expected YamlTagged, got {type(data).__name__}"
        raise TypeError(message)
    
    node = dumper.represent_data(data.__wrapped__)
    node.tag = data.tag
    return node


def yaml_represent_pairs(dumper: SafeDumper, data: YamlPairs) -> MappingNode:
    """Represent YAML pairs that may contain duplicates.
    
    Args:
        dumper: The YAML dumper instance
        data: The pairs to represent
    
    Returns:
        A YAML mapping node
    
    Raises:
        TypeError: If data is not a YamlPairs instance
    """
    if not isinstance(data, YamlPairs):
        message = f"Expected YamlPairs, got {type(data).__name__}"
        raise TypeError(message)
    return dumper.represent_dict(data)
