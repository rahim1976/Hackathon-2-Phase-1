from fastapi import FastAPI, HTTPException
from todo_cli.daemon.store import task_store
from todo_cli.models.task import Task, TaskCreate, TaskUpdate
import os
import signal

app = FastAPI(title="Todo Daemon")

@app.get("/tasks", response_model=list[Task])
async def list_tasks():
    return task_store.get_all_tasks()

@app.post("/tasks", response_model=Task)
async def create_task(task: TaskCreate):
    return task_store.add_task(task.model_dump())

@app.patch("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: TaskUpdate):
    updated = task_store.update_task(task_id, task_update.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    success = task_store.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "success"}

@app.get("/daemon/status")
async def status():
    return {"status": "online"}

@app.post("/daemon/shutdown")
async def shutdown():
    os.kill(os.getpid(), signal.SIGINT)
    return {"status": "shutting down"}
