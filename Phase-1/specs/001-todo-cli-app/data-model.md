# Data Model: In-Memory Python Todo Console Application

**Feature**: [In-Memory Python Todo Console Application](../spec.md)
**Status**: Finalized

## Entities

### Task
Represents a single todo item.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| id | int | Unique identifier | Must be > 0, auto-incremented |
| title | str | Short name of the task | Required, non-empty |
| description | str | Detailed info | Optional |
| status | str | Current state | Enum: ['Pending', 'Completed'] |

## State Transitions

- **Pending** → **Completed**: Via `toggle_status` or `complete_task`
- **Completed** → **Pending**: Via `toggle_status`

## Storage Pattern
- **InMemoryStore**: A singleton-like list `tasks_db` contained within the store module.
- **ID Generation**: A global counter `next_id` initialized at 1 and incremented on every `add_task`.
