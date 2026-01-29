from datetime import datetime, timedelta, timezone


def parse_iso_date(date_str):
    return datetime.fromisoformat(date_str)


def cutoff_days(days):
    return datetime.now(timezone.utc) - timedelta(days=days)
