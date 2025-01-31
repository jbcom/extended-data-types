"""Format-specific serializer registration.

This module registers both benedict's built-in serializers and our custom serializers
with the serialization system.
"""

from __future__ import annotations

from benedict.serializers import (IniSerializer, JsonSerializer,
                                  QuerySerializer, TomlSerializer,
                                  XmlSerializer, YamlSerializer)

from ..registry import register_serializer
from .hcl2 import Hcl2Serializer

# Register benedict's built-in serializers
register_serializer('json', JsonSerializer())
register_serializer('yaml', YamlSerializer())
register_serializer('toml', TomlSerializer())
register_serializer('xml', XmlSerializer())
register_serializer('ini', IniSerializer())
register_serializer('query', QuerySerializer())

# Register our custom serializers
register_serializer('hcl2', Hcl2Serializer()) 