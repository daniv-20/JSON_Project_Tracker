from pathlib import Path
import json


def load_all(root):
    events = []
    for path in Path(root).glob("*.json"):
        with open(path) as f:
            events.extend(json.load(f))
    return events


def all_wip(events):
    return [
        {"project": e["project"], "day": e["day"], "item": item}
        for e in events
        for item in e.get("wip", [])
    ]


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
