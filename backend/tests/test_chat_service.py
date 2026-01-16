import pytest
from unittest.mock import MagicMock, patch
from sqlmodel import Session
from backend.src.services.chat_service import ChatService
from backend.src.services.cohere_service import CohereService
from backend.src.tools.mcp_tools import MCPTaskTools


@pytest.fixture
def mock_db_session():
    """Mock database session for testing."""
    return MagicMock(spec=Session)


@pytest.fixture
def mock_cohere_service():
    """Mock Cohere service for testing."""
    service = MagicMock(spec=CohereService)
    service.generate_response.return_value = "ACTION: reply\nPARAMETERS: {}"
    return service


@pytest.fixture
def mock_mcp_tools():
    """Mock MCP tools for testing."""
    tools = MagicMock(spec=MCPTaskTools)
    tools.add_task.return_value = {"task_id": 1, "status": "pending", "title": "Test task"}
    tools.list_tasks.return_value = [{"task_id": 1, "status": "pending", "title": "Test task"}]
    tools.complete_task.return_value = {"task_id": 1, "status": "completed", "title": "Test task"}
    tools.update_task.return_value = {"task_id": 1, "status": "pending", "title": "Updated task"}
    tools.delete_task.return_value = {"task_id": 1, "status": "deleted", "title": "Test task"}
    return tools


@pytest.fixture
def chat_service(mock_db_session, mock_cohere_service, mock_mcp_tools):
    """Create a ChatService instance with mocked dependencies."""
    service = ChatService(mock_db_session)
    service.cohere_service = mock_cohere_service
    service.mcp_tools = mock_mcp_tools
    return service


def test_process_user_message_add_task(chat_service, mock_cohere_service):
    """Test processing a user message that adds a task."""
    # Mock the Cohere response to simulate adding a task
    mock_cohere_service.generate_response.return_value = "ACTION: add_task\nPARAMETERS: {\"title\": \"Buy groceries\", \"description\": \"Milk and bread\"}"
    
    user_id = "user123"
    conversation_id = 1
    user_message = "Add a task to buy groceries"
    conversation_history = [
        {"sender_type": "user", "content": "Hi there"},
        {"sender_type": "assistant", "content": "Hello! How can I help you?"}
    ]
    
    result = chat_service.process_user_message(
        user_id, 
        conversation_id, 
        user_message, 
        conversation_history
    )
    
    # Verify the result
    assert result["response"] == "I've added the task 'Test task' to your list."
    assert len(result["tool_calls"]) == 1
    assert result["tool_calls"][0]["tool_name"] == "add_task"
    assert result["tool_calls"][0]["parameters"]["title"] == "Buy groceries"


def test_process_user_message_list_tasks(chat_service, mock_cohere_service):
    """Test processing a user message that lists tasks."""
    # Mock the Cohere response to simulate listing tasks
    mock_cohere_service.generate_response.return_value = "ACTION: list_tasks\nPARAMETERS: {}"
    
    user_id = "user123"
    conversation_id = 1
    user_message = "Show me my tasks"
    conversation_history = []
    
    result = chat_service.process_user_message(
        user_id, 
        conversation_id, 
        user_message, 
        conversation_history
    )
    
    # Verify the result
    assert "Here are your tasks" in result["response"]
    assert len(result["tool_calls"]) == 1
    assert result["tool_calls"][0]["tool_name"] == "list_tasks"


def test_process_user_message_complete_task(chat_service, mock_cohere_service):
    """Test processing a user message that completes a task."""
    # Mock the Cohere response to simulate completing a task
    mock_cohere_service.generate_response.return_value = "ACTION: complete_task\nPARAMETERS: {\"task_id\": 1}"
    
    user_id = "user123"
    conversation_id = 1
    user_message = "Mark task 1 as complete"
    conversation_history = []
    
    result = chat_service.process_user_message(
        user_id, 
        conversation_id, 
        user_message, 
        conversation_history
    )
    
    # Verify the result
    assert "marked the task 'Test task' as completed" in result["response"]
    assert len(result["tool_calls"]) == 1
    assert result["tool_calls"][0]["tool_name"] == "complete_task"


def test_process_user_message_reply(chat_service, mock_cohere_service):
    """Test processing a user message that results in a reply."""
    # Mock the Cohere response to simulate a general reply
    mock_cohere_service.generate_response.return_value = "I can help you with that."
    
    user_id = "user123"
    conversation_id = 1
    user_message = "Tell me a joke"
    conversation_history = []
    
    result = chat_service.process_user_message(
        user_id, 
        conversation_id, 
        user_message, 
        conversation_history
    )
    
    # Verify the result
    assert len(result["tool_calls"]) == 0
    assert "I can help you with that." in result["response"]


def test_process_user_message_parsing_failure(chat_service, mock_cohere_service):
    """Test processing a user message when Cohere response parsing fails."""
    # Mock the Cohere response to be unparsable
    mock_cohere_service.generate_response.return_value = "This is not a valid action format"
    
    user_id = "user123"
    conversation_id = 1
    user_message = "Do something"
    conversation_history = []
    
    result = chat_service.process_user_message(
        user_id, 
        conversation_id, 
        user_message, 
        conversation_history
    )
    
    # Verify the result defaults to a reply
    assert len(result["tool_calls"]) == 0


def test_validate_response_with_context(chat_service, mock_cohere_service):
    """Test validating a response with context."""
    mock_cohere_service.validate_response_against_context.return_value = True
    
    response = "This is a valid response"
    context = ["Previous context"]
    
    result = chat_service.validate_response_with_context(response, context)
    
    assert result is True
    mock_cohere_service.validate_response_against_context.assert_called_once_with(response, context)


def test_generate_response_with_context(chat_service, mock_cohere_service):
    """Test generating a response with context."""
    mock_cohere_service.generate_response_with_context.return_value = "Contextual response"
    
    question = "What is the status of my tasks?"
    context = ["You have 3 pending tasks"]
    
    result = chat_service.generate_response_with_context(question, context)
    
    assert result == "Contextual response"
    mock_cohere_service.generate_response_with_context.assert_called_once_with(
        question, context, "full-book"
    )