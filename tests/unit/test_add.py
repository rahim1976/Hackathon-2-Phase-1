import pytest
from todo_cli.daemon.store import TaskStore

@pytest.fixture
def store():
    # Reset store for each test
    s = TaskStore()
    s.tasks = {}
    s.next_id = 1
    return s

def test_add_task(store):
    task_data = {"title": "Test Task", "description": "Test Desc"}
    task = store.add_task(task_data)

    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Desc"
    assert task.is_completed is False
    assert len(store.get_all_tasks()) == 1

def test_add_task_no_desc(store):
    task_data = {"title": "Test Task"}
    task = store.add_task(task_data)

    assert task.title == "Test Task"
    assert task.description == ""
    assert len(store.get_all_tasks()) == 1
