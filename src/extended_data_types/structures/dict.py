"""Dictionary operations with backward compatibility."""

from collections.abc import Mapping
from typing import Any

from benedict import benedict


# New Core Layer
class EnhancedDict(benedict):
    """Modern dictionary operations."""

    def to_flat(self, separator: str = ".") -> "EnhancedDict":
        """Flatten dictionary with modern API."""
        return self.flatten(separator=separator)


# Backward Compatibility Layer
def flatten_map(
    dictionary: Mapping[str, Any], parent_key: str = "", separator: str = "."
) -> dict[str, Any]:
    """Original bob API for flattening dictionaries.

    Args:
        dictionary: Dictionary to flatten
        parent_key: Optional parent key
        separator: Key separator

    Returns:
        Flattened dictionary

    Note:
        Maintains exact API compatibility with bob.map_data_type.flatten_map
    """
    enhanced = EnhancedDict(dictionary)
    if parent_key:
        enhanced = EnhancedDict({parent_key: enhanced})
    return dict(enhanced.to_flat(separator=separator))
