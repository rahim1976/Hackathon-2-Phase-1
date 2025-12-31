# Todo CLI & Rich TUI

A professional-grade, modern Python Todo application featuring a **Client-Daemon architecture** for in-memory persistence and a **Rich Interactive TUI** for a premium user experience.

## 🚀 Overview

This project was built using **Spec-Driven Development (SDD)** with Python 3.13+. It satisfies the strict requirement for **volatile in-memory storage** by utilizing a background daemon that preserves application state across multiple CLI/TUI sessions without writing to disk.

## ✨ Key Features

### 🖥️ Rich Interactive TUI (Terminal User Interface)
- **Tabbed Navigation**: Separate views for **Pending** and **Completed** tasks.
- **Keyboard & Mouse Support**: Fast navigation via arrow keys/Enter or mouse clicks.
- **Interactive Modals**: Dedicated screens for adding and editing tasks with auto-focus.
- **Real-time Feedback**: Notifications for successful actions and error handling.
- **One-click Actions**: "Done" and "Reopen" buttons for immediate status transitions.

### ⌨️ Standard CLI Commands
- `todo add <title>`: Quickly create a task without entering the TUI.
- `todo list`: Output a beautiful [Rich](https://github.com/Textualize/rich) table of your tasks.
- `todo complete <id>`: Mark tasks done from the command line.
- `todo status`: Check the health of the background daemon.

### ⏱️ Time Tracking
- **Creation Timestamps**: Every task tracks exactly when it was made.
- **Update Tracking**: Automatically shows the last modified time when a task is edited.

## 🏗️ Technical Architecture

### **The Stack**
- **Language**: Python 3.13+
- **CLI Framework**: [Typer](https://typer.tiangolo.com/)
- **TUI Framework**: [Textual](https://textual.textualize.io/)
- **Backend API**: [FastAPI](https://fastapi.tiangolo.com/)
- **Server**: [Uvicorn](https://www.uvicorn.org/)
- **HTTP Client**: [httpx](https://www.python-httpx.org/)
- **Validation**: [Pydantic v2](https://docs.pydantic.dev/)

### **System Design**
1.  **Daemon Layer**: A background process starts automatically on the first command. It holds a singleton class in memory that stores all tasks.
2.  **Service Layer**: A decoupled `TodoService` acts as the brain, converting low-level HTTP responses into typed Pydantic models for the UI.
3.  **Client Layer**: Both the `Typer` CLI and `Textual` TUI consume the same service layer, ensuring consistent logic across all interfaces.

## 📥 Installation

1.  **Prerequisites**: Python 3.13 or newer.
2.  **Setup**:
    ```bash
    git clone <repo-url>
    cd todo-cli
    pip install -e .
    ```

## 🛠️ Usage

### **Primary Interface (TUI)**
Launch the interactive dashboard:
```bash
todo tui
```
**Controls**:
- `a`: Add new task
- `e`: Edit selected task
- `Enter`: Toggle status (or click the button)
- `d`: Delete selected task
- `Tab`: Switch between Pending/Completed lists
- `q`: Quit

### **CLI Interface**
For quick one-off operations:
```bash
todo add "Finish README" --desc "Include all project details"
todo list
todo complete 1
todo delete 1
todo shutdown  # Stop the background daemon (Warning: clears memory)
```

## 🧪 Testing
The project includes a suite of unit tests for all core CRUD operations.
```bash
pytest tests/unit
```

## 📂 Project Structure
- `specs/`: Detailed SDD documentation (Spec, Plan, Tasks, Research).
- `src/todo_cli/daemon/`: Backend logic and in-memory storage.
- `src/todo_cli/client/`: CLI commands, TUI application, and Service Layer.
- `src/todo_cli/models/`: Shared data structures.
- `history/`: Prompt History Records (PHRs) for full development traceability.

---
*Built with ❤️ using Claude Code and Spec-Kit Plus.*
