import pytest
from todo_cli.daemon.store import TaskStore

@pytest.fixture
def store():
    s = TaskStore()
    s.tasks = {}
    s.next_id = 1
    return s

def test_update_task(store):
    store.add_task({"title": "Old"})
    store.update_task(1, {"title": "New", "description": "Updated"})

    task = store.get_task(1)
    assert task.title == "New"
    assert task.description == "Updated"

def test_complete_task(store):
    store.add_task({"title": "Task"})
    store.update_task(1, {"is_completed": True})

    task = store.get_task(1)
    assert task.is_completed is True
