from __future__ import annotations, division, print_function, unicode_literals

from typing import Any

import wrapt  # type: ignore


class YamlTagged(wrapt.ObjectProxy):
    """Wrapper class for YAML tagged objects."""

    def __init__(self, tag: str, wrapped: Any) -> None:
        """
        Initialize YamlTagged object.

        Args:
            tag (str): The tag for the YAML object.
            wrapped (Any): The original object to wrap.
        """
        super().__init__(wrapped)
        self._self_tag = tag

    def __repr__(self) -> str:
        """
        Represent the YamlTagged object as a string.

        Returns:
            str: String representation of the object.
        """
        return f"{type(self).__name__}({self._self_tag!r}, {self.__wrapped__!r})"

    @property
    def tag(self) -> str:
        """
        Get the tag of the YamlTagged object.

        Returns:
            str: The tag of the object.
        """
        return self._self_tag


class YamlPairs(list):
    """Class to represent YAML pairs."""

    def __repr__(self) -> str:
        """
        Represent the YamlPairs object as a string.

        Returns:
            str: String representation of the object.
        """
        return f"{type(self).__name__}({super().__repr__()})"
