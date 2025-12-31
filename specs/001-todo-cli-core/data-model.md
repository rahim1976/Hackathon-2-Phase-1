# Data Model: Todo CLI

## Task Entity

The core entity is the `Task`.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| `id` | `int` | Unique identifier (primary key) | Auto-incrementing, > 0 |
| `title` | `str` | Title of the task | Required, 1-200 chars |
| `description` | `str` | Detailed description | Optional, default "" |
| `is_completed` | `bool` | Completion status | Required, default `False` |
| `created_at` | `datetime` | Creation timestamp | Auto-generated |
| `updated_at` | `datetime` | Last modification timestamp | Auto-updated |

## In-Memory Storage (Daemon)

The Daemon will maintain state in a `TaskStore` singleton.

```python
class TaskStore:
    tasks: dict[int, Task]
    next_id: int
```

- **ID Generation**: A simple counter (`next_id`) that increments with each task added.
- **Concurrency**: Use a `threading.Lock` if needed, although simple dictionary operations are largely safe in this single-daemon context.

## State Transitions
1. `Null` → `Pending`: Task created.
2. `Pending` → `Completed`: `is_completed` set to `True`.
3. `Completed` → `Pending`: `is_completed` set to `False`.
4. `Any` → `Deleted`: Removed from dictionary.
