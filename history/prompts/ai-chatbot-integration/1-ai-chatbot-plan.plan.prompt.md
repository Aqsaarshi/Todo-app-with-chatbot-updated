---
id: 1
title: AI Chatbot Plan
stage: plan
date: 2026-01-10
surface: agent
model: Qwen
feature: ai-chatbot-integration
branch: 1-ai-chatbot-integration
user: user
command: /sp.plan
labels: [plan, ai, chatbot, todo]
links:
  spec: ../specs/1-ai-chatbot-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-ai-chatbot-integration/plan.md
  - specs/1-ai-chatbot-integration/research.md
  - specs/1-ai-chatbot-integration/data-model.md
  - specs/1-ai-chatbot-integration/contracts/chat-api.yaml
  - specs/1-ai-chatbot-integration/quickstart.md
  - QWEN.md
tests:
  - null
---

## Prompt

```
/sp.plan # Todo AI Chatbot - Phase III Action Plan

## Context
You are assisting in implementing an AI-powered chatbot for a full-stack Todo application. 
The backend uses Python FastAPI, SQLModel ORM, and Neon Serverless PostgreSQL. 
The frontend is Next.js 16+ with Better Auth JWT authentication.
The chatbot integrates **Cohere API** for LLM processing and **MCP tools / OpenAI Agents SDK** for task operations.
All operations must persist in NeonDB while keeping the server stateless.

## Objectives
- Provide a step-by-step plan to implement the AI chatbot feature.
- Include frontend, backend, AI agent, MCP tool integration, and database persistence.
- Ensure JWT authentication is respected and users only access their tasks.
- Integrate chatbot UI (icon/button) in the frontend.
- Replace any Gemini SDK code with Cohere API integration.

## Deliverables
The plan should provide:
1. **Backend Steps**: Chat endpoint, MCP tool integration, database updates, Cohere API setup.
2. **Frontend Steps**: Chat UI component, icon integration, API client setup, message display.
3. **AI Agent Steps**: Intent recognition, tool mapping, response generation, confirmation messages.
4. **Database Steps**: Store conversations, messages, and task updates in NeonDB.
5. **Security Steps**: JWT verification, user-specific task access, stateless server design.
6. **Testing & Iteration**: Unit tests for backend endpoints, integration tests for frontend-chatbot, validating AI responses.
7. **Deployment Notes**: Environment variable setup for COHERE_API_KEY, MCP configuration, frontend and backend deployment.

## Output Format
Provide the action plan in a **clear ordered list** or **numbered steps**, grouped by:
- Backend Implementation
- Frontend Implementation
- AI Agent Logic
- Database Integration
- Security & Authentication
- Testing & Deployment

## Constraints
- All backend operations must use MCP tools: add_task, list_tasks, complete_task, update_task, delete_task.
- Cohere API must handle natural language understanding and response generation.
- Chatbot server should remain stateless.
- Ensure smooth integration with existing Todo full-stack application.
```

## Response snapshot

I've created a comprehensive implementation plan for the AI Todo Chatbot feature, including:

1. Implementation Plan (plan.md): Outlined the technical context, architecture, and structure for the feature.

2. Research Document (research.md): Researched key decisions including Cohere API integration, MCP tools usage, conversation storage schema, and stateless architecture implementation.

3. Data Model (data-model.md): Defined the data models for Conversation, Message, and ToolCall entities with their relationships and validation rules.

4. API Contracts (contracts/chat-api.yaml): Specified the API endpoints for chat functionality, including request/response schemas and authentication requirements.

5. Quickstart Guide (quickstart.md): Created a developer guide with setup instructions and key components overview.

6. Agent Context (QWEN.md): Updated the agent context with information about the new technologies and patterns used in this feature.

All components follow the required architecture with Cohere API integration, MCP tools for task operations, JWT authentication, and stateless server design. The database schema supports storing conversations and messages while maintaining user data isolation.

## Outcome

- ✅ Impact: Comprehensive implementation plan created with all required components
- 🧪 Tests: N/A (planning phase)
- 📁 Files: Multiple planning documents created in specs/1-ai-chatbot-integration/
- 🔁 Next prompts: Ready for task breakdown with /sp.tasks
- 🧠 Reflection: Plan addresses all requirements including Cohere integration, MCP tools, and security

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A