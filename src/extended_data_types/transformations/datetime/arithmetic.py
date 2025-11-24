"""Datetime arithmetic operations aligned to legacy behavior."""

from __future__ import annotations

import calendar
import math
from datetime import date, datetime, time, timedelta, tzinfo
from typing import Literal
from zoneinfo import ZoneInfo

from extended_data_types.transformations.core import Transform

TimeRule = Literal["nearest", "up", "down"]
RoundUnit = Literal["hour", "minute", "15min", "day"]
TimeBetweenUnit = Literal["days", "hours", "minutes", "seconds", "microseconds"]


def _validate_units(kwargs: dict[str, int | float]) -> None:
    allowed = {"years", "months", "weeks", "days", "hours", "minutes"}
    invalid = set(kwargs) - allowed
    if invalid:
        raise ValueError(f"Invalid units: {', '.join(sorted(invalid))}")


def _shift_months(base: date, years: int, months: int) -> date:
    """Adjust year/month while clamping day to month length."""
    total_months = base.year * 12 + (base.month - 1) + years * 12 + months
    new_year, new_month_index = divmod(total_months, 12)
    new_month = new_month_index + 1
    last_day = calendar.monthrange(new_year, new_month)[1]
    return date(new_year, new_month, min(base.day, last_day))


def _combine_datetime(dt: datetime, delta: timedelta) -> datetime:
    return dt + delta


def _apply_timedelta(dt: date | datetime | time, delta: timedelta) -> date | datetime | time:
    if isinstance(dt, datetime):
        return dt + delta
    if isinstance(dt, date):
        return dt + delta
    anchor = datetime.combine(date(1970, 1, 1), dt)
    result = anchor + delta
    return result.timetz() if dt.tzinfo else result.time()


def add_time(dt: date | datetime | time, **units: int | float) -> date | datetime | time:
    """Add time units to date, datetime, or time."""
    _validate_units(units)
    years = int(units.get("years", 0))
    months = int(units.get("months", 0))
    weeks = units.get("weeks", 0) or 0
    days = units.get("days", 0) or 0
    hours = units.get("hours", 0) or 0
    minutes = units.get("minutes", 0) or 0

    if isinstance(dt, (date, datetime)):
        base_date = dt if isinstance(dt, date) else dt.date()
        if years or months:
            base_date = _shift_months(base_date, years, months)
        delta = timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes)
        if isinstance(dt, datetime):
            combined = datetime.combine(base_date, dt.timetz() if dt.tzinfo else dt.time())
            return combined + delta
        return base_date + delta

    # time only supports delta-based math; convert weeks/days to hours
    total_delta = timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes)
    anchor = datetime.combine(date(1970, 1, 1), dt)
    result = anchor + total_delta
    return result.timetz() if dt.tzinfo else result.time()


def subtract_time(dt: date | datetime | time, **units: int | float) -> date | datetime | time:
    """Subtract time units from date, datetime, or time."""
    _validate_units(units)
    return add_time(
        dt,
        years=-int(units.get("years", 0)),
        months=-int(units.get("months", 0)),
        weeks=-(units.get("weeks", 0) or 0),
        days=-(units.get("days", 0) or 0),
        hours=-(units.get("hours", 0) or 0),
        minutes=-(units.get("minutes", 0) or 0),
    )


def multiply_time(delta: timedelta, factor: int | float) -> timedelta:
    """Multiply timedelta by a factor."""
    if isinstance(factor, float) and factor < 0:
        raise ValueError("Negative fractional multipliers are not supported")
    return delta * factor


def divide_time(delta: timedelta, divisor: int | float | timedelta) -> float | timedelta:
    """Divide timedelta by a scalar or another timedelta."""
    if divisor == 0:
        raise ValueError("Division by zero")
    if isinstance(divisor, (int, float)) and divisor < 0:
        raise ValueError("Divisor must be positive")
    if isinstance(divisor, timedelta):
        return delta / divisor
    return delta / divisor


def time_between(start: date | datetime, end: date | datetime, unit: TimeBetweenUnit = "days") -> float:
    """Calculate the difference between two dates/datetimes."""
    delta = end - start
    conversions = {
        "days": delta.days + delta.seconds / 86400,
        "hours": delta.total_seconds() / 3600,
        "minutes": delta.total_seconds() / 60,
        "seconds": delta.total_seconds(),
        "microseconds": delta.total_seconds() * 1_000_000,
    }
    if unit not in conversions:
        raise ValueError(f"Unsupported unit: {unit}")
    return conversions[unit]


def _normalize_dt(dt: date | datetime | time) -> tuple[datetime, bool]:
    """Return datetime plus flag indicating original was time."""
    if isinstance(dt, datetime):
        return dt, False
    if isinstance(dt, time):
        anchor = datetime.combine(date(1970, 1, 1), dt)
        return anchor, True
    # date
    return datetime.combine(dt, time()), False


def _round_base(dt: datetime, unit_seconds: int, rule: TimeRule) -> datetime:
    total_seconds = (
        dt.hour * 3600 + dt.minute * 60 + dt.second + dt.microsecond / 1_000_000
    )
    if rule == "up":
        target = math.ceil(total_seconds / unit_seconds) * unit_seconds
    elif rule == "down":
        target = math.floor(total_seconds / unit_seconds) * unit_seconds
    else:
        target = round(total_seconds / unit_seconds) * unit_seconds

    delta_seconds = target - total_seconds
    return dt + timedelta(seconds=delta_seconds)


def round_time(dt: date | datetime | time, unit: RoundUnit = "hour", rule: TimeRule = "nearest") -> date | datetime | time:
    """Round to the nearest/ceiling/floor unit."""
    unit_map = {"hour": 3600, "minute": 60, "15min": 900, "day": 86_400}
    if unit not in unit_map:
        raise ValueError(f"Unsupported round unit: {unit}")
    normalized, was_time = _normalize_dt(dt)
    rounded = _round_base(normalized, unit_map[unit], rule)
    if unit == "day":
        rounded = rounded.replace(hour=0, minute=0, second=0, microsecond=0)
    if was_time:
        return rounded.timetz() if isinstance(dt, time) and dt.tzinfo else rounded.time()
    if isinstance(dt, date) and not isinstance(dt, datetime):
        return rounded.date()
    return rounded


def floor_time(dt: date | datetime | time, unit: RoundUnit = "hour") -> date | datetime | time:
    """Floor to the given unit."""
    return round_time(dt, unit, rule="down")


def ceil_time(dt: date | datetime | time, unit: RoundUnit = "hour") -> date | datetime | time:
    """Ceil to the given unit."""
    return round_time(dt, unit, rule="up")


def shift_timezone(dt: datetime, timezone: tzinfo | str, keep_local: bool = False) -> datetime:
    """Shift datetime to a different timezone."""
    if isinstance(timezone, str):
        timezone = ZoneInfo(timezone)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone)
    return dt.replace(tzinfo=timezone) if keep_local else dt.astimezone(timezone)


# Register transforms
add_time_transform = Transform(add_time)
subtract_time_transform = Transform(subtract_time)
multiply_time_transform = Transform(multiply_time)
divide_time_transform = Transform(divide_time)
round_time_transform = Transform(round_time)
floor_time_transform = Transform(floor_time)
ceil_time_transform = Transform(ceil_time)
shift_timezone_transform = Transform(shift_timezone)
time_between_transform = Transform(time_between)
