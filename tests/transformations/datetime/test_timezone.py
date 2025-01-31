"""Tests for timezone operations."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from extended_data_types.transformations.datetime.timezone import (
    convert_timezone,
    get_current_timezone,
    get_timezone_offset,
    is_dst,
    list_timezones,
    set_timezone,
)


def test_convert_timezone() -> None:
    """Test timezone conversion."""
    dt = datetime(2024, 1, 15, 14, 30)

    # Test basic conversion
    utc = convert_timezone(dt, "UTC")
    est = convert_timezone(dt, "US/Eastern")
    pst = convert_timezone(dt, "US/Pacific")

    # Verify offset differences
    assert (est.hour - pst.hour) == 3  # 3 hours difference between EST and PST

    # Test conversion with string input
    dt_str = "2024-01-15 14:30:00"
    converted = convert_timezone(dt_str, "UTC", "US/Pacific")
    assert isinstance(converted, datetime)

    # Test conversion with explicit source timezone
    result = convert_timezone(dt, "US/Eastern", "US/Pacific")
    assert result.hour == (dt.hour - 3)  # 3 hours behind

    # Test with UTC offset timezones
    utc_plus_1 = timezone(timedelta(hours=1))
    result = convert_timezone(dt, utc_plus_1, "UTC")
    assert result.hour == (dt.hour - 1)

    # Test invalid timezones
    with pytest.raises(ValueError):
        convert_timezone(dt, "Invalid/Timezone")


def test_get_timezone_offset() -> None:
    """Test getting timezone offset."""
    dt = datetime(2024, 1, 15, 14, 30)

    # Test basic offsets
    assert get_timezone_offset("UTC") == timedelta(0)
    assert abs(get_timezone_offset("US/Eastern").total_seconds()) == 5 * 3600  # 5 hours

    # Test with datetime (to account for DST)
    est_offset = get_timezone_offset("US/Eastern", dt)
    pst_offset = get_timezone_offset("US/Pacific", dt)
    assert (est_offset - pst_offset).total_seconds() == 3 * 3600  # 3 hours difference

    # Test with string input
    offset = get_timezone_offset("UTC+2")
    assert offset.total_seconds() == 2 * 3600

    # Test invalid timezone
    with pytest.raises(ValueError):
        get_timezone_offset("Invalid/Timezone")


def test_list_timezones() -> None:
    """Test timezone listing."""
    # Test basic listing
    zones = list_timezones()
    assert isinstance(zones, list)
    assert "UTC" in zones
    assert "US/Eastern" in zones
    assert "US/Pacific" in zones

    # Test with region filter
    us_zones = list_timezones(region="US")
    assert all("US" in zone for zone in us_zones)

    # Test with offset filter
    plus_1_zones = list_timezones(offset=1)
    for zone in plus_1_zones:
        assert get_timezone_offset(zone).total_seconds() == 3600

    # Test with DST filter
    dst_zones = list_timezones(dst_only=True)
    assert all(is_dst(zone) for zone in dst_zones)


def test_is_dst() -> None:
    """Test DST checking."""
    # Test specific dates
    summer_dt = datetime(2024, 7, 15, 14, 30)
    winter_dt = datetime(2024, 1, 15, 14, 30)

    # US Eastern should be DST in summer, not in winter
    assert is_dst("US/Eastern", summer_dt) is True
    assert is_dst("US/Eastern", winter_dt) is False

    # UTC should never be DST
    assert is_dst("UTC", summer_dt) is False
    assert is_dst("UTC", winter_dt) is False

    # Test current time
    assert isinstance(is_dst("US/Eastern"), bool)

    # Test invalid timezone
    with pytest.raises(ValueError):
        is_dst("Invalid/Timezone")


def test_get_current_timezone() -> None:
    """Test getting current timezone."""
    # Test basic functionality
    tz = get_current_timezone()
    assert tz is not None
    assert isinstance(str(tz), str)

    # Test with name_only option
    tz_name = get_current_timezone(name_only=True)
    assert isinstance(tz_name, str)

    # Test with offset option
    offset = get_current_timezone(return_offset=True)
    assert isinstance(offset, timedelta)


def test_set_timezone() -> None:
    """Test setting timezone."""
    original_tz = get_current_timezone()

    try:
        # Test setting timezone by name
        set_timezone("UTC")
        assert str(get_current_timezone()) == "UTC"

        # Test setting timezone by timezone object
        utc_plus_1 = timezone(timedelta(hours=1))
        set_timezone(utc_plus_1)
        assert get_current_timezone().utcoffset(None) == timedelta(hours=1)

        # Test invalid timezone
        with pytest.raises(ValueError):
            set_timezone("Invalid/Timezone")

    finally:
        # Restore original timezone
        set_timezone(original_tz)
