# src/extended_data_types/yaml_utils/formatting.py
"""YAML formatting utilities."""
from __future__ import annotations

from typing import Any

from ruamel.yaml import scalarstring


class YAMLFormatter:
    """Handles YAML formatting decisions."""
    
    @staticmethod
    def format_string(value: str) -> Any:
        """Format string values appropriately."""
        if '\n' in value:
            if value.count('\n') > 2:
                # Use literal block for multi-line strings
                return scalarstring.LiteralScalarString(value)
            # Use folded style for shorter multi-line strings
            return scalarstring.FoldedScalarString(value)
        
        # Quote strings containing special characters
        if any(char in value for char in ':{}[]!@#$%^&*'):
            return scalarstring.DoubleQuotedScalarString(value)
        
        return value
    
    @staticmethod
    def format_mapping(data: dict) -> dict:
        """Format dictionary values."""
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = YAMLFormatter.format_string(value)
            elif isinstance(value, dict):
                result[key] = YAMLFormatter.format_mapping(value)
            elif isinstance(value, list):
                result[key] = YAMLFormatter.format_sequence(value)
            else:
                result[key] = value
        return result
    
    @staticmethod
    def format_sequence(data: list) -> list:
        """Format list values."""
        result = []
        for item in data:
            if isinstance(item, str):
                result.append(YAMLFormatter.format_string(item))
            elif isinstance(item, dict):
                result.append(YAMLFormatter.format_mapping(item))
            elif isinstance(item, list):
                result.append(YAMLFormatter.format_sequence(item))
            else:
                result.append(item)
        return result