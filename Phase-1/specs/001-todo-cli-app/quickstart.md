# Quickstart: In-Memory Python Todo Console Application

**Feature**: [In-Memory Python Todo Console Application](../spec.md)

## Prerequisites
- Python 3.13+
- `uv` installed

## Setup
1. Checkout the branch: `git checkout 001-todo-cli-app`
2. Initialize environment: `uv init` (if not already done)

## Running the Application
```bash
uv run src/main.py
```

## Menu Options
1. **Add Task**: Enter title and description.
2. **List Tasks**: View all tasks and their IDs.
3. **Update Task**: Provide ID and new content.
4. **Complete Task**: Toggle status by ID.
5. **Delete Task**: Remove by ID.
6. **Exit**: Terminate session (Warning: Data is not persistent).
