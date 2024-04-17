from __future__ import annotations, division, print_function, unicode_literals

from typing import Any

from yaml import SafeLoader

from .constructors import yaml_construct_pairs, yaml_construct_undefined


class PureLoader(SafeLoader):
    """Custom YAML loader."""

    def __init__(self, stream: Any) -> None:
        super().__init__(stream)
        self.add_constructor("!CustomTag", yaml_construct_undefined)
        self.add_constructor("!Ref", yaml_construct_undefined)
        self.add_constructor("!Sub", yaml_construct_undefined)
        self.add_constructor("tag:yaml.org,2002:map", yaml_construct_pairs)
