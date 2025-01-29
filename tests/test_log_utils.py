"""Tests for the log_utils module."""

from __future__ import annotations

import logging

from extended_data_types.log_utils import LoggerProtocol, get_null_logger


def test_get_null_logger() -> None:
    """Test that get_null_logger returns a logger with NullHandler.

    This test verifies that:
    1. The returned logger is an instance of logging.Logger
    2. The logger has exactly one handler
    3. The handler is an instance of logging.NullHandler
    4. The logger implements the LoggerProtocol
    """
    logger = get_null_logger("test_logger")

    # Check that we got a proper logger instance
    assert isinstance(logger, logging.Logger)

    # Check that the logger implements our protocol
    assert isinstance(logger, LoggerProtocol)

    # Check that the logger has exactly one handler
    assert len(logger.handlers) == 1

    # Check that the handler is a NullHandler
    assert isinstance(logger.handlers[0], logging.NullHandler)

    # Verify that the logger name is set correctly
    assert logger.name == "test_logger"


def test_logger_protocol_methods() -> None:
    """Test that the logger implements all required protocol methods.

    This test verifies that the logger returned by get_null_logger
    has all the methods defined in LoggerProtocol and that they
    can be called without raising exceptions.
    """
    logger = get_null_logger()

    # Test all logging methods
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")

    # If we got here without exceptions, the test passes
    assert True


def test_multiple_null_loggers() -> None:
    """Test that multiple calls to get_null_logger work correctly.

    This test verifies that:
    1. Multiple calls with the same name return the same logger instance (Python's logging behavior)
    2. The logger has exactly one NullHandler
    3. The loggers don't interfere with each other
    """
    logger1 = get_null_logger("test_logger")
    logger2 = get_null_logger("test_logger")

    # Check that we got the same logger instance (Python's logging behavior)
    assert logger1 is logger2

    # Check that we only have one handler
    assert len(logger1.handlers) == 1
    assert isinstance(logger1.handlers[0], logging.NullHandler)

    # Check that different names give different loggers
    logger3 = get_null_logger("different_logger")
    assert logger1 is not logger3
