---
id: 7
title: TUI UX Improvements: Edit Focus and Action Buttons
stage: refactor
date: 2026-01-01
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-todo-cli-core
branch: 001-todo-cli-core
user: Unknown
command: sp.implement (UX Improvements)
labels: [tui, textual, fix, focus, buttons, interactive]
links:
  spec: specs/001-todo-cli-core/spec.md
files:
  - src/todo_cli/client/tui.py
tests:
  - Manual verification of modal focus
  - Manual verification of "Done/Reopen" button clicks
  - Manual verification of empty selection notifications
---

## Prompt

i cant edit the task, i want to edit the task and also i want to see a check or buttons to be "mark as complete" or something like that and after clicking on that the task will move to completed tab

## Response snapshot

Improved TUI interactivity by fixing the focus issue in modals (enabling editing) and adding clickable "Done" / "Reopen" buttons to each task row. Implemented a Message-based architecture to handle button events and updated the UI layout to a Horizontal container for better spacing.

## Outcome

- ✅ Impact: The TUI is now much more intuitive. Editing is functional again, and mouse users can manage tasks without using keyboard shortcuts via the new buttons.
- 🧪 Tests: Verified focus on modal open, notification on empty action, and button-triggered tab moves.
- 📁 Files: Updated `src/todo_cli/client/tui.py`.
- 🔁 Next prompts: Add a confirmation dialog for task deletion.
- 🧠 Reflection: Using Textual's Message system to communicate button clicks from the TaskItem up to the TodoApp was the most robust architectural choice.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
