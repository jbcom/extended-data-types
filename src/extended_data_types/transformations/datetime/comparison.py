"""Datetime comparison helpers (test-aligned)."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import date, datetime, time
from typing import Literal

from extended_data_types.transformations.datetime.arithmetic import round_time


CompareUnit = Literal["second", "minute", "hour", "day"]


def _normalize(value: date | datetime | time) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime.combine(value, time())
    return datetime.combine(date.today(), value)


def compare_dates(
    a: date | datetime | time, b: date | datetime | time, unit: CompareUnit = "second"
) -> int:
    """Compare two date/time values with optional unit granularity."""
    if unit not in {"second", "minute", "hour", "day"}:
        raise ValueError(f"Unsupported unit: {unit}")
    dt1, dt2 = _normalize(a), _normalize(b)
    if unit in {"minute", "hour", "day"}:
        # use rounding down to the unit boundary
        truncate_to = {"minute": "minute", "hour": "hour", "day": "day"}[unit]  # type: ignore[index]
        dt1 = round_time(dt1, truncate_to, rule="down")  # type: ignore[arg-type]
        dt2 = round_time(dt2, truncate_to, rule="down")  # type: ignore[arg-type]
    if dt1 < dt2:
        return -1
    if dt1 > dt2:
        return 1
    return 0


def find_earliest(items: Iterable[date | datetime | time]) -> date | datetime | time:
    """Return the earliest value."""
    values = list(items)
    if not values:
        raise ValueError("No dates provided")
    return min(values, key=_normalize)


def find_latest(items: Iterable[date | datetime | time]) -> date | datetime | time:
    """Return the latest value."""
    values = list(items)
    if not values:
        raise ValueError("No dates provided")
    return max(values, key=_normalize)


def is_between(
    value: date | datetime | time,
    start: date | datetime | time,
    end: date | datetime | time,
    *,
    inclusive: bool = True,
) -> bool:
    """Check if value lies within [start, end]."""
    v, s, e = _normalize(value), _normalize(start), _normalize(end)
    if inclusive:
        return s <= v <= e
    return s < v < e


def is_weekend(value: date | datetime | time) -> bool:
    """Return True for Saturday/Sunday."""
    return _normalize(value).weekday() >= 5


def is_business_day(
    value: date | datetime | time,
    *,
    weekend_days: list[int] | None = None,
    holidays: list[str] | None = None,
) -> bool:
    """Return True for weekdays excluding holidays."""
    dt = _normalize(value)
    weekend = weekend_days or [5, 6]
    if dt.weekday() in weekend:
        return False
    if holidays:
        return dt.date().isoformat() not in set(holidays)
    return True


def get_overlap(
    range1: tuple[datetime, datetime],
    range2: tuple[datetime, datetime],
) -> tuple[datetime, datetime] | None:
    """Return overlapping range or None."""
    start1, end1 = range1
    start2, end2 = range2
    if start1 > end1 or start2 > end2:
        raise ValueError("Range start must be before end")
    start = max(start1, start2)
    end = min(end1, end2)
    return (start, end) if start <= end else None
