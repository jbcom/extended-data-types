"""Extended collection types."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import TypeVar

from sortedcontainers import SortedDict


KT = TypeVar("KT")
VT = TypeVar("VT")


class SortedDefaultDict(defaultdict[KT, VT], SortedDict[KT, VT]):  # type: ignore[misc]
    """A dictionary that combines defaultdict and SortedDict functionality.

    This class inherits from both collections.defaultdict and sortedcontainers.SortedDict,
    providing a dictionary that both automatically creates values for missing keys and maintains
    its keys in sorted order.

    Args:
        default_factory: Callable that provides the default value for missing keys.
            If None, attempts to access missing keys will raise KeyError.

    Examples:
        >>> d = SortedDefaultDict(list)
        >>> d['c'].append(3)
        >>> d['a'].append(1)
        >>> d['b'].append(2)
        >>> list(d.keys())
        ['a', 'b', 'c']
        >>> d['d']  # Creates new list automatically
        []
    """

    def __init__(self, default_factory: Callable[[], VT] | None = None) -> None:
        """Initialize a new SortedDefaultDict.

        Args:
            default_factory: Callable that provides the default value for missing keys.

        Raises:
            TypeError: If default_factory is not callable or None.
        """
        defaultdict.__init__(self, default_factory)
        SortedDict.__init__(self)
