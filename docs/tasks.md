# Task Tracker

This repository includes a small JSON-backed task tracker.

## Library Usage

```python
from tasks import TaskList

tasks = TaskList("tasks.json")
task = tasks.add("write documentation")
tasks.complete(task["id"])

print(tasks.list_pending())
print(tasks.list_done())
```

`TaskList` stores tasks as JSON and writes changes atomically by writing a
temporary file in the same directory, flushing it, and renaming it into place.
If the JSON file is missing or corrupt, the list starts empty.

## CLI Usage

The CLI stores tasks in `~/.tasks.json` by default. Use `--file` to choose a
different file.

```sh
python taskcli.py --file tasks.json add "write tests"
python taskcli.py --file tasks.json ls
python taskcli.py --file tasks.json done 1
python taskcli.py --file tasks.json ls --done
python taskcli.py --file tasks.json rm 1
```

Examples:

```text
$ python taskcli.py --file tasks.json add "write tests"
Added task 1: write tests

$ python taskcli.py --file tasks.json ls
1	pending	write tests

$ python taskcli.py --file tasks.json done 1
Completed task 1: write tests
```
