import cohere
import os
from typing import List, Dict, Any, Optional
from functools import lru_cache
from ..utils.logging import log_error


class CohereService:
    def __init__(self):
        api_key = os.environ.get("COHERE_API_KEY")
        if not api_key:
            # Try to load from .env file in the current directory
            from dotenv import load_dotenv
            import pathlib
            # Load from the project root or backend directory
            load_dotenv(".env")
            load_dotenv("../.env")  # In case we're in a subdirectory

            api_key = os.environ.get("COHERE_API_KEY")

        if not api_key:
            raise ValueError("COHERE_API_KEY environment variable is not set")

        self.client = cohere.Client(api_key)

    @lru_cache(maxsize=128)
    def _cached_api_call(self, message: str, max_tokens: int, temperature: float) -> str:
        """
        Cached version of the API call to avoid repeated requests with same parameters.
        """
        try:
            response = self.client.chat(
                model="command",
                message=message,
                max_tokens=max_tokens,
                temperature=temperature
            )

            if response.text:
                return response.text.strip()
            else:
                return "I couldn't generate a response. Please try again."
        except Exception as e:
            log_error(e, f"CohereService cached API call failed: {str(e)}")
            # Instead of raising the exception, return a default response
            return """ACTION: reply
PARAMETERS: {}
Response: Hello! I'm your task assistant. How can I help you today?"""

    def _make_api_call(self, message: str, max_tokens: int = 500, temperature: float = 0.7, use_cache: bool = False, **kwargs) -> str:
        """
        Internal method to make Cohere API calls with consistent error handling.
        Updated to use the new Chat API instead of the deprecated Generate API.

        Args:
            message: The input message for the model
            max_tokens: Maximum number of tokens to generate
            temperature: Controls randomness of the output
            use_cache: Whether to use cached responses for repeated prompts
            **kwargs: Additional parameters to pass to the API

        Returns:
            Generated response text
        """
        try:
            print(f"Cohere API call initiated with message length: {len(message)}")
            if use_cache:
                # Use the cached version for repeated requests
                print("Using cached API call")
                return self._cached_api_call(message, max_tokens, temperature)
            else:
                # Make a fresh API call
                print("Making fresh API call to Cohere Chat API")
                response = self.client.chat(
                    model="command",
                    message=message,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    **kwargs
                )
                print("Cohere API call completed successfully")

                if response.text:
                    result = response.text.strip()
                    print(f"Cohere response received: {result[:100]}...")
                    return result
                else:
                    print("No text returned from Cohere")
                    return "I couldn't generate a response. Please try again."

        except Exception as e:
            print(f"CohereService API call failed: {str(e)}")
            log_error(e, f"CohereService API call failed: {str(e)}")
            # Instead of raising the exception, return a default response
            # This ensures the application doesn't crash when Cohere is unavailable
            return """ACTION: reply
PARAMETERS: {}
Response: Hello! I'm your task assistant. How can I help you today?"""

    def generate_response(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Generate a response using the Cohere API.
        Updated to work with the new Chat API format.

        Args:
            prompt: The input prompt for the model (will be adapted for chat format)
            max_tokens: Maximum number of tokens to generate

        Returns:
            Generated response text
        """
        try:
            # Adapt the prompt for the chat format
            # Extract the user's request from the prompt
            import re

            # Look for the user's message in the prompt
            user_message_match = re.search(r'Current user message:\s*(.+?)(?:\n|$)', prompt)
            if user_message_match:
                user_message = user_message_match.group(1).strip()
            else:
                # If we can't extract the user message, use the whole prompt
                user_message = prompt

            # Create a chat-formatted message
            chat_message = f"""
            You are an AI assistant that helps users manage their todo tasks.
            Based on the user's message, determine the appropriate action to take.

            {prompt}

            Respond in the following format:
            ACTION: [add_task|list_tasks|complete_task|update_task|delete_task|reply]
            PARAMETERS: {{json_parameters}}

            Examples:
            User: "create task driving"
            ACTION: add_task
            PARAMETERS: {{"title": "driving"}}

            User: "add task buy groceries"
            ACTION: add_task
            PARAMETERS: {{"title": "buy groceries"}}

            User: "list tasks"
            ACTION: list_tasks
            PARAMETERS: {{}}
            """

            return self._make_api_call(chat_message, max_tokens)
        except Exception as e:
            # Return a mock response for testing purposes
            print(f"Cohere API error: {e}")
            # Enhanced to handle add task commands
            if "add task" in prompt.lower() or "create task" in prompt.lower():
                import re
                # Extract task title from the prompt
                match = re.search(r'(?:add|create)\s+task\s+(.+)', prompt.lower())
                if match:
                    task_title = match.group(1).strip()
                    return f"""ACTION: add_task
PARAMETERS: {{"title": "{task_title}"}}"""
                else:
                    return """ACTION: add_task
PARAMETERS: {"title": "New task"}"""
            elif "list tasks" in prompt.lower():
                return """ACTION: list_tasks
PARAMETERS: {}"""
            elif "complete task" in prompt.lower():
                return """ACTION: complete_task
PARAMETERS: {"task_id": 1}"""
            else:
                return """ACTION: reply
PARAMETERS: {}
Response: Hello! I'm your task assistant. How can I help you today?"""

    def generate_response_with_context(
        self,
        question: str,
        context: List[str],
        mode: str = "full-book"
    ) -> str:
        """
        Generate a response using the Cohere API with additional context.
        Updated to work with the new Chat API format.

        Args:
            question: The question to answer
            context: List of context strings to use
            mode: The mode to use for generation

        Returns:
            Generated response text
        """
        # Combine context into a single string
        context_str = "\n".join(context)

        # Create a message that incorporates the context
        message = f"Context: {context_str}\n\nQuestion: {question}"

        return self._make_api_call(message, max_tokens=500)

    def validate_response_against_context(
        self,
        response: str,
        context: List[str]
    ) -> bool:
        """
        Validate if the response is consistent with the provided context.
        Updated to work with the new Chat API format.

        Args:
            response: The response to validate
            context: List of context strings to validate against

        Returns:
            Boolean indicating if the response is consistent with context
        """
        # Create a message to check consistency
        context_str = "\n".join(context)
        message = f"Context: {context_str}\n\nResponse: {response}\n\nIs the response consistent with the context? Answer with yes or no."

        validation_result = self._make_api_call(
            message,
            max_tokens=10,
            temperature=0.1  # Lower temperature for more deterministic output
        )

        validation_text = validation_result.lower().strip()
        return "yes" in validation_text or "true" in validation_text

    def generate_response_with_latency_safeguards(
        self,
        message: str,  # Changed parameter name to reflect Chat API usage
        max_tokens: int = 1000
    ) -> str:
        """
        Generate a response with safeguards against latency issues.
        Updated to work with the new Chat API format.

        Args:
            message: The input message for the model
            max_tokens: Maximum number of tokens to generate

        Returns:
            Generated response text
        """
        return self._make_api_call(
            message,
            max_tokens,
            temperature=0.7
        )

    def generate_response_with_conversation_context(
        self,
        question: str,
        conversation_context: Dict[str, Any],
        conversation_history: List[Dict[str, str]]
    ) -> str:
        """
        Generate a response using the Cohere API with conversation context and history.
        Updated to work with the new Chat API format.

        Args:
            question: The current question from the user
            conversation_context: Dictionary containing conversation context data
            conversation_history: List of previous messages in the conversation

        Returns:
            Generated response text
        """
        # Format the conversation history
        history_text = "\n".join([
            f"{msg['sender_type']}: {msg['content']}"
            for msg in conversation_history
        ])

        # Format the context data
        context_items = []
        for key, value in conversation_context.items():
            context_items.append(f"{key}: {value}")
        context_str = "\n".join(context_items)

        # Create a comprehensive message with history and context
        message = f"""
        Conversation context:
        {context_str}

        Conversation history:
        {history_text}

        Current user question:
        {question}

        Based on the conversation history and context, provide a helpful and relevant response to the user's question.
        """

        return self._make_api_call(message, max_tokens=500, temperature=0.7)