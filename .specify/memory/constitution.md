<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.1.0
- Modified principles: API Contract Compliance (expanded to include chat endpoints), Database Management with SQLModel and Neon PostgreSQL (expanded to include conversation persistence)
- Added principles: AI-Powered Natural Language Processing, MCP Tools Integration, Stateless Server Architecture
- Added sections: AI Chatbot Technology Stack and Architecture Standards, Enhanced Development Workflow and Quality Standards
- Templates requiring updates: ✅ .specify/templates/plan-template.md, ✅ .specify/templates/spec-template.md, ✅ .specify/templates/tasks-template.md
- Follow-up TODOs: None
-->
# Todo AI Chatbot Constitution

## Core Principles

### Spec-Driven Development Compliance
Follow Spec-Kit Plus specifications for features, APIs, database, and UI; All implementations must align with documented specs

### Monorepo Organization
Maintain proper monorepo structure with frontend, backend, specs, and configuration files organized in dedicated directories

### Secure Authentication & Data Isolation
Implement JWT authentication for frontend-backend communication; Enforce user data isolation on all API endpoints; Ensure conversation data is properly isolated by user

### API Contract Compliance
Follow established API conventions for task CRUD operations with user_id scoping; Maintain consistent endpoint patterns; Implement new chat endpoints following the same standards: POST /api/{user_id}/chat for AI interactions

### Full-Stack Coordination
Coordinate between frontend (Next.js 16+ App Router) and backend (FastAPI) layers; Implement proper integration patterns; Support AI chat interface integration with existing task management UI

### Database Management with SQLModel and Neon PostgreSQL
Manage database design, migrations, and queries using SQLModel and Neon PostgreSQL; Follow proper schema evolution practices; Persist conversation histories and messages in addition to task data

### AI-Powered Natural Language Processing
Integrate Cohere API for natural language understanding and response generation; Map user intents to appropriate task operations; Ensure AI responses are contextually relevant and accurate

### MCP Tools Integration
Leverage MCP tools (add_task, list_tasks, complete_task, update_task, delete_task) for backend operations; Map user intent to correct tool calls; Confirm actions in natural language after tool execution

### Stateless Server Architecture
Maintain stateless server design where every request is independent; No in-memory session data for conversations; Retrieve conversation history from database for each request

## Technology Stack and Architecture Standards
Use Next.js, TypeScript, and Tailwind CSS for frontend UI components; Use FastAPI for backend; Implement Better Auth for session management; Apply clean code principles for both frontend and backend; Integrate Cohere API for LLM processing; Implement MCP tools for task operations; Use environment variables for API keys (COHERE_API_KEY)

## Development Workflow and Quality Standards
Maintain coding standards and clean code principles; Use CLAUDE.md files to provide context at root, frontend, and backend levels; Update specs if requirements change and reference them correctly; Test and iterate on features, API endpoints, database queries, and AI interactions; Ensure proper error handling for AI API calls and tool executions

## Governance
Reference this constitution whenever implementing or reviewing any AI chatbot feature, backend or frontend logic, database schema, authentication flow, integration task, or AI response handling; Ensure all agents and skills follow the same architecture, security standards, and project workflow; Maintain backward compatibility with existing task management features

**Version**: 1.1.0 | **Ratified**: 2025-12-27 | **Last Amended**: 2026-01-10