from typing import Dict, Any, List, Optional
import json
from sqlmodel import Session
from ..services.cohere_service import CohereService
from ..tools.mcp_tools import MCPTaskTools
from ..utils.logging import log_chat_interaction, log_tool_execution, log_error


class ChatService:
    """
    Service to handle chat interactions, integrating Cohere AI with MCP tools.
    """
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.cohere_service = CohereService()
        self.mcp_tools = MCPTaskTools(db_session)
    
    def process_user_message(
        self,
        user_id: str,
        conversation_id: int,
        user_message: str,
        conversation_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Process a user message and generate an appropriate response.

        Args:
            user_id: ID of the user
            conversation_id: ID of the conversation
            user_message: The message from the user
            conversation_history: History of the conversation

        Returns:
            Dictionary containing response text and any tool calls made
        """
        try:
            # Prepare the prompt with conversation history
            history_text = "\n".join([
                f"{msg['sender_type']}: {msg['content']}"
                for msg in conversation_history
            ])

            full_prompt = f"""
            Conversation history:
            {history_text}

            Current user message:
            {user_message}

            Based on the user's message, decide which action to take. Respond in the following format:
            ACTION: [add_task|list_tasks|complete_task|update_task|delete_task|reply]
            PARAMETERS: {{json_parameters}}

            If the user wants to perform a task operation, use the appropriate action.
            If the user is asking a general question or just chatting, use ACTION: reply
            """

            # Get response from Cohere
            cohere_response = self.cohere_service.generate_response(full_prompt)

            # Parse the response to determine action
            action = "reply"
            params = {}

            if "ACTION:" in cohere_response and "PARAMETERS:" in cohere_response:
                try:
                    action_parts = cohere_response.split("ACTION:")
                    if len(action_parts) > 1:
                        action_line = action_parts[1].split("\n")[0].strip()
                        params_parts = cohere_response.split("PARAMETERS:")
                        if len(params_parts) > 1:
                            params_line = params_parts[1].strip()

                            action = action_line
                            params = json.loads(params_line)
                except (IndexError, json.JSONDecodeError):
                    # If parsing fails, treat as a reply
                    action = "reply"
                    params = {}

            # Execute the appropriate action
            tool_calls = []
            response_text = ""

            if action == "add_task":
                result = self.mcp_tools.add_task(
                    user_id=user_id,
                    title=params.get("title", ""),
                    description=params.get("description", "")
                )
                response_text = f"I've added the task '{result['title']}' to your list."
                tool_calls.append({
                    "tool_name": "add_task",
                    "parameters": params,
                    "result": result
                })
            elif action == "list_tasks":
                status_filter = params.get("status")
                result = self.mcp_tools.list_tasks(user_id, status_filter)
                if result:
                    task_titles = [task["title"] for task in result]
                    response_text = f"Here are your tasks: {', '.join(task_titles)}"
                else:
                    response_text = "You don't have any tasks."
                tool_calls.append({
                    "tool_name": "list_tasks",
                    "parameters": params,
                    "result": result
                })
            elif action == "complete_task":
                result = self.mcp_tools.complete_task(
                    user_id=user_id,
                    task_id=params.get("task_id")
                )
                response_text = f"I've marked the task '{result['title']}' as completed."
                tool_calls.append({
                    "tool_name": "complete_task",
                    "parameters": params,
                    "result": result
                })
            elif action == "update_task":
                result = self.mcp_tools.update_task(
                    user_id=user_id,
                    task_id=params.get("task_id"),
                    title=params.get("title"),
                    description=params.get("description")
                )
                response_text = f"I've updated the task to '{result['title']}'."
                tool_calls.append({
                    "tool_name": "update_task",
                    "parameters": params,
                    "result": result
                })
            elif action == "delete_task":
                result = self.mcp_tools.delete_task(
                    user_id=user_id,
                    task_id=params.get("task_id")
                )
                response_text = f"I've deleted the task '{result['title']}'."
                tool_calls.append({
                    "tool_name": "delete_task",
                    "parameters": params,
                    "result": result
                })
            else:  # reply
                # If Cohere didn't specify an action or parsing failed, generate a general response
                response_text = self.cohere_service.generate_response(
                    f"User message: {user_message}. Provide a helpful response."
                )

            # Log the chat interaction
            log_chat_interaction(
                user_id=user_id,
                conversation_id=conversation_id,
                user_message=user_message,
                assistant_response=response_text,
                tool_calls=tool_calls
            )

            return {
                "response": response_text,
                "tool_calls": tool_calls
            }
        except Exception as e:
            log_error(e, f"ChatService.process_user_message for user {user_id}")
            return {
                "response": "Sorry, I encountered an error processing your request. Please try again.",
                "tool_calls": []
            }
    
    def validate_response_with_context(
        self,
        response: str,
        context: List[str]
    ) -> bool:
        """
        Validate if the response is consistent with the provided context.
        
        Args:
            response: The response to validate
            context: List of context strings to validate against
            
        Returns:
            Boolean indicating if the response is consistent with context
        """
        return self.cohere_service.validate_response_against_context(response, context)
    
    def generate_response_with_context(
        self,
        question: str,
        context: List[str],
        mode: str = "full-book"
    ) -> str:
        """
        Generate a response using the Cohere API with additional context.
        
        Args:
            question: The question to answer
            context: List of context strings to use
            mode: The mode to use for generation
            
        Returns:
            Generated response text
        """
        return self.cohere_service.generate_response_with_context(question, context, mode)