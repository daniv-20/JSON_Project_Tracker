import json
from jsonschema import validate
from projectlog.core import ProjectLog
from pathlib import Path


def test_event_conforms_to_schema(tmp_path):
    log = ProjectLog(root=tmp_path)
    event = log.append(
        project="Smith_TestProject_2024",
        decision_type="note",
        notes="Schema test"
    )

    schema_path = Path(__file__).parents[1] / "src/projectlog/schema.json"
    with open(schema_path) as f:
        schema = json.load(f)

    validate(instance=event, schema=schema)
