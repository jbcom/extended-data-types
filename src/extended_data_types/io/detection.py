"""File type detection utilities.

This module provides utilities for detecting and inferring file types,
encodings, and formats based on file paths and content patterns.
"""

from __future__ import annotations

from pathlib import Path

from .types import EncodingType, FilePath


def get_encoding_for_file_path(file_path: FilePath) -> EncodingType:
    """Determine encoding type based on file extension.
    
    Args:
        file_path: Path to check
        
    Returns:
        Detected encoding type
        
    Examples:
        >>> get_encoding_for_file_path("config.yaml")
        'yaml'
        >>> get_encoding_for_file_path("data.json")
        'json'
        >>> get_encoding_for_file_path("main.tf")
        'hcl'
    """
    suffix = Path(file_path).suffix.lower()
    
    if suffix in {".yaml", ".yml"}:
        return "yaml"
    if suffix == ".json":
        return "json"
    if suffix in {".hcl", ".tf"}:
        return "hcl"
    if suffix in {".toml", ".tml"}:
        return "toml"
    return "raw"

def is_config_file(file_path: FilePath) -> bool:
    """Check if file path matches common configuration file patterns.
    
    Args:
        file_path: Path to check
        
    Returns:
        True if path matches config file pattern
        
    Examples:
        >>> is_config_file("config.yaml")
        True
        >>> is_config_file("settings.json")
        True
        >>> is_config_file("main.tf")
        True
    """
    return get_encoding_for_file_path(file_path) != "raw" 