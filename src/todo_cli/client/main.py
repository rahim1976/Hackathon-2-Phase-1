import typer
from todo_cli.client import commands

app = typer.Typer(help="Todo CLI with in-memory storage", no_args_is_help=True)

# Register commands as subcommands
app.command(name="add")(commands.add)
app.command(name="list")(commands.list_tasks)
app.command(name="update")(commands.update)
app.command(name="complete")(commands.complete)
app.command(name="incomplete")(commands.incomplete)
app.command(name="delete")(commands.delete)
app.command(name="shutdown")(commands.shutdown)
app.command(name="status")(commands.status)

@app.command(name="tui")
def launch_tui():
    """Launch the rich interactive TUI."""
    from todo_cli.client import tui
    tui.run()

if __name__ == "__main__":
    app()
