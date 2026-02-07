# Data Model: Auth Security JWT

## Entity: User (Enhanced)
**Description**: Represents an authenticated user with JWT-based authentication
**Fields**:
- id (String/UUID): Unique identifier for the user (matches JWT subject claim)
- email (String): User's email address (verified through Better Auth)
- created_at (DateTime): Timestamp when user was created
- updated_at (DateTime): Timestamp when user record was last updated
- is_active (Boolean): Whether the user account is active

## Entity: JWT Token
**Description**: JWT token structure for authentication and authorization
**Fields**:
- sub (String): Subject (user ID) - identifies the user
- email (String): User's email address
- exp (Integer): Expiration timestamp (Unix timestamp)
- iat (Integer): Issued at timestamp (Unix timestamp)
- iss (String): Issuer (application identifier)
- jti (String): JWT ID (unique identifier for the token)

## Entity: Auth Session
**Description**: Stateless authentication session represented by JWT token
**Fields**:
- token (String): The JWT token string
- user_id (String): Reference to the authenticated user
- expires_at (DateTime): When the token expires
- created_at (DateTime): When the session was established

## Relationships
- User (1) <---> (Many) Auth Session: A user can have multiple JWT tokens simultaneously

## Validation Rules
- JWT tokens must have valid signature matching shared secret
- JWT tokens must not be expired at time of validation
- User ID in JWT must correspond to an existing user in the database
- Email in JWT should match the email in the user record

## State Transitions
- JWT token: Active (before expiration) --> Expired (after expiration)
- Auth Session: Valid (token exists and unexpired) --> Invalid (token expired or revoked)