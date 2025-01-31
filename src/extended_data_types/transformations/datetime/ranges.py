"""Datetime range operations."""

from __future__ import annotations

from collections.abc import Generator
from datetime import date, datetime, time, timedelta
from typing import Literal, TypeVar

from ..core import Transform


DT = TypeVar("DT", date, datetime)
Frequency = Literal["daily", "weekly", "monthly", "yearly"]


def date_range(
    start: date,
    end: date | None = None,
    periods: int | None = None,
    freq: Frequency | timedelta = "daily",
    inclusive: bool = True,
) -> Generator[date, None, None]:
    """Generate sequence of dates.

    Args:
        start: Start date
        end: End date (optional if periods given)
        periods: Number of periods (optional if end given)
        freq: Frequency of dates
        inclusive: Include end date

    Yields:
        Sequence of dates

    Example:
        >>> list(date_range(date(2024, 1, 1), date(2024, 1, 5)))
        [date(2024, 1, 1), date(2024, 1, 2), date(2024, 1, 3),
         date(2024, 1, 4), date(2024, 1, 5)]
    """
    if isinstance(freq, str):
        freq_map = {
            "daily": timedelta(days=1),
            "weekly": timedelta(weeks=1),
            "monthly": timedelta(days=30),  # Approximate
            "yearly": timedelta(days=365),  # Approximate
        }
        delta = freq_map[freq]
    else:
        delta = freq

    if end is None and periods is None:
        raise ValueError("Must specify either end or periods")

    if end is None:
        end = start + delta * (periods - 1)
    elif periods is not None:
        delta = (end - start) / (periods - 1)

    current = start
    if inclusive:
        while current <= end:
            yield current
            current += delta
    else:
        while current < end:
            yield current
            current += delta


def time_range(
    start: time,
    end: time,
    step: timedelta = timedelta(minutes=1),
    inclusive: bool = True,
) -> Generator[time, None, None]:
    """Generate sequence of times.

    Args:
        start: Start time
        end: End time
        step: Time step
        inclusive: Include end time

    Yields:
        Sequence of times

    Example:
        >>> list(time_range(time(9, 0), time(9, 30),
        ...                timedelta(minutes=15)))
        [time(9, 0), time(9, 15), time(9, 30)]
    """
    # Convert times to datetime for arithmetic
    base_date = date(2000, 1, 1)
    start_dt = datetime.combine(base_date, start)
    end_dt = datetime.combine(base_date, end)

    if end_dt < start_dt:  # Handle overnight ranges
        end_dt += timedelta(days=1)

    current = start_dt
    if inclusive:
        while current <= end_dt:
            yield current.time()
            current += step
    else:
        while current < end_dt:
            yield current.time()
            current += step


def datetime_range(
    start: datetime,
    end: datetime | None = None,
    periods: int | None = None,
    freq: Frequency | timedelta = "daily",
    inclusive: bool = True,
) -> Generator[datetime, None, None]:
    """Generate sequence of datetimes.

    Args:
        start: Start datetime
        end: End datetime (optional if periods given)
        periods: Number of periods (optional if end given)
        freq: Frequency of datetimes
        inclusive: Include end datetime

    Yields:
        Sequence of datetimes

    Example:
        >>> list(datetime_range(datetime(2024, 1, 1, 9),
        ...                    datetime(2024, 1, 1, 17),
        ...                    freq=timedelta(hours=4)))
        [datetime(2024, 1, 1, 9), datetime(2024, 1, 1, 13),
         datetime(2024, 1, 1, 17)]
    """
    if isinstance(freq, str):
        freq_map = {
            "daily": timedelta(days=1),
            "weekly": timedelta(weeks=1),
            "monthly": timedelta(days=30),  # Approximate
            "yearly": timedelta(days=365),  # Approximate
        }
        delta = freq_map[freq]
    else:
        delta = freq

    if end is None and periods is None:
        raise ValueError("Must specify either end or periods")

    if end is None:
        end = start + delta * (periods - 1)
    elif periods is not None:
        delta = (end - start) / (periods - 1)

    current = start
    if inclusive:
        while current <= end:
            yield current
            current += delta
    else:
        while current < end:
            yield current
            current += delta


def is_between(dt: DT, start: DT, end: DT, inclusive: bool = True) -> bool:
    """Check if date/datetime is between start and end.

    Args:
        dt: Date/datetime to check
        start: Start date/datetime
        end: End date/datetime
        inclusive: Include start/end in range

    Returns:
        True if date/datetime is in range

    Example:
        >>> is_between(date(2024, 1, 15),
        ...           date(2024, 1, 1),
        ...           date(2024, 1, 31))
        True
    """
    if inclusive:
        return start <= dt <= end
    return start < dt < end


def overlap(range1: tuple[DT, DT], range2: tuple[DT, DT]) -> tuple[DT, DT] | None:
    """Find overlap between two date/datetime ranges.

    Args:
        range1: First (start, end) range
        range2: Second (start, end) range

    Returns:
        Overlapping range or None

    Example:
        >>> r1 = (date(2024, 1, 1), date(2024, 1, 31))
        >>> r2 = (date(2024, 1, 15), date(2024, 2, 15))
        >>> overlap(r1, r2)
        (date(2024, 1, 15), date(2024, 1, 31))
    """
    start1, end1 = range1
    start2, end2 = range2

    latest_start = max(start1, start2)
    earliest_end = min(end1, end2)

    if latest_start <= earliest_end:
        return (latest_start, earliest_end)
    return None


# Register transforms
date_range_transform = Transform(date_range)
time_range_transform = Transform(time_range)
datetime_range_transform = Transform(datetime_range)
is_between_transform = Transform(is_between)
overlap_transform = Transform(overlap)
