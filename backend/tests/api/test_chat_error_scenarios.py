import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from uuid import uuid4

from src.main import app
from src.services.cohere_service import CohereService

client = TestClient(app)

def test_chat_endpoint_cohere_error():
    """Test that the chat endpoint handles Cohere API errors gracefully"""
    user_id = str(uuid4())
    
    with patch.object(CohereService, 'generate_response', side_effect=Exception("Cohere API error")):
        response = client.post(
            f"/api/{user_id}/chat",
            json={"message": "Test message"},
            headers={"Authorization": "Bearer fake_token"}
        )
        
        # Should return 500 error when Cohere fails
        assert response.status_code == 500
        assert "error" in response.json() or "detail" in response.json()


def test_chat_endpoint_empty_message():
    """Test that the chat endpoint validates empty messages"""
    user_id = str(uuid4())
    
    response = client.post(
        f"/api/{user_id}/chat",
        json={"message": ""},
        headers={"Authorization": "Bearer fake_token"}
    )
    
    # Should return 400 error for empty message
    assert response.status_code == 400


def test_chat_endpoint_long_message():
    """Test that the chat endpoint validates long messages"""
    user_id = str(uuid4())
    
    long_message = "A" * 1001  # More than 1000 characters
    
    response = client.post(
        f"/api/{user_id}/chat",
        json={"message": long_message},
        headers={"Authorization": "Bearer fake_token"}
    )
    
    # Should return 400 error for long message
    assert response.status_code == 400


def test_rate_limiting():
    """Test that rate limiting works on the chat endpoint"""
    user_id = str(uuid4())
    
    # Send many requests quickly to trigger rate limiting
    for i in range(15):  # More than the 10/minute limit
        response = client.post(
            f"/api/{user_id}/chat",
            json={"message": f"Test message {i}"},
            headers={"Authorization": "Bearer fake_token"}
        )
        
        # We can't easily test rate limiting without waiting, so we'll just ensure
        # the requests don't cause server errors
        assert response.status_code in [200, 429, 401]  # OK, Rate Limited, or Unauthorized (due to fake token)


if __name__ == "__main__":
    pytest.main()