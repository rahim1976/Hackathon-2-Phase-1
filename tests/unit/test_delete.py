import pytest
from todo_cli.daemon.store import TaskStore

@pytest.fixture
def store():
    s = TaskStore()
    s.tasks = {}
    s.next_id = 1
    return s

def test_delete_task(store):
    store.add_task({"title": "Delete Me"})
    assert len(store.get_all_tasks()) == 1

    success = store.delete_task(1)
    assert success is True
    assert len(store.get_all_tasks()) == 0

def test_delete_nonexistent(store):
    success = store.delete_task(999)
    assert success is False
