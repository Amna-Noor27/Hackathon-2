# Internal API Contracts: In-Memory Python Todo Console Application

Since this is a CLI application, these "contracts" define the interface between the CLI View/Controller and the Logic Layer.

## Core Logic Internal API

### `add_task(title: str, description: str) -> dict`
- **Purpose**: Creates and stores a new task.
- **Input**: Title and description strings.
- **Output**: The created task dictionary with its assigned ID.

### `list_tasks() -> list[dict]`
- **Purpose**: Retrieves all stored tasks.
- **Output**: List of task dictionaries.

### `update_task(task_id: int, title: str = None, description: str = None) -> bool`
- **Purpose**: Updates title or description of an existing task.
- **Output**: `True` if success, `False` if ID not found.

### `toggle_task_status(task_id: int) -> bool`
- **Purpose**: Switches status between 'Pending' and 'Completed'.
- **Output**: `True` if success, `False` if ID not found.

### `delete_task(task_id: int) -> bool`
- **Purpose**: Removes a task from storage.
- **Output**: `True` if success, `False` if ID not found.
