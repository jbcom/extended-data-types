"""Format-specific serializer registration."""

from __future__ import annotations

from extended_data_types.serialization.formats.ini import IniSerializer
from extended_data_types.serialization.formats.json import JsonSerializer
from extended_data_types.serialization.formats.query import QuerySerializer
from extended_data_types.serialization.formats.toml import TomlSerializer
from extended_data_types.serialization.formats.xml import XmlSerializer
from extended_data_types.serialization.formats.yaml import YamlSerializer
from extended_data_types.serialization.registry import register_serializer


# Register all serializers
register_serializer("json", JsonSerializer())
register_serializer("yaml", YamlSerializer())
register_serializer("toml", TomlSerializer())
register_serializer("xml", XmlSerializer())
register_serializer("ini", IniSerializer())
register_serializer("query", QuerySerializer())
