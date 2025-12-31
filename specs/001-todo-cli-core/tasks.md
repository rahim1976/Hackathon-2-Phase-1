# Tasks: Core Todo Functionality

**Input**: Design documents from `/specs/001-todo-cli-core/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure `src/todo_cli/{client,daemon,models,common}` and `tests/`
- [x] T002 [P] Initialize Python 3.13 project with `pyproject.toml` containing dependencies (typer, fastapi, uvicorn, httpx)
- [x] T003 [P] Configure linting (ruff) and formatting tools in `pyproject.toml`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core daemon and common models that MUST be complete before ANY user story

- [x] T004 Define shared Pydantic `Task` model in `src/todo_cli/models/task.py`
- [x] T005 [P] Implement `TaskStore` singleton for in-memory storage in `src/todo_cli/daemon/store.py`
- [x] T006 [P] Implement base FastAPI app and daemon status endpoints in `src/todo_cli/daemon/main.py`
- [x] T007 Implement client base for HTTP communication in `src/todo_cli/client/base.py`
- [x] T008 [P] Implement daemon lifecycle manager (auto-start) in `src/todo_cli/client/lifecycle.py`

**Checkpoint**: Foundation ready - Client can communicate with a running daemon.

---

## Phase 3: User Story 1 - Add Task (Priority: P1) 🎯 MVP

**Goal**: Allow users to add tasks with title and optional description via CLI

- [x] T009 [P] [US1] Create unit tests for add-task logic in `tests/unit/test_add.py`
- [x] T010 [US1] Implement POST `/tasks` endpoint in `src/todo_cli/daemon/main.py`
- [x] T011 [US1] Implement `add` command logic in `src/todo_cli/client/commands.py`
- [x] T012 [US1] Integrate `add` command into Typer app in `src/todo_cli/client/main.py`

**Checkpoint**: User Story 1 functional - Tasks can be added via CLI.

---

## Phase 4: User Story 2 - View Tasks (Priority: P1)

**Goal**: List all tasks in a formatted terminal table

- [x] T013 [P] [US2] Create unit tests for list-task logic in `tests/unit/test_list.py`
- [x] T014 [US2] Implement GET `/tasks` endpoint in `src/todo_cli/daemon/main.py`
- [x] T015 [US2] Implement `list` command and table formatting in `src/todo_cli/client/commands.py`
- [x] T016 [US2] Integrate `list` command into Typer app in `src/todo_cli/client/main.py`

**Checkpoint**: User Story 2 functional - Added tasks can be listed in the terminal.

---

## Phase 5: User Story 3 - Update/Mark Tasks (Priority: P2)

**Goal**: Update task title/description or toggle completion status

- [x] T017 [P] [US3] Create unit tests for update/complete logic in `tests/unit/test_update.py`
- [x] T018 [US3] Implement PATCH `/tasks/{task_id}` endpoint in `src/todo_cli/daemon/main.py`
- [x] T019 [P] [US3] Implement `update`, `complete`, and `incomplete` command logic in `src/todo_cli/client/commands.py`
- [x] T020 [US3] Integrate update/status commands into Typer app in `src/todo_cli/client/main.py`

**Checkpoint**: User Story 3 functional - Tasks can be modified and completed.

---

## Phase 6: User Story 4 - Delete Task (Priority: P3)

**Goal**: Remove a task by its ID

- [x] T021 [P] [US4] Create unit tests for delete logic in `tests/unit/test_delete.py`
- [x] T022 [US4] Implement DELETE `/tasks/{task_id}` endpoint in `src/todo_cli/daemon/main.py`
- [x] T023 [US4] Implement `delete` command in `src/todo_cli/client/commands.py`
- [x] T024 [US4] Integrate `delete` command into Typer app in `src/todo_cli/client/main.py`

**Checkpoint**: All core features functional.

---

## Phase 7: Polish & Cross-Cutting Concerns

- [x] T025 [P] Implement `shutdown` command to stop the daemon in `src/todo_cli/client/commands.py`
- [x] T026 Improve error handling for daemon connection timeouts in `src/todo_cli/client/base.py`
- [x] T027 Run and verify `quickstart.md` examples
- [x] T028 [P] Perform final code cleanup and docstring verification

---

## Dependencies & Execution Order

- **Foundational (Phase 2)**: Depends on T001-T003.
- **User Story 1 (P1)**: Depends on Phase 2.
- **User Story 2 (P1)**: Depends on US1 (to have tasks to list).
- **User Story 3/4**: Depends on US2 (to know IDs for update/delete).

## Parallel Opportunities

- T002, T003 (Setup)
- T005, T006, T008 (Foundation)
- Unit tests (T009, T013, T017, T021) can be written in parallel with endpoints.
- Different user stories can technically be implemented in parallel once Foundational is done, but follow priority order for testing.
