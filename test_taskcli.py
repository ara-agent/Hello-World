import pytest

import taskcli


def run_cli(args, capsys):
    code = taskcli.main(args)
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def test_cli_add_and_list_pending(tmp_path, capsys):
    path = tmp_path / "tasks.json"

    code, out, err = run_cli(["--file", str(path), "add", "write", "docs"], capsys)
    assert code == 0
    assert out == "Added task 1: write docs\n"
    assert err == ""

    code, out, err = run_cli(["--file", str(path), "ls"], capsys)
    assert code == 0
    assert out == "1\tpending\twrite docs\n"
    assert err == ""


def test_cli_done_and_list_done(tmp_path, capsys):
    path = tmp_path / "tasks.json"
    taskcli.main(["--file", str(path), "add", "write tests"])
    capsys.readouterr()

    code, out, err = run_cli(["--file", str(path), "done", "1"], capsys)
    assert code == 0
    assert out == "Completed task 1: write tests\n"
    assert err == ""

    code, out, err = run_cli(["--file", str(path), "ls", "--done"], capsys)
    assert code == 0
    assert out == "1\tdone\twrite tests\n"
    assert err == ""


def test_cli_remove(tmp_path, capsys):
    path = tmp_path / "tasks.json"
    taskcli.main(["--file", str(path), "add", "temporary"])
    capsys.readouterr()

    code, out, err = run_cli(["--file", str(path), "rm", "1"], capsys)
    assert code == 0
    assert out == "Removed task 1: temporary\n"
    assert err == ""

    code, out, err = run_cli(["--file", str(path), "ls"], capsys)
    assert code == 0
    assert out == ""
    assert err == ""


def test_cli_missing_task_has_clear_error(tmp_path, capsys):
    path = tmp_path / "tasks.json"

    code, out, err = run_cli(["--file", str(path), "done", "42"], capsys)

    assert code == 1
    assert out == ""
    assert err == "error: 'task id 42 not found'\n"


def test_cli_requires_subcommand(capsys):
    with pytest.raises(SystemExit) as excinfo:
        taskcli.main([])

    assert excinfo.value.code == 2
    assert "the following arguments are required: command" in capsys.readouterr().err
