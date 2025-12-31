import asyncio
from typing import Optional
import typer
import httpx
from todo_cli.client.service import todo_service
from todo_cli.client.lifecycle import ensure_daemon
from todo_cli.client.base import DaemonConnectionError

def _run_async(coro):
    try:
        return asyncio.run(coro)
    except DaemonConnectionError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

def add(title: str, description: Optional[str] = typer.Option("", "--desc", help="Task description")):
    ensure_daemon()
    task = _run_async(todo_service.add_task(title, description))
    typer.echo(f"Task {task.id} created: {task.title}")

def list_tasks():
    ensure_daemon()
    tasks = _run_async(todo_service.list_tasks())

    if not tasks:
        typer.echo("No tasks found.")
        return

    from rich.console import Console
    from rich.table import Table

    console = Console()
    table = Table(title="Todo List")
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Title", style="magenta")
    table.add_column("Created", style="dim")

    for t in tasks:
        status = "[green]Done[/green]" if t.is_completed else "[yellow]Pending[/yellow]"
        table.add_row(str(t.id), status, t.title, t.created_at.strftime("%Y-%m-%d %H:%M"))

    console.print(table)

def update(
    task_id: int,
    title: Optional[str] = typer.Option(None, "--title", help="New title"),
    description: Optional[str] = typer.Option(None, "--desc", help="New description"),
):
    ensure_daemon()
    try:
        _run_async(todo_service.update_task(task_id, title, description))
        typer.echo(f"Task {task_id} updated.")
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            typer.echo(f"Error: Task {task_id} not found.", err=True)
        else:
            raise

def complete(task_id: int):
    ensure_daemon()
    try:
        _run_async(todo_service.set_task_status(task_id, True))
        typer.echo(f"Task {task_id} marked as complete.")
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            typer.echo(f"Error: Task {task_id} not found.", err=True)
        else:
            raise

def incomplete(task_id: int):
    ensure_daemon()
    try:
        _run_async(todo_service.set_task_status(task_id, False))
        typer.echo(f"Task {task_id} marked as incomplete.")
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            typer.echo(f"Error: Task {task_id} not found.", err=True)
        else:
            raise

def delete(task_id: int):
    ensure_daemon()
    try:
        _run_async(todo_service.delete_task(task_id))
        typer.echo(f"Task {task_id} deleted.")
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            typer.echo(f"Error: Task {task_id} not found.", err=True)
        else:
            raise

def shutdown():
    ensure_daemon()
    try:
        _run_async(todo_service.shutdown_daemon())
        typer.echo("Daemon shutting down... All in-memory data will be cleared.")
    except (httpx.ConnectError, httpx.RemoteProtocolError):
        typer.echo("Daemon shutting down.")

def status():
    from todo_cli.client.lifecycle import is_daemon_running
    if is_daemon_running():
        typer.echo("Daemon is online.")
    else:
        typer.echo("Daemon is offline.")
