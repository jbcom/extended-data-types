"""HCL2 serializer implementation for the serialization registry."""

from __future__ import annotations

from typing import Any

from benedict.serializers import AbstractSerializer

from .core import HCL2
from .types import HCLFile


class HCL2Serializer(AbstractSerializer):
    """Serializer for HashiCorp Configuration Language (HCL) version 2.
    
    This serializer implements the benedict AbstractSerializer interface,
    providing HCL2 serialization support for the serialization registry.
    
    Attributes:
        hcl: HCL2 instance for parsing and generating
        
    Example:
        >>> from extended_data_types.serialization import get_serializer
        >>> serializer = get_serializer('hcl2')
        >>> data = {
        ...     "resource": {
        ...         "aws_instance": {
        ...             "web": {
        ...                 "instance_type": "t2.micro"
        ...             }
        ...         }
        ...     }
        ... }
        >>> hcl = serializer.encode(data)
        >>> decoded = serializer.decode(hcl)
    """
    
    def __init__(self, indent_size: int = 2, sort_keys: bool = False):
        """Initialize the HCL2 serializer.
        
        Args:
            indent_size: Number of spaces for indentation
            sort_keys: Whether to sort keys alphabetically
        """
        self.hcl = HCL2(indent_size=indent_size, sort_keys=sort_keys)
    
    def encode(self, obj: Any, **kwargs) -> str:
        """Encode a Python object to HCL2 string.
        
        Args:
            obj: Object to serialize (typically a dict)
            **kwargs: Additional arguments for the encoder
                indent_size: Override default indentation
                sort_keys: Override default key sorting
        
        Returns:
            str: HCL2-formatted string
            
        Raises:
            TypeError: If object cannot be converted to HCL2
        """
        if not isinstance(obj, dict):
            raise TypeError("HCL2 can only encode dictionary objects")
        
        # Convert dictionary to HCLFile structure
        hcl_file = self._dict_to_hcl_file(obj)
        
        # Update generator options if provided
        if 'indent_size' in kwargs or 'sort_keys' in kwargs:
            self.hcl.generator.indent_size = kwargs.get('indent_size', self.hcl.generator.indent_size)
            self.hcl.generator.sort_keys = kwargs.get('sort_keys', self.hcl.generator.sort_keys)
        
        return self.hcl.generate(hcl_file)
    
    def decode(self, s: str, **kwargs) -> dict:
        """Decode a HCL2 string to Python object.
        
        Args:
            s: HCL2-formatted string
            **kwargs: Additional arguments for the decoder
                filename: Optional filename for error reporting
        
        Returns:
            dict: Decoded Python dictionary
            
        Raises:
            ValueError: If string cannot be parsed as valid HCL2
        """
        hcl_file = self.hcl.parse(s)
        return self._hcl_file_to_dict(hcl_file)
    
    def _dict_to_hcl_file(self, data: dict) -> HCLFile:
        """Convert a dictionary to HCLFile structure.
        
        Args:
            data: Dictionary to convert
            
        Returns:
            HCLFile: Converted HCL file structure
            
        Example:
            >>> data = {
            ...     "resource": {
            ...         "aws_instance": {
            ...             "web": {
            ...                 "instance_type": "t2.micro"
            ...             }
            ...         }
            ...     }
            ... }
            >>> hcl_file = serializer._dict_to_hcl_file(data)
        """
        from .types import Block, BlockType
        
        hcl_file = HCLFile()
        
        # Handle terraform configuration
        if "terraform" in data:
            terraform_data = data["terraform"]
            if "required_version" in terraform_data:
                hcl_file.terraform_version = terraform_data["required_version"]
            if "required_providers" in terraform_data:
                hcl_file.required_providers = terraform_data["required_providers"]
        
        # Convert blocks
        for block_type, block_data in data.items():
            if block_type == "terraform":
                continue
                
            try:
                block_type_enum = BlockType.from_str(block_type)
            except ValueError:
                continue
            
            if isinstance(block_data, dict):
                for resource_type, instances in block_data.items():
                    if isinstance(instances, dict):
                        for name, attributes in instances.items():
                            block = Block(
                                type=block_type_enum,
                                labels=[resource_type, name],
                                attributes=attributes
                            )
                            hcl_file.blocks.append(block)
        
        return hcl_file
    
    def _hcl_file_to_dict(self, hcl_file: HCLFile) -> dict:
        """Convert HCLFile structure to dictionary.
        
        Args:
            hcl_file: HCLFile to convert
            
        Returns:
            dict: Converted dictionary structure
            
        Example:
            >>> hcl_file = HCLFile(blocks=[...])
            >>> data = serializer._hcl_file_to_dict(hcl_file)
        """
        result = {}
        
        # Add terraform configuration if present
        if hcl_file.terraform_version or hcl_file.required_providers:
            result["terraform"] = {}
            if hcl_file.terraform_version:
                result["terraform"]["required_version"] = hcl_file.terraform_version
            if hcl_file.required_providers:
                result["terraform"]["required_providers"] = hcl_file.required_providers
        
        # Convert blocks
        for block in hcl_file.blocks:
            block_type = block.type.value
            
            if block_type not in result:
                result[block_type] = {}
            
            if len(block.labels) >= 2:
                resource_type, name = block.labels[:2]
                if resource_type not in result[block_type]:
                    result[block_type][resource_type] = {}
                result[block_type][resource_type][name] = block.attributes
            elif len(block.labels) == 1:
                name = block.labels[0]
                result[block_type][name] = block.attributes
            else:
                result[block_type].update(block.attributes)
        
        return result 