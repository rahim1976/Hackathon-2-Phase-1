import threading
from todo_cli.models.task import Task

class TaskStore:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.tasks: dict[int, Task] = {}
        self.next_id: int = 1
        self._lock = threading.Lock()
        self._initialized = True

    def add_task(self, task_data: dict) -> Task:
        with self._lock:
            task_id = self.next_id
            self.next_id += 1
            task = Task(id=task_id, **task_data)
            self.tasks[task_id] = task
            return task

    def get_all_tasks(self) -> list[Task]:
        with self._lock:
            return list(self.tasks.values())

    def get_task(self, task_id: int) -> Task | None:
        with self._lock:
            return self.tasks.get(task_id)

    def update_task(self, task_id: int, update_data: dict) -> Task | None:
        with self._lock:
            if task_id not in self.tasks:
                return None

            task = self.tasks[task_id]
            updated_task = task.model_copy(update=update_data)
            from datetime import datetime
            updated_task.updated_at = datetime.now()
            self.tasks[task_id] = updated_task
            return updated_task

    def delete_task(self, task_id: int) -> bool:
        with self._lock:
            if task_id in self.tasks:
                del self.tasks[task_id]
                return True
            return False

task_store = TaskStore()
