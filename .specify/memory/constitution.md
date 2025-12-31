# Python CLI Todo Constitution

<!--
Sync Impact Report
- Version change: 0.0.0 → 1.0.0
- List of modified principles:
  - PRINCIPLE_1: Python 3.13+ Mandate
  - PRINCIPLE_2: CLI-Only Interface
  - PRINCIPLE_3: In-Memory Storage Only
  - PRINCIPLE_4: Clean Code & SOLID
  - PRINCIPLE_5: Spec-Driven Development (SDD)
  - PRINCIPLE_6: No Manual Coding
- Added sections: Core Principles, Governance
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md
  - ✅ .specify/templates/spec-template.md
  - ✅ .specify/templates/tasks-template.md
- Follow-up TODOs: None
-->

## Core Principles

### I. Python 3.13+ Mandate
The application MUST be built using Python 3.13 or newer. All language features used should be
compatible with the target version. This ensures use of modern Python patterns and type hinting.

### II. CLI-Only Interface
Interaction MUST be strictly via the Command Line Interface (CLI). There shall be no graphical
user interface (GUI) or web interface. Text in/out protocol: stdin/args → stdout,
errors → stderr. Support for machine-readable output (JSON) is preferred.

### III. In-Memory Storage Only
Task storage MUST be volatile and in-memory only. No persistence to disk (databases, CSV,
JSON files) is permitted. This constraint reinforces simple data models and emphasizes
runtime efficiency.

### IV. Clean Code & SOLID
The codebase MUST adhere to Clean Code principles and SOLID design patterns. Code should be
self-documenting, modular, and easy to maintain. Functions should be small and have a single
responsibility.

### V. Spec-Driven Development (SDD)
All development MUST follow the Spec-Kit Plus SDD workflow. No code changes are made without
a corresponding feature specification, implementation plan, and task list.

### VI. No Manual Coding
All code implementation, refactoring, and debugging MUST be executed via Claude Code. No
manual editing of source files outside the agent's controlled environment is allowed to
ensure full traceability.

## Governance

The constitution supersedes all other documentation and practices. Amendments to these
principles require a formal proposal and a version bump. All implementations must be
verified against these principles before merging.

**Version**: 1.0.0 | **Ratified**: 2025-12-31 | **Last Amended**: 2025-12-31
