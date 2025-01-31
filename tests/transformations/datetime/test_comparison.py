"""Tests for datetime comparison operations."""

from __future__ import annotations

from datetime import date, datetime, time, timedelta

import pytest

from extended_data_types.transformations.datetime.comparison import (
    compare_dates,
    find_earliest,
    find_latest,
    get_overlap,
    is_between,
    is_business_day,
    is_weekend,
)


def test_compare_dates() -> None:
    """Test date comparison."""
    dt1 = datetime(2024, 1, 15, 14, 30)
    dt2 = datetime(2024, 1, 15, 15, 30)
    dt3 = datetime(2024, 1, 16, 14, 30)

    # Test basic comparison
    assert compare_dates(dt1, dt2) == -1  # dt1 < dt2
    assert compare_dates(dt2, dt1) == 1  # dt2 > dt1
    assert compare_dates(dt1, dt1) == 0  # dt1 == dt1

    # Test with different units
    assert compare_dates(dt1, dt2, unit="day") == 0  # Same day
    assert compare_dates(dt1, dt3, unit="day") == -1  # Different days

    # Test with date objects
    d1 = date(2024, 1, 15)
    d2 = date(2024, 1, 16)
    assert compare_dates(d1, d2) == -1

    # Test with time objects
    t1 = time(14, 30)
    t2 = time(15, 30)
    assert compare_dates(t1, t2) == -1

    # Test with mixed types
    assert compare_dates(dt1, d1, unit="day") == 0

    # Test invalid unit
    with pytest.raises(ValueError):
        compare_dates(dt1, dt2, unit="invalid")


def test_find_earliest() -> None:
    """Test finding earliest date."""
    dt1 = datetime(2024, 1, 15, 14, 30)
    dt2 = datetime(2024, 1, 15, 15, 30)
    dt3 = datetime(2024, 1, 16, 14, 30)

    # Test basic functionality
    assert find_earliest([dt1, dt2, dt3]) == dt1
    assert find_earliest([dt3, dt2, dt1]) == dt1

    # Test with different types
    d1 = date(2024, 1, 15)
    d2 = date(2024, 1, 16)
    assert find_earliest([d1, d2]) == d1

    # Test with single item
    assert find_earliest([dt1]) == dt1

    # Test with empty list
    with pytest.raises(ValueError):
        find_earliest([])


def test_find_latest() -> None:
    """Test finding latest date."""
    dt1 = datetime(2024, 1, 15, 14, 30)
    dt2 = datetime(2024, 1, 15, 15, 30)
    dt3 = datetime(2024, 1, 16, 14, 30)

    # Test basic functionality
    assert find_latest([dt1, dt2, dt3]) == dt3
    assert find_latest([dt3, dt2, dt1]) == dt3

    # Test with different types
    d1 = date(2024, 1, 15)
    d2 = date(2024, 1, 16)
    assert find_latest([d1, d2]) == d2

    # Test with single item
    assert find_latest([dt1]) == dt1

    # Test with empty list
    with pytest.raises(ValueError):
        find_latest([])


def test_is_between() -> None:
    """Test date range checking."""
    dt = datetime(2024, 1, 15, 14, 30)
    start = datetime(2024, 1, 15, 14, 0)
    end = datetime(2024, 1, 15, 15, 0)

    # Test basic range checking
    assert is_between(dt, start, end) is True
    assert is_between(start, start, end) is True  # Inclusive by default
    assert is_between(end, start, end) is True

    # Test exclusive boundaries
    assert is_between(start, start, end, inclusive=False) is False
    assert is_between(end, start, end, inclusive=False) is False

    # Test with different types
    d = date(2024, 1, 15)
    d_start = date(2024, 1, 14)
    d_end = date(2024, 1, 16)
    assert is_between(d, d_start, d_end) is True

    # Test out of range
    assert is_between(dt, end, end + timedelta(hours=1)) is False


def test_is_weekend() -> None:
    """Test weekend checking."""
    # Test weekdays
    monday = date(2024, 1, 15)
    friday = date(2024, 1, 19)
    assert is_weekend(monday) is False
    assert is_weekend(friday) is False

    # Test weekend
    saturday = date(2024, 1, 20)
    sunday = date(2024, 1, 21)
    assert is_weekend(saturday) is True
    assert is_weekend(sunday) is True

    # Test with datetime
    dt = datetime(2024, 1, 20, 14, 30)  # Saturday
    assert is_weekend(dt) is True


def test_is_business_day() -> None:
    """Test business day checking."""
    # Test regular weekdays
    monday = date(2024, 1, 15)
    friday = date(2024, 1, 19)
    assert is_business_day(monday) is True
    assert is_business_day(friday) is True

    # Test weekends
    saturday = date(2024, 1, 20)
    sunday = date(2024, 1, 21)
    assert is_business_day(saturday) is False
    assert is_business_day(sunday) is False

    # Test holidays (example)
    new_years = date(2024, 1, 1)
    assert is_business_day(new_years, holidays=["2024-01-01"]) is False

    # Test with custom weekend definition
    assert (
        is_business_day(friday, weekend_days=[4, 5]) is False
    )  # Friday is now weekend


def test_get_overlap() -> None:
    """Test date range overlap."""
    range1 = (datetime(2024, 1, 15), datetime(2024, 1, 20))
    range2 = (datetime(2024, 1, 18), datetime(2024, 1, 25))

    # Test basic overlap
    overlap = get_overlap(range1, range2)
    assert overlap == (datetime(2024, 1, 18), datetime(2024, 1, 20))

    # Test no overlap
    range3 = (datetime(2024, 1, 21), datetime(2024, 1, 25))
    assert get_overlap(range1, range3) is None

    # Test exact same range
    assert get_overlap(range1, range1) == range1

    # Test one range inside another
    range4 = (datetime(2024, 1, 16), datetime(2024, 1, 19))
    assert get_overlap(range1, range4) == range4

    # Test invalid ranges
    with pytest.raises(ValueError):
        get_overlap((range1[1], range1[0]), range2)  # End before start
