from __future__ import annotations, division, print_function, unicode_literals

from typing import Any, Dict, Union

from yaml import MappingNode, SafeLoader, ScalarNode, SequenceNode

from .tag_classes import YamlPairs, YamlTagged


def yaml_construct_undefined(
    loader: SafeLoader, node: Union[ScalarNode, SequenceNode, MappingNode]
) -> YamlTagged:
    """
    Construct a YAML tagged object for undefined tags.

    Args:
        loader (SafeLoader): The YAML loader.
        node (Union[ScalarNode, SequenceNode, MappingNode]): The YAML node.

    Returns:
        YamlTagged: The constructed YAML tagged object.
    """
    value: Any
    if isinstance(node, ScalarNode):
        value = loader.construct_scalar(node)
    elif isinstance(node, SequenceNode):
        value = loader.construct_sequence(node)
    elif isinstance(node, MappingNode):
        value = loader.construct_mapping(node)
    else:
        raise TypeError(f"Unexpected node type: {type(node).__name__}")
    return YamlTagged(node.tag, value)


def yaml_construct_pairs(
    loader: SafeLoader, node: MappingNode
) -> Union[Dict, YamlPairs]:
    """
    Construct YAML pairs.

    Args:
        loader (SafeLoader): The YAML loader.
        node (MappingNode): The YAML mapping node.

    Returns:
        Union[Dict, YamlPairs]: The constructed YAML pairs.
    """
    value = loader.construct_pairs(node)
    try:
        return dict(value)
    except TypeError:
        return YamlPairs(value)
