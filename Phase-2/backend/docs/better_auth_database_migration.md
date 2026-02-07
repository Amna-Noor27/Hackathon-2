# Better Auth Database Schema Migration

## Overview
This document describes the database schema changes made to ensure compatibility with Better Auth requirements.

## Schema Changes

### 1. Updated Users Table
The existing `users` table was updated to include Better Auth required fields:

- **email_verified** (TIMESTAMP WITH TIME ZONE): Tracks when the user's email was verified
- **image** (TEXT): Stores URL to the user's profile image

### 2. Added Sessions Table
New table to manage user sessions with Better Auth compatibility:

```sql
CREATE TABLE sessions (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 3. Added Accounts Table
New table to manage third-party provider accounts:

```sql
CREATE TABLE accounts (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    provider_id VARCHAR(255) NOT NULL,
    provider_user_id VARCHAR(255) NOT NULL,
    access_token TEXT,
    refresh_token TEXT,
    id_token TEXT,
    token_type VARCHAR(255),
    scope TEXT,
    expires_at BIGINT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(provider_id, provider_user_id)
);
```

## Model Updates

### User Model
Updated `src/models/user.py` to include:
- `email_verified` field (Optional[datetime])
- `image` field (Optional[str])

### New Models
- `src/models/session.py`: Session management model
- `src/models/account.py`: Third-party account management model

## API Changes

### Auth Endpoints
Updated `src/api/auth.py` to:
- Return proper Better Auth format in `/get-session` endpoint
- Include emailVerified and image in user data
- Support user updates through PUT `/user` endpoint

## Migration Process

1. Run the migration script: `python migrate_to_better_auth.py`
2. The script will:
   - Create/update the required tables
   - Add missing columns to existing tables
   - Migrate existing users to include new fields
   - Validate Better Auth compatibility

## Environment Variables

Ensure your `.env` file contains the proper database URL for Neon:
```
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
```

## Testing

After migration, you can test Better Auth compatibility by:
1. Registering a new user
2. Logging in to get a JWT token
3. Calling `/api/auth/get-session` with the token
4. Verifying the response includes all required Better Auth fields