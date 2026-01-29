from pathlib import Path
import json
from projectlog.timeutils import parse_iso_date, cutoff_days
from datetime import date

from datetime import date


def events_in_date_range(events, start_date=None, end_date=None):
    """
    Return events whose `day` falls within the given date range (inclusive).

    Parameters
    ----------
    events : list[dict]
        List of event records.
    start_date : str | None
        ISO date string (YYYY-MM-DD). If None, no lower bound.
    end_date : str | None
        ISO date string (YYYY-MM-DD). If None, no upper bound.

    Returns
    -------
    list[dict]
        Events within the specified date range.
    """
    def to_date(d):
        return date.fromisoformat(d)

    start = to_date(start_date) if start_date else None
    end = to_date(end_date) if end_date else None

    out = []
    for e in events:
        event_day = to_date(e["day"])

        if start and event_day < start:
            continue
        if end and event_day > end:
            continue

        out.append(e)

    return out



def load_all(root, since_days=90):
    events = []
    cutoff = cutoff_days(since_days) if since_days else None

    for path in Path(root).glob("*.json"):
        with open(path) as f:
            for e in json.load(f):
                if cutoff:
                    event_time = parse_iso_date(e["timestamp"])
                    if event_time < cutoff:
                        continue
                events.append(e)

    return events


def all_wip(events, since_days=14):
    cutoff = cutoff_days(since_days)

    out = []
    for e in events:
        event_time = parse_iso_date(e["timestamp"])
        if event_time < cutoff:
            continue

        for item in e.get("wip", []):
            out.append({
                "project": e["project"],
                "day": e["day"],
                "timestamp": e["timestamp"],
                "item": item,
            })
    return out



def datasets_by_project(events):
    out = {}
    for e in events:
        for ds in e.get("dataset_ids", []):
            out.setdefault(e["project"], set()).add(ds)
    return {k: sorted(v) for k, v in out.items()}


def outputs_by_project(events):
    out = {}
    for e in events:
        for p in e.get("output_dirs", []):
            out.setdefault(e["project"], set()).add(p)
    return {k: sorted(v) for k, v in out.items()}


def last_event_by_project(events):
    out = {}
    for e in events:
        proj = e["project"]
        if proj not in out or e["timestamp"] > out[proj]["timestamp"]:
            out[proj] = e
    return out

