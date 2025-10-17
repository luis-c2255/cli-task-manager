import pytest
from pathlib import Path
import sys
from cli_task import db, tasks 

@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    """
    Redirect the config directory and DB path to a temporary directory for tests.
    """
    temp_config = tmp_path / "config"
    temp_dbfile = temp_config / "tasks.db"
    monkeypatch.setattr(db, "CONFIG_DIR", temp_config)
    monkeypatch.setattr(db, "DB_PATH", temp_dbfile)

    # Initialize a fresh database
    db.init_db()
    yield
    # tmp_path is auto-cleaned by pytest

def test_list_tasks_empty():
    """
    Listing tasks on a fresh DB should return an empty list.
    """
    assert tasks.list_tasks() == []

def test_create_and_list_task():
    """
    After creating a task, it appears in list_tasks.
    """
    tid = tasks.create_task("Test task", "Desc", "2025-10-30", 2)
    all_tasks = tasks.list_tasks()
    assert len(all_tasks) == 1

    id_, title, due, prio, status = all_tasks[0]
    assert id_ == tid
    assert title == "Test task"
    assert due == "2025-10-30"
    assert prio == 2
    assert status == "pending"

def test_get_task_by_id():
    """
    get_task should return the full row when it exists.
    """
    tid = tasks.create_task("Single fetch")
    row = tasks.get_task(tid)
    assert row[0] == tid
    assert row[1] == "Single fetch"

def test_create_empty_title_raises():
    """
    Creating a task with an empty title must raise ValueError.
    """
    with pytest.raises(ValueError):
        tasks.create_task("   ")

def test_update_task_success_and_errors():
    """
    update_task should modify fields or raise on invalid cases.
    """
    tid = tasks.create_task("Before update")
    tasks.update_task(tid, title="After update", status="done")
    updated = tasks.get_task(tid)
    assert updated[1] == "After update"
    assert updated[5] == "done"  # status column

    # No fields => ValueError
    with pytest.raises(ValueError):
        tasks.update_task(tid)

    # Non-existent ID => ValueError
    with pytest.raises(ValueError):
        tasks.update_task(999, title="Nope")

def test_delete_task_success_and_not_found():
    """
    delete_task should remove existing tasks and error on missing.
    """
    tid = tasks.create_task("To be deleted")
    tasks.delete_task(tid)
    assert tasks.list_tasks() == []

    with pytest.raises(ValueError):
        tasks.delete_task(tid)
