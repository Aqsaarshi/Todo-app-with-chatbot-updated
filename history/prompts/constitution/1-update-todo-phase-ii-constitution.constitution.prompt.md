---
id: 1
title: Update Todo Phase II Constitution
stage: constitution
date: 2025-12-27
surface: agent
model: Claude Sonnet 4.5
feature: Todo Phase II
branch: main
user: User
command: sp.constitution
labels: [constitution, todo-app, phase-ii]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - null
---

## Prompt

```text
Name: Todo Phase II Constitution
Description: This constitution defines the rules, architecture, and operational principles for Phase II of the multi-user full stack Todo application. It guides all agents and skills in implementing the web application consistently and according to specifications.

Key Responsibilities:
- Follow Spec-Kit Plus specifications for features, APIs, database, and UI
- Ensure proper monorepo organization:
  hackathon-todo/
    ├── .spec-kit/
    ├── specs/
    ├── frontend/
    ├── backend/
    ├── docker-compose.yml
    └── README.md
- Maintain coding standards and clean code principles for both frontend and backend
- Coordinate between frontend (Next.js 16+ App Router) and backend (FastAPI) layers
- Ensure secure user authentication and session management using Better Auth
- Implement JWT authentication for frontend-backend communication
- Enforce user data isolation on all API endpoints
- Manage database design, migrations, and queries using SQLModel and Neon PostgreSQL
- Follow API conventions for task CRUD:
    GET /api/{user_id}/tasks
    POST /api/{user_id}/tasks
    GET /api/{user_id}/tasks/{id}
    PUT /api/{user_id}/tasks/{id}
    DELETE /api/{user_id}/tasks/{id}
    PATCH /api/{user_id}/tasks/{id}/complete
- Verify all authentication flows and token handling
- Implement frontend UI components with Next.js, TypeScript, and Tailwind CSS
- Use CLAUDE.md files to provide context at root, frontend, and backend levels
- Update specs if requirements change and reference them correctly
- Test and iterate on features, API endpoints, and database queries

When to use: Reference this constitution whenever implementing or reviewing any Phase II feature, backend or frontend logic, database schema, authentication flow, or integration task. It ensures all agents and skills follow the same architecture, security standards, and project workflow.
```

## Response snapshot

I have successfully updated the project constitution based on your input. Here's the summary:

## Summary

**Version Bump Rationale**: This is the initial version (1.0.0) of the Todo Phase II Constitution, created to define the rules, architecture, and operational principles for the multi-user full stack Todo application. The version follows semantic versioning as a minor addition to the project governance.

**Files Updated**:
- `.specify/memory/constitution.md` - Contains the new Todo Phase II Constitution with 6 core principles covering spec-driven development, monorepo organization, authentication, API contracts, full-stack coordination, and database management.

**Commit Message**:
```
docs: add Todo Phase II Constitution with core principles and governance
```

The updated constitution includes:
1. Core Principles: Spec-Driven Development Compliance, Monorepo Organization, Secure Authentication & Data Isolation, API Contract Compliance, Full-Stack Coordination, and Database Management
2. Technology Stack and Architecture Standards section
3. Development Workflow and Quality Standards section
4. Governance section with compliance requirements

All placeholders from the original template have been replaced with concrete values based on your input, and the constitution aligns with the requirements for Phase II of the multi-user full stack Todo application.

## Outcome

- ✅ Impact: Created new constitution for Todo Phase II project
- 🧪 Tests: No tests required for documentation update
- 📁 Files: Updated .specify/memory/constitution.md with new constitution
- 🔁 Next prompts: Ready for spec, plan, and task creation for Todo Phase II
- 🧠 Reflection: Constitution properly captures all key responsibilities and requirements from user input

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin creating feature specifications for Todo Phase II