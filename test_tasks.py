import json
import tempfile
import unittest
from pathlib import Path

from tasks import TaskList


class TaskListTest(unittest.TestCase):
    def test_add_lists_pending_and_persists(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            tasks = TaskList(path)

            first = tasks.add("write tests")
            second = tasks.add("ship change")

            self.assertEqual(first, {"id": 1, "title": "write tests", "done": False})
            self.assertEqual(second, {"id": 2, "title": "ship change", "done": False})
            self.assertEqual(tasks.list_pending(), [first, second])
            self.assertEqual(TaskList(path).list_pending(), [first, second])

    def test_complete_moves_task_to_done(self):
        with tempfile.TemporaryDirectory() as directory:
            tasks = TaskList(Path(directory) / "tasks.json")
            task = tasks.add("document cli")

            completed = tasks.complete(task["id"])

            self.assertEqual(completed, {"id": 1, "title": "document cli", "done": True})
            self.assertEqual(tasks.list_pending(), [])
            self.assertEqual(tasks.list_done(), [completed])

    def test_remove_by_id(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            tasks = TaskList(path)
            keep = tasks.add("keep")
            remove = tasks.add("remove")

            self.assertEqual(tasks.remove(remove["id"]), remove)
            self.assertEqual(TaskList(path).list_pending(), [keep])

    def test_missing_task_raises_key_error(self):
        with tempfile.TemporaryDirectory() as directory:
            tasks = TaskList(Path(directory) / "tasks.json")

            with self.assertRaisesRegex(KeyError, "task id 99 not found"):
                tasks.complete(99)

            with self.assertRaisesRegex(KeyError, "task id 99 not found"):
                tasks.remove(99)

    def test_empty_title_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            tasks = TaskList(Path(directory) / "tasks.json")

            with self.assertRaisesRegex(ValueError, "task title cannot be empty"):
                tasks.add("   ")

    def test_corrupt_file_recovers_and_overwrites_on_save(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            path.write_text("{bad json", encoding="utf-8")
            tasks = TaskList(path)

            self.assertEqual(tasks.list_pending(), [])
            added = tasks.add("recovered")

            self.assertEqual(added["id"], 1)
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), [added])


if __name__ == "__main__":
    unittest.main()
