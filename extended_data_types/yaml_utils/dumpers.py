from __future__ import annotations, division, print_function, unicode_literals

import datetime
import pathlib
from typing import Any

from yaml import SafeDumper

from .representers import (
    yaml_represent_pairs,
    yaml_represent_tagged,
    yaml_str_representer,
)
from .tag_classes import YamlPairs, YamlTagged


class PureDumper(SafeDumper):
    """Custom YAML dumper."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.add_representer(str, yaml_str_representer)
        self.add_multi_representer(YamlTagged, yaml_represent_tagged)
        self.add_multi_representer(YamlPairs, yaml_represent_pairs)
        self.add_representer(
            datetime.date,
            lambda dumper, data: dumper.represent_scalar(
                "tag:yaml.org,2002:timestamp", data.isoformat()
            ),
        )
        self.add_representer(
            datetime.datetime,
            lambda dumper, data: dumper.represent_scalar(
                "tag:yaml.org,2002:timestamp", data.isoformat()
            ),
        )
        self.add_representer(
            pathlib.Path,
            lambda dumper, data: dumper.represent_scalar(
                "tag:yaml.org,2002:str", str(data)
            ),
        )

    def ignore_aliases(self, data: Any) -> bool:
        return True
