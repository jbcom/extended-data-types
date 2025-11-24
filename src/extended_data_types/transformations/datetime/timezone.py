"""Timezone helpers (compatibility)."""

from __future__ import annotations

import datetime as _dt

from collections.abc import Iterable
from datetime import timedelta, timezone
from zoneinfo import ZoneInfo


_current_timezone: timezone | ZoneInfo = (
    _dt.datetime.now().astimezone().tzinfo or timezone.utc
)


def _coerce_timezone(tz: str | timezone | ZoneInfo) -> timezone | ZoneInfo:
    """Convert user input into a timezone object."""
    if isinstance(tz, (timezone, ZoneInfo)):
        return tz
    if isinstance(tz, str):
        # Handle simple UTC offsets like "UTC+2"
        if tz.upper().startswith("UTC") and len(tz) > 3:
            try:
                hours = int(tz[3:])
                return timezone(timedelta(hours=hours))
            except Exception as exc:  # pragma: no cover - defensive
                raise ValueError(f"Invalid timezone offset {tz}") from exc
        try:
            return ZoneInfo(tz)
        except Exception as exc:
            raise ValueError(f"Unknown timezone {tz}") from exc
    raise ValueError(f"Unsupported timezone type: {type(tz)}")


def _parse_datetime(dt: _dt.datetime | str) -> _dt.datetime:
    if isinstance(dt, _dt.datetime):
        return dt
    try:
        return _dt.datetime.fromisoformat(dt)
    except Exception as exc:
        raise ValueError(f"Invalid datetime string {dt}") from exc


def ensure_timezone(
    dt: _dt.datetime, tz: str | timezone | ZoneInfo | None = None
) -> _dt.datetime:
    """Attach or convert timezone."""
    target = _coerce_timezone(tz) if tz else timezone.utc
    if dt.tzinfo is None:
        return dt.replace(tzinfo=target)
    return dt.astimezone(target)


def convert_timezone(
    dt: _dt.datetime | str,
    from_tz: str | timezone | ZoneInfo | None = None,
    to_tz: str | timezone | ZoneInfo | None = None,
) -> _dt.datetime:
    """Convert datetime between timezones."""
    if to_tz is None:
        to_tz = from_tz
        from_tz = None

    target_tz = _coerce_timezone(to_tz) if to_tz else timezone.utc
    source_dt = _parse_datetime(dt)

    if from_tz:
        source_tz = _coerce_timezone(from_tz)
        if source_dt.tzinfo is None:
            source_dt = source_dt.replace(tzinfo=source_tz)
        else:
            source_dt = source_dt.astimezone(source_tz)
    elif source_dt.tzinfo is None:
        source_dt = source_dt.replace(tzinfo=timezone.utc)

    return source_dt.astimezone(target_tz)


def get_current_timezone(name_only: bool = False, return_offset: bool = False):
    """Return the current module-level timezone."""
    tz = _current_timezone
    if return_offset:
        now = _dt.datetime.now(tz)
        return tz.utcoffset(now) or timedelta(0)
    if name_only:
        if isinstance(tz, ZoneInfo):
            return tz.key
        return str(tz)
    return tz


def get_timezone_offset(
    tz: str | timezone | ZoneInfo, dt: _dt.datetime | None = None
) -> timedelta:
    """Return offset as timedelta for a timezone."""
    target = _coerce_timezone(tz)
    probe = dt or _dt.datetime.now(target)
    offset = target.utcoffset(probe)
    if offset is None:
        raise ValueError(f"Could not determine offset for {tz}")
    return offset


def is_dst(tz: str | timezone | ZoneInfo, dt: _dt.datetime | None = None) -> bool:
    """Check if a timezone is currently observing DST."""
    target = _coerce_timezone(tz)
    probe = dt or _dt.datetime.now(target)
    delta = target.dst(probe) if hasattr(target, "dst") else None
    if delta is None:
        return False
    return delta != timedelta(0)


def list_timezones(
    region: str | None = None, offset: int | None = None, dst_only: bool = False
) -> list[str]:
    """Return available timezone keys with optional filters."""
    try:
        zones: Iterable[str] = ZoneInfo.available_timezones()
    except Exception:
        zones = ["UTC", "US/Eastern", "US/Pacific", "Europe/London"]
    if not zones:
        zones = ["UTC", "US/Eastern", "US/Pacific", "Europe/London"]

    def _match(zone: str) -> bool:
        if region and region not in zone:
            return False
        if offset is not None:
            try:
                if get_timezone_offset(zone).total_seconds() != offset * 3600:
                    return False
            except Exception:
                return False
        if dst_only:
            try:
                if not is_dst(zone):
                    return False
            except Exception:
                return False
        return True

    matched = sorted(zone for zone in zones if _match(zone))
    if (
        offset is None
        and not dst_only
        and (not region or region in "UTC")
        and "UTC" not in matched
    ):
        matched.append("UTC")
    return matched


def set_timezone(tz: str | timezone | ZoneInfo) -> None:
    """Set the module-level timezone used by helpers."""
    global _current_timezone
    _current_timezone = _coerce_timezone(tz)
