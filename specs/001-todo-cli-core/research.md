# Research: Core Todo CLI Architecture

## Decision: Client-Daemon Architecture
**Choice**: One-shot CLI communicating with a FastAPI-based background daemon.
**Rationale**:
1. The requirement is **in-memory only**. A standard one-shot CLI (e.g., `python todo.py add ...`) exits immediately, losing its memory.
2. A separate long-running daemon process can hold the task list in a Python object until explicitly shut down or the machine reboots.
3. Communication via standard HTTP (localhost) is robust and leverages mature libraries like FastAPI and httpx.

## Lifecycle Management
**Choice**: Lazy Daemon Start.
**Rationale**: The CLI client will check if the daemon is reachable. If not, it will spawn the daemon process in the background before sending the request. This provides a seamless user experience.

## CLI Framework
**Choice**: `Typer`.
**Rationale**: Typer provides a clean, type-hint-driven interface that works perfectly with Python 3.13. It is built on Click but is more modern and easier to maintain.

## Data Schema
**Choice**: Pydantic models.
**Rationale**: Shared Pydantic models between the client and daemon ensure contract consistency and easy serialization.

## Error Handling Pattern
**Choice**: System Exit with Status Codes.
**Rationale**:
- `Status 0`: Success.
- `Status 1`: General error (daemon unreachable after retry).
- `Status 2`: Invalid user input (validation error).
- `Status 3`: Logic error (ID not found).
Error messages will be sent to `stderr`.

## Alternatives Considered
- **Standard One-shot without Daemon**: Rejected because it cannot satisfy the "in-memory persistence across calls" requirement.
- **Interactive REPL**: Rejected because the user implicitly requested a standard "CLI-based" interaction (add, list, etc. as subcommands). A REPL would be a different user experience.
- **SQLite (In-Memory mode)**: Rejected because it still requires a process to keep the connection open. A Python list/dict in a daemon is simpler and fits the constraint better.
- **Named Pipes / Unix Sockets**: Considered for faster IPC, but HTTP/Localhost is more cross-platform (Win32 compatibility) and easier to debug with standard tools.
