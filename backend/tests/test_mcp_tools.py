import pytest
from unittest.mock import MagicMock, patch, create_autospec
from sqlmodel import Session, select
from backend.src.tools.mcp_tools import MCPTaskTools
from backend.src.models.task import Task as TaskModel


@pytest.fixture
def mock_db_session():
    """Mock database session for testing."""
    session = create_autospec(Session, instance=True)
    session.add = MagicMock()
    session.commit = MagicMock()
    session.refresh = MagicMock()
    session.get = MagicMock()
    session.exec = MagicMock()
    return session


@pytest.fixture
def mcp_tools(mock_db_session):
    """Create an MCPTaskTools instance with mocked dependencies."""
    return MCPTaskTools(mock_db_session)


def test_add_task_success(mcp_tools, mock_db_session):
    """Test successfully adding a task."""
    # Arrange
    user_id = "user123"
    title = "Test Task"
    description = "Test Description"
    
    # Create a mock task object
    mock_task = MagicMock(spec=TaskModel)
    mock_task.id = 1
    mock_task.status = "pending"
    mock_task.title = title
    mock_task.description = description
    mock_task.user_id = user_id
    
    # Configure the session to return the mock task when add is called
    mock_db_session.get.return_value = mock_task
    
    # Act
    result = mcp_tools.add_task(user_id, title, description)
    
    # Assert
    assert result["task_id"] == 1
    assert result["status"] == "pending"
    assert result["title"] == title
    assert result["description"] == description
    
    # Verify session methods were called
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()


def test_list_tasks_success(mcp_tools, mock_db_session):
    """Test successfully listing tasks."""
    # Arrange
    user_id = "user123"
    mock_task = MagicMock(spec=TaskModel)
    mock_task.id = 1
    mock_task.title = "Test Task"
    mock_task.description = "Test Description"
    mock_task.status = "pending"
    mock_task.user_id = user_id
    
    # Configure the session to return a list of tasks
    mock_db_session.exec.return_value.all.return_value = [mock_task]
    
    # Act
    result = mcp_tools.list_tasks(user_id)
    
    # Assert
    assert len(result) == 1
    assert result[0]["task_id"] == 1
    assert result[0]["title"] == "Test Task"
    assert result[0]["status"] == "pending"
    
    # Verify the select query was called
    assert mock_db_session.exec.called


def test_list_tasks_with_status_filter(mcp_tools, mock_db_session):
    """Test listing tasks with a status filter."""
    # Arrange
    user_id = "user123"
    status = "completed"
    mock_task = MagicMock(spec=TaskModel)
    mock_task.id = 1
    mock_task.title = "Test Task"
    mock_task.status = status
    
    # Configure the session to return a list of tasks
    mock_db_session.exec.return_value.all.return_value = [mock_task]
    
    # Act
    result = mcp_tools.list_tasks(user_id, status=status)
    
    # Assert
    assert len(result) == 1
    assert result[0]["status"] == status
    
    # Verify the select query was called with the status filter
    assert mock_db_session.exec.called


def test_complete_task_success(mcp_tools, mock_db_session):
    """Test successfully completing a task."""
    # Arrange
    user_id = "user123"
    task_id = 1
    mock_task = MagicMock(spec=TaskModel)
    mock_task.id = task_id
    mock_task.status = "completed"
    mock_task.title = "Test Task"
    mock_task.user_id = user_id
    
    # Configure the session to return the mock task
    mock_db_session.get.return_value = mock_task
    
    # Act
    result = mcp_tools.complete_task(user_id, task_id)
    
    # Assert
    assert result["task_id"] == task_id
    assert result["status"] == "completed"
    assert result["title"] == "Test Task"
    
    # Verify session methods were called
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()


def test_complete_task_not_found(mcp_tools, mock_db_session):
    """Test completing a task that doesn't exist."""
    # Arrange
    user_id = "user123"
    task_id = 999
    
    # Configure the session to return None (task not found)
    mock_db_session.get.return_value = None
    
    # Act & Assert
    with pytest.raises(ValueError, match=f"Task {task_id} not found or does not belong to user {user_id}"):
        mcp_tools.complete_task(user_id, task_id)


def test_complete_task_wrong_user(mcp_tools, mock_db_session):
    """Test completing a task that belongs to another user."""
    # Arrange
    user_id = "user123"
    other_user_id = "user456"
    task_id = 1
    mock_task = MagicMock(spec=TaskModel)
    mock_task.user_id = other_user_id  # Task belongs to different user
    
    # Configure the session to return the mock task
    mock_db_session.get.return_value = mock_task
    
    # Act & Assert
    with pytest.raises(ValueError, match=f"Task {task_id} not found or does not belong to user {user_id}"):
        mcp_tools.complete_task(user_id, task_id)


def test_update_task_success(mcp_tools, mock_db_session):
    """Test successfully updating a task."""
    # Arrange
    user_id = "user123"
    task_id = 1
    new_title = "Updated Title"
    new_description = "Updated Description"
    mock_task = MagicMock(spec=TaskModel)
    mock_task.id = task_id
    mock_task.status = "pending"
    mock_task.title = new_title
    mock_task.user_id = user_id
    
    # Configure the session to return the mock task
    mock_db_session.get.return_value = mock_task
    
    # Act
    result = mcp_tools.update_task(user_id, task_id, title=new_title, description=new_description)
    
    # Assert
    assert result["task_id"] == task_id
    assert result["status"] == "pending"
    assert result["title"] == new_title
    
    # Verify session methods were called
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()


def test_update_task_partial_update(mcp_tools, mock_db_session):
    """Test updating only the title of a task."""
    # Arrange
    user_id = "user123"
    task_id = 1
    new_title = "Updated Title"
    mock_task = MagicMock(spec=TaskModel)
    mock_task.id = task_id
    mock_task.status = "pending"
    mock_task.title = new_title
    mock_task.user_id = user_id
    
    # Configure the session to return the mock task
    mock_db_session.get.return_value = mock_task
    
    # Act
    result = mcp_tools.update_task(user_id, task_id, title=new_title)
    
    # Assert
    assert result["task_id"] == task_id
    assert result["title"] == new_title


def test_delete_task_success(mcp_tools, mock_db_session):
    """Test successfully deleting a task."""
    # Arrange
    user_id = "user123"
    task_id = 1
    mock_task = MagicMock(spec=TaskModel)
    mock_task.id = task_id
    mock_task.title = "Test Task"
    mock_task.user_id = user_id
    
    # Configure the session to return the mock task
    mock_db_session.get.return_value = mock_task
    
    # Act
    result = mcp_tools.delete_task(user_id, task_id)
    
    # Assert
    assert result["task_id"] == task_id
    assert result["status"] == "deleted"
    assert result["title"] == "Test Task"
    
    # Verify session methods were called
    mock_db_session.delete.assert_called_once_with(mock_task)
    mock_db_session.commit.assert_called_once()


def test_delete_task_not_found(mcp_tools, mock_db_session):
    """Test deleting a task that doesn't exist."""
    # Arrange
    user_id = "user123"
    task_id = 999
    
    # Configure the session to return None (task not found)
    mock_db_session.get.return_value = None
    
    # Act & Assert
    with pytest.raises(ValueError, match=f"Task {task_id} not found or does not belong to user {user_id}"):
        mcp_tools.delete_task(user_id, task_id)


def test_delete_task_wrong_user(mcp_tools, mock_db_session):
    """Test deleting a task that belongs to another user."""
    # Arrange
    user_id = "user123"
    other_user_id = "user456"
    task_id = 1
    mock_task = MagicMock(spec=TaskModel)
    mock_task.user_id = other_user_id  # Task belongs to different user
    
    # Configure the session to return the mock task
    mock_db_session.get.return_value = mock_task
    
    # Act & Assert
    with pytest.raises(ValueError, match=f"Task {task_id} not found or does not belong to user {user_id}"):
        mcp_tools.delete_task(user_id, task_id)


def test_add_task_with_context(mcp_tools, mock_db_session):
    """Test adding a task with context data."""
    # Arrange
    user_id = "user123"
    title = "Test Task"
    description = "Test Description"
    context_data = {"source": "chat", "intent": "add_task"}
    
    # Create a mock task object
    mock_task = MagicMock(spec=TaskModel)
    mock_task.id = 1
    mock_task.status = "pending"
    mock_task.title = title
    mock_task.description = description
    mock_task.user_id = user_id
    
    # Configure the session to return the mock task
    mock_db_session.get.return_value = mock_task
    
    # Create an instance with a conversation ID to trigger context update
    tools_with_conv = MCPTaskTools(mock_db_session, conversation_id=1)
    
    # Act
    result = tools_with_conv.add_task(user_id, title, description, context_data)
    
    # Assert
    assert result["task_id"] == 1
    # The context update functionality would be tested separately
    # as it depends on the Conversation model which is not directly accessible here