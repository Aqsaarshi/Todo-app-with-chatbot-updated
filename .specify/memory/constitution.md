<!--
Sync Impact Report:
- Version change: N/A → 1.0.0
- Added principles: Spec-Driven Development Compliance, Monorepo Organization, Secure Authentication & Data Isolation, API Contract Compliance, Full-Stack Coordination, Database Management with SQLModel and Neon PostgreSQL
- Added sections: Technology Stack and Architecture Standards, Development Workflow and Quality Standards
- Templates requiring updates: N/A (new constitution)
- Follow-up TODOs: None
-->
# Todo Phase II Constitution

## Core Principles

### Spec-Driven Development Compliance
Follow Spec-Kit Plus specifications for features, APIs, database, and UI; All implementations must align with documented specs

### Monorepo Organization
Maintain proper monorepo structure with frontend, backend, specs, and configuration files organized in dedicated directories

### Secure Authentication & Data Isolation
Implement JWT authentication for frontend-backend communication; Enforce user data isolation on all API endpoints

### API Contract Compliance
Follow established API conventions for task CRUD operations with user_id scoping; Maintain consistent endpoint patterns

### Full-Stack Coordination
Coordinate between frontend (Next.js 16+ App Router) and backend (FastAPI) layers; Implement proper integration patterns

### Database Management with SQLModel and Neon PostgreSQL
Manage database design, migrations, and queries using SQLModel and Neon PostgreSQL; Follow proper schema evolution practices

## Technology Stack and Architecture Standards
Use Next.js, TypeScript, and Tailwind CSS for frontend UI components; Use FastAPI for backend; Implement Better Auth for session management; Apply clean code principles for both frontend and backend

## Development Workflow and Quality Standards
Maintain coding standards and clean code principles; Use CLAUDE.md files to provide context at root, frontend, and backend levels; Update specs if requirements change and reference them correctly; Test and iterate on features, API endpoints, and database queries

## Governance
Reference this constitution whenever implementing or reviewing any Phase II feature, backend or frontend logic, database schema, authentication flow, or integration task; Ensure all agents and skills follow the same architecture, security standards, and project workflow

**Version**: 1.0.0 | **Ratified**: 2025-12-27 | **Last Amended**: 2025-12-27