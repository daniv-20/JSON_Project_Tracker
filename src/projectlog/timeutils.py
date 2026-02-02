from datetime import datetime, timezone, date


def parse_iso_date(ts):
    """
    Normalize a timestamp to a timezone-aware UTC datetime.

    Accepts:
    - ISO-8601 string
    - datetime (naive or aware)

    Returns:
    - timezone-aware datetime in UTC
    """
    if isinstance(ts, datetime):
        dt = ts
    elif isinstance(ts, str):
        dt = datetime.fromisoformat(ts)
    else:
        raise TypeError(f"Unsupported timestamp type: {type(ts)}")

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    return dt


def normalize_day(day):
    """
    Normalize a user-supplied date string to ISO YYYY-MM-DD.
    Accepts YYYY-MM-DD, YYYY-M-D, MM/DD/YYYY.
    """
    if day is None:
        return date.today().isoformat()

    # Flexible ISO-like input
    for fmt in ("%Y-%m-%d", "%Y-%m-%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(day, fmt).date().isoformat()
        except ValueError:
            continue

    raise ValueError(
        f"Invalid date '{day}'. Expected YYYY-MM-DD or MM/DD/YYYY."
    )