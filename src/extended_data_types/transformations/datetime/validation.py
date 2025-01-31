"""Datetime validation operations."""

from __future__ import annotations

import calendar

from datetime import date, datetime, time, timedelta
from typing import Literal, TypeVar

from ..core import Transform


DT = TypeVar("DT", date, datetime)
CompareResult = Literal["before", "after", "same"]


def is_valid_date(year: int, month: int, day: int) -> bool:
    """Check if date is valid.

    Args:
        year: Year value
        month: Month value
        day: Day value

    Returns:
        True if date is valid

    Example:
        >>> is_valid_date(2024, 2, 29)  # Leap year
        True
        >>> is_valid_date(2023, 2, 29)  # Not leap year
        False
    """
    try:
        date(year, month, day)
        return True
    except ValueError:
        return False


def is_valid_time(
    hour: int, minute: int, second: int = 0, microsecond: int = 0
) -> bool:
    """Check if time is valid.

    Args:
        hour: Hour value
        minute: Minute value
        second: Second value
        microsecond: Microsecond value

    Returns:
        True if time is valid

    Example:
        >>> is_valid_time(23, 59, 59)
        True
        >>> is_valid_time(24, 0, 0)
        False
    """
    try:
        time(hour, minute, second, microsecond)
        return True
    except ValueError:
        return False


def compare_dates(
    date1: DT, date2: DT, tolerance: timedelta | None = None
) -> CompareResult:
    """Compare two dates/datetimes.

    Args:
        date1: First date/datetime
        date2: Second date/datetime
        tolerance: Allowed difference for "same"

    Returns:
        Comparison result

    Example:
        >>> compare_dates(date(2024, 1, 1), date(2024, 1, 2))
        'before'
        >>> compare_dates(
        ...     datetime(2024, 1, 1, 12, 0),
        ...     datetime(2024, 1, 1, 12, 1),
        ...     tolerance=timedelta(minutes=5)
        ... )
        'same'
    """
    if tolerance is not None:
        if abs(date1 - date2) <= tolerance:
            return "same"
    elif date1 == date2:
        return "same"

    return "before" if date1 < date2 else "after"


def normalize_date(dt: DT, mode: Literal["start", "end", "workday"] = "start") -> DT:
    """Normalize date/datetime to specific point.

    Args:
        dt: Date/datetime to normalize
        mode: Normalization mode

    Returns:
        Normalized date/datetime

    Example:
        >>> normalize_date(datetime(2024, 1, 1, 12, 30), "start")
        datetime(2024, 1, 1, 0, 0)
        >>> normalize_date(datetime(2024, 1, 1, 12, 30), "end")
        datetime(2024, 1, 1, 23, 59, 59, 999999)
    """
    if isinstance(dt, datetime):
        if mode == "start":
            return dt.replace(hour=0, minute=0, second=0, microsecond=0)
        elif mode == "end":
            return dt.replace(hour=23, minute=59, second=59, microsecond=999999)
        else:  # workday
            if dt.hour < 9:
                return dt.replace(hour=9, minute=0, second=0, microsecond=0)
            elif dt.hour >= 17:
                return dt.replace(hour=17, minute=0, second=0, microsecond=0)
            return dt
    return dt


def is_weekend(dt: DT) -> bool:
    """Check if date/datetime is weekend.

    Args:
        dt: Date/datetime to check

    Returns:
        True if weekend

    Example:
        >>> is_weekend(date(2024, 1, 6))  # Saturday
        True
    """
    return dt.weekday() >= 5


def is_leap_year(year: int | DT) -> bool:
    """Check if year is leap year.

    Args:
        year: Year or date/datetime

    Returns:
        True if leap year

    Example:
        >>> is_leap_year(2024)
        True
        >>> is_leap_year(date(2023, 1, 1))
        False
    """
    if isinstance(year, (date, datetime)):
        year = year.year
    return calendar.isleap(year)


def days_in_month(year: int, month: int) -> int:
    """Get number of days in month.

    Args:
        year: Year value
        month: Month value

    Returns:
        Number of days

    Example:
        >>> days_in_month(2024, 2)  # Leap year February
        29
    """
    return calendar.monthrange(year, month)[1]


def age(birth_date: date, reference_date: date | None = None) -> int:
    """Calculate age from birth date.

    Args:
        birth_date: Date of birth
        reference_date: Reference date (default: today)

    Returns:
        Age in years

    Example:
        >>> age(date(2000, 1, 1), date(2024, 1, 1))
        24
    """
    if reference_date is None:
        reference_date = date.today()

    years = reference_date.year - birth_date.year

    # Adjust if birthday hasn't occurred this year
    if (reference_date.month, reference_date.day) < (birth_date.month, birth_date.day):
        years -= 1

    return years


# Register transforms
is_valid_date_transform = Transform(is_valid_date)
is_valid_time_transform = Transform(is_valid_time)
compare_dates_transform = Transform(compare_dates)
normalize_date_transform = Transform(normalize_date)
is_weekend_transform = Transform(is_weekend)
is_leap_year_transform = Transform(is_leap_year)
days_in_month_transform = Transform(days_in_month)
age_transform = Transform(age)
