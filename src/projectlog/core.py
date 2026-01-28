from pathlib import Path
from datetime import datetime, date
import json
import uuid
import os
from projectlog.lint import validate_project_name


DEFAULT_ROOT = os.environ.get(
    "PROJECTLOG_ROOT",
    os.path.expanduser("~/project_log/projects")
)


class ProjectLog:
    def __init__(self, root="project_log/projects"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, project):
        return self.root / f"{project}.json"

    def load(self, project):
        path = self._path(project)
        if not path.exists():
            return []
        with open(path) as f:
            return json.load(f)

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

        events = self.load(project)

        event = {
            "event_id": str(uuid.uuid4()),
            "project": project,
            "day": day or date.today().isoformat(),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "decision_type": decision_type,
            "notes": notes,
            "dataset_ids": dataset_ids or [],
            "output_dirs": output_dirs or [],
            "wip": wip or [],
            "deadlines": deadlines or [],
            "tags": tags or [],
        }

        events.append(event)

        with open(self._path(project), "w") as f:
            json.dump(events, f, indent=2)

        return event
