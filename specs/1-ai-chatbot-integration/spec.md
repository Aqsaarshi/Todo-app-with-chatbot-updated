# Feature Specification: AI Todo Chatbot Integration

**Feature Branch**: `1-ai-chatbot-integration`
**Created**: 2026-01-10
**Status**: Draft
**Input**: User description: "AI Todo Chatbot Implementation ## Project Context You are tasked with implementing an AI-powered Todo Chatbot for an existing **full-stack Todo application**. - **Backend**: Python FastAPI + SQLModel ORM + Neon Serverless PostgreSQL - **Frontend**: Next.js 16+ with Better Auth JWT authentication - **Current Features**: Full CRUD for tasks, user authentication - **New Feature**: AI Chatbot interface using **Cohere LLM** and **MCP/OpenAI Agents SDK** - Frontend will have a **chatbot icon UI** to open the chat interface. The chatbot should allow users to interact via **natural language** to perform all task operations while keeping the **server stateless**. All conversation and task data should persist in NeonDB. --- ## Objectives 1. Map **user natural language commands** to MCP/OpenAI Agent tools: - `add_task`, `list_tasks`, `complete_task`, `update_task`, `delete_task` 2. Use **Cohere LLM** to generate assistant responses and identify tool usage. 3. Store **all conversations, messages, and task changes** in NeonDB. 4. Ensure **JWT authentication** for user-specific tasks. 5. Maintain **stateless backend**; no in-memory sessions. --- ## Cohere + MCP Integration Instructions - **Cohere Service**: - Replace Gemini code with **Cohere API**. - Use `COHERE_API_KEY` from environment variables. - Implement methods: 1. `generate_response(prompt: str) -> str` 2. `generate_response_with_context(question: str, context: List[str], mode: str = "full-book") -> str` 3. `validate_response_against_context(response: str, context: List[str]) -> bool` 4. `generate_response_with_latency_safeguards(prompt: str, max_tokens: int = 1000) -> str` - Example: ```python import cohere import os class CohereService: def __init__(self): self.client = cohere.Client(os.environ.get("COHERE_API_KEY")) def generate_response(self, prompt: str, max_tokens: int = 500) -> str: response = self.client.generate( model="command", prompt=prompt, max_tokens=max_tokens ) return response.generations[0].text ``` - **MCP/OpenAI Agents Tools**: - `add_task(user_id, title, description) -> task_id, status, title` - `list_tasks(user_id, status) -> array of tasks` - `complete_task(user_id, task_id) -> task_id, status, title` - `update_task(user_id, task_id, title?, description?) -> task_id, status, title` - `delete_task(user_id, task_id) -> task_id, status, title` - Map **user intent → correct tool**. - Always **confirm actions in natural language**. --- ## Conversation Flow 1. Receive user message via `POST /api/{user_id}/chat`. 2. Verify JWT → extract `user_id`. 3. Fetch conversation history from **NeonDB**. 4. Store user message in `messages` table. 5. Pass `history + new message` to **CohereService**. 6. Cohere generates response + identifies tool calls. 7. Execute **MCP/OpenAI Agent tools** with parameters. 8. Store assistant response in `messages` table. 9. Return JSON: ```json { "conversation_id": integer, "response": string, "tool_calls": [ ... ] }"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Natural Language Task Management (Priority: P1)

As a user, I want to interact with my todo list using natural language so that I can manage my tasks more efficiently without navigating through UI elements.

**Why this priority**: This is the core functionality of the AI chatbot and provides the primary value proposition of the feature.

**Independent Test**: Can be fully tested by sending natural language commands to the chatbot and verifying that the appropriate task operations are performed and persisted in the database.

**Acceptance Scenarios**:

1. **Given** a user is authenticated and has access to the chatbot interface, **When** the user sends a message like "Add a task to buy groceries", **Then** a new task with the title "buy groceries" is created and persisted in the database, and the chatbot confirms the action in natural language.

2. **Given** a user has existing tasks in their list, **When** the user sends a message like "Show me my tasks", **Then** the chatbot returns a natural language summary of the user's tasks.

3. **Given** a user has tasks in their list, **When** the user sends a message like "Mark the grocery task as complete", **Then** the appropriate task is marked as complete in the database, and the chatbot confirms the action in natural language.

---

### User Story 2 - Chat Interface Integration (Priority: P2)

As a user, I want to access the AI chatbot through a dedicated UI element so that I can easily switch between traditional UI and AI-powered task management.

**Why this priority**: Essential for user adoption and providing a seamless experience alongside existing UI features.

**Independent Test**: Can be tested by verifying that the chatbot interface is accessible, displays conversation history, and allows sending and receiving messages.

**Acceptance Scenarios**:

1. **Given** a user is on any page of the application, **When** the user clicks the chatbot icon, **Then** a chat interface panel opens where they can interact with the AI assistant.

---

### User Story 3 - Conversation Context and History (Priority: P3)

As a user, I want the AI assistant to remember our conversation context so that I can have a natural, flowing conversation about my tasks.

**Why this priority**: Enhances user experience by providing continuity in conversations, but not essential for core functionality.

**Independent Test**: Can be tested by having a multi-turn conversation with the chatbot and verifying that it maintains context appropriately.

**Acceptance Scenarios**:

1. **Given** a user is in an ongoing conversation with the chatbot, **When** the user refers to a previous task by context (e.g., "update that task"), **Then** the chatbot correctly identifies the referenced task based on conversation history.

---

### Edge Cases

- What happens when the Cohere API is unavailable or returns an error?
- How does the system handle ambiguous user requests that could map to multiple possible actions?
- What happens when a user tries to perform an action on a task that doesn't exist?
- How does the system handle very long conversations that might exceed API token limits?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST authenticate all chat requests using JWT tokens to ensure user-specific task operations
- **FR-002**: System MUST map natural language user commands to appropriate task operations (add, list, complete, update, delete)
- **FR-003**: Users MUST be able to initiate conversations with the AI assistant via a chat interface
- **FR-004**: System MUST persist all conversation messages and task changes in NeonDB
- **FR-005**: System MUST generate natural language responses that confirm actions taken based on user requests
- **FR-006**: System MUST maintain a stateless backend architecture with no in-memory session data
- **FR-007**: System MUST integrate with Cohere API for natural language processing and response generation
- **FR-008**: System MUST execute appropriate MCP/OpenAI Agent tools based on identified user intent
- **FR-009**: System MUST provide a frontend chat interface accessible via a dedicated UI element

### Key Entities

- **Conversation**: Represents a session of interaction between user and AI assistant, containing multiple messages
- **Message**: A single communication in a conversation, either from user or assistant
- **Task**: A todo item that can be created, read, updated, completed, or deleted through the chat interface

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully create, list, update, complete, and delete tasks using natural language commands with at least 90% accuracy
- **SC-002**: 85% of users who try the chatbot feature use it at least once per week for task management
- **SC-003**: Users can complete common task operations 30% faster using the chatbot compared to traditional UI methods
- **SC-004**: System maintains 99% uptime for chat functionality during business hours