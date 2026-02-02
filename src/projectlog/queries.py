from pathlib import Path
import json
from datetime import date, timedelta
import os

DEFAULT_ROOT = os.environ.get(
    "PROJECTLOG_ROOT",
    os.path.expanduser("~/project_log/projects")
)


# ---------------------------------------------------------------------
# Core loaders
# ---------------------------------------------------------------------

def load_all(root=DEFAULT_ROOT, projects=None, since_days=None):
    """
    Load events from project logs, optionally filtered by project
    and by recency based on event 'day'.

    Parameters
    ----------
    root : str or Path
        Root directory containing project JSON files.
    projects : str | list[str] | None
        Project name or names to load.
    since_days : int | None
        Only include events whose 'day' is within the last N days.

    Returns
    -------
    list[dict]
        Event records.
    """
    root = Path(root)

    if isinstance(projects, str):
        projects = {projects}
    elif projects is not None:
        projects = set(projects)

    cutoff_day = (
        date.today() - timedelta(days=since_days)
        if since_days is not None
        else None
    )

    events = []

    for path in root.glob("*.json"):
        project_name = path.stem

        if projects and project_name not in projects:
            continue

        with open(path) as f:
            data = json.load(f)

        for e in data["events"]:
            if cutoff_day:
                event_day = date.fromisoformat(e["day"])
                if event_day < cutoff_day:
                    continue

            events.append(e)

    return events


# ---------------------------------------------------------------------
# Time-based queries
# ---------------------------------------------------------------------

def events_in_date_range(events, start_date=None, end_date=None):
    """
    Return events whose 'day' falls within the given date range (inclusive).
    """
    start = date.fromisoformat(start_date) if start_date else None
    end = date.fromisoformat(end_date) if end_date else None

    out = []
    for e in events:
        event_day = date.fromisoformat(e["day"])

        if start and event_day < start:
            continue
        if end and event_day > end:
            continue

        out.append(e)

    return out


def all_wip(events, since_days=14):
    """
    Return WIP items from events whose 'day' is within the last N days.
    """
    cutoff_day = date.today() - timedelta(days=since_days)

    out = []
    for e in events:
        event_day = date.fromisoformat(e["day"])
        if event_day < cutoff_day:
            continue

        for item in e.get("wip", []):
            out.append({
                "project": e["project"],
                "day": e["day"],
                "timestamp": e["timestamp"],
                "item": item,
            })

    return out


# ---------------------------------------------------------------------
# Aggregations
# ---------------------------------------------------------------------

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


# ---------------------------------------------------------------------
# Last-activity logic
# ---------------------------------------------------------------------

def last_event_by_project(events):
    """
    Return the most recent event per project,
    ordered by (day, timestamp).
    """
    out = {}

    for e in events:
        proj = e["project"]

        key = (
            date.fromisoformat(e["day"]),
            e["timestamp"],
        )

        if proj not in out:
            out[proj] = e
        else:
            prev = out[proj]
            prev_key = (
                date.fromisoformat(prev["day"]),
                prev["timestamp"],
            )
            if key > prev_key:
                out[proj] = e

    return out
