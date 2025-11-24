"""Datetime formatting operations."""

from __future__ import annotations

from datetime import date, datetime, time, timedelta, tzinfo
from typing import Literal
from zoneinfo import ZoneInfo

from extended_data_types.transformations.core import Transform


TimeFormat = Literal["12h", "24h"]
DateFormat = Literal["short", "medium", "long", "iso"]


def format_date(
    dt: date | datetime, format: str | DateFormat = "iso", locale: str = "en_US"
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
    if format == "short":
        return f"{dt.month:02d}/{dt.day:02d}/{dt.year % 100:02d}"
    if locale.startswith("es"):
        months_es = [
            "enero",
            "febrero",
            "marzo",
            "abril",
            "mayo",
            "junio",
            "julio",
            "agosto",
            "septiembre",
            "octubre",
            "noviembre",
            "diciembre",
        ]
        if format == "long":
            return f"{dt.day} de {months_es[dt.month - 1]} de {dt.year}"
        return dt.strftime("%d/%m/%Y")

    if isinstance(format, str) and not format.startswith("%"):
        formats = {
            "medium": "%b %d, %Y",
            "long": "%B %d, %Y",
            "iso": "%Y-%m-%d",
            "full": "%A, %B %d, %Y",
        }
        if format not in formats and not format.startswith("%"):
            raise ValueError(f"Unsupported date format: {format}")
        format = formats.get(format, format)

    return dt.strftime(format)


def format_time(
    t: time | datetime,
    format: str | TimeFormat = "24h",
    locale: str = "en_US",
    *,
    microseconds: bool = False,
    timezone: tzinfo | str | None = None,
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
    fmt = format
    if format == "short":
        fmt = "%I:%M %p"
    elif format == "medium":
        fmt = "%I:%M:%S %p"
    elif format == "12h":
        fmt = "%I:%M:%S %p"
    elif format == "24h":
        fmt = "%H:%M:%S"
    elif format == "long":
        fmt = "%I:%M:%S %p"
    elif isinstance(format, str) and not format.startswith("%"):
        raise ValueError(f"Unsupported time format: {format}")
    if microseconds and "%S" in fmt and ".%f" not in fmt:
        fmt = fmt.replace("%S", "%S.%f")
    if timezone is not None:
        base_dt = datetime.combine(date.today(), t)
        if isinstance(timezone, str):
            timezone = ZoneInfo(timezone)
        base_dt = base_dt.replace(tzinfo=ZoneInfo("UTC")).astimezone(timezone)
        t = base_dt.time()
    result = t.strftime(fmt)
    if format in {"12h", "short", "medium"}:
        result = result.lstrip("0").replace(" 0", " ")
    if format == "long":
        result = result.lstrip("0").replace(" 0", " ")
        result = f"{result} UTC"
    return result


def format_datetime(
    dt: datetime,
    date_format: str | DateFormat = "iso",
    time_format: str | TimeFormat = "24h",
    include_timezone: bool = True,
    locale: str = "en_US",
    format: str | None = None,
    timezone: tzinfo | str | None = None,
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
    if format:
        return dt.strftime(format)

    if locale.startswith("es"):
        date_str = format_date(dt, date_format, locale)
        time_str = dt.strftime("%H:%M:%S")
        return f"{date_str}, {time_str}"

    if timezone is not None:
        if isinstance(timezone, str):
            timezone = ZoneInfo(timezone)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo("UTC"))
        dt = dt.astimezone(timezone)

    if date_format == "short" and time_format == "24h":
        time_format = "short"
    if date_format == "medium" and time_format == "24h":
        time_format = "medium"
    if date_format == "long" and time_format == "24h":
        time_format = "long"

    if date_format == "short":
        date_str = f"{dt.month}/{dt.day}/{dt.year % 100:02d}"
    else:
        date_str = format_date(dt, date_format, locale)
    time_str = format_time(dt, time_format, locale)
    separator = " at " if date_format == "long" else (", " if date_format in {"short", "medium"} else " ")

    if include_timezone and dt.tzinfo:
        return f"{date_str}{separator}{time_str} {dt.tzinfo}"
    return f"{date_str}{separator}{time_str}"


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
        formats = ["%Y-%m-%d", "%m/%d/%Y", "%b %d, %Y", "%B %d, %Y", "%d-%b-%Y", "%d/%m/%Y"]
        for fmt in formats:
            try:
                return datetime.strptime(text, fmt).date()
            except ValueError:
                continue
        raise ValueError(f"Could not parse date: {text}")

    return datetime.strptime(text, format).date()


def parse_time(text: str, format: str | None = None, locale: str = "en_US", timezone: tzinfo | str | None = None) -> time:
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
        formats = ["%H:%M", "%H:%M:%S", "%H:%M:%S.%f", "%I:%M %p", "%I:%M:%S %p"]
        for fmt in formats:
            try:
                parsed = datetime.strptime(text, fmt).time()
                break
            except ValueError:
                continue
        else:
            raise ValueError(f"Could not parse time: {text}")
    else:
        parsed = datetime.strptime(text, format).time()

    if timezone is not None:
        if isinstance(timezone, str):
            timezone = ZoneInfo(timezone)
        return parsed.replace(tzinfo=timezone)
    return parsed

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
            "%m/%d/%y, %I:%M %p",
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


def format_timedelta(delta: timedelta, style: str = "default", units: str | None = None) -> str:
    """Format timedelta to HH:MM:SS."""
    valid_styles = {"default", "short", "medium", "long"}
    if style not in valid_styles:
        raise ValueError(f"Unsupported timedelta style: {style}")
    sign = "-" if delta.total_seconds() < 0 else ""
    total_seconds = int(abs(delta.total_seconds()))
    days, remainder = divmod(total_seconds, 86_400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    time_part = f"{hours}:{minutes:02d}:{seconds:02d}"
    if units == "hours":
        hours_total = total_seconds / 3600
        return f"{sign}{hours_total:.2f} hours"
    if units == "minutes":
        minutes_total = total_seconds / 60
        return f"{sign}{minutes_total:.2f} minutes"
    if style == "short":
        parts = []
        if days:
            parts.append(f"{days}d")
        if hours:
            parts.append(f"{hours}h")
        if minutes:
            parts.append(f"{minutes}m")
        if not parts:
            parts.append(f"{seconds}s")
        return " ".join(parts)
    if style == "medium":
        components = []
        if days:
            components.append(f"{days} {'day' if days == 1 else 'days'}")
        if hours:
            components.append(f"{hours} {'hour' if hours == 1 else 'hours'}")
        if minutes:
            components.append(f"{minutes} {'minute' if minutes == 1 else 'minutes'}")
        if not components:
            components.append(f"{seconds} seconds")
        return ", ".join(components)
    if style == "long":
        components = []
        if days:
            components.append(f"{days} {'day' if days == 1 else 'days'}")
        components.append(f"{hours} {'hour' if hours == 1 else 'hours'}")
        components.append(f"{minutes} {'minute' if minutes == 1 else 'minutes'}")
        components.append(f"{seconds} {'second' if seconds == 1 else 'seconds'}")
        return sign + ", ".join(components)
    if days:
        day_label = "day" if days == 1 else "days"
        return f"{sign}{days} {day_label}, {time_part}"
    return f"{sign}{time_part}"


def parse_timedelta(text: str) -> timedelta:
    """Parse 'D days, HH:MM:SS', 'HH:MM:SS', or short '1d 2h 30m'."""
    text = text.strip()
    sign = -1 if text.startswith("-") else 1
    if text.startswith(("-", "+")):
        text = text[1:].strip()
    lower = text.lower()
    if "hour" in lower and ":" not in text and "day" not in lower and "d" not in lower:
        value_str = lower.split("hour")[0].strip()
        hours_float = float(value_str)
        hours_int = int(hours_float)
        minutes = int(round((hours_float - hours_int) * 60))
        return sign * timedelta(hours=hours_int, minutes=minutes)
    if "minute" in lower and ":" not in text:
        value_str = lower.split("minute")[0].strip()
        minutes_val = float(value_str)
        whole = int(minutes_val)
        seconds = int(round((minutes_val - whole) * 60))
        return sign * timedelta(minutes=whole, seconds=seconds)
    day_part = 0
    if "day" in text:
        day_section, time_part = text.split(",", 1)
        day_part = int(day_section.split()[0])
        time_part = time_part.strip()
        parts = time_part.split(":")
        if len(parts) != 3:
            raise ValueError("Invalid timedelta format")
        hours, minutes, seconds = map(int, parts)
        return sign * timedelta(days=day_part, hours=hours, minutes=minutes, seconds=seconds)

    if ":" in text:
        parts = text.split(":")
        if len(parts) != 3:
            raise ValueError("Invalid timedelta format")
        hours, minutes, seconds = map(int, parts)
        return sign * timedelta(hours=hours, minutes=minutes, seconds=seconds)

    # short format: "1d 2h 30m"
    days = hours = minutes = 0
    for token in text.split():
        if token.endswith("d"):
            days = int(token[:-1])
        elif token.endswith("h"):
            hours = int(token[:-1])
        elif token.endswith("m"):
            minutes = int(token[:-1])
    return sign * timedelta(days=days, hours=hours, minutes=minutes)


# Register transforms
format_date_transform = Transform(format_date)
format_time_transform = Transform(format_time)
format_datetime_transform = Transform(format_datetime)
parse_date_transform = Transform(parse_date)
parse_time_transform = Transform(parse_time)
parse_datetime_transform = Transform(parse_datetime)
to_iso_transform = Transform(to_iso)
from_iso_transform = Transform(from_iso)
format_timedelta_transform = Transform(format_timedelta)
parse_timedelta_transform = Transform(parse_timedelta)
