# Data Model: Todo Full-Stack Web Application

**Date**: 2025-12-27
**Feature**: 002-todo-fullstack-web-app
**Related Plan**: [plan.md](plan.md)

## Entity Models

### User Entity
**Purpose**: Represents application users with authentication credentials

```python
class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, nullable=False)
    name: str
    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    tasks: List["Task"] = Relationship(back_populates="user")
```

**Validation Rules**:
- Email must be unique and valid email format
- Password must meet minimum security requirements
- Name is required

### Task Entity
**Purpose**: Represents individual todo items with user ownership

```python
class Task(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", nullable=False)
    title: str = Field(nullable=False)
    description: Optional[str] = None
    completed: bool = Field(default=False)
    priority: str = Field(default="medium")  # low, medium, high
    due_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    user: Optional[User] = Relationship(back_populates="tasks")
```

**Validation Rules**:
- Title is required (min 1 character)
- Priority must be one of: "low", "medium", "high"
- Due date cannot be in the past (optional validation)
- User_id must reference an existing user

## Database Schema

### Tables and Relationships
```
Users Table:
- id (UUID, Primary Key, Unique)
- email (VARCHAR, Unique, Not Null)
- name (VARCHAR, Not Null)
- password_hash (VARCHAR, Not Null)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

Tasks Table:
- id (UUID, Primary Key, Unique)
- user_id (UUID, Foreign Key to Users.id, Not Null)
- title (VARCHAR, Not Null)
- description (TEXT, Nullable)
- completed (BOOLEAN, Default: False)
- priority (VARCHAR, Default: "medium")
- due_date (TIMESTAMP, Nullable)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

### Indexes
- Users: Index on `email` (unique) for authentication performance
- Tasks: Index on `user_id` for user-specific queries
- Tasks: Index on `user_id, completed` for filtered queries
- Tasks: Index on `user_id, priority` for priority-based queries
- Tasks: Index on `user_id, due_date` for date-based queries
- Tasks: Index on `user_id, created_at` for chronological queries

## State Transitions

### Task States
- **Active**: New task created, completed=False
- **Completed**: Task marked as completed, completed=True
- **Deleted**: Task removed from user's list (soft delete with deleted_at field)

### User States
- **Active**: User account created and verified
- **Suspended**: User account temporarily disabled (future feature)
- **Deleted**: User account removed (soft delete with deleted_at field)

## Data Validation Rules

### Business Rules
1. **Ownership**: Users can only access tasks they own (user_id validation)
2. **Uniqueness**: Email addresses must be unique across all users
3. **Completeness**: Tasks must have a title (non-empty)
4. **Security**: No user can access another user's tasks

### Constraints
- Foreign key constraints between users and tasks
- Unique constraints on user emails
- Not-null constraints on required fields
- Check constraints for priority field values