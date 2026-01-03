from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from ..database import get_session
from ..models.task import Task, TaskCreate, TaskRead, TaskUpdate
from ..models.user import User
from ..auth.jwt import verify_token
from ..services.task_service import create_task, get_tasks, get_task, update_task, delete_task, toggle_task_completion
from ..utils.errors import raise_auth_required_error, raise_forbidden_error, raise_not_found_error

router = APIRouter()

def get_current_user(token: str = Query(..., alias="token")):
    """Get current user from token"""
    payload = verify_token(token)
    if payload is None:
        raise_auth_required_error("Could not validate credentials")
    user_id = payload.get("sub")
    if user_id is None:
        raise_auth_required_error("Could not validate credentials")
    return UUID(user_id)

@router.get("/{user_id}/tasks", response_model=List[TaskRead])
async def read_tasks(
    user_id: UUID,
    current_user_id: UUID = Depends(get_current_user),
    completed: Optional[bool] = Query(None),
    priority: Optional[str] = Query(None),
    sort: Optional[str] = Query("created_at"),
    order: Optional[str] = Query("desc"),
    session: AsyncSession = Depends(get_session)
):
    """Get all tasks for a specific user"""
    # Verify that the current user is the same as the requested user
    if current_user_id != user_id:
        raise_forbidden_error("Not authorized to access these tasks")

    tasks = await get_tasks(session, user_id, completed, priority, sort, order)
    return tasks

@router.post("/{user_id}/tasks", response_model=TaskRead)
async def create_new_task(
    user_id: UUID,
    task_create: TaskCreate,
    current_user_id: UUID = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Create a new task for a user"""
    # Verify that the current user is the same as the requested user
    if current_user_id != user_id:
        raise_forbidden_error("Not authorized to create tasks for this user")

    task = await create_task(session, user_id, task_create)
    return task

@router.get("/{user_id}/tasks/{id}", response_model=TaskRead)
async def read_task(
    user_id: UUID,
    id: UUID,
    current_user_id: UUID = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get a specific task by ID"""
    # Verify that the current user is the same as the requested user
    if current_user_id != user_id:
        raise_forbidden_error("Not authorized to access this task")

    task = await get_task(session, id, user_id)
    if not task:
        raise_not_found_error("Task not found")

    return task

@router.put("/{user_id}/tasks/{id}", response_model=TaskRead)
async def update_existing_task(
    user_id: UUID,
    id: UUID,
    task_update: TaskUpdate,
    current_user_id: UUID = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Update a specific task by ID"""
    # Verify that the current user is the same as the requested user
    if current_user_id != user_id:
        raise_forbidden_error("Not authorized to update this task")

    task = await update_task(session, id, user_id, task_update)
    if not task:
        raise_not_found_error("Task not found")

    return task

import logging

@router.delete("/{user_id}/tasks/{id}")
async def delete_existing_task(
    user_id: UUID,
    id: UUID,
    current_user_id: UUID = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Delete a specific task by ID"""
    logging.info(f"Delete request: user_id={user_id}, current_user_id={current_user_id}, task_id={id}")

    # Verify that the current user is the same as the requested user
    if current_user_id != user_id:
        logging.warning(f"Authorization failed: {current_user_id} != {user_id}")
        raise_forbidden_error("Not authorized to delete this task")

    logging.info(f"Attempting to delete task {id} for user {user_id}")
    success = await delete_task(session, id, user_id)
    logging.info(f"Delete operation result: {success}")

    if not success:
        logging.warning(f"Task {id} not found for user {user_id}")
        raise_not_found_error("Task not found")

    logging.info(f"Task {id} successfully deleted for user {user_id}")
    return {"message": "Task deleted successfully"}

@router.patch("/{user_id}/tasks/{id}/complete", response_model=TaskRead)
async def toggle_task_complete(
    user_id: UUID,
    id: UUID,
    completed: bool,
    current_user_id: UUID = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Toggle task completion status"""
    # Verify that the current user is the same as the requested user
    if current_user_id != user_id:
        raise_forbidden_error("Not authorized to update this task")

    task = await toggle_task_completion(session, id, user_id, completed)
    if not task:
        raise_not_found_error("Task not found")

    return task