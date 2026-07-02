import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import taskcli


def run_cli(args):
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        code = taskcli.main(args)
    return code, stdout.getvalue(), stderr.getvalue()


class TaskCliTest(unittest.TestCase):
    def test_cli_add_and_list_pending(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"

            code, out, err = run_cli(["--file", str(path), "add", "write", "docs"])
            self.assertEqual(code, 0)
            self.assertEqual(out, "Added task 1: write docs\n")
            self.assertEqual(err, "")

            code, out, err = run_cli(["--file", str(path), "ls"])
            self.assertEqual(code, 0)
            self.assertEqual(out, "1\tpending\twrite docs\n")
            self.assertEqual(err, "")

    def test_cli_done_and_list_done(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            run_cli(["--file", str(path), "add", "write tests"])

            code, out, err = run_cli(["--file", str(path), "done", "1"])
            self.assertEqual(code, 0)
            self.assertEqual(out, "Completed task 1: write tests\n")
            self.assertEqual(err, "")

            code, out, err = run_cli(["--file", str(path), "ls", "--done"])
            self.assertEqual(code, 0)
            self.assertEqual(out, "1\tdone\twrite tests\n")
            self.assertEqual(err, "")

    def test_cli_remove(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"
            run_cli(["--file", str(path), "add", "temporary"])

            code, out, err = run_cli(["--file", str(path), "rm", "1"])
            self.assertEqual(code, 0)
            self.assertEqual(out, "Removed task 1: temporary\n")
            self.assertEqual(err, "")

            code, out, err = run_cli(["--file", str(path), "ls"])
            self.assertEqual(code, 0)
            self.assertEqual(out, "")
            self.assertEqual(err, "")

    def test_cli_missing_task_has_clear_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.json"

            code, out, err = run_cli(["--file", str(path), "done", "42"])

            self.assertEqual(code, 1)
            self.assertEqual(out, "")
            self.assertEqual(err, "error: task id 42 not found\n")

    def test_cli_requires_subcommand(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with self.assertRaises(SystemExit) as excinfo:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                taskcli.main([])

        self.assertEqual(excinfo.exception.code, 2)
        self.assertIn("the following arguments are required: command", stderr.getvalue())
        self.assertEqual(stdout.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
