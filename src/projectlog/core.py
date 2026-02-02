from pathlib import Path
from datetime import datetime, date, timezone
import json
import uuid
import os

from projectlog.lint import validate_project_name
from projectlog.timeutils import normalize_day

DEFAULT_ROOT = os.environ.get(
    "PROJECTLOG_ROOT",
    os.path.expanduser("~/project_log/projects")
)


class ProjectLog:
    def __init__(self, root=DEFAULT_ROOT):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, project):
        return self.root / f"{project}.json"

    def load(self, project):
        path = self._path(project)
        if not path.exists():
            return []

        with open(path) as f:
            data = json.load(f)

        return data["events"]

    def append(
        self,
        project,
        decision_type,
        notes,
        dataset_ids=None,
        output_dirs=None,
        wip=None,
        deadlines=None,
        tags=None,
        day=None,
    ):
        validate_project_name(project)

        path = self._path(project)

        if path.exists():
            with open(path) as f:
                data = json.load(f)
        else:
            data = {
                "project_metadata": {
                    "project": project,
                    "pi": project.split("_", 1)[0],
                    "created": date.today().isoformat(),
                },
                "events": [],
            }

        event = {
            "event_id": str(uuid.uuid4()),
            "project": project,
            "day": normalize_day(day),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "decision_type": decision_type,
            "notes": notes,
            "dataset_ids": dataset_ids or [],
            "output_dirs": output_dirs or [],
            "wip": wip or [],
            "deadlines": deadlines or [],
            "tags": tags or [],
        }

        data["events"].append(event)

        with open(path, "w") as f:
            json.dump(data, f, indent=2)

        return event
