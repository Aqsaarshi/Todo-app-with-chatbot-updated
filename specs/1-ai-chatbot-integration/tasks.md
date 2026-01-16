# Tasks: AI Todo Chatbot Integration

**Input**: Design documents from `/specs/1-ai-chatbot-integration/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Paths shown below assume web app structure based on plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan in backend/src/ and frontend/src/
- [x] T002 Install required dependencies for Cohere API integration in backend/requirements.txt
- [x] T003 [P] Configure environment variables for Cohere API in backend/.env.example and frontend/.env.local.example

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Setup database schema for Conversation, Message, and ToolCall entities in backend/src/models/
- [x] T005 [P] Implement JWT authentication middleware for chat endpoints in backend/src/middleware/
- [x] T006 [P] Setup API routing structure for chat endpoints in backend/src/api/chat.py
- [x] T007 Create base models: Conversation, Message, and ToolCall in backend/src/models/
- [x] T008 Configure error handling and logging infrastructure for chat functionality
- [x] T009 Setup database migration framework for new chat entities

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Natural Language Task Management (Priority: P1) 🎯 MVP

**Goal**: Enable users to interact with their todo list using natural language commands to perform task operations

**Independent Test**: Can be fully tested by sending natural language commands to the chatbot and verifying that the appropriate task operations are performed and persisted in the database.

### Implementation for User Story 1

- [x] T010 [P] [US1] Create Conversation model in backend/src/models/conversation.py
- [x] T011 [P] [US1] Create Message model in backend/src/models/message.py
- [x] T012 [P] [US1] Create ToolCall model in backend/src/models/tool_call.py
- [x] T013 [US1] Implement CohereService in backend/src/services/cohere_service.py
- [x] T014 [US1] Implement MCP tools for task operations in backend/src/tools/mcp_tools.py
- [x] T015 [US1] Implement chat endpoint POST /api/{user_id}/chat in backend/src/api/chat.py
- [x] T016 [US1] Add conversation history retrieval logic in backend/src/services/conversation_service.py
- [x] T017 [US1] Add message persistence logic in backend/src/services/message_service.py
- [x] T018 [US1] Integrate CohereService with MCP tools in backend/src/services/chat_service.py
- [x] T019 [US1] Add validation and error handling for chat operations
- [x] T020 [US1] Add logging for chat operations and tool executions

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Chat Interface Integration (Priority: P2)

**Goal**: Provide a dedicated UI element for users to access the AI chatbot and interact with it

**Independent Test**: Can be tested by verifying that the chatbot interface is accessible, displays conversation history, and allows sending and receiving messages.

### Implementation for User Story 2

- [x] T021 [P] [US2] Create ChatBotIcon component in frontend/src/components/ChatBotIcon.tsx
- [x] T022 [US2] Create ChatInterface component in frontend/src/components/ChatInterface.tsx
- [x] T023 [US2] Implement API client for chat endpoints in frontend/src/services/apiClient.ts
- [x] T024 [US2] Add chat interface to dashboard page in frontend/src/pages/dashboard.tsx
- [x] T025 [US2] Implement conversation history display in ChatInterface component
- [x] T026 [US2] Connect frontend to backend chat API endpoints
- [x] T027 [US2] Add UI styling and responsive design for chat components

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Conversation Context and History (Priority: P3)

**Goal**: Enable the AI assistant to remember conversation context and maintain history for continuity

**Independent Test**: Can be tested by having a multi-turn conversation with the chatbot and verifying that it maintains context appropriately.

### Implementation for User Story 3

- [x] T028 [P] [US3] Enhance Conversation model with context management fields in backend/src/models/conversation.py
- [x] T029 [US3] Implement conversation context retrieval in backend/src/services/conversation_service.py
- [x] T030 [US3] Modify CohereService to include conversation context in prompts in backend/src/services/cohere_service.py
- [x] T031 [US3] Add conversation context awareness to MCP tools in backend/src/tools/mcp_tools.py
- [x] T032 [US3] Implement conversation listing endpoint GET /api/{user_id}/conversations in backend/src/api/chat.py
- [x] T033 [US3] Implement message history endpoint GET /api/{user_id}/conversations/{conversation_id}/messages in backend/src/api/chat.py
- [x] T034 [US3] Update frontend to support multiple conversations and context switching

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T035 [P] Update documentation with chatbot usage instructions in docs/
- [x] T036 Code cleanup and refactoring across chatbot components
- [x] T037 Performance optimization for Cohere API calls and database queries
- [x] T038 [P] Add comprehensive unit tests for backend services in backend/tests/
- [x] T039 Security hardening for JWT validation and user data isolation
- [x] T040 Run quickstart.md validation to ensure complete functionality

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 backend implementation
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on US1 backend implementation

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "Create Conversation model in backend/src/models/conversation.py"
Task: "Create Message model in backend/src/models/message.py"
Task: "Create ToolCall model in backend/src/models/tool_call.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence