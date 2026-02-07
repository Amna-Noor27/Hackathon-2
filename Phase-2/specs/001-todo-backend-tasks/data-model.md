# Data Model: Todo Backend Tasks

## Entity: User
**Description**: Represents a registered user who owns tasks
**Fields**:
- id (UUID/String): Unique identifier for the user
- email (String): User's email address (unique)
- created_at (DateTime): Timestamp when user was created
- updated_at (DateTime): Timestamp when user record was last updated

## Entity: Task
**Description**: Represents a user's todo item
**Fields**:
- id (UUID/String): Unique identifier for the task
- title (String): Title of the task (required, max length 255)
- description (Text): Detailed description of the task (optional)
- completed (Boolean): Whether the task is completed (default: false)
- user_id (UUID/String): Reference to the user who owns this task
- created_at (DateTime): Timestamp when task was created
- updated_at (DateTime): Timestamp when task was last updated

## Relationships
- User (1) <---> (Many) Task: A user can have many tasks, but each task belongs to one user

## Validation Rules
- Task title must not be empty
- Task user_id must reference an existing user
- Task completion status can be updated independently
- Task can only be accessed by the user who owns it

## State Transitions
- Task is created with completed=False
- Task can transition from completed=False to completed=True
- Task can transition from completed=True to completed=False
- Task can be deleted by the owning user