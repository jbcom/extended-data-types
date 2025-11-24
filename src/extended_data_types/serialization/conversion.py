"""Serialization with backward compatibility."""

from typing import Any

from extended_data_types.core.types import TypeSystem


# New Core Layer
class SerializationSystem:
    """Modern serialization system."""

    def __init__(self):
        self.type_system = TypeSystem()

    def serialize(self, data: Any, format: str = "json") -> str:
        """Modern serialization method."""
        converted = self.type_system.convert_value(data, dict)
        # Use marshmallow for schema validation
        return self._get_serializer(format).dumps(converted)


# Backward Compatibility Layer
def wrap_raw_data_for_export(
    raw_data: Any, allow_encoding: bool | str = True, **format_opts: Any
) -> str:
    """Original bob API for data export.

    Args:
        raw_data: Data to export
        allow_encoding: Encoding flag or format
        **format_opts: Format options

    Returns:
        Exported string

    Note:
        Maintains exact API compatibility with bob.export_utils.wrap_raw_data_for_export
    """
    system = SerializationSystem()
    format = "json" if allow_encoding is True else str(allow_encoding)
    return system.serialize(raw_data, format=format, **format_opts)
