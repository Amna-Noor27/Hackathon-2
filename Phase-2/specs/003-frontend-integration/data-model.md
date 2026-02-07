# Data Model: Frontend Integration

## Entity: User Session
**Description**: Represents an authenticated user's session state in the frontend
**Fields**:
- user_id (String): Unique identifier for the authenticated user
- email (String): User's email address
- name (String, optional): User's display name
- access_token (String): JWT token for API authentication
- expires_at (DateTime): When the token expires
- is_authenticated (Boolean): Whether the user is currently authenticated

## Entity: Task List
**Description**: Collection of tasks belonging to the authenticated user
**Fields**:
- tasks (Array<Task>): Array of task objects
- loading_state (String): Current loading state (idle, loading, error, success)
- error_message (String, optional): Error message if in error state
- total_count (Integer): Total number of tasks for the user

## Entity: Individual Task
**Description**: A single task with properties as defined by the backend API
**Fields**:
- id (String): Unique identifier for the task
- title (String): Title of the task (required, max length 255)
- description (String, optional): Detailed description of the task
- completed (Boolean): Whether the task is completed (default: false)
- user_id (String): Reference to the user who owns this task
- created_at (DateTime): Timestamp when task was created
- updated_at (DateTime): Timestamp when task was last updated

## Entity: UI State
**Description**: Various states for different UI components
**Fields**:
- loading (Boolean): Whether a component is in a loading state
- error (String, optional): Error message if component is in error state
- empty (Boolean): Whether a component is displaying empty state
- success (Boolean): Whether an operation was successful

## Relationships
- User Session (1) <---> (Many) Task List: An authenticated user has one task list
- Task List (1) <---> (Many) Individual Task: A task list contains multiple tasks
- Individual Task (Many) <---> (1) User Session: Many tasks belong to one user session

## Validation Rules
- Task title must not be empty when creating/updating
- Task completion status can be toggled independently
- User Session must have valid JWT token to access protected routes
- Task List should only contain tasks belonging to the authenticated user

## State Transitions
- User Session: Anonymous (not authenticated) --> Authenticated (with valid token) --> Logged out (token cleared)
- UI State: Idle (no operation) --> Loading (during API call) --> Success/Error (after API call)
- Individual Task: Incomplete (completed: false) <---> Complete (completed: true)