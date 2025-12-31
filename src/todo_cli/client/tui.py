from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListItem, ListView, Static, Input, TabbedContent, TabPane, Button
from textual.containers import Container, Vertical, Horizontal
from textual.screen import ModalScreen
from textual.binding import Binding
from textual.reactive import reactive
from textual.message import Message

from todo_cli.client.service import todo_service
from todo_cli.client.lifecycle import ensure_daemon
from todo_cli.client.base import DaemonConnectionError
from todo_cli.models.task import Task

class TaskItem(Horizontal):
    """A widget to display a task with timestamps and action buttons."""
    def __init__(self, task: Task, **kwargs):
        super().__init__(**kwargs)
        self.todo_task = task

    def compose(self) -> ComposeResult:
        status_icon = "[green]✔[/green]" if self.todo_task.is_completed else "[yellow]○[/yellow]"
        created = self.todo_task.created_at.strftime("%Y-%m-%d %H:%M")

        info = f"{status_icon} [b]{self.todo_task.title}[/b]\n[dim]Created: {created}[/dim]"
        if self.todo_task.updated_at > self.todo_task.created_at:
            updated = self.todo_task.updated_at.strftime("%Y-%m-%d %H:%M")
            info += f" [dim]| Updated: {updated}[/dim]"

        yield Static(info, classes="task-info")

        btn_label = "Reopen" if self.todo_task.is_completed else "Done"
        btn_variant = "warning" if self.todo_task.is_completed else "success"
        yield Button(btn_label, variant=btn_variant, id="toggle-btn")

    class ToggleRequest(Message):
        """Sent when the toggle button is clicked."""
        def __init__(self, task_id: int) -> None:
            self.task_id = task_id
            super().__init__()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "toggle-btn":
            self.post_message(self.ToggleRequest(self.todo_task.id))

class AddTaskModal(ModalScreen[tuple[str, str]]):
    """A modal to add a new task."""
    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Add New Task", classes="title"),
            Input(placeholder="Task Title", id="title"),
            Input(placeholder="Description (optional)", id="desc"),
            Horizontal(
                Static("Press ENTER to save, ESC to cancel", classes="help"),
            ),
            id="dialog"
        )

    def on_mount(self) -> None:
        self.query_one("#title", Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        title = self.query_one("#title", Input).value
        desc = self.query_one("#desc", Input).value
        if title:
            self.dismiss((title, desc))

    def on_key(self, event) -> None:
        if event.key == "escape":
            self.app.pop_screen()

class EditTaskModal(ModalScreen[tuple[str, str]]):
    """A modal to edit an existing task."""
    def __init__(self, task: Task, **kwargs):
        super().__init__(**kwargs)
        self.todo_task = task

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Edit Task", classes="title"),
            Input(value=self.todo_task.title, placeholder="Task Title", id="title"),
            Input(value=self.todo_task.description, placeholder="Description (optional)", id="desc"),
            Horizontal(
                Static("Press ENTER to save, ESC to cancel", classes="help"),
            ),
            id="dialog"
        )

    def on_mount(self) -> None:
        self.query_one("#title", Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        title = self.query_one("#title", Input).value
        desc = self.query_one("#desc", Input).value
        if title:
            self.dismiss((title, desc))

    def on_key(self, event) -> None:
        if event.key == "escape":
            self.app.pop_screen()

class TodoApp(App):
    """A Textual TUI for Todo management with Tabs and interactive buttons."""
    CSS = """
    Screen {
        background: $surface;
    }
    #dialog {
        padding: 1 2;
        background: $panel;
        border: thick $primary;
        width: 60;
        height: 12;
        align: center middle;
    }
    .title {
        text-align: center;
        width: 100%;
        color: $accent;
        text-style: bold;
    }
    .help {
        text-align: center;
        width: 100%;
        color: $text-disabled;
        margin-top: 1;
    }
    ListItem {
        padding: 0;
        height: auto;
    }
    TaskItem {
        height: auto;
        padding: 1 2;
    }
    .task-info {
        width: 1fr;
        height: auto;
    }
    #toggle-btn {
        width: 12;
        min-width: 12;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("a", "add", "Add Task"),
        Binding("e", "edit", "Edit Task"),
        Binding("d", "delete", "Delete Task"),
        Binding("r", "refresh", "Refresh"),
        Binding("enter", "toggle", "Toggle (Select)"),
    ]

    tasks = reactive([])

    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent():
            with TabPane("Pending", id="pending-tab"):
                yield ListView(id="pending-list")
            with TabPane("Completed", id="completed-tab"):
                yield ListView(id="completed-list")
        yield Footer()

    async def on_mount(self) -> None:
        ensure_daemon()
        await self.action_refresh()

    async def action_refresh(self) -> None:
        try:
            self.tasks = await todo_service.list_tasks()
            pending_list = self.query_one("#pending-list", ListView)
            completed_list = self.query_one("#completed-list", ListView)

            await pending_list.clear()
            await completed_list.clear()

            for task in self.tasks:
                item = ListItem(TaskItem(task))
                if task.is_completed:
                    await completed_list.append(item)
                else:
                    await pending_list.append(item)
        except DaemonConnectionError:
            self.notify("Error: Daemon unavailable", severity="error")

    async def on_task_item_toggle_request(self, message: TaskItem.ToggleRequest) -> None:
        """Handle toggle message from TaskItem button."""
        await todo_service.toggle_task(message.task_id)
        await self.action_refresh()

    async def action_add(self) -> None:
        async def check_add_result(result: tuple[str, str] | None) -> None:
            if result:
                title, desc = result
                await todo_service.add_task(title, desc)
                await self.action_refresh()

        self.push_screen(AddTaskModal(), check_add_result)

    def _get_active_list(self) -> ListView | None:
        tc = self.query_one(TabbedContent)
        list_id = "#pending-list" if tc.active == "pending-tab" else "#completed-list"
        return self.query_one(list_id, ListView)

    async def action_edit(self) -> None:
        list_view = self._get_active_list()
        if list_view is None or list_view.index is None:
            self.notify("No task selected", severity="warning")
            return

        item = list_view.children[list_view.index]
        task_item = item.query_one(TaskItem)

        async def check_edit_result(result: tuple[str, str] | None) -> None:
            if result:
                title, desc = result
                await todo_service.update_task(task_item.todo_task.id, title, desc)
                await self.action_refresh()

        self.push_screen(EditTaskModal(task_item.todo_task), check_edit_result)

    async def action_delete(self) -> None:
        list_view = self._get_active_list()
        if list_view is None or list_view.index is None:
            self.notify("No task selected", severity="warning")
            return

        item = list_view.children[list_view.index]
        task_item = item.query_one(TaskItem)
        await todo_service.delete_task(task_item.todo_task.id)
        await self.action_refresh()

    async def action_toggle(self) -> None:
        """Keyboard entry for toggle."""
        list_view = self._get_active_list()
        if list_view is None or list_view.index is None:
            self.notify("No task selected", severity="warning")
            return

        item = list_view.children[list_view.index]
        task_item = item.query_one(TaskItem)
        await todo_service.toggle_task(task_item.todo_task.id)
        await self.action_refresh()

def run():
    app = TodoApp()
    app.run()

if __name__ == "__main__":
    run()
