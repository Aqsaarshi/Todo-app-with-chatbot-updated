import logging
from datetime import datetime
from typing import Any, Dict


def setup_chat_logger(name: str = "chat_logger"):
    """
    Set up a logger for chat functionality.
    
    Args:
        name: Name of the logger
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Prevent adding multiple handlers if logger already exists
    if logger.handlers:
        return logger
    
    # Create console handler
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger


def log_chat_interaction(
    user_id: str,
    conversation_id: int,
    user_message: str,
    assistant_response: str,
    tool_calls: list = None
):
    """
    Log a chat interaction.
    
    Args:
        user_id: ID of the user
        conversation_id: ID of the conversation
        user_message: Message from the user
        assistant_response: Response from the assistant
        tool_calls: List of tool calls made during the interaction
    """
    logger = setup_chat_logger()
    
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "conversation_id": conversation_id,
        "user_message": user_message,
        "assistant_response": assistant_response,
        "tool_calls": tool_calls or []
    }
    
    logger.info(f"Chat interaction: {log_data}")


def log_tool_execution(
    user_id: str,
    conversation_id: int,
    tool_name: str,
    parameters: Dict[str, Any],
    result: Dict[str, Any]
):
    """
    Log a tool execution.

    Args:
        user_id: ID of the user
        conversation_id: ID of the conversation
        tool_name: Name of the tool executed
        parameters: Parameters passed to the tool
        result: Result of the tool execution
    """
    logger = setup_chat_logger()

    # Convert UUIDs to strings for JSON serialization
    import uuid
    def convert_uuids(obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        elif isinstance(obj, dict):
            return {key: convert_uuids(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_uuids(item) for item in obj]
        return obj

    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "conversation_id": conversation_id,
        "tool_name": tool_name,
        "parameters": convert_uuids(parameters),
        "result": convert_uuids(result)
    }

    logger.info(f"Tool execution: {log_data}")


def log_error(error: Exception, context: str = ""):
    """
    Log an error with context.
    
    Args:
        error: Exception that occurred
        context: Context where the error occurred
    """
    logger = setup_chat_logger()
    
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "error_type": type(error).__name__,
        "error_message": str(error),
        "context": context
    }
    
    logger.error(f"Error occurred: {log_data}")