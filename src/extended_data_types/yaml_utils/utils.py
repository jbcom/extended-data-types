"""Core YAML utility functions.

This module provides the main YAML handling functionality, serving as the primary
interface for YAML operations.

Key Components:
    - YAMLHandler: Main class for YAML operations
    - decode_yaml: Function to parse YAML content
    - encode_yaml: Function to serialize to YAML
    - configure_yaml: Function to set global options

See Also:
    - types.py: For configuration options and type definitions
    - loaders.py: For custom loading behavior
    - dumpers.py: For custom dumping behavior
    - tag_classes.py: For handling tagged objects

Examples:
    Basic usage::

        from extended_data_types.yaml_utils import decode_yaml, encode_yaml
        
        # Load YAML
        data = decode_yaml('''
        server:
          host: localhost
          port: 8080
        ''')
        
        # Modify data
        data['server']['port'] = 9000
        
        # Dump YAML
        yaml_str = encode_yaml(data)

    Configuration::

        from extended_data_types.yaml_utils import (
            YAMLFlags,
            configure_yaml,
            MINIMAL_INDENT
        )
        
        # Set global configuration
        configure_yaml(
            flags=YAMLFlags.MINIMAL | YAMLFlags.NO_WRAP,
            indent=MINIMAL_INDENT
        )

    CloudFormation template handling::

        template = decode_yaml('''
        Resources:
          MyFunction:
            Type: AWS::Lambda::Function
            Properties:
              Runtime: python3.9
              Code:
                S3Bucket: !Ref CodeBucket
                S3Key: !Sub ${Version}/lambda.zip
        ''')
        
        # Template is parsed with proper CloudFormation tag handling
        print(template['Resources']['MyFunction']['Properties']['Code'])

    Working with custom tags::

        from extended_data_types.yaml_utils import YamlTagged
        
        # Create custom tagged data
        config = {
            'database': YamlTagged('!Ref', 'DatabaseName'),
            'timeout': YamlTagged('!Ref', 'Timeout')
        }
        
        # Dumps as:
        # database: !Ref DatabaseName
        # timeout: !Ref Timeout
        yaml_str = encode_yaml(config)
"""
from __future__ import annotations

from io import StringIO
from typing import Any

from ruamel.yaml import YAML

from extended_data_types.string_data_type import bytestostr

from .dumpers import PureDumper
from .loaders import PureLoader
from .tag_classes import YamlPairs, YamlTagged
from .types import (DEFAULT_INDENT, YAMLFlags, YAMLIndent, YAMLSettings,
                    YAMLVersion, flags_to_dict, validate_yaml_indent,
                    validate_yaml_version)


class YAMLHandler:
    """Main YAML handler maintaining compatibility.
    
    This class provides a high-level interface for YAML operations with
    configurable behavior and proper error handling.
    
    Attributes:
        yaml: The underlying ruamel.yaml instance
    """
    
    def __init__(self) -> None:
        """Initialize the YAML handler with default settings."""
        self.yaml = YAML(typ='safe')
        self._configure(YAMLSettings(
            flags=YAMLFlags.DEFAULT,
            indent=DEFAULT_INDENT,
            version=(1, 2)
        ))
    
    def _configure(self, settings: YAMLSettings) -> None:
        """Configure YAML handler with validated settings.
        
        Args:
            settings: The settings to apply
        """
        # Core configuration
        self.yaml.Constructor = PureLoader
        self.yaml.Dumper = PureDumper
        
        # Apply validated settings
        options = flags_to_dict(settings.flags)
        self.yaml.indent(
            mapping=settings.indent["mapping"],
            sequence=settings.indent["sequence"],
            offset=settings.indent["offset"]
        )
        self.yaml.version = settings.version
        
        for key, value in options.items():
            setattr(self.yaml, key, value)
    
    def configure(
        self,
        flags: YAMLFlags = YAMLFlags.DEFAULT,
        indent: YAMLIndent | None = None,
        version: YAMLVersion = (1, 2)
    ) -> None:
        """Configure YAML handler with type-safe options.
        
        Args:
            flags: Configuration flags
            indent: Indentation settings (uses DEFAULT_INDENT if None)
            version: YAML version tuple
        
        Raises:
            ValueError: If any settings are invalid
        """
        if indent is None:
            indent = DEFAULT_INDENT.copy()
        
        settings = YAMLSettings(flags=flags, indent=indent, version=version)
        self._configure(settings)
    
    def load(self, stream: str | memoryview | bytes | bytearray) -> Any:
        """Load YAML with full compatibility.
        
        Args:
            stream: The YAML content to load
        
        Returns:
            The parsed YAML data
        
        Raises:
            ValueError: If the input cannot be decoded
        """
        try:
            stream = bytestostr(stream)
        except UnicodeDecodeError as exc:
            raise ValueError(f"Failed to decode bytes to string: {stream!r}") from exc
            
        return self.yaml.load(stream)
    
    def dump(self, data: Any) -> str:
        """Dump YAML maintaining existing format.
        
        Args:
            data: The data to serialize
        
        Returns:
            The YAML string representation
        """
        stream = StringIO()
        self.yaml.dump(data, stream)
        return stream.getvalue()
    
    def is_yaml_data(self, data: Any) -> bool:
        """Check for YAML features.
        
        Args:
            data: The data to check
        
        Returns:
            True if the data contains YAML-specific features
        """
        if isinstance(data, (YamlTagged, YamlPairs)):
            return True
        if isinstance(data, dict):
            return any(self.is_yaml_data(v) for v in data.values())
        if isinstance(data, (list, tuple)):
            return any(self.is_yaml_data(item) for item in data)
        return False


# Single global handler instance
_handler = YAMLHandler()


def decode_yaml(yaml_data: str | memoryview | bytes | bytearray) -> Any:
    """Decode YAML data into a Python object.
    
    Args:
        yaml_data: The YAML content to decode
    
    Returns:
        The parsed YAML data
    
    Raises:
        ValueError: If the input cannot be decoded
    """
    return _handler.load(yaml_data)


def encode_yaml(raw_data: Any) -> str:
    """Encode a Python object into a YAML string.
    
    Args:
        raw_data: The data to encode
    
    Returns:
        The YAML string representation
    """
    return _handler.dump(raw_data)


def is_yaml_data(data: Any) -> bool:
    """Check if the data is a YAML tagged object.
    
    Args:
        data: The data to check
    
    Returns:
        True if the data contains YAML-specific features
    """
    return _handler.is_yaml_data(data)


def configure_yaml(
    flags: YAMLFlags = YAMLFlags.DEFAULT,
    indent: YAMLIndent | None = None,
    version: YAMLVersion = (1, 2)
) -> None:
    """Configure global YAML handler with type-safe options.
    
    Args:
        flags: Configuration flags
        indent: Indentation settings
        version: YAML version tuple
    
    Example:
        >>> configure_yaml(
        ...     YAMLFlags.MINIMAL | YAMLFlags.NO_WRAP,
        ...     indent={"mapping": 2, "sequence": 2, "offset": 0},
        ...     version=(1, 2)
        ... )
    
    Raises:
        ValueError: If any settings are invalid
    """
    _handler.configure(flags, indent, version)
