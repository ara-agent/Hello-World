import json

import pytest

from tasks import TaskList


def test_add_lists_pending_and_persists(tmp_path):
    path = tmp_path / "tasks.json"
    tasks = TaskList(path)

    first = tasks.add("write tests")
    second = tasks.add("ship change")

    assert first == {"id": 1, "title": "write tests", "done": False}
    assert second == {"id": 2, "title": "ship change", "done": False}
    assert tasks.list_pending() == [first, second]
    assert TaskList(path).list_pending() == [first, second]


def test_complete_moves_task_to_done(tmp_path):
    tasks = TaskList(tmp_path / "tasks.json")
    task = tasks.add("document cli")

    completed = tasks.complete(task["id"])

    assert completed == {"id": 1, "title": "document cli", "done": True}
    assert tasks.list_pending() == []
    assert tasks.list_done() == [completed]


def test_remove_by_id(tmp_path):
    tasks = TaskList(tmp_path / "tasks.json")
    keep = tasks.add("keep")
    remove = tasks.add("remove")

    assert tasks.remove(remove["id"]) == remove
    assert TaskList(tmp_path / "tasks.json").list_pending() == [keep]


def test_missing_task_raises_key_error(tmp_path):
    tasks = TaskList(tmp_path / "tasks.json")

    with pytest.raises(KeyError, match="task id 99 not found"):
        tasks.complete(99)

    with pytest.raises(KeyError, match="task id 99 not found"):
        tasks.remove(99)


def test_empty_title_rejected(tmp_path):
    tasks = TaskList(tmp_path / "tasks.json")

    with pytest.raises(ValueError, match="task title cannot be empty"):
        tasks.add("   ")


def test_corrupt_file_recovers_and_overwrites_on_save(tmp_path):
    path = tmp_path / "tasks.json"
    path.write_text("{bad json", encoding="utf-8")
    tasks = TaskList(path)

    assert tasks.list_pending() == []
    added = tasks.add("recovered")

    assert added["id"] == 1
    assert json.loads(path.read_text(encoding="utf-8")) == [added]
