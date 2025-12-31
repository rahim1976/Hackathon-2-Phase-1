from todo_cli.client.base import client, DaemonConnectionError
from todo_cli.models.task import Task, TaskCreate, TaskUpdate
from typing import List

class TodoService:
    async def list_tasks(self) -> List[Task]:
        tasks_json = await client.get("/tasks")
        return [Task(**t) for t in tasks_json]

    async def add_task(self, title: str, description: str = "") -> Task:
        task_create = TaskCreate(title=title, description=description)
        task_json = await client.post("/tasks", json=task_create.model_dump())
        return Task(**task_json)

    async def update_task(self, task_id: int, title: str | None = None, description: str | None = None) -> Task:
        updates = {}
        if title is not None: updates["title"] = title
        if description is not None: updates["description"] = description

        task_update = TaskUpdate(**updates)
        task_json = await client.patch(f"/tasks/{task_id}", json=task_update.model_dump(exclude_unset=True))
        return Task(**task_json)

    async def toggle_task(self, task_id: int) -> Task:
        # Get current state first or just call toggle if API supported it
        # Current API requires explicit boolean, so we fetch first
        tasks = await self.list_tasks()
        task = next((t for t in tasks if t.id == task_id), None)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        task_json = await client.patch(f"/tasks/{task_id}", json={"is_completed": not task.is_completed})
        return Task(**task_json)

    async def set_task_status(self, task_id: int, is_completed: bool) -> Task:
        task_json = await client.patch(f"/tasks/{task_id}", json={"is_completed": is_completed})
        return Task(**task_json)

    async def delete_task(self, task_id: int) -> None:
        await client.delete(f"/tasks/{task_id}")

    async def shutdown_daemon(self) -> None:
        await client.post("/daemon/shutdown")

todo_service = TodoService()
