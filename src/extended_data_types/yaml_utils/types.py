"""Type definitions and configuration flags for YAML handling.

This module provides the type definitions, enums, and validation functions used
throughout the YAML utilities package.

Key Components:
    - YAMLFlags: Configuration flags for customizing behavior
    - YAMLIndent: Type definition for indentation settings
    - YAMLSettings: Complete configuration settings container
    - Validation functions for type safety

See Also:
    - utils.py: Uses these types for configuration
    - loaders.py: Implements flag-based loading behavior
    - dumpers.py: Implements flag-based dumping behavior

Example:
    Basic flag usage::

        from extended_data_types.yaml_utils import YAMLFlags
        
        # Combine flags
        flags = YAMLFlags.PRESERVE_QUOTES | YAMLFlags.NO_WRAP
        
        # Check flags
        if flags & YAMLFlags.PRESERVE_QUOTES:
            print("Quotes will be preserved")

    Custom indentation::

        from extended_data_types.yaml_utils import YAMLIndent
        
        indent: YAMLIndent = {
            "mapping": 4,
            "sequence": 6,
            "offset": 2
        }

    Complete configuration::

        from extended_data_types.yaml_utils import YAMLSettings
        
        settings = YAMLSettings(
            flags=YAMLFlags.DEFAULT,
            indent=DEFAULT_INDENT,
            version=(1, 2)
        )
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Flag, auto
from typing import Literal, TypedDict, get_args


class YAMLFlags(Flag):
    """Configuration flags for YAML handling.
    
    Attributes:
        PRESERVE_QUOTES: Preserve original string quoting style
        ALLOW_UNICODE: Allow Unicode characters in output
        SORT_KEYS: Sort dictionary keys in output
        EXPLICIT_START: Add document start marker ('---')
        EXPLICIT_END: Add document end marker ('...')
        ALLOW_DUPLICATE_KEYS: Allow duplicate keys in mappings
        NO_WRAP: Prevent line wrapping
        PRESERVE_COMMENTS: Keep comments in round-trip mode
        ROUND_TRIP: Preserve all formatting details
        DEFAULT: Standard configuration (PRESERVE_QUOTES | ALLOW_UNICODE)
        CLOUDFORMATION: CloudFormation-specific settings
        MINIMAL: Minimal formatting settings
        ROUND_TRIP_MODE: Full round-trip preservation
    """
    
    # Formatting flags
    PRESERVE_QUOTES = auto()
    ALLOW_UNICODE = auto()
    SORT_KEYS = auto()
    EXPLICIT_START = auto()  # Add '---' at start
    EXPLICIT_END = auto()    # Add '...' at end
    
    # CloudFormation flags
    ALLOW_DUPLICATE_KEYS = auto()
    NO_WRAP = auto()         # Don't wrap long lines
    
    # Advanced flags
    PRESERVE_COMMENTS = auto()
    ROUND_TRIP = auto()      # Preserve all formatting
    
    # Default configurations as combinations
    DEFAULT = PRESERVE_QUOTES | ALLOW_UNICODE
    CLOUDFORMATION = DEFAULT | ALLOW_DUPLICATE_KEYS | NO_WRAP
    MINIMAL = ALLOW_UNICODE | SORT_KEYS
    ROUND_TRIP_MODE = DEFAULT | PRESERVE_COMMENTS | ROUND_TRIP


class YAMLIndent(TypedDict):
    """Type for YAML indentation settings.
    
    Attributes:
        mapping: Number of spaces to indent mappings
        sequence: Number of spaces to indent sequences
        offset: Base indentation offset
    """
    mapping: int
    sequence: int
    offset: int


@dataclass
class YAMLSettings:
    """Full YAML configuration settings.
    
    Attributes:
        flags: Configuration flags
        indent: Indentation settings
        version: YAML version tuple
    
    Raises:
        ValueError: If any settings are invalid
    """
    flags: YAMLFlags
    indent: YAMLIndent
    version: YAMLVersion

    def __post_init__(self) -> None:
        """Validate settings after initialization."""
        validate_yaml_indent(self.indent)
        validate_yaml_version(self.version)


# Type aliases
YAMLVersion = tuple[Literal[1], Literal[1] | Literal[2]]
ValidVersions = Literal[(1, 1), (1, 2)]

# Common indentation presets
DEFAULT_INDENT: YAMLIndent = {
    "mapping": 2,
    "sequence": 4,
    "offset": 2,
}

MINIMAL_INDENT: YAMLIndent = {
    "mapping": 2,
    "sequence": 2,
    "offset": 0,
}

# Validation functions
def validate_yaml_indent(indent: YAMLIndent) -> None:
    """Validate YAML indentation settings.
    
    Args:
        indent: The indentation settings to validate
    
    Raises:
        ValueError: If any indentation values are invalid
    """
    required_keys = {"mapping", "sequence", "offset"}
    if not all(key in indent for key in required_keys):
        missing = required_keys - set(indent)
        raise ValueError(f"Missing required indent keys: {missing}")
    
    for key, value in indent.items():
        if not isinstance(value, int) or value < 0:
            raise ValueError(f"Invalid indent value for {key}: {value}")


def validate_yaml_version(version: YAMLVersion) -> None:
    """Validate YAML version tuple.
    
    Args:
        version: The version tuple to validate
    
    Raises:
        ValueError: If the version is not supported
    """
    valid_versions = get_args(ValidVersions)
    if version not in valid_versions:
        raise ValueError(
            f"Invalid YAML version {version}. "
            f"Must be one of: {valid_versions}"
        )


def flags_to_dict(flags: YAMLFlags) -> dict[str, bool]:
    """Convert YAMLFlags to configuration dictionary.
    
    Args:
        flags: The flags to convert
    
    Returns:
        A dictionary of configuration options
    """
    return {
        "preserve_quotes": bool(flags & YAMLFlags.PRESERVE_QUOTES),
        "allow_unicode": bool(flags & YAMLFlags.ALLOW_UNICODE),
        "sort_keys": bool(flags & YAMLFlags.SORT_KEYS),
        "explicit_start": bool(flags & YAMLFlags.EXPLICIT_START),
        "explicit_end": bool(flags & YAMLFlags.EXPLICIT_END),
        "allow_duplicate_keys": bool(flags & YAMLFlags.ALLOW_DUPLICATE_KEYS),
        "width": None if flags & YAMLFlags.NO_WRAP else 4096,
        "preserve_comments": bool(flags & YAMLFlags.PRESERVE_COMMENTS),
        "round_trip": bool(flags & YAMLFlags.ROUND_TRIP),
    } 