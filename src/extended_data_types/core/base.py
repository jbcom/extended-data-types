"""Minimal base class for backward compatibility."""


class ExtendedBase:
    """Legacy marker/base class."""

    def __repr__(self) -> str:  # pragma: no cover - simple compatibility shim
        return f"{type(self).__name__}({super().__repr__()})"
