from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from arayeshgah import config

TZ = ZoneInfo(config.TIMEZONE)


def utc_now_naive() -> datetime:
    """
    Current time zone utc -> naive timezone datetime
    """

    return datetime.now(timezone.utc).replace(tzinfo=None)


def aware_utc(dt: datetime) -> datetime:
    """
    Converts a naive UTC datetime into timezone-aware UTC datetime.
    If it is already aware, converts it to UTC.
    """

    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)

    return dt.astimezone(timezone.utc)


def local_now() -> datetime:
    """
    Current time into the configured local timezone.
    """

    return datetime.now(TZ)


def minutes_to_label(minutes: int) -> str:
    """
    Convert minutes from 00:00 to HH:MM
    """
    if minutes == 1440:
        return "24:00"

    hour = minutes // 60
    minute = minutes % 60

    return f"{hour:02d} {minute:02d}"


def format_local(dt_utc_naive: datetime) -> str:
    """
    Formats a naive UTC datetime from database into local human-readable time.
    """

    local_dt = aware_utc(dt_utc_naive).astimezone(TZ)
    return local_dt.strftime("%a %d %b %Y %H:%M")
