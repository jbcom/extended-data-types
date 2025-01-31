"""Tests for datetime formatting operations."""

from __future__ import annotations

from datetime import date, datetime, time, timedelta

import pytest

from extended_data_types.transformations.datetime.format import (
    format_date,
    format_datetime,
    format_time,
    format_timedelta,
    parse_date,
    parse_datetime,
    parse_time,
    parse_timedelta,
)


def test_format_date() -> None:
    """Test date formatting."""
    d = date(2024, 1, 15)

    # Test basic formatting
    assert format_date(d) == "2024-01-15"
    assert format_date(d, "short") == "01/15/24"
    assert format_date(d, "medium") == "Jan 15, 2024"
    assert format_date(d, "long") == "January 15, 2024"
    assert format_date(d, "full") == "Monday, January 15, 2024"

    # Test custom format
    assert format_date(d, format="%Y/%m/%d") == "2024/01/15"
    assert format_date(d, format="%B %d") == "January 15"

    # Test with locale
    assert format_date(d, locale="es") == "15/01/2024"
    assert format_date(d, "long", locale="es") == "15 de enero de 2024"

    # Test invalid format
    with pytest.raises(ValueError):
        format_date(d, "invalid")


def test_format_time() -> None:
    """Test time formatting."""
    t = time(14, 30, 45, 123456)

    # Test basic formatting
    assert format_time(t) == "14:30:45"
    assert format_time(t, "short") == "2:30 PM"
    assert format_time(t, "medium") == "2:30:45 PM"
    assert format_time(t, "long") == "2:30:45 PM UTC"

    # Test with microseconds
    assert format_time(t, microseconds=True) == "14:30:45.123456"

    # Test custom format
    assert format_time(t, format="%I:%M %p") == "02:30 PM"
    assert format_time(t, format="%H.%M") == "14.30"

    # Test with timezone
    assert format_time(t, timezone="US/Pacific") == "06:30:45"

    # Test invalid format
    with pytest.raises(ValueError):
        format_time(t, "invalid")


def test_format_datetime() -> None:
    """Test datetime formatting."""
    dt = datetime(2024, 1, 15, 14, 30, 45, 123456)

    # Test basic formatting
    assert format_datetime(dt) == "2024-01-15 14:30:45"
    assert format_datetime(dt, "short") == "1/15/24, 2:30 PM"
    assert format_datetime(dt, "medium") == "Jan 15, 2024, 2:30:45 PM"
    assert format_datetime(dt, "long") == "January 15, 2024 at 2:30:45 PM UTC"

    # Test custom format
    assert format_datetime(dt, format="%Y-%m-%d %H:%M") == "2024-01-15 14:30"

    # Test with timezone
    assert format_datetime(dt, timezone="US/Pacific").startswith("2024-01-15 06:30:45")

    # Test with locale
    assert format_datetime(dt, "long", locale="es") == "15 de enero de 2024, 14:30:45"

    # Test invalid format
    with pytest.raises(ValueError):
        format_datetime(dt, "invalid")


def test_format_timedelta() -> None:
    """Test timedelta formatting."""
    td = timedelta(days=1, hours=2, minutes=30, seconds=45)

    # Test basic formatting
    assert format_timedelta(td) == "1 day, 2:30:45"
    assert format_timedelta(td, "short") == "1d 2h 30m"
    assert format_timedelta(td, "medium") == "1 day, 2 hours, 30 minutes"
    assert format_timedelta(td, "long") == "1 day, 2 hours, 30 minutes, 45 seconds"

    # Test negative timedelta
    td_neg = -td
    assert format_timedelta(td_neg) == "-1 day, 2:30:45"

    # Test with different units
    td = timedelta(seconds=3665)  # 1h 1m 5s
    assert format_timedelta(td, units="hours") == "1.02 hours"
    assert format_timedelta(td, units="minutes") == "61.08 minutes"

    # Test invalid format
    with pytest.raises(ValueError):
        format_timedelta(td, "invalid")


def test_parse_date() -> None:
    """Test date parsing."""
    # Test basic parsing
    assert parse_date("2024-01-15") == date(2024, 1, 15)
    assert parse_date("01/15/2024") == date(2024, 1, 15)
    assert parse_date("15-Jan-2024") == date(2024, 1, 15)

    # Test custom format
    assert parse_date("2024/01/15", format="%Y/%m/%d") == date(2024, 1, 15)

    # Test with locale
    assert parse_date("15/01/2024", locale="es") == date(2024, 1, 15)

    # Test invalid dates
    with pytest.raises(ValueError):
        parse_date("invalid")
    with pytest.raises(ValueError):
        parse_date("2024-13-45")


def test_parse_time() -> None:
    """Test time parsing."""
    # Test basic parsing
    assert parse_time("14:30:45") == time(14, 30, 45)
    assert parse_time("2:30 PM") == time(14, 30)

    # Test with microseconds
    assert parse_time("14:30:45.123456") == time(14, 30, 45, 123456)

    # Test custom format
    assert parse_time("02:30 PM", format="%I:%M %p") == time(14, 30)

    # Test with timezone
    t = parse_time("14:30:45", timezone="US/Pacific")
    assert t.hour == 14

    # Test invalid times
    with pytest.raises(ValueError):
        parse_time("invalid")
    with pytest.raises(ValueError):
        parse_time("25:00:00")


def test_parse_datetime() -> None:
    """Test datetime parsing."""
    # Test basic parsing
    assert parse_datetime("2024-01-15 14:30:45") == datetime(2024, 1, 15, 14, 30, 45)
    assert parse_datetime("1/15/24, 2:30 PM") == datetime(2024, 1, 15, 14, 30)

    # Test custom format
    assert parse_datetime("2024-01-15 14:30", format="%Y-%m-%d %H:%M") == datetime(
        2024, 1, 15, 14, 30
    )

    # Test with timezone
    dt = parse_datetime("2024-01-15 14:30:45", timezone="US/Pacific")
    assert dt.hour == 14

    # Test invalid datetimes
    with pytest.raises(ValueError):
        parse_datetime("invalid")
    with pytest.raises(ValueError):
        parse_datetime("2024-13-45 25:00:00")


def test_parse_timedelta() -> None:
    """Test timedelta parsing."""
    # Test basic parsing
    assert parse_timedelta("1 day, 2:30:45") == timedelta(
        days=1, hours=2, minutes=30, seconds=45
    )
    assert parse_timedelta("1d 2h 30m") == timedelta(days=1, hours=2, minutes=30)

    # Test negative timedelta
    assert parse_timedelta("-1 day, 2:30:45") == -timedelta(
        days=1, hours=2, minutes=30, seconds=45
    )

    # Test with units
    assert parse_timedelta("1.5 hours") == timedelta(hours=1, minutes=30)
    assert parse_timedelta("90 minutes") == timedelta(hours=1, minutes=30)

    # Test invalid timedelta
    with pytest.raises(ValueError):
        parse_timedelta("invalid")
