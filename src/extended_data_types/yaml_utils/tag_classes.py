"""This module provides classes for handling YAML tagged objects and pairs.

It includes a wrapper class for YAML tagged objects and a class to represent YAML pairs.
"""

from __future__ import annotations

from typing import Any, List

import wrapt


class YamlTagged(wrapt.ObjectProxy):  # type: ignore[misc]
    """Wrapper class for YAML tagged objects."""

    def __init__(self, tag: str, wrapped: Any) -> None:
        """Initialize YamlTagged object.

        Args:
            tag (str): The tag for the YAML object.
            wrapped (Any): The original object to wrap.
        """
        super().__init__(wrapped)
        self._self_tag = tag

    def __repr__(self) -> str:
        """Represent the YamlTagged object as a string.

        Returns:
            str: String representation of the object.
        """
        return f"{type(self).__name__}({self._self_tag!r}, {self.__wrapped__!r})"

    @property
    def tag(self) -> str:
        """Get the tag of the YamlTagged object.

        Returns:
            str: The tag of the object.
        """
        return self._self_tag


class YamlPairs(List[Any]):
    """Class to represent YAML pairs."""

    def __repr__(self) -> str:
        """Represent the YamlPairs object as a string.

        Returns:
            str: String representation of the object.
        """
        return f"{type(self).__name__}({super().__repr__()})"
