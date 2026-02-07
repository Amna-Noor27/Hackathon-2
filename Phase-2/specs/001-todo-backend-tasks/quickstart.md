# Quickstart Guide: Todo Backend Tasks

## Overview
This guide provides instructions for setting up and running the Todo backend service locally.

## Prerequisites
- Python 3.11+
- Poetry or pip for dependency management
- Neon Serverless PostgreSQL database instance

## Setup Instructions

### 1. Clone the repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Set up Python environment
Using Poetry:
```bash
cd backend
poetry install
poetry shell
```

Or using pip:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the backend directory with the following variables:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Database Setup
Run the database migrations:
```bash
# This would be implemented with Alembic in a complete setup
# For now, the app creates tables on startup
```

### 5. Run the Application
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### Authentication
All endpoints require authentication. Include the user_id as a parameter for testing purposes.
In a complete implementation, this would be replaced with proper authentication middleware.

### Available Endpoints

- `GET /api/tasks?user_id={user_id}` - Get all tasks for the specified user
- `POST /api/tasks` - Create a new task (include user_id in the request body)
- `GET /api/tasks/{task_id}?user_id={user_id}` - Get a specific task
- `PUT /api/tasks/{task_id}?user_id={user_id}` - Update a specific task
- `DELETE /api/tasks/{task_id}?user_id={user_id}` - Delete a specific task

## Testing
Run the tests using pytest:
```bash
cd backend
pytest
```

## Configuration Notes
- The database connection is configured to work with Neon Serverless PostgreSQL
- All tasks are automatically scoped to the user_id provided in requests
- The API follows RESTful conventions with appropriate HTTP status codes
- User isolation is enforced at the service layer to prevent unauthorized access