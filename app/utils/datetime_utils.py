from datetime import datetime, timezone, timedelta
from typing import Optional

def get_utc_now() -> datetime:
    """Returns the current UTC timestamp with timezone awareness."""
    return datetime.now(timezone.utc)

def format_iso(dt: Optional[datetime]) -> Optional[str]:
    """Safely converts a datetime object to an ISO 8601 string format."""
    if not dt:
        return None
    return dt.isoformat()

def parse_iso(date_str: Optional[str]) -> Optional[datetime]:
    """Parses an ISO 8601 string into a datetime object."""
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except ValueError:
        return None

def calculate_time_window_start(minutes: int) -> datetime:
    """Calculates a timestamp looking back a specified number of minutes from now (for structuring/window checks)."""
    return get_utc_now() - timedelta(minutes=minutes)

def is_within_business_hours(dt: datetime, start_hour: int = 9, end_hour: int = 18) -> bool:
    """Checks whether a given timestamp falls within standard working hours (used for insider access rules)."""
    return start_hour <= dt.hour < end_hour