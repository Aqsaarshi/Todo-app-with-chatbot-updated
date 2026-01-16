# Data Model: AI Todo Chatbot Integration

## Overview
This document defines the data models for the AI Todo Chatbot feature, including conversations, messages, and their relationships to existing task entities.

## Entity: Conversation
Represents a session of interaction between a user and the AI assistant.

**Fields**:
- `id` (Integer): Primary key, auto-incrementing
- `user_id` (String): Foreign key referencing the user (from Better Auth)
- `created_at` (DateTime): Timestamp when conversation was initiated
- `updated_at` (DateTime): Timestamp when conversation was last updated
- `title` (String, optional): Auto-generated title based on first message or topic

**Relationships**:
- One-to-many with Message (conversation.messages)
- Belongs to User (conversation.user)

**Validation Rules**:
- `user_id` is required
- `created_at` defaults to current timestamp
- `updated_at` updates automatically on changes

## Entity: Message
Represents a single communication in a conversation, either from user or assistant.

**Fields**:
- `id` (Integer): Primary key, auto-incrementing
- `conversation_id` (Integer): Foreign key referencing the conversation
- `sender_type` (String): Enum {'user', 'assistant'}
- `content` (String): The actual message content
- `timestamp` (DateTime): When the message was sent/received
- `metadata` (JSON, optional): Additional data like tool calls, confidence scores

**Relationships**:
- Belongs to Conversation (message.conversation)
- One-to-one with ToolCall (message.tool_call) if applicable

**Validation Rules**:
- `conversation_id` is required
- `sender_type` must be 'user' or 'assistant'
- `content` is required and must be non-empty
- `timestamp` defaults to current timestamp

## Entity: ToolCall
Represents an action taken by the AI assistant based on user request.

**Fields**:
- `id` (Integer): Primary key, auto-incrementing
- `message_id` (Integer): Foreign key referencing the message that triggered this call
- `tool_name` (String): Name of the tool called (add_task, list_tasks, etc.)
- `parameters` (JSON): Parameters passed to the tool
- `result` (JSON, optional): Result of the tool execution
- `executed_at` (DateTime): When the tool was executed

**Relationships**:
- Belongs to Message (tool_call.message)

**Validation Rules**:
- `message_id` is required
- `tool_name` is required and must be one of the allowed tools
- `parameters` must match the expected schema for the tool

## Relationship Diagram

```
User ||--o{ Conversation ||--o{ Message }o--|| ToolCall
```

## State Transitions

### Conversation
- Created when user initiates first chat
- Updated when new messages are added
- Remains active indefinitely (no automatic expiration)

### Message
- Created when user sends a message or assistant responds
- Immutable after creation (no updates allowed)

### ToolCall
- Created when assistant decides to execute a tool
- Result populated after tool execution completes