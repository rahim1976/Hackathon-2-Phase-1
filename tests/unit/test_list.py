import pytest
from todo_cli.daemon.store import TaskStore

@pytest.fixture
def store():
    s = TaskStore()
    s.tasks = {}
    s.next_id = 1
    return s

def test_list_tasks_empty(store):
    tasks = store.get_all_tasks()
    assert len(tasks) == 0

def test_list_tasks_populated(store):
    store.add_task({"title": "T1"})
    store.add_task({"title": "T2"})

    tasks = store.get_all_tasks()
    assert len(tasks) == 2
    assert tasks[0].title == "T1"
    assert tasks[1].title == "T2"
