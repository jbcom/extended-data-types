"""Datetime arithmetic operations."""

from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone, tzinfo
from typing import Literal, TypeVar, Union, overload
from zoneinfo import ZoneInfo

from ..core import Transform

DT = TypeVar('DT', date, datetime)
TimeUnit = Literal["days", "hours", "minutes", "seconds", "microseconds"]
RoundTo = Literal["hour", "minute", "second"]


def add_time(
    dt: DT,
    value: int | float | timedelta,
    unit: TimeUnit | None = None
) -> DT:
    """Add time to date/datetime.
    
    Args:
        dt: Date/datetime to modify
        value: Amount to add
        unit: Time unit (required if value is number)
        
    Returns:
        Modified date/datetime
        
    Example:
        >>> add_time(date(2024, 1, 1), 5, "days")
        datetime.date(2024, 1, 6)
        >>> add_time(datetime.now(), timedelta(hours=2))
        datetime.datetime(...)
    """
    if isinstance(value, (int, float)):
        if unit is None:
            raise ValueError("Unit required for numeric value")
        delta = timedelta(**{unit: value})
    else:
        delta = value
    return dt + delta


def subtract_time(
    dt: DT,
    value: int | float | timedelta,
    unit: TimeUnit | None = None
) -> DT:
    """Subtract time from date/datetime.
    
    Args:
        dt: Date/datetime to modify
        value: Amount to subtract
        unit: Time unit (required if value is number)
        
    Returns:
        Modified date/datetime
        
    Example:
        >>> subtract_time(date(2024, 1, 1), 5, "days")
        datetime.date(2023, 12, 27)
    """
    if isinstance(value, (int, float)):
        if unit is None:
            raise ValueError("Unit required for numeric value")
        delta = timedelta(**{unit: value})
    else:
        delta = value
    return dt - delta


def time_between(
    start: DT,
    end: DT,
    unit: TimeUnit = "days"
) -> float:
    """Calculate time between two dates/datetimes.
    
    Args:
        start: Start date/datetime
        end: End date/datetime
        unit: Time unit for result
        
    Returns:
        Time difference in specified unit
        
    Example:
        >>> time_between(date(2024, 1, 1), date(2024, 1, 6))
        5.0
    """
    delta = end - start
    
    conversions = {
        "days": 1,
        "hours": 24,
        "minutes": 24 * 60,
        "seconds": 24 * 60 * 60,
        "microseconds": 24 * 60 * 60 * 1_000_000
    }
    
    return delta.total_seconds() * conversions[unit] / conversions["seconds"]


def shift_timezone(
    dt: datetime,
    timezone: tzinfo | str,
    keep_local: bool = False
) -> datetime:
    """Shift datetime to different timezone.
    
    Args:
        dt: Datetime to shift
        timezone: Target timezone
        keep_local: Keep local time (vs converting)
        
    Returns:
        Datetime in new timezone
        
    Example:
        >>> dt = datetime.now(timezone.utc)
        >>> shift_timezone(dt, "US/Eastern")
        datetime.datetime(..., tzinfo=zoneinfo.ZoneInfo('US/Eastern'))
    """
    if isinstance(timezone, str):
        timezone = ZoneInfo(timezone)
        
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone)
        
    if keep_local:
        return dt.replace(tzinfo=timezone)
    return dt.astimezone(timezone)


def round_time(
    dt: datetime,
    round_to: RoundTo = "hour",
    mode: Literal["up", "down", "nearest"] = "nearest"
) -> datetime:
    """Round datetime to nearest unit.
    
    Args:
        dt: Datetime to round
        round_to: Unit to round to
        mode: Rounding mode
        
    Returns:
        Rounded datetime
        
    Example:
        >>> dt = datetime(2024, 1, 1, 13, 30)
        >>> round_time(dt, "hour")
        datetime.datetime(2024, 1, 1, 14, 0)
    """
    units = {
        "hour": {"minutes": 60, "seconds": 0, "microseconds": 0},
        "minute": {"seconds": 60, "microseconds": 0},
        "second": {"microseconds": 1_000_000}
    }
    
    # Get the target values
    values = units[round_to]
    first_unit = next(iter(values))
    unit_size = values[first_unit]
    
    # Get the value to round
    value = getattr(dt, first_unit)
    
    # Calculate rounded value
    if mode == "up":
        new_value = math.ceil(value / unit_size) * unit_size
    elif mode == "down":
        new_value = math.floor(value / unit_size) * unit_size
    else:  # nearest
        new_value = round(value / unit_size) * unit_size
    
    # Apply rounding
    delta = {first_unit: new_value - value}
    for unit, value in values.items():
        if unit != first_unit:
            delta[unit] = -getattr(dt, unit)
    
    return dt + timedelta(**delta)


# Register transforms
add_time_transform = Transform(add_time)
subtract_time_transform = Transform(subtract_time)
time_between_transform = Transform(time_between)
shift_timezone_transform = Transform(shift_timezone)
round_time_transform = Transform(round_time) 