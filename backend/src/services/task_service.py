from typing import List, Optional
from uuid import UUID
import logging

from sqlmodel import select, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from ..models.task import Task, TaskCreate, TaskUpdate


# =========================
# CREATE TASK
# =========================
async def create_task(
    session: AsyncSession,
    user_id: UUID,
    task_create: TaskCreate
) -> Task:
    """Create a new task for a user"""

    db_task = Task(
        **task_create.model_dump(),
        user_id=user_id
    )

    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)

    return db_task


# =========================
# GET ALL TASKS
# =========================
async def get_tasks(
    session: AsyncSession,
    user_id: UUID,
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    sort: str = "created_at",
    order: str = "desc"
) -> List[Task]:
    """Get all tasks for a user with optional filters"""

    statement = select(Task).where(Task.user_id == user_id)

    # Filters
    if completed is not None:
        statement = statement.where(Task.completed == completed)

    if priority is not None:
        statement = statement.where(Task.priority == priority)

    # Sorting
    if sort == "created_at":
        statement = (
            statement.order_by(Task.created_at.desc())
            if order == "desc"
            else statement.order_by(Task.created_at.asc())
        )

    elif sort == "due_date":
        statement = (
            statement.order_by(Task.due_date.desc())
            if order == "desc"
            else statement.order_by(Task.due_date.asc())
        )

    elif sort == "priority":
        statement = (
            statement.order_by(Task.priority.desc())
            if order == "desc"
            else statement.order_by(Task.priority.asc())
        )

    elif sort == "title":
        statement = (
            statement.order_by(Task.title.desc())
            if order == "desc"
            else statement.order_by(Task.title.asc())
        )

    result = await session.exec(statement)
    return result.all()


# =========================
# GET SINGLE TASK
# =========================
async def get_task(
    session: AsyncSession,
    task_id: UUID,
    user_id: UUID
) -> Optional[Task]:
    """Get a specific task by ID for a user"""

    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )

    result = await session.exec(statement)
    return result.first()


# =========================
# UPDATE TASK
# =========================
async def update_task(
    session: AsyncSession,
    task_id: UUID,
    user_id: UUID,
    task_update: TaskUpdate
) -> Optional[Task]:
    """Update a specific task by ID for a user"""

    task = await get_task(session, task_id, user_id)
    if not task:
        return None

    update_data = task_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task


# =========================
# DELETE TASK
# =========================
async def delete_task(
    session: AsyncSession,
    task_id: UUID,
    user_id: UUID
) -> bool:
    """Delete a specific task by ID for a user"""

    logging.info(f"Attempting to delete task {task_id} for user {user_id}")

    task = await get_task(session, task_id, user_id)
    if not task:
        logging.warning("Task not found")
        return False

    # Use a direct delete statement instead of session.delete() to avoid async issues
    from sqlmodel import delete
    statement = delete(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.exec(statement)

    await session.commit()

    # Check if any rows were affected
    if result.rowcount > 0:
        logging.info("Task deleted successfully")
        return True
    else:
        logging.warning("No task was deleted")
        return False


# =========================
# TOGGLE TASK COMPLETION
# =========================
async def toggle_task_completion(
    session: AsyncSession,
    task_id: UUID,
    user_id: UUID,
    completed: bool
) -> Optional[Task]:
    """Toggle the completion status of a task"""

    task = await get_task(session, task_id, user_id)
    if not task:
        return None

    task.completed = completed
    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task
