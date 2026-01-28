from projectlog.core import ProjectLog
from pathlib import Path


def test_append_creates_event(tmp_path):
    log = ProjectLog(root=tmp_path)

    event = log.append(
        project="Smith_TestProject_2024",
        decision_type="analysis",
        notes="Did a thing",
        dataset_ids=["ds1"],
        output_dirs=["/tmp/out"]
    )

    assert event["project"] == "Smith_TestProject_2024"
    assert event["decision_type"] == "analysis"

    events = log.load("Smith_TestProject_2024")
    assert len(events) == 1
