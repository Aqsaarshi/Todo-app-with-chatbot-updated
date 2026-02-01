---
id: 1
title: Update Chatbot Constitution
stage: constitution
date: 2026-01-10
surface: agent
model: Qwen
feature: ai-chatbot
branch: main
user: user
command: /sp.constitution
labels: [constitution, ai, chatbot, todo]
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

```
/sp.constitution # Todo AI Chatbot Constitution Prompt

## Project Context
You are assisting in integrating an AI-powered chatbot into a full-stack Todo application. The backend is built using **Python FastAPI**, **SQLModel ORM**, and **Neon Serverless PostgreSQL**. The frontend is **Next.js 16+** with **Better Auth JWT** authentication. The application currently supports full CRUD operations for tasks and user authentication.

This chatbot will allow users to **manage tasks via natural language** using **Cohere API** for LLM processing and **MCP tools / OpenAI Agents SDK** for task operations. All operations must persist in NeonDB while keeping the server stateless.

---

## Objectives
1. Enable AI-driven conversation for **all Todo CRUD operations**.
2. Use **Cohere API** to generate responses and understand user commands.
3. Use **MCP tools** (add_task, list_tasks, complete_task, update_task, delete_task) to perform backend operations.
4. Persist conversations, messages, and task changes in **NeonDB**.
5. Respect **JWT-based authentication** to ensure tasks are user-specific.
6. Stateless server: every request should be independent; no in-memory session data.

---

## Cohere + MCP Integration Instructions
- **Cohere LLM**:
  - Use the `COHERE_API_KEY` from environment variables.
  - Generate responses to user's messages while identifying intended actions.
- **MCP Tools**:
  - `add_task(user_id, title, description) -> task_id, status, title`
  - `list_tasks(user_id, status) -> array of tasks`
  - `complete_task(user_id, task_id) -> task_id, status, title`
  - `update_task(user_id, task_id, title?, description?) -> task_id, status, title`
  - `delete_task(user_id, task_id) -> task_id, status, title`
- The agent **must map user intent** to the correct tool.
- Always **confirm actions** in natural language after performing a tool operation.

---

## Conversation Handling
1. Receive user message via `POST /api/{user_id}/chat`.
2. Fetch conversation history from NeonDB (conversations + messages tables).
3. Build message array: `history + new message`.
4. Store user message in **messages table**.
5. Pass message array to **Cohere LLM**.
6. Cohere LLM generates assistant response **and identifies MCP tools to call**.
7. Call MCP tools with user_id and parameters extracted from user input.
8. Store assistant response in **messages table**.
9. Return JSON response:
```json
{
  "conversation_id": integer,
  "response": string,
  "tool_calls": [ ... ]
}
```
 cohere key YOUR_COHERE_API_KEY_HERE
```

## Response

Based on the user input, I'll update the project constitution to reflect the new AI chatbot functionality while preserving the existing principles that still apply. I'll incorporate the new requirements for Cohere API integration, MCP tools usage, and conversation handling.

```

## Response snapshot

Based on the information provided, I can see that there's already a constitution file in place, but it appears to be for a different phase of the project (Todo Phase II). Since you're working on integrating an AI chatbot with Cohere API and MCP tools, I'll update the constitution to reflect the new requirements and principles for this phase.

Let me create an updated constitution that incorporates the new AI chatbot functionality while preserving the existing principles that still apply:

I've successfully updated the constitution file at `.specify/memory/constitution.md` to include the new AI chatbot functionality while preserving the existing principles. The updated constitution now includes:

1. Added new principles:
   - AI-Powered Natural Language Processing
   - MCP Tools Integration
   - Stateless Server Architecture

2. Modified existing principles:
   - API Contract Compliance (expanded to include chat endpoints)
   - Database Management with SQLModel and Neon PostgreSQL (expanded to include conversation persistence)

3. Updated technology stack and development workflow sections to include AI-specific requirements

The version has been updated from 1.0.0 to 1.1.0 to reflect these changes. The templates have also been checked for consistency.

## Outcome

- ✅ Impact: Updated constitution to include AI chatbot functionality with Cohere API and MCP tools integration
- 🧪 Tests: N/A (documentation update)
- 📁 Files: .specify/memory/constitution.md updated
- 🔁 Next prompts: Can proceed with feature specification based on updated constitution
- 🧠 Reflection: The constitution now properly reflects the AI chatbot requirements while maintaining existing project principles

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A