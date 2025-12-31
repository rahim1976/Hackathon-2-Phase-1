# Quickstart: Core Todo CLI

## Prerequisites
- Python 3.13+
- `pip install -e .` (after implementation)

## Usage

The application is controlled via the `todo` command.

### 1. Add a Task
```bash
todo add "Task Title" --desc "Optional description"
```
*Note: This will automatically start the background daemon if it's not running.*

### 2. List Tasks
```bash
todo list
```

### 3. Complete a Task
```bash
todo complete <ID>
```

### 4. Delete a Task
```bash
todo delete <ID>
```

### 5. Management
To check daemon status:
```bash
todo status
```
To stop the daemon (warning: data is lost!):
```bash
todo shutdown
```

## Developer Notes
- Logs are available at `~/.todo-cli/daemon.log` (if implemented).
- The daemon runs on `http://localhost:8000` by default.
