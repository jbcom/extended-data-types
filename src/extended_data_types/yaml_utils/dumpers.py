"""Custom YAML dumpers for serializing Python objects.

This module provides custom YAML dumper classes that handle special formatting
and object serialization.

Key Components:
    - PureDumper: Main dumper class with enhanced formatting
    - Custom representers for various Python types
    - Flag-based configuration for output formatting

See Also:
    - loaders.py: For deserialization of dumped content
    - representers.py: For the actual serialization logic
    - types.py: For configuration flags
    - utils.py: For high-level dumping interface

Examples:
    Direct dumper usage::

        from io import StringIO
        from ruamel.yaml import YAML
        from extended_data_types.yaml_utils import YAMLFlags
        from extended_data_types.yaml_utils.dumpers import PureDumper

        # Configure YAML with custom dumper
        yaml = YAML()
        yaml.Dumper = PureDumper
        
        # Dump with custom formatting
        data = {
            'multi_line': '''
                This is a
                multi-line string
                with formatting
            ''',
            'date': datetime.date(2024, 1, 1),
            'path': pathlib.Path('/path/to/file')
        }
        
        stream = StringIO()
        yaml.dump(data, stream)

    CloudFormation template dumping::

        template = {
            'Resources': {
                'MyBucket': {
                    'Type': 'AWS::S3::Bucket',
                    'Properties': {
                        'BucketName': YamlTagged('!Sub', '${AWS::StackName}-bucket')
                    }
                }
            }
        }
        
        # Dumps with proper tag handling
        yaml.dump(template, stream)

    Custom formatting::

        # Configure dumper with flags
        yaml.Dumper = lambda *args, **kwargs: PureDumper(
            *args,
            flags=YAMLFlags.PRESERVE_QUOTES | YAMLFlags.NO_WRAP,
            **kwargs
        )
        
        # Dumps with preserved quotes and no line wrapping
        data = {'key': '"quoted value"'}
        yaml.dump(data, stream)

Implementation Notes:
    - String formatting is context-aware (quotes, blocks, etc.)
    - Date/time values are formatted as ISO8601
    - Path objects are converted to strings
    - Tags are preserved during round-trip
    - Output formatting is highly configurable via flags
"""

from __future__ import annotations

import datetime
import pathlib
from typing import Any

from ruamel.yaml import SafeDumper

from .representers import (yaml_represent_pairs, yaml_represent_tagged,
                           yaml_str_representer)
from .tag_classes import YamlPairs, YamlTagged
from .types import YAMLFlags


class PureDumper(SafeDumper):
    """Custom YAML dumper with enhanced formatting.
    
    This dumper extends ruamel.yaml's SafeDumper to provide:
        - Custom tag representation
        - Enhanced string formatting
        - Date/time handling
        - Path object support
        - Configurable output formatting
    """

    def __init__(self, *args: Any, flags: YAMLFlags = YAMLFlags.DEFAULT, **kwargs: Any) -> None:
        """Initialize the custom YAML dumper with additional representers.
        
        Args:
            *args: Variable length argument list
            flags: Configuration flags for the dumper
            **kwargs: Arbitrary keyword arguments
        """
        super().__init__(*args, **kwargs)
        
        # Register core representers
        self.add_representer(str, yaml_str_representer)
        self.add_multi_representer(YamlTagged, yaml_represent_tagged)
        self.add_multi_representer(YamlPairs, yaml_represent_pairs)
        
        # Register date/time representers
        self.add_representer(
            datetime.date,
            lambda dumper, data: dumper.represent_scalar(
                "tag:yaml.org,2002:timestamp",
                data.isoformat(),
            ),
        )
        self.add_representer(
            datetime.datetime,
            lambda dumper, data: dumper.represent_scalar(
                "tag:yaml.org,2002:timestamp",
                data.isoformat(),
            ),
        )
        
        # Register path representer
        self.add_representer(
            pathlib.Path,
            lambda dumper, data: dumper.represent_scalar(
                "tag:yaml.org,2002:str",
                str(data),
            ),
        )
        
        # Configure based on flags
        self.default_flow_style = False
        self.allow_unicode = bool(flags & YAMLFlags.ALLOW_UNICODE)
        self.sort_keys = bool(flags & YAMLFlags.SORT_KEYS)
        self.width = None if flags & YAMLFlags.NO_WRAP else 4096

    def ignore_aliases(self, data: Any) -> bool:  # noqa: ARG002
        """Ignore aliases for the given data.
        
        Args:
            data: The data to check for aliases
        
        Returns:
            bool: Always returns True to prevent alias generation
        """
        return True
