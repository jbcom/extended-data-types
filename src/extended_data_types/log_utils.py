"""Utility functions for logging."""

from __future__ import annotations

import logging
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class LoggerProtocol(Protocol):
    """Protocol defining the required logger interface."""

    def debug(self, msg: str, /, *args: Any, **kwargs: Any) -> None:
        """Log a debug message.

        Args:
            msg: The message to log.
            args: Format string arguments.
            kwargs: Additional keyword arguments.
        """
        ...

    def info(self, msg: str, /, *args: Any, **kwargs: Any) -> None:
        """Log an info message.

        Args:
            msg: The message to log.
            args: Format string arguments.
            kwargs: Additional keyword arguments.
        """
        ...

    def warning(self, msg: str, /, *args: Any, **kwargs: Any) -> None:
        """Log a warning message.

        Args:
            msg: The message to log.
            args: Format string arguments.
            kwargs: Additional keyword arguments.
        """
        ...

    def error(self, msg: str, /, *args: Any, **kwargs: Any) -> None:
        """Log an error message.

        Args:
            msg: The message to log.
            args: Format string arguments.
            kwargs: Additional keyword arguments.
        """
        ...

    def critical(self, msg: str, /, *args: Any, **kwargs: Any) -> None:
        """Log a critical message.

        Args:
            msg: The message to log.
            args: Format string arguments.
            kwargs: Additional keyword arguments.
        """
        ...

    def exception(self, msg: str, /, *args: Any, **kwargs: Any) -> None:
        """Log an exception message.

        Args:
            msg: The message to log.
            args: Format string arguments.
            kwargs: Additional keyword arguments.
        """
        ...


def get_null_logger(name: str = __name__) -> logging.Logger:
    """Get a logger with a NullHandler.

    Args:
        name: The name for the logger. Defaults to module name.

    Returns:
        A logger that won't emit any messages unless configured.
        Note: Python's logging module reuses logger instances by name.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.addHandler(logging.NullHandler())
    return logger
