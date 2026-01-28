from projectlog.queries import all_wip, datasets_by_project


def test_all_wip():
    events = [
        {"project": "A", "day": "2026-01-01", "wip": ["x"], "dataset_ids": [], "output_dirs": []}
    ]
    wip = all_wip(events)
    assert wip[0]["item"] == "x"


def test_datasets_by_project():
    events = [
        {"project": "A", "dataset_ids": ["d1"], "output_dirs": []},
        {"project": "A", "dataset_ids": ["d2"], "output_dirs": []}
    ]
    out = datasets_by_project(events)
    assert out["A"] == ["d1", "d2"]
