from __future__ import annotations, division, print_function, unicode_literals

from yaml import MappingNode, Node, SafeDumper, ScalarNode

from .tag_classes import YamlPairs, YamlTagged


def yaml_represent_tagged(dumper: SafeDumper, data: YamlTagged) -> Node:
    """
    Represent a YAML tagged object.

    Args:
        dumper (SafeDumper): The YAML dumper.
        data (YamlTagged): The YAML tagged object.

    Returns:
        Node: The represented YAML node.
    """
    assert isinstance(data, YamlTagged), data
    node = dumper.represent_data(data.__wrapped__)
    node.tag = data.tag
    return node


def yaml_represent_pairs(dumper: SafeDumper, data: YamlPairs) -> MappingNode:
    """
    Represent YAML pairs.

    Args:
        dumper (SafeDumper): The YAML dumper.
        data (YamlPairs): The YAML pairs object.

    Returns:
        MappingNode: The represented YAML node.
    """
    assert isinstance(data, YamlPairs), data
    node = dumper.represent_dict(data)
    return node


def yaml_str_representer(dumper: SafeDumper, data: str) -> ScalarNode:
    """
    Represent a YAML string.

    Args:
        dumper (SafeDumper): The YAML dumper.
        data (str): The string to represent.

    Returns:
        ScalarNode: The represented YAML node.
    """
    if "\n" in data or "||" in data or "&&" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    if any(char in data for char in ":{}[],&*#?|-><!%@`"):
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style='"')
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)
