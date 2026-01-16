import pytest
from unittest.mock import MagicMock, patch
from backend.src.services.cohere_service import CohereService


@pytest.fixture
def mock_cohere_client():
    """Mock Cohere client for testing."""
    with patch('backend.src.services.cohere_service.cohere') as mock_cohere:
        mock_client = MagicMock()
        mock_cohere.Client.return_value = mock_client
        yield mock_client


@pytest.fixture
def cohere_service(mock_cohere_client):
    """Create a CohereService instance with mocked dependencies."""
    # Temporarily set the environment variable
    with patch.dict('os.environ', {'COHERE_API_KEY': 'test-key'}):
        service = CohereService()
        service.client = mock_cohere_client
        return service


def test_cohere_service_initialization():
    """Test CohereService initialization with valid API key."""
    with patch.dict('os.environ', {'COHERE_API_KEY': 'test-key'}):
        service = CohereService()
        assert service.client is not None


def test_cohere_service_initialization_missing_key():
    """Test CohereService initialization without API key raises error."""
    with patch.dict('os.environ', {}, clear=True):
        with pytest.raises(ValueError, match="COHERE_API_KEY environment variable is not set"):
            CohereService()


def test_generate_response(cohere_service, mock_cohere_client):
    """Test generating a response with the Cohere API."""
    prompt = "Hello, world!"
    expected_response = "Hello, user!"
    
    # Mock the Cohere API response
    mock_generation = MagicMock()
    mock_generation.text = expected_response
    mock_cohere_client.generate.return_value = MagicMock(generations=[mock_generation])
    
    result = cohere_service.generate_response(prompt)
    
    assert result == expected_response
    mock_cohere_client.generate.assert_called_once_with(
        model="command",
        prompt=prompt,
        max_tokens=500,
        temperature=0.7
    )


def test_generate_response_empty_generations(cohere_service, mock_cohere_client):
    """Test generating a response when Cohere returns empty generations."""
    prompt = "Hello, world!"
    
    # Mock the Cohere API response with empty generations
    mock_cohere_client.generate.return_value = MagicMock(generations=[])
    
    result = cohere_service.generate_response(prompt)
    
    assert result == "I couldn't generate a response. Please try again."


def test_generate_response_with_context(cohere_service, mock_cohere_client):
    """Test generating a response with additional context."""
    question = "What is the status of my tasks?"
    context = ["You have 3 pending tasks", "Task 1: Buy groceries", "Task 2: Call John"]
    expected_response = "You have 3 pending tasks"
    
    # Mock the Cohere API response
    mock_generation = MagicMock()
    mock_generation.text = expected_response
    mock_cohere_client.generate.return_value = MagicMock(generations=[mock_generation])
    
    result = cohere_service.generate_response_with_context(question, context)
    
    assert result == expected_response
    # Verify the prompt was constructed correctly
    expected_prompt = f"Context: {chr(10).join(context)}\n\nQuestion: {question}\n\nAnswer:"
    mock_cohere_client.generate.assert_called_once_with(
        model="command",
        prompt=expected_prompt,
        max_tokens=500,
        temperature=0.7
    )


def test_validate_response_against_context_valid(cohere_service, mock_cohere_client):
    """Test validating a response that is consistent with context."""
    response = "Yes, you have 3 pending tasks"
    context = ["You have 3 pending tasks", "Task 1: Buy groceries"]
    
    # Mock the Cohere API response for validation
    mock_generation = MagicMock()
    mock_generation.text = "yes"
    mock_cohere_client.generate.return_value = MagicMock(generations=[mock_generation])
    
    result = cohere_service.validate_response_against_context(response, context)
    
    assert result is True


def test_validate_response_against_context_invalid(cohere_service, mock_cohere_client):
    """Test validating a response that is inconsistent with context."""
    response = "No, you don't have any tasks"
    context = ["You have 3 pending tasks", "Task 1: Buy groceries"]
    
    # Mock the Cohere API response for validation
    mock_generation = MagicMock()
    mock_generation.text = "no"
    mock_cohere_client.generate.return_value = MagicMock(generations=[mock_generation])
    
    result = cohere_service.validate_response_against_context(response, context)
    
    assert result is False


def test_validate_response_against_context_empty_response(cohere_service, mock_cohere_client):
    """Test validating when Cohere returns an empty response."""
    response = "Some response"
    context = ["Some context"]
    
    # Mock the Cohere API response for validation with empty generations
    mock_cohere_client.generate.return_value = MagicMock(generations=[])
    
    result = cohere_service.validate_response_against_context(response, context)
    
    assert result is False


def test_generate_response_with_latency_safeguards(cohere_service, mock_cohere_client):
    """Test generating a response with latency safeguards."""
    prompt = "Process this quickly"
    expected_response = "Processed response"
    
    # Mock the Cohere API response
    mock_generation = MagicMock()
    mock_generation.text = expected_response
    mock_cohere_client.generate.return_value = MagicMock(generations=[mock_generation])
    
    result = cohere_service.generate_response_with_latency_safeguards(prompt, max_tokens=800)
    
    assert result == expected_response
    mock_cohere_client.generate.assert_called_once_with(
        model="command",
        prompt=prompt,
        max_tokens=800,
        temperature=0.7,
        k=0,
        p=0.9
    )


def test_generate_response_with_conversation_context(cohere_service, mock_cohere_client):
    """Test generating a response with conversation context and history."""
    question = "What did I ask before?"
    conversation_context = {"previous_topic": "grocery_list", "user_preference": "detailed_responses"}
    conversation_history = [
        {"sender_type": "user", "content": "Can you help me with groceries?"},
        {"sender_type": "assistant", "content": "Sure, what do you need?"}
    ]
    expected_response = "You asked about groceries"
    
    # Mock the Cohere API response
    mock_generation = MagicMock()
    mock_generation.text = expected_response
    mock_cohere_client.generate.return_value = MagicMock(generations=[mock_generation])
    
    result = cohere_service.generate_response_with_conversation_context(
        question, conversation_context, conversation_history
    )
    
    assert result == expected_response
    # Verify the call was made with the expected prompt
    call_args = mock_cohere_client.generate.call_args
    assert call_args is not None
    prompt_arg = call_args[1]['prompt']
    assert "Conversation context:" in prompt_arg
    assert "previous_topic: grocery_list" in prompt_arg
    assert "user_preference: detailed_responses" in prompt_arg
    assert "user: Can you help me with groceries?" in prompt_arg
    assert "assistant: Sure, what do you need?" in prompt_arg
    assert question in prompt_arg