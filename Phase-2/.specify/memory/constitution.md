<!--
Sync Impact Report:
- Version change: N/A (initial creation) -> 1.0.0
- Modified principles:
  - Core principles (5)
  - Key standards (9)
  - Project Constraints (6)
  - Success Criteria (7)
- Added sections: "Key Standards", "Project Constraints", "Success Criteria"
- Removed sections: None (template sections were replaced)
- Templates requiring updates:
  - .specify/templates/plan-template.md: ✅ updated (mentions "Constitution Check" which aligns with new principles)
  - .specify/templates/spec-template.md: ✅ updated (scope/requirements alignment aligns with new principles)
  - .specify/templates/tasks-template.md: ✅ updated (task categorization aligns with new principle-driven task types)
  - .specify/templates/commands/*.md: ⚠ pending (will need to verify command files individually if they contain specific references)
- Follow-up TODOs: None
-->
# Todo Full-Stack Web Application (Hackathon Phase-2) Constitution

## Core Principles

### I. Spec-Driven Development
All implementation must strictly follow approved specifications (specs). This ensures clarity, consistency, and alignment with project goals.

### II. Agentic Workflow Compliance
Development must adhere to the Agentic Dev Stack workflow: Write spec → Generate plan → Break into tasks → Implement via Claude Code. Manual coding is not permitted.

### III. Security-First Design
Authentication, authorization, and user isolation must be enforced by default across all layers of the application to protect data and user privacy.

### IV. Deterministic Behavior
APIs and the user interface must behave consistently and predictably across different users and sessions, eliminating ambiguity and enhancing user experience.

### V. Full-Stack Coherence
Frontend, backend, and database components must integrate seamlessly without mismatches in data contracts, business logic, or user experience.

## Key Standards

### 1. Development Process
No implementation is allowed without an approved specification and detailed implementation plan.

### 2. API Definition
All API behavior, including inputs, outputs, and error handling, must be explicitly defined in the specifications.

### 3. Authentication Protocol
Authentication must exclusively use Better Auth with JSON Web Tokens (JWT).

### 4. Backend Authorization
All backend routes must validate incoming JWTs and strictly enforce task ownership, ensuring users can only access their own data.

### 5. Database Query Scope
All database queries must be user-scoped, preventing unauthorized access to other users' data.

### 6. REST API Semantics
REST APIs must strictly adhere to HTTP semantics and appropriate status codes for all operations.

### 7. Error Handling
Errors must be explicit, predictable, and thoroughly documented for both API consumers and frontend integration.

### 8. Frontend API Consumption
The frontend must consume backend APIs exactly as specified in the API contracts, ensuring consistent data flow and behavior.

### 9. Secret Management
No hard-coded secrets are permitted; all sensitive information must be managed through environment variables.

## Project Constraints

### 1. Automation Mandate
No manual coding is allowed; all code for the project must be generated exclusively via Claude Code.

### 2. Fixed Technology Stack
The technology stack is fixed and non-negotiable:
-   **Frontend**: Next.js 16+ (App Router)
-   **Backend**: Python FastAPI
-   **ORM**: SQLModel
-   **Database**: Neon Serverless PostgreSQL
-   **Authentication**: Better Auth (JWT-based)

### 3. JWT Requirement
All API endpoints, after initial authentication, require a valid JWT for access.

### 4. Stateless Backend
Backend authentication must be stateless, relying solely on JWTs for session management.

### 5. Multi-User Support
The application must fully support multiple distinct users.

### 6. Data Persistence
All user and task data must be persistently stored across sessions.

## Success Criteria

### 1. Full Implementation & Integration
All three primary specifications (Backend, Authentication, Frontend) must be fully implemented and seamlessly integrated.

### 2. User & Task Management
Users must be able to sign up, sign in, and manage only their own tasks effectively.

### 3. Unauthorized Access Handling
Unauthorized requests to any endpoint must consistently return a 401 HTTP status code.

### 4. Task Ownership Enforcement
Task ownership must be rigorously enforced on every Create, Read, Update, and Delete (CRUD) operation.

### 5. End-to-End Functionality
The application must function correctly end-to-end as a complete full-stack system.

### 6. Traceability
All specifications, plans, and development iterations must be reviewable and fully traceable.

### 7. Hackathon Evaluation
The project must successfully pass the hackathon evaluation criteria based on both process adherence and correctness of implementation.

## Governance
This Constitution supersedes all other project practices and documentation. Amendments require formal documentation, explicit approval from project stakeholders, and a clear migration plan if changes impact existing systems. All Pull Requests (PRs) and code reviews must explicitly verify compliance with these principles, standards, and constraints. Any introduction of complexity must be thoroughly justified.

**Version**: 1.0.0 | **Ratified**: 2026-01-19 | **Last Amended**: 2026-01-19
