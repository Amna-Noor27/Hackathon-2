---
id: 1
title: Todo Fullstack Webapp Constitution
stage: constitution
date: 2026-01-19
surface: agent
model: claude-haiku-4-5-20251001
feature: none
branch: master
user: user
command: sp.constitution
labels: [constitution,fullstack,todo,webapp,hackathon]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

Project: Todo Full-Stack Web Application (Hackathon Phase-2)
Core principles:
- Spec-driven development: all implementation must strictly follow approved specs
- Agentic workflow compliance: spec plan tasks implementation (no manual coding)
- Security-first design: authentication, authorization, and user isolation enforced by default
- Deterministic behavior: APIs and UI must behave consistently across users and sessions
- Full-stack coherence: frontend, backend, and database must integrate without mismatches

Key standards:
- No implementation without an approved spec and plan
- All API behavior must be explicitly defined in specs
- Authentication must use Better Auth with JWT tokens
- All backend routes must validate JWT and enforce task ownership
- All database queries must be user-scoped
- REST APIs must follow HTTP semantics and status codes
- Errors must be explicit, predictable, and documented
- Frontend must consume APIs exactly as specified
- No hard-coded secrets; environment variables only

Constraints:
- No manual coding; all code generated via Claude Code
- Technology stack is fixed and non-negotiable:
  - Frontend: Next.js 16+ (App Router)
  - Backend: Python FastAPI
  - ORM: SQLModel
  - Database: Neon Serverless PostgreSQL
  - Auth: Better Auth (JWT-based)
- All endpoints require valid JWT after authentication
- Stateless backend authentication (JWT only)
- Multi-user support is mandatory
- Data persistence required across sessions

Success criteria:
All three specs (Backend, Auth, Frontend) are fully implemented and integrated
Users can sign up, sign in, and manage only their own tasks
Unauthorized requests return, 401 consistently
Task ownership is enforced on every CRUD operation
Application works end-to-end as a full-stack system
Specs, plans, and iterations are reviewable and traceable
Project passes hackathon evaluation based on process and correctness

## Response snapshot

Updated the constitution file with the project-specific principles, standards, constraints, and success criteria for the Todo Full-Stack Web Application.

## Outcome

- ✅ Impact: Created new constitution file with project-specific principles, standards, constraints and success criteria
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md
- 🔁 Next prompts: None needed at this stage
- 🧠 Reflection: Successfully created a comprehensive constitution document that captures all the project requirements and constraints

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Continue with spec development