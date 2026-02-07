# Research: Auth Security JWT

## Decision: JWT Payload Fields Required by Backend
**Rationale**: The backend needs to extract specific user identity information from the JWT payload to enforce proper authorization.
**Alternatives considered**:
- Include only user ID in the token
- Include user ID, email, and roles
- Include user ID and email (selected approach)
**Decision**: Include user ID and email in the JWT payload to allow the backend to identify the authenticated user without additional database lookups.

## Decision: Token Expiration Duration and Validation Rules
**Rationale**: JWT tokens need appropriate expiration times to balance security and user experience.
**Alternatives considered**:
- Short-lived tokens (15-30 minutes): More secure but requires frequent refresh
- Medium-lived tokens (1-8 hours): Balance between security and UX (selected approach)
- Long-lived tokens (days): Better UX but less secure
**Decision**: Use 4-hour expiration for access tokens to balance security and user experience. The token should be validated for expiration, signature, and issuer on every protected API request.

## Decision: Strategy for Matching JWT User Identity with Route user_id
**Rationale**: The backend must ensure users can only access their own tasks, requiring correlation between JWT identity and requested user_id.
**Alternatives considered**:
- Extract user ID from JWT and compare with user_id in route parameters
- Use JWT user ID to override any user_id in requests (selected approach)
- Store session data linking tokens to user IDs (not compatible with stateless requirement)
**Decision**: Extract user ID from JWT token and use it to override any user_id parameter in requests, ensuring users can only access their own data regardless of what user_id is sent in the request.

## Decision: JWT Signing Algorithm
**Rationale**: Need to select a secure algorithm for signing JWT tokens that both frontend and backend can handle.
**Alternatives considered**:
- HS256 (symmetric): Simpler implementation with shared secret
- RS256 (asymmetric): More complex but allows different keys for signing/verification
- ES256 (elliptic curve): Modern but less widely supported
**Decision**: Use HS256 with a strong shared secret that is used by both Better Auth and FastAPI backend for token verification.

## Decision: Frontend API Client Strategy for Token Attachment
**Rationale**: The frontend must automatically attach JWT tokens to all API requests to protected endpoints.
**Alternatives considered**:
- Manual token attachment for each request
- Axios interceptors to automatically add Authorization header (selected approach)
- Custom API wrapper with automatic token inclusion
**Decision**: Implement axios interceptors in the frontend to automatically attach the JWT token to all outgoing API requests in the Authorization: Bearer <token> format.

## Decision: Error Handling for Invalid JWTs
**Rationale**: The system needs consistent error handling when JWT validation fails.
**Alternatives considered**:
- Generic 401 responses for all auth failures
- Specific error messages for different validation failures
- Consistent 401 responses with standard error format (selected approach)
**Decision**: Return consistent 401 Unauthorized responses with a standard error format when JWT validation fails, regardless of the specific reason (expired, invalid signature, etc.).