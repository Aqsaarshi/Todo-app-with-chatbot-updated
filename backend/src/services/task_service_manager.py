from sqlmodel import Session, select
from typing import List, Optional
from ..models.task import Task, TaskCreate, TaskUpdate


class TaskServiceManager:
    """
    Service for managing tasks.
    """
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def create_task(self, task_create: TaskCreate) -> Task:
        """
        Create a new task.
        
        Args:
            task_create: TaskCreate object with task details
            
        Returns:
            The created Task object
        """
        task = Task.from_orm(task_create) if hasattr(Task, 'from_orm') else Task(**task_create.dict())
        self.db_session.add(task)
        self.db_session.commit()
        self.db_session.refresh(task)
        return task
    
    def get_task(self, task_id: int, user_id: str) -> Optional[Task]:
        """
        Get a task by ID for a specific user.
        
        Args:
            task_id: The ID of the task
            user_id: The ID of the user who owns the task
            
        Returns:
            The Task object or None if not found
        """
        statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        return self.db_session.exec(statement).first()
    
    def get_tasks(self, user_id: str, status: Optional[str] = None, limit: int = 100, offset: int = 0) -> List[Task]:
        """
        Get all tasks for a user, optionally filtered by status.
        
        Args:
            user_id: The ID of the user
            status: Optional status to filter by
            limit: Maximum number of tasks to return
            offset: Number of tasks to skip
            
        Returns:
            List of Task objects
        """
        statement = select(Task).where(Task.user_id == user_id)
        
        if status:
            statement = statement.where(Task.status == status)
        
        statement = statement.offset(offset).limit(limit)
        return self.db_session.exec(statement).all()
    
    def update_task(self, task_id: int, user_id: str, task_update: TaskUpdate) -> Optional[Task]:
        """
        Update a task.
        
        Args:
            task_id: The ID of the task to update
            user_id: The ID of the user who owns the task
            task_update: TaskUpdate object with updated values
            
        Returns:
            The updated Task object or None if not found
        """
        task = self.get_task(task_id, user_id)
        if not task:
            return None
        
        # Update the task with new values
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        
        self.db_session.add(task)
        self.db_session.commit()
        self.db_session.refresh(task)
        return task
    
    def delete_task(self, task_id: int, user_id: str) -> bool:
        """
        Delete a task.
        
        Args:
            task_id: The ID of the task to delete
            user_id: The ID of the user who owns the task
            
        Returns:
            True if the task was deleted, False if not found
        """
        task = self.get_task(task_id, user_id)
        if not task:
            return False
        
        self.db_session.delete(task)
        self.db_session.commit()
        return True
    
    def complete_task(self, task_id: int, user_id: str) -> Optional[Task]:
        """
        Mark a task as completed.
        
        Args:
            task_id: The ID of the task to complete
            user_id: The ID of the user who owns the task
            
        Returns:
            The updated Task object or None if not found
        """
        task = self.get_task(task_id, user_id)
        if not task:
            return None
        
        task.status = "completed"
        self.db_session.add(task)
        self.db_session.commit()
        self.db_session.refresh(task)
        return task