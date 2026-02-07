# Todo Backend Authentication Documentation

This document describes the authentication and authorization implementation for the Todo application backend.

## Overview

The backend implements JWT-based authentication to verify user identity and enforce access controls. All protected API endpoints require a valid JWT token in the Authorization header.

## Architecture

- **JWT Middleware**: Validates JWT tokens and extracts user identity
- **Authentication Dependencies**: Provides dependency injection for authentication state
- **Access Controls**: Enforces user-specific access to resources
- **Token Validation**: Verifies token signature, expiration, and claims

## Components

### JWT Utilities (`src/auth/jwt.py`)
- `create_access_token()`: Creates JWT tokens with standardized payload structure
- `verify_token()`: Validates token signature and extracts user ID
- `get_current_user()`: Retrieves user object from token
- `decode_token_payload()`: Inspects token claims without validation

### Authentication Middleware (`src/auth/middleware.py`)
- `JWTBearer`: HTTP Bearer authentication scheme
- Token validation and user identity extraction
- Request state population with user data

### Authentication Dependencies (`src/auth/deps.py`)
- `get_current_user_dep()`: Gets current user object from token
- `get_current_user_id()`: Extracts user ID from token
- `get_current_user_identity()`: Extracts full user identity from token

## Security Features

- Standardized JWT payload structure with required claims (sub, email, exp, iat, iss, aud)
- User-specific access controls ensuring users can only access their own resources
- Automatic 401 Unauthorized responses for invalid or missing tokens
- Statelessness (no session database lookups required)

## API Integration

Protected endpoints in `src/api/tasks.py` use authentication dependencies to:
- Verify JWT token validity
- Extract authenticated user ID
- Enforce user-specific access to tasks
- Return 401 responses for unauthorized access attempts

## Token Claims Structure

```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "exp": 9999999999,
  "iat": 1000000000,
  "iss": "todo-app",
  "aud": "todo-users",
  "role": "user",
  "permissions": ["read", "write"]
}
```