from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional
from uuid import UUID
from datetime import datetime
import logging
from ..database import get_session
from ..models.task import Task, TaskCreate, TaskRead, TaskUpdate
from ..models.user import User
from ..auth.jwt import verify_token
from ..services.task_service import create_task, get_tasks, get_task, update_task, delete_task, toggle_task_completion
from ..utils.errors import raise_auth_required_error, raise_forbidden_error, raise_not_found_error

router = APIRouter()

def get_current_user(token: str = Query(..., alias="token")):
    """Get current user from token"""
    try:
        payload = verify_token(token)
        if payload is None:
            raise_auth_required_error("Could not validate credentials")
        user_id = payload.get("sub")
        if user_id is None:
            raise_auth_required_error("Could not validate credentials")

        # Handle both UUID strings and regular strings
        try:
            return UUID(user_id)
        except ValueError:
            # If it's not a valid UUID string, return as-is for backward compatibility
            return user_id
    except Exception as e:
        logging.error(f"Error getting current user from token: {e}")
        raise_auth_required_error("Could not validate credentials")

@router.get("/{user_id}/tasks", response_model=List[TaskRead])
async def read_tasks(
    user_id: str,  # Changed to str to handle both UUID and string formats
    current_user_id: str = Depends(get_current_user),
    completed: Optional[bool] = Query(None),
    priority: Optional[str] = Query(None),
    sort: Optional[str] = Query("created_at"),
    order: Optional[str] = Query("desc"),
    session: AsyncSession = Depends(get_session)
):
    """Get all tasks for a specific user"""
    # Verify that the current user is the same as the requested user
    # Convert both to string for comparison to handle UUID objects vs strings
    if str(current_user_id) != str(user_id):
        raise_forbidden_error("Not authorized to access these tasks")

    # Convert user_id to UUID if possible, otherwise keep as string
    try:
        actual_user_id = UUID(user_id)
    except ValueError:
        actual_user_id = user_id

    tasks = await get_tasks(session, actual_user_id, completed, priority, sort, order)
    return tasks

@router.post("/{user_id}/tasks", response_model=TaskRead)
async def create_new_task(
    user_id: str,  # Changed to str to handle both UUID and string formats
    task_create: TaskCreate,
    current_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Create a new task for a user"""
    # Verify that the current user is the same as the requested user
    # Convert both to string for comparison to handle UUID objects vs strings
    if str(current_user_id) != str(user_id):
        raise_forbidden_error("Not authorized to create tasks for this user")

    # Convert user_id to UUID if possible, otherwise keep as string
    try:
        actual_user_id = UUID(user_id)
    except ValueError:
        actual_user_id = user_id

    task = await create_task(session, actual_user_id, task_create)
    return task

@router.get("/{user_id}/tasks/{id}", response_model=TaskRead)
async def read_task(
    user_id: str,  # Changed to str to handle both UUID and string formats
    id: str,       # Changed to str to handle both UUID and string formats
    current_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Get a specific task by ID"""
    # Verify that the current user is the same as the requested user
    # Convert both to string for comparison to handle UUID objects vs strings
    if str(current_user_id) != str(user_id):
        raise_forbidden_error("Not authorized to access this task")

    # Convert user_id and id to UUID if possible, otherwise keep as string
    try:
        actual_user_id = UUID(user_id)
    except ValueError:
        actual_user_id = user_id

    try:
        actual_task_id = UUID(id)
    except ValueError:
        actual_task_id = id

    task = await get_task(session, actual_task_id, actual_user_id)
    if not task:
        raise_not_found_error("Task not found")

    return task

@router.put("/{user_id}/tasks/{id}", response_model=TaskRead)
async def update_existing_task(
    user_id: str,  # Changed to str to handle both UUID and string formats
    id: str,       # Changed to str to handle both UUID and string formats
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Update a specific task by ID"""
    # Verify that the current user is the same as the requested user
    # Convert both to string for comparison to handle UUID objects vs strings
    if str(current_user_id) != str(user_id):
        raise_forbidden_error("Not authorized to update this task")

    # Convert user_id and id to UUID if possible, otherwise keep as string
    try:
        actual_user_id = UUID(user_id)
    except ValueError:
        actual_user_id = user_id

    try:
        actual_task_id = UUID(id)
    except ValueError:
        actual_task_id = id

    task = await update_task(session, actual_task_id, actual_user_id, task_update)
    if not task:
        raise_not_found_error("Task not found")

    return task

import logging

@router.delete("/{user_id}/tasks/{id}")
async def delete_existing_task(
    user_id: str,  # Changed to str to handle both UUID and string formats
    id: str,       # Changed to str to handle both UUID and string formats
    current_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Delete a specific task by ID"""

    # Convert user_id and id to UUID if possible, otherwise keep as string
    try:
        actual_user_id = UUID(user_id)
    except ValueError:
        actual_user_id = user_id

    try:
        actual_task_id = UUID(id)
    except ValueError:
        actual_task_id = id

    logging.info(f"Delete request: user_id={actual_user_id}, current_user_id={current_user_id}, task_id={actual_task_id}")

    # Verify that the current user is the same as the requested user
    if str(current_user_id) != str(actual_user_id):
        logging.warning(f"Authorization failed: {current_user_id} != {actual_user_id}")
        raise_forbidden_error("Not authorized to delete this task")

    logging.info(f"Attempting to delete task {actual_task_id} for user {actual_user_id}")
    success = await delete_task(session, actual_task_id, actual_user_id)
    logging.info(f"Delete operation result: {success}")

    if not success:
        logging.warning(f"Task {actual_task_id} not found for user {actual_user_id}")
        raise_not_found_error("Task not found")

    logging.info(f"Task {actual_task_id} successfully deleted for user {actual_user_id}")
    return {"message": "Task deleted successfully"}

@router.patch("/{user_id}/tasks/{id}/complete", response_model=TaskRead)
async def toggle_task_complete(
    user_id: str,  # Changed to str to handle both UUID and string formats
    id: str,       # Changed to str to handle both UUID and string formats
    completed: bool,
    current_user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Toggle task completion status"""
    # Verify that the current user is the same as the requested user
    # Convert both to string for comparison to handle UUID objects vs strings
    if str(current_user_id) != str(user_id):
        raise_forbidden_error("Not authorized to update this task")

    # Convert user_id and id to UUID if possible, otherwise keep as string
    try:
        actual_user_id = UUID(user_id)
    except ValueError:
        actual_user_id = user_id

    try:
        actual_task_id = UUID(id)
    except ValueError:
        actual_task_id = id

    task = await toggle_task_completion(session, actual_task_id, actual_user_id, completed)
    if not task:
        raise_not_found_error("Task not found")

    return task