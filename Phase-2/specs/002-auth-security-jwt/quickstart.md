# Quickstart Guide: Auth Security JWT

## Overview
This guide provides instructions for setting up and running the authentication and security system for the Todo application.

## Prerequisites
- Node.js 18+ (for Next.js frontend)
- Python 3.11+ (for FastAPI backend)
- Better Auth account/configured instance
- Shared secret key for JWT signing
- Existing backend API from Spec-1 (Todo Backend Tasks)

## Setup Instructions

### 1. Clone the repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Frontend Setup (Next.js with Better Auth)
```bash
cd frontend
npm install
npm install @better-auth/react @better-auth/next-js
```

### 3. Backend Setup (FastAPI JWT Middleware)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in both frontend and backend with the following variables:

**Frontend (.env.local):**
```
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8080
NEXTAUTH_SECRET=your-shared-secret-key-here-replace-with-a-real-secret
NEXT_PUBLIC_JWT_SECRET=your-shared-secret-key-here-replace-with-a-real-secret
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

**Backend (.env):**
```
DATABASE_URL=postgresql://neondb_owner:npg_INkw1zTjZD8X@ep-small-dawn-aho1jjn9-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_SECRET_KEY=your-shared-secret-key-here-replace-with-a-real-secret
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=240
```

### 5. Better Auth Configuration
Configure Better Auth in `frontend/auth.config.ts`:
```typescript
import { betterAuth } = from("@better-auth/node");
import { nextJs } = from("@better-auth/next-js");

export const auth = betterAuth({
  secret: process.env.NEXTAUTH_SECRET || "your-fallback-secret-for-development",
  database: {
    provider: "postgresql",
    url: process.env.DATABASE_URL || "",
  },
  socialProviders: {
    // Configure as needed
  },
  jwt: {
    secret: process.env.JWT_SECRET_KEY,
    expiresIn: "4h",  // 4 hours
  }
});

export const authHandler = nextJs(auth);
```

### 6. Run the Applications
**Frontend:**
```bash
cd frontend
npm run dev
```

**Backend:**
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

## Authentication Flow

### User Registration
1. User visits `/register` page
2. Better Auth handles registration
3. JWT token is issued upon successful registration
4. Token is stored in browser's secure storage

### User Login
1. User visits `/login` page
2. Better Auth handles authentication
3. JWT token is issued upon successful login
4. Token is attached to all subsequent API requests

### API Access with JWT
1. Frontend retrieves JWT from storage
2. All API requests include `Authorization: Bearer <token>` header
3. Backend middleware verifies JWT signature and expiration
4. User identity is extracted from JWT claims
5. Request is processed with user-specific authorization

## API Endpoints

### Authentication Endpoints
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/profile` - Get user profile

### Protected Task Endpoints (require JWT)
- `GET /api/tasks` - Get authenticated user's tasks
- `POST /api/tasks` - Create a task for authenticated user
- `GET /api/tasks/{task_id}` - Get a specific task
- `PUT /api/tasks/{task_id}` - Update a specific task
- `DELETE /api/tasks/{task_id}` - Delete a specific task

## Testing
Run the tests using pytest for backend and jest for frontend:
```bash
# Backend tests
cd backend
pytest tests/auth/

# Frontend tests
cd frontend
npm run test
```

## Validation Steps
To verify the implementation works correctly:

1. **Start both applications** (frontend and backend)
2. **Register a new user** via the `/register` page
3. **Log in** with the new user credentials
4. **Create a task** - verify it's associated with the authenticated user
5. **View tasks** - verify only the user's tasks are returned
6. **Attempt to access API without token** - verify 401 responses
7. **Use an invalid/expired token** - verify 401 responses

## Configuration Notes
- The JWT secret key must be identical between frontend and backend
- All API requests to protected endpoints require valid JWT in Authorization header
- JWT tokens expire after 4 hours and must be refreshed
- User ID from JWT is used to enforce user-specific data access
- The authentication system integrates seamlessly with existing backend API's from Spec-1