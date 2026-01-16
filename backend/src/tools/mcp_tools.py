from typing import Dict, Any, List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from ..models.task import Task as TaskModel
from ..models.user import User
from ..models.conversation import Conversation
from ..database import engine
from ..utils.logging import log_tool_execution, log_error


class MCPTaskTools:
    """
    MCP (Model Context Protocol) tools for task operations.
    These tools allow the AI model to perform specific task operations.
    """

    def __init__(self, db_session: AsyncSession, conversation_id: Optional[int] = None):
        self.db_session = db_session
        self.conversation_id = conversation_id

    def _execute_tool_and_log(
        self,
        tool_name: str,
        user_id: str,
        result: Dict[str, Any],
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a tool and log the execution.

        Args:
            tool_name: Name of the tool being executed
            user_id: ID of the user performing the action
            result: Result of the tool execution
            parameters: Parameters passed to the tool

        Returns:
            The result of the tool execution
        """
        log_tool_execution(
            user_id=user_id,
            conversation_id=self.conversation_id or 0,
            tool_name=tool_name,
            parameters=parameters,
            result=result
        )
        return result

    async def _update_conversation_context(self, context_data: Dict[str, Any]):
        """
        Update the conversation context with new data.

        Args:
            context_data: Dictionary of context data to update
        """
        if not self.conversation_id:
            return

        conversation = await self.db_session.get(Conversation, self.conversation_id)
        if not conversation:
            return

        # Merge the new context data with existing context
        existing_context = conversation.context_data or {}
        updated_context = {**existing_context, **context_data}

        conversation.context_data = updated_context
        self.db_session.add(conversation)
        await self.db_session.commit()

    def _verify_user_owns_task(self, task, user_id: str, task_id: str) -> None:
        """
        Verify that a task belongs to the specified user.

        Args:
            task: The task object to verify
            user_id: ID of the user
            task_id: ID of the task

        Raises:
            ValueError: If the task doesn't exist or doesn't belong to the user
        """
        # Convert the user_id string to UUID for comparison with the task's user_id
        from uuid import UUID
        try:
            user_id_uuid = UUID(user_id)
        except ValueError:
            raise ValueError(f"Invalid user ID format: {user_id}")

        if not task or task.user_id != user_id_uuid:
            raise ValueError(f"Task {task_id} not found or does not belong to user {user_id}")

    def _sanitize_text(self, text: str) -> str:
        """
        Sanitize text input to prevent injection attacks.

        Args:
            text: Text to sanitize

        Returns:
            Sanitized text
        """
        if not text:
            return text

        import re
        # Remove potentially dangerous characters/sequences
        sanitized = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE)
        sanitized = re.sub(r'<iframe[^>]*>.*?</iframe>', '', sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(r'[<>"\';]', '', sanitized)  # Basic tag removal
        return sanitized.strip()

    def _validate_task_params(self, title: Optional[str] = None, description: Optional[str] = None) -> None:
        """
        Validate task parameters to ensure they meet security and business requirements.

        Args:
            title: Title of the task
            description: Description of the task

        Raises:
            ValueError: If parameters don't meet requirements
        """
        if title is not None:
            if len(title) > 200:
                raise ValueError("Title must be less than 200 characters")
            if not title.strip():
                raise ValueError("Title cannot be empty or just whitespace")

        if description is not None and len(description) > 1000:
            raise ValueError("Description must be less than 1000 characters")

    async def add_task(self, user_id: str, title: str, description: str = "", context_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Add a new task for the user.

        Args:
            user_id: ID of the user
            title: Title of the task
            description: Optional description of the task
            context_data: Optional context data to store with the task

        Returns:
            Dictionary with task details
        """
        try:
            # Sanitize inputs to prevent injection attacks
            title = self._sanitize_text(title)
            description = self._sanitize_text(description)

            # Validate inputs
            if not title or len(title) > 200:
                raise ValueError("Title is required and must be less than 200 characters")

            if description and len(description) > 1000:
                raise ValueError("Description must be less than 1000 characters")

            # Create a new task
            task = TaskModel(
                title=title,
                description=description,
                user_id=user_id,
                completed=False  # Default to not completed
            )

            # Add to database
            self.db_session.add(task)
            await self.db_session.commit()
            await self.db_session.refresh(task)

            # Update conversation context if provided
            if self.conversation_id and context_data:
                await self._update_conversation_context(context_data)

            # Prepare result and parameters for logging
            # Convert UUID to string for JSON serialization
            result = {
                "task_id": str(task.id) if hasattr(task, 'id') else task.id,
                "completed": task.completed,
                "title": task.title,
                "description": task.description
            }
            parameters = {"title": title, "description": description, "context_data": context_data}

            return self._execute_tool_and_log("add_task", user_id, result, parameters)
        except ValueError as ve:
            log_error(ve, "MCPTaskTools.add_task validation error")
            raise ve
        except Exception as e:
            log_error(e, "MCPTaskTools.add_task")
            raise e

    async def list_tasks(self, user_id: str, status: Optional[str] = None, context_data: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        List tasks for the user, optionally filtered by status.

        Args:
            user_id: ID of the user
            status: Optional status to filter by (pending, completed, etc.)
            context_data: Optional context data to store with the operation

        Returns:
            List of task dictionaries
        """
        try:
            # Build query
            query = select(TaskModel).where(TaskModel.user_id == user_id)

            if status:
                # Map status to completed field
                if status == "completed":
                    query = query.where(TaskModel.completed == True)
                elif status == "pending":
                    query = query.where(TaskModel.completed == False)

            # Execute query
            result = await self.db_session.exec(query)
            tasks = result.all()

            # Convert to dictionary format, ensuring UUIDs are converted to strings
            tasks_list = [
                {
                    "task_id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed
                }
                for task in tasks
            ]

            # Update conversation context if provided
            if self.conversation_id and context_data:
                await self._update_conversation_context(context_data)

            # Prepare result and parameters for logging
            result = {"tasks_count": len(tasks_list), "tasks": tasks_list}
            parameters = {"user_id": user_id, "status": status, "context_data": context_data}

            self._execute_tool_and_log("list_tasks", user_id, result, parameters)
            return tasks_list
        except Exception as e:
            log_error(e, "MCPTaskTools.list_tasks")
            raise e

    async def complete_task(self, user_id: str, task_id: str, context_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Mark a task as completed.

        Args:
            user_id: ID of the user
            task_id: ID of the task to complete (UUID string)
            context_data: Optional context data to store with the operation

        Returns:
            Dictionary with updated task details
        """
        try:
            from uuid import UUID

            # Validate task_id is a valid UUID string
            try:
                uuid_obj = UUID(task_id)
            except ValueError:
                raise ValueError(f"Invalid task ID format: {task_id}. Expected a valid UUID.")

            # Find the task using the UUID
            task = await self.db_session.get(TaskModel, uuid_obj)

            # Check if task exists
            if not task:
                raise ValueError(f"Task with ID {task_id} not found")

            # Verify the task belongs to the user
            self._verify_user_owns_task(task, user_id, str(uuid_obj))

            # Update completed status
            task.completed = True
            self.db_session.add(task)
            await self.db_session.commit()
            await self.db_session.refresh(task)

            # Update conversation context if provided
            if self.conversation_id and context_data:
                await self._update_conversation_context(context_data)

            # Prepare result and parameters for logging
            # Convert UUID to string for JSON serialization
            result = {
                "task_id": str(task.id),
                "completed": task.completed,
                "title": task.title
            }
            parameters = {"task_id": str(uuid_obj), "context_data": context_data}

            return self._execute_tool_and_log("complete_task", user_id, result, parameters)
        except ValueError as ve:
            log_error(ve, "MCPTaskTools.complete_task validation error")
            raise ve
        except Exception as e:
            log_error(e, "MCPTaskTools.complete_task")
            raise e

    async def update_task(
        self,
        user_id: str,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        context_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Update a task's title or description.

        Args:
            user_id: ID of the user
            task_id: ID of the task to update (UUID string)
            title: Optional new title
            description: Optional new description
            context_data: Optional context data to store with the operation

        Returns:
            Dictionary with updated task details
        """
        try:
            from uuid import UUID

            # Validate task_id is a valid UUID string
            try:
                uuid_obj = UUID(task_id)
            except ValueError:
                raise ValueError(f"Invalid task ID format: {task_id}. Expected a valid UUID.")

            # Sanitize inputs to prevent injection attacks
            if title is not None:
                title = self._sanitize_text(title)
            if description is not None:
                description = self._sanitize_text(description)

            # Validate inputs
            self._validate_task_params(title=title, description=description)

            # Find the task using the UUID
            task = await self.db_session.get(TaskModel, uuid_obj)

            # Check if task exists
            if not task:
                raise ValueError(f"Task with ID {task_id} not found")

            # Verify the task belongs to the user
            self._verify_user_owns_task(task, user_id, str(uuid_obj))

            # Update fields if provided
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description

            self.db_session.add(task)
            await self.db_session.commit()
            await self.db_session.refresh(task)

            # Update conversation context if provided
            if self.conversation_id and context_data:
                await self._update_conversation_context(context_data)

            # Prepare result and parameters for logging
            # Convert UUID to string for JSON serialization
            result = {
                "task_id": str(task.id),
                "completed": task.completed,
                "title": task.title
            }
            parameters = {"task_id": str(uuid_obj), "title": title, "description": description, "context_data": context_data}

            return self._execute_tool_and_log("update_task", user_id, result, parameters)
        except ValueError as ve:
            log_error(ve, "MCPTaskTools.update_task validation error")
            raise ve
        except Exception as e:
            log_error(e, "MCPTaskTools.update_task")
            raise e

    async def delete_task(self, user_id: str, task_id: str, context_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Delete a task.

        Args:
            user_id: ID of the user
            task_id: ID of the task to delete (UUID string)
            context_data: Optional context data to store with the operation

        Returns:
            Dictionary confirming deletion
        """
        try:
            from uuid import UUID

            # Validate task_id is a valid UUID string
            try:
                uuid_obj = UUID(task_id)
            except ValueError:
                raise ValueError(f"Invalid task ID format: {task_id}. Expected a valid UUID.")

            # Find the task using the UUID
            task = await self.db_session.get(TaskModel, uuid_obj)

            # Check if task exists
            if not task:
                raise ValueError(f"Task with ID {task_id} not found")

            # Verify the task belongs to the user
            self._verify_user_owns_task(task, user_id, str(uuid_obj))

            # Delete the task
            await self.db_session.delete(task)
            await self.db_session.commit()

            # Update conversation context if provided
            if self.conversation_id and context_data:
                await self._update_conversation_context(context_data)

            # Prepare result and parameters for logging
            # Convert UUID to string for JSON serialization
            result = {
                "task_id": str(uuid_obj),
                "status": "deleted",  # For delete operation, we can keep status as "deleted"
                "title": task.title
            }
            parameters = {"task_id": str(uuid_obj), "context_data": context_data}

            return self._execute_tool_and_log("delete_task", user_id, result, parameters)
        except ValueError as ve:
            log_error(ve, "MCPTaskTools.delete_task validation error")
            raise ve
        except Exception as e:
            log_error(e, "MCPTaskTools.delete_task")
            raise e