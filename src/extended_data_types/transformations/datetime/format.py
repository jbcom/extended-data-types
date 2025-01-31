"""Datetime formatting operations."""

from __future__ import annotations

from datetime import date, datetime, time, tzinfo
from typing import Literal
from zoneinfo import ZoneInfo

from ..core import Transform


TimeFormat = Literal["12h", "24h"]
DateFormat = Literal["short", "medium", "long", "iso"]


def format_date(
    dt: date | datetime, format: str | DateFormat = "medium", locale: str = "en_US"
) -> str:
    """Format date to string.

    Args:
        dt: Date to format
        format: Format string or predefined format
        locale: Locale code

    Returns:
        Formatted date string

    Example:
        >>> format_date(date(2024, 1, 1))
        'Jan 1, 2024'
        >>> format_date(date(2024, 1, 1), "long")
        'January 1, 2024'
        >>> format_date(date(2024, 1, 1), "%Y-%m-%d")
        '2024-01-01'
    """
    if isinstance(format, str) and not format.startswith("%"):
        formats = {
            "short": "%b %d, %Y",
            "medium": "%b %d, %Y",
            "long": "%B %d, %Y",
            "iso": "%Y-%m-%d",
        }
        format = formats.get(format, format)

    return dt.strftime(format)


def format_time(
    t: time | datetime, format: str | TimeFormat = "24h", locale: str = "en_US"
) -> str:
    """Format time to string.

    Args:
        t: Time to format
        format: Format string or time format
        locale: Locale code

    Returns:
        Formatted time string

    Example:
        >>> format_time(time(13, 30))
        '13:30'
        >>> format_time(time(13, 30), "12h")
        '1:30 PM'
    """
    if format == "12h":
        return t.strftime("%I:%M %p").lstrip("0")
    elif format == "24h":
        return t.strftime("%H:%M")
    return t.strftime(format)


def format_datetime(
    dt: datetime,
    date_format: str | DateFormat = "medium",
    time_format: str | TimeFormat = "24h",
    include_timezone: bool = True,
    locale: str = "en_US",
) -> str:
    """Format datetime to string.

    Args:
        dt: Datetime to format
        date_format: Date format
        time_format: Time format
        include_timezone: Include timezone
        locale: Locale code

    Returns:
        Formatted datetime string

    Example:
        >>> dt = datetime(2024, 1, 1, 13, 30, tzinfo=timezone.utc)
        >>> format_datetime(dt)
        'Jan 1, 2024 13:30 UTC'
    """
    date_str = format_date(dt, date_format, locale)
    time_str = format_time(dt, time_format, locale)

    if include_timezone and dt.tzinfo:
        return f"{date_str} {time_str} {dt.tzinfo}"
    return f"{date_str} {time_str}"


def parse_date(text: str, format: str | None = None, locale: str = "en_US") -> date:
    """Parse date from string.

    Args:
        text: Date string
        format: Format string (None for automatic)
        locale: Locale code

    Returns:
        Parsed date

    Example:
        >>> parse_date("2024-01-01")
        datetime.date(2024, 1, 1)
        >>> parse_date("Jan 1, 2024", "%b %d, %Y")
        datetime.date(2024, 1, 1)
    """
    if format is None:
        formats = ["%Y-%m-%d", "%m/%d/%Y", "%b %d, %Y", "%B %d, %Y"]
        for fmt in formats:
            try:
                return datetime.strptime(text, fmt).date()
            except ValueError:
                continue
        raise ValueError(f"Could not parse date: {text}")

    return datetime.strptime(text, format).date()


def parse_time(text: str, format: str | None = None, locale: str = "en_US") -> time:
    """Parse time from string.

    Args:
        text: Time string
        format: Format string (None for automatic)
        locale: Locale code

    Returns:
        Parsed time

    Example:
        >>> parse_time("13:30")
        datetime.time(13, 30)
        >>> parse_time("1:30 PM", "%I:%M %p")
        datetime.time(13, 30)
    """
    if format is None:
        formats = ["%H:%M", "%H:%M:%S", "%I:%M %p", "%I:%M:%S %p"]
        for fmt in formats:
            try:
                return datetime.strptime(text, fmt).time()
            except ValueError:
                continue
        raise ValueError(f"Could not parse time: {text}")

    return datetime.strptime(text, format).time()


def parse_datetime(
    text: str,
    format: str | None = None,
    timezone: tzinfo | str | None = None,
    locale: str = "en_US",
) -> datetime:
    """Parse datetime from string.

    Args:
        text: Datetime string
        format: Format string (None for automatic)
        timezone: Timezone to apply
        locale: Locale code

    Returns:
        Parsed datetime

    Example:
        >>> parse_datetime("2024-01-01 13:30")
        datetime.datetime(2024, 1, 1, 13, 30)
        >>> parse_datetime("2024-01-01 13:30", timezone="UTC")
        datetime.datetime(2024, 1, 1, 13, 30, tzinfo=UTC)
    """
    if format is None:
        formats = [
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d %H:%M:%S",
            "%m/%d/%Y %I:%M %p",
            "%b %d, %Y %H:%M",
        ]
        for fmt in formats:
            try:
                dt = datetime.strptime(text, fmt)
                break
            except ValueError:
                continue
        else:
            raise ValueError(f"Could not parse datetime: {text}")
    else:
        dt = datetime.strptime(text, format)

    if timezone is not None:
        if isinstance(timezone, str):
            timezone = ZoneInfo(timezone)
        return dt.replace(tzinfo=timezone)
    return dt


def to_iso(dt: date | datetime | time, timezone: bool = True) -> str:
    """Convert to ISO format string.

    Args:
        dt: Date/time to convert
        timezone: Include timezone (if available)

    Returns:
        ISO format string

    Example:
        >>> to_iso(datetime(2024, 1, 1, 13, 30, tzinfo=timezone.utc))
        '2024-01-01T13:30:00+00:00'
    """
    if isinstance(dt, datetime):
        return dt.isoformat() if timezone else dt.isoformat().split("+")[0]
    return dt.isoformat()


def from_iso(text: str, timezone: tzinfo | str | None = None) -> date | datetime | time:
    """Parse from ISO format string.

    Args:
        text: ISO format string
        timezone: Timezone to apply

    Returns:
        Parsed date/time

    Example:
        >>> from_iso("2024-01-01T13:30:00")
        datetime.datetime(2024, 1, 1, 13, 30)
    """
    try:
        if "T" in text:
            dt = datetime.fromisoformat(text)
            if timezone is not None:
                if isinstance(timezone, str):
                    timezone = ZoneInfo(timezone)
                dt = dt.replace(tzinfo=timezone)
            return dt
        elif ":" in text:
            return time.fromisoformat(text)
        return date.fromisoformat(text)
    except ValueError as e:
        raise ValueError(f"Invalid ISO format: {text}") from e


# Register transforms
format_date_transform = Transform(format_date)
format_time_transform = Transform(format_time)
format_datetime_transform = Transform(format_datetime)
parse_date_transform = Transform(parse_date)
parse_time_transform = Transform(parse_time)
parse_datetime_transform = Transform(parse_datetime)
to_iso_transform = Transform(to_iso)
from_iso_transform = Transform(from_iso)
