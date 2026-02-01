from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional
from datetime import datetime
import json
import traceback
import re
import uuid
from ..models.message import Message
from ..database import get_session
from ..middleware.auth import get_current_user, verify_user_in_path_matches_token
from ..models.user import User
from ..models.conversation import Conversation

from ..models.tool_call import ToolCall
from ..services.cohere_service import CohereService
from ..tools.mcp_tools import MCPTaskTools
from ..utils.logging import log_error, log_chat_interaction, log_tool_execution




def sanitize_input(input_str: str) -> str:
    """
    Sanitize user input to prevent injection attacks.

    Args:
        input_str: User input string

    Returns:
        Sanitized string
    """
    if not input_str:
        return input_str

    # Remove potentially dangerous characters/sequences
    # Allow alphanumeric, spaces, punctuation, but remove potential script tags or SQL injection patterns
    sanitized = re.sub(r'<script[^>]*>.*?</script>', '', input_str, flags=re.IGNORECASE)
    sanitized = re.sub(r'<iframe[^>]*>.*?</iframe>', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'[<>"\';]', '', sanitized)  # Basic tag removal
    return sanitized.strip()


# Router for authenticated users
router = APIRouter(prefix="/{user_id}", tags=["chat"])




@router.post("/chat", response_model=dict)
async def chat(
    user_id: str,
    message_data: dict,
    token: str = Query(..., alias="token"),
    db_session: AsyncSession = Depends(get_session)
):
    # Get current user from token (same as in tasks endpoint)
    from ..auth.jwt import verify_token
    from uuid import UUID

    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_user_id = payload.get("sub")
    if token_user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Convert to UUID for comparison
    try:
        token_user_id_uuid = UUID(token_user_id)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid user ID in token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify that the user ID in the path matches the token
    try:
        path_user_id = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID format"
        )

    if path_user_id != token_user_id_uuid:
        raise HTTPException(
            status_code=403,
            detail="User ID in path does not match token"
        )

    # Get user from database
    from sqlmodel import select
    from ..models.user import User
    result = await db_session.exec(select(User).where(User.id == token_user_id_uuid))
    current_user = result.first()
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    """
    Initiate or continue a conversation with the AI assistant.

    Args:
        user_id: The ID of the authenticated user
        message_data: Contains the message content and optional conversation_id
        current_user: The authenticated user
        db_session: Database session

    Returns:
        Dictionary containing conversation_id, response, tool_calls, and timestamp
    """
    # Verify that the user ID in the path matches the token
    await verify_user_in_path_matches_token(user_id, current_user)

    # Extract message and conversation_id from the request
    user_message = message_data.get("message")
    conversation_id = message_data.get("conversation_id")

    # Validation: Check if message content is provided
    if not user_message or not user_message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message content is required and cannot be empty"
        )

    # Sanitize user input to prevent injection attacks
    user_message = sanitize_input(user_message)

    # Validation: Check message length
    if len(user_message) > 1000:  # Arbitrary limit, can be adjusted
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message is too long. Please keep it under 1000 characters."
        )

    # Log the incoming request
    print(f"Processing chat request for user {user_id}, conversation {conversation_id}")

    # Get or create conversation
    current_conversation_id = None
    # Use a consistent variable name
    conversation_obj = None
    if conversation_id:
        # Convert conversation_id to int if it's a string
        try:
            conversation_id_int = int(conversation_id)
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid conversation ID format"
            )

        # Try to get existing conversation
        conversation_obj = await db_session.get(Conversation, conversation_id_int)
        if not conversation_obj or conversation_obj.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found or does not belong to user"
            )
        current_conversation_id = conversation_obj.id
    else:
        # Create new conversation
        conversation_obj = Conversation(user_id=user_id)
        db_session.add(conversation_obj)
        await db_session.commit()
        await db_session.refresh(conversation_obj)
        current_conversation_id = conversation_obj.id

    # Debug print
    print(f"About to create user message for conversation {current_conversation_id}")

    # Save user message
    user_msg = Message(
        conversation_id=current_conversation_id,
        sender_type="user",
        content=user_message
    )
    db_session.add(user_msg)
    await db_session.commit()
    await db_session.refresh(user_msg)

    # Get conversation history for context
    # Using direct query to avoid async issues
    try:
        statement = (
            select(Message)
            .where(Message.conversation_id == current_conversation_id)
            .order_by(Message.timestamp.asc())
        )
        result = await db_session.exec(statement)
        history = result.all()
    except Exception as e:
        log_error(e, f"Error retrieving conversation history for conversation {current_conversation_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving conversation history"
        )

    try:
        # Initialize Cohere service and MCP tools
        print(f"Initializing Cohere service and MCP tools for conversation {current_conversation_id}")
        cohere_service = CohereService()
        mcp_tools = MCPTaskTools(db_session, conversation_id=current_conversation_id)

        # Prepare the prompt with conversation history
        history_text = "\n".join([f"{msg.sender_type}: {msg.content}" for msg in history])
        full_prompt = f"""
        You are an AI assistant that helps users manage their todo tasks.
        Based on the user's message, determine the appropriate action to take.

        Conversation history:
        {history_text}

        Current user message:
        {user_message}

        Available actions:
        - add_task: When user wants to create/add a new task
          Example: "Add task driving" -> ACTION: add_task, PARAMETERS: {{"title": "driving"}}
          Example: "Create a task to buy groceries" -> ACTION: add_task, PARAMETERS: {{"title": "buy groceries"}}

        - list_tasks: When user wants to see their tasks
          Example: "Show my tasks" -> ACTION: list_tasks, PARAMETERS: {{}}

        - complete_task: When user wants to mark a task as completed
          Example: "Complete task 1" -> ACTION: complete_task, PARAMETERS: {{"task_id": 1}}

        - update_task: When user wants to modify a task
          Example: "Update task 1 to 'updated title'" -> ACTION: update_task, PARAMETERS: {{"task_id": 1, "title": "updated title"}}

        - delete_task: When user wants to remove a task
          Example: "Delete task 1" -> ACTION: delete_task, PARAMETERS: {{"task_id": 1}}

        - reply: For general conversation or when no task action is needed

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

        Now respond to the current user message:
        """

        # Get response from Cohere
        print(f"Sending prompt to Cohere service: {len(full_prompt)} characters")
        try:
            cohere_response = cohere_service.generate_response(full_prompt)
            print(f"Cohere response received: {cohere_response[:100]}...")
        except Exception as e:
            print(f"Cohere service error: {str(e)}")
            # Fallback to rule-based processing if Cohere is unavailable
            cohere_response = f"Current user message: {user_message}"
            print(f"Using fallback rule-based processing with user message: {user_message}")

        # Parse the response to determine action
        action = "reply"
        params = {}

        print(f"Parsing Cohere response: {cohere_response[:200]}...")

        # Look for ACTION and PARAMETERS sections in the response
        if "ACTION:" in cohere_response and "PARAMETERS:" in cohere_response:
            try:
                # Extract action
                action_start = cohere_response.find("ACTION:") + len("ACTION:")
                action_end = cohere_response.find("\n", action_start)
                if action_end == -1:  # If no newline, use end of "ACTION:" section
                    action_end = cohere_response.find("PARAMETERS:")

                action_text = cohere_response[action_start:action_end].strip().rstrip(':')
                action = action_text.split()[0] if action_text.split() else "reply"

                # Extract parameters
                param_start = cohere_response.find("PARAMETERS:") + len("PARAMETERS:")
                param_section = cohere_response[param_start:].strip()

                # Find the JSON object in the parameters section
                brace_start = param_section.find('{')
                if brace_start != -1:
                    # Find matching closing brace
                    brace_count = 0
                    brace_end = -1
                    for i, char in enumerate(param_section[brace_start:], brace_start):
                        if char == '{':
                            brace_count += 1
                        elif char == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                brace_end = i + 1
                                break

                    if brace_end != -1:
                        json_str = param_section[brace_start:brace_end]
                        params = json.loads(json_str)

                print(f"Parsed action: {action}, params: {params}")
            except (ValueError, json.JSONDecodeError, IndexError) as parse_error:
                # If parsing fails, log the error and treat as a reply
                log_error(parse_error, f"Error parsing Cohere response: {cohere_response}")
                action = "reply"
                params = {}
                print(f"Parsing failed, treating as reply. Error: {parse_error}")
        else:
            # If no proper ACTION/PARAMETERS format found, treat as a reply
            action = "reply"
            params = {}
            print("No proper ACTION/PARAMETERS format found in response, treating as reply")

        # If action is still reply, try to infer from user message using simple rule-based approach
        if action == "reply":
            print(f"Attempting to infer action from user message: {user_message}")
            import re

            # Simple and effective command detection
            message_lower = user_message.lower().strip()

            # Determine action based on the first word/command
            if message_lower.startswith('list') or 'list task' in message_lower or message_lower.startswith('show'):
                action = "list_tasks"
                params = {}
                print(f"Rule-based inference: {action}")

            elif message_lower.startswith('complete') or message_lower.startswith('finish') or message_lower.startswith('done'):
                # Extract task ID - look for number or UUID after command
                # More flexible pattern to catch both numeric IDs and UUIDs
                match = re.search(r'(complete|finish|done)\s+(task\s+|#)?([a-f0-9\-]+)', message_lower)
                if match:
                    task_id = match.group(3)
                    action = "complete_task"
                    params = {"task_id": task_id}
                    print(f"Rule-based inference: {action} with params: {params}")
                else:
                    # Try to extract the ID in other ways
                    parts = message_lower.split()
                    for i, part in enumerate(parts):
                        if part in ['task', '#'] and i + 1 < len(parts):
                            # Next part after 'task' or '#' is the ID
                            task_id = parts[i + 1]
                            # Clean up the ID
                            task_id = re.sub(r'[^\w\-]', '', task_id)
                            if task_id:
                                action = "complete_task"
                                params = {"task_id": task_id}
                                print(f"Rule-based inference: {action} with params: {params}")
                                break
                        elif i > 0 and part.replace('-', '').isdigit():  # Check if it's numeric
                            # Previous part was likely 'complete', so this is the ID
                            task_id = part
                            action = "complete_task"
                            params = {"task_id": task_id}
                            print(f"Rule-based inference: {action} with params: {params}")
                            break

            elif message_lower.startswith('update') or message_lower.startswith('edit'):
                # Look for "update task X to Y" pattern with more flexibility
                match = re.search(r'(update|edit)\s+(task\s+|#)?([a-f0-9\-]+)\s+(to|as|with)\s+(.+)', message_lower)
                if match:
                    task_id = match.group(3)
                    new_title = match.group(4)
                    action = "update_task"
                    params = {"task_id": task_id, "title": new_title}
                    print(f"Rule-based inference: {action} with params: {params}")
                else:
                    # Alternative pattern: "update task X Y" (without 'to')
                    match = re.search(r'(update|edit)\s+(task\s+|#)?([a-f0-9\-]+)\s+(.+)', message_lower)
                    if match:
                        task_id = match.group(3)
                        new_title = match.group(4)
                        action = "update_task"
                        params = {"task_id": task_id, "title": new_title}
                        print(f"Rule-based inference: {action} with params: {params}")

            elif message_lower.startswith('delete') or message_lower.startswith('remove'):
                # Extract task ID for delete with more flexibility
                match = re.search(r'(delete|remove)\s+(task\s+|#)?([a-f0-9\-]+)', message_lower)
                if match:
                    task_id = match.group(3)
                    action = "delete_task"
                    params = {"task_id": task_id}
                    print(f"Rule-based inference: {action} with params: {params}")
                else:
                    # Try to extract the ID in other ways
                    parts = message_lower.split()
                    for i, part in enumerate(parts):
                        if part in ['task', '#'] and i + 1 < len(parts):
                            # Next part after 'task' or '#' is the ID
                            task_id = parts[i + 1]
                            # Clean up the ID
                            task_id = re.sub(r'[^\w\-]', '', task_id)
                            if task_id:
                                action = "delete_task"
                                params = {"task_id": task_id}
                                print(f"Rule-based inference: {action} with params: {params}")
                                break
                        elif i > 0 and part.replace('-', '').isdigit():  # Check if it's numeric
                            # Previous part was likely 'delete', so this is the ID
                            task_id = part
                            action = "delete_task"
                            params = {"task_id": task_id}
                            print(f"Rule-based inference: {action} with params: {params}")
                            break

            elif message_lower.startswith('add') or message_lower.startswith('create'):
                # Extract task title after 'add'/'create' command
                match = re.search(r'(add|create)\s+(a\s+)?(task\s+|#)?(.+)', message_lower)
                if match:
                    task_title = match.group(4).strip()
                    # Clean up the title (remove trailing punctuation)
                    task_title = re.sub(r'[^\w\s\-_]', '', task_title).strip()
                    if task_title:
                        action = "add_task"
                        params = {"title": task_title}
                        print(f"Rule-based inference: {action} with params: {params}")

            else:
                # Default to reply if no command is recognized
                action = "reply"
                params = {}
                print(f"Defaulting to reply action")

        # Execute the appropriate action with validation
        tool_calls = []
        response_text = ""

        print(f"Executing action: {action} with params: {params}")

        try:
            # For authenticated users, proceed with normal task operations
            if action == "add_task":
                print("Processing add_task action")
                # Validate required parameters
                if not params.get("title"):
                    # If no title in params, try to extract from the original user message
                    import re
                    # Look for patterns like "add task [title]" or "create task [title]"
                    match = re.search(r'(?:add|create)\s+task\s+(.+)', user_message.lower())
                    if match:
                        extracted_title = match.group(1).strip()
                        params["title"] = extracted_title
                        print(f"Extracted title from user message: {extracted_title}")
                    else:
                        print("No title provided in params or user message")
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Title is required to add a task"
                        )

                print(f"Calling mcp_tools.add_task with title: {params.get('title', '')}")

                # Validate the title parameter to prevent empty titles
                title = params.get("title", "").strip()
                if not title:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Task title cannot be empty"
                    )

                result = await mcp_tools.add_task(
                    user_id=user_id,
                    title=title,
                    description=params.get("description", "")
                )
                print(f"Task added successfully: {result}")
                response_text = f"I've added the task '{result['title']}' to your list."
                tool_calls.append({
                    "tool_name": "add_task",
                    "parameters": params,
                    "result": result
                })
                # Log the tool execution
                log_tool_execution(
                    user_id=user_id,
                    conversation_id=current_conversation_id,
                    tool_name="add_task",
                    parameters=params,
                    result=result
                )
            elif action == "list_tasks":
                status_filter = params.get("status")
                result = await mcp_tools.list_tasks(user_id, status_filter)
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
                # Log the tool execution
                log_tool_execution(
                    user_id=user_id,
                    conversation_id=current_conversation_id,
                    tool_name="list_tasks",
                    parameters=params,
                    result=result
                )
            elif action == "complete_task":
                # Validate required parameters
                if not params.get("task_id"):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Task ID is required to complete a task"
                    )

                # The task_id can be either a UUID string or a numeric ID
                # Pass the task_id as a string to the MCP tools which will handle validation
                task_id = params.get("task_id")

                result = await mcp_tools.complete_task(
                    user_id=user_id,
                    task_id=task_id
                )
                response_text = f"I've marked the task '{result['title']}' as completed."
                tool_calls.append({
                    "tool_name": "complete_task",
                    "parameters": params,
                    "result": result
                })
                # Log the tool execution
                log_tool_execution(
                    user_id=user_id,
                    conversation_id=current_conversation_id,
                    tool_name="complete_task",
                    parameters=params,
                    result=result
                )
            elif action == "update_task":
                # Validate required parameters
                if not params.get("task_id"):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Task ID is required to update a task"
                    )

                if not params.get("title"):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Title is required to update a task"
                    )

                # The task_id can be either a UUID string or a numeric ID
                # Pass the task_id as a string to the MCP tools which will handle validation
                task_id = params.get("task_id")
                title = params.get("title")

                try:
                    result = await mcp_tools.update_task(
                        user_id=user_id,
                        task_id=task_id,
                        title=title,
                        description=params.get("description")
                    )
                    response_text = f"I've updated the task to '{result['title']}'."
                    tool_calls.append({
                        "tool_name": "update_task",
                        "parameters": params,
                        "result": result
                    })
                    # Log the tool execution
                    log_tool_execution(
                        user_id=user_id,
                        conversation_id=current_conversation_id,
                        tool_name="update_task",
                        parameters=params,
                        result=result
                    )
                except Exception as e:
                    print(f"Error updating task {task_id}: {str(e)}")
                    response_text = f"Sorry, I couldn't update the task. The task with ID '{task_id}' might not exist."
                    # Still log the attempt
                    log_tool_execution(
                        user_id=user_id,
                        conversation_id=current_conversation_id,
                        tool_name="update_task",
                        parameters=params,
                        result={"error": str(e)}
                    )
            elif action == "delete_task":
                # Validate required parameters
                if not params.get("task_id"):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Task ID is required to delete a task"
                    )

                # The task_id can be either a UUID string or a numeric ID
                # Pass the task_id as a string to the MCP tools which will handle validation
                task_id = params.get("task_id")

                result = await mcp_tools.delete_task(
                    user_id=user_id,
                    task_id=task_id
                )
                response_text = f"I've deleted the task '{result['title']}'."
                tool_calls.append({
                    "tool_name": "delete_task",
                    "parameters": params,
                    "result": result
                })
                # Log the tool execution
                log_tool_execution(
                    user_id=user_id,
                    conversation_id=current_conversation_id,
                    tool_name="delete_task",
                    parameters=params,
                    result=result
                )
            else:  # reply
                # If Cohere didn't specify an action or parsing failed, generate a general response
                response_text = "I understood your message. How else can I help you?"
        except HTTPException:
            # Re-raise HTTP exceptions as they are already properly formatted
            raise
        except Exception as e:
            print(f"Error executing action: {e}")
            log_error(e, f"Error executing action {action} with params {params}")
            response_text = f"Sorry, I encountered an error processing your request: {str(e)}"
            # Still save the assistant message even if there was an error

        # Save assistant message
        assistant_msg = Message(
            conversation_id=current_conversation_id,
            sender_type="assistant",
            content=response_text
        )
        db_session.add(assistant_msg)
        await db_session.flush()  # Use flush instead of commit to avoid session conflicts

        # Save tool calls if any (in the same session to avoid conflicts)
        if tool_calls:
            try:
                for tool_call_data in tool_calls:
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

                    tool_call = ToolCall(
                        message_id=assistant_msg.id,
                        tool_name=tool_call_data["tool_name"],
                        parameters=convert_uuids(tool_call_data["parameters"]),
                        result=convert_uuids(tool_call_data["result"])
                    )
                    db_session.add(tool_call)

            except Exception as e:
                # If tool call saving fails, log the error but don't fail the main request
                print(f"Error saving tool call: {e}")
                from ..utils.logging import log_error
                log_error(e, f"Failed to save tool call for message {assistant_msg.id}")
                # Continue with the main request anyway

        # Final commit for all changes
        await db_session.commit()
        await db_session.refresh(assistant_msg)

        # Log the chat interaction
        log_chat_interaction(
            user_id=user_id,
            conversation_id=current_conversation_id,
            user_message=user_message,
            assistant_response=response_text,
            tool_calls=tool_calls
        )

        # Return response
        response_data = {
            "conversation_id": current_conversation_id,
            "response": response_text,
            "tool_calls": tool_calls,
            "timestamp": datetime.utcnow().isoformat()
        }

        # Ensure response is properly formatted JSON
        print(f"Returning response for conversation {current_conversation_id}: {response_data}")

        return response_data
    except HTTPException:
        # Re-raise HTTP exceptions as they are already properly formatted
        raise
    except Exception as e:
        # Log the full traceback for debugging
        error_details = traceback.format_exc()
        from ..utils.logging import log_error
        log_error(e, f"Unexpected error in chat endpoint: {error_details}")

        # Ensure we have a conversation ID to return
        if 'current_conversation_id' not in locals() and conversation_id:
            current_conversation_id = conversation_id
        elif 'current_conversation_id' not in locals():
            # Create a new conversation if needed
            conversation_obj = Conversation(user_id=user_id)
            db_session.add(conversation_obj)
            await db_session.commit()
            await db_session.refresh(conversation_obj)
            current_conversation_id = conversation_obj.id

        # Handle any errors in the AI processing
        error_msg = "Sorry, I encountered an error processing your request. Please try again."

        try:
            assistant_msg = Message(
                conversation_id=current_conversation_id,
                sender_type="assistant",
                content=error_msg
            )
            db_session.add(assistant_msg)
            await db_session.commit()
            await db_session.refresh(assistant_msg)
        except Exception as db_error:
            print(f"Error saving error message to DB: {db_error}")

        # Log the error interaction
        try:
            log_chat_interaction(
                user_id=user_id,
                conversation_id=current_conversation_id,
                user_message=user_message,
                assistant_response=error_msg,
                tool_calls=[]
            )
        except Exception as log_error:
            print(f"Error logging chat interaction: {log_error}")

        return {
            "conversation_id": current_conversation_id,
            "response": error_msg,
            "tool_calls": [],
            "timestamp": datetime.utcnow().isoformat()
        }






@router.get("/conversations", response_model=dict)
async def get_conversations(
    user_id: str,
    token: str = Query(..., alias="token"),
    db_session: AsyncSession = Depends(get_session),
    limit: int = 10,
    offset: int = 0
):
    # Get current user from token (same as in tasks endpoint)
    from ..auth.jwt import verify_token
    from uuid import UUID

    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_user_id = payload.get("sub")
    if token_user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Convert to UUID for comparison
    try:
        token_user_id_uuid = UUID(token_user_id)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid user ID in token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify that the user ID in the path matches the token
    try:
        path_user_id = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID format"
        )

    if path_user_id != token_user_id_uuid:
        raise HTTPException(
            status_code=403,
            detail="User ID in path does not match token"
        )

    # Get user from database
    from sqlmodel import select
    from ..models.user import User
    result = await db_session.exec(select(User).where(User.id == token_user_id_uuid))
    current_user = result.first()
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    """
    Retrieve a list of user's conversations.

    Args:
        user_id: The ID of the authenticated user
        current_user: The authenticated user
        db_session: Database session
        limit: Number of conversations to return
        offset: Number of conversations to skip

    Returns:
        Dictionary containing conversations and total count
    """
    # Verify that the user ID in the path matches the token
    await verify_user_in_path_matches_token(user_id, current_user)

    # Query conversations for the user
    statement = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())  # Order by most recent first
        .offset(offset)
        .limit(limit)
    )
    result = await db_session.exec(statement)
    conversations = result.all()

    # Count total conversations for the user
    count_statement = select(Conversation).where(Conversation.user_id == user_id)
    count_result = await db_session.exec(count_statement)
    total_count = len(count_result.all())

    # Format response
    conversations_data = [
        {
            "id": conv.id,
            "title": conv.title,
            "created_at": conv.created_at.isoformat(),
            "updated_at": conv.updated_at.isoformat(),
            "context_data": conv.context_data  # Include context data for enhanced functionality
        }
        for conv in conversations
    ]

    return {
        "conversations": conversations_data,
        "total_count": total_count
    }


@router.get("/conversations/{conversation_id}/messages", response_model=dict)
async def get_messages(
    user_id: str,
    conversation_id: int,
    token: str = Query(..., alias="token"),
    db_session: AsyncSession = Depends(get_session),
    limit: int = 50,
    offset: int = 0
):
    # Get current user from token (same as in tasks endpoint)
    from ..auth.jwt import verify_token
    from uuid import UUID

    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_user_id = payload.get("sub")
    if token_user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Convert to UUID for comparison
    try:
        token_user_id_uuid = UUID(token_user_id)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid user ID in token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify that the user ID in the path matches the token
    try:
        path_user_id = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID format"
        )

    if path_user_id != token_user_id_uuid:
        raise HTTPException(
            status_code=403,
            detail="User ID in path does not match token"
        )

    # Get user from database
    from sqlmodel import select
    from ..models.user import User
    result = await db_session.exec(select(User).where(User.id == token_user_id_uuid))
    current_user = result.first()
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    """
    Retrieve messages for a specific conversation.

    Args:
        user_id: The ID of the authenticated user
        conversation_id: The ID of the conversation
        current_user: The authenticated user
        db_session: Database session
        limit: Number of messages to return
        offset: Number of messages to skip

    Returns:
        Dictionary containing messages and total count
    """
    # Verify that the user ID in the path matches the token
    await verify_user_in_path_matches_token(user_id, current_user)

    # Verify that the conversation belongs to the user
    conversation = await db_session.get(Conversation, conversation_id)
    if not conversation or conversation.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or does not belong to user"
        )

    # Query messages for the conversation
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.timestamp.asc())  # Order messages chronologically
        .offset(offset)
        .limit(limit)
    )
    result = await db_session.exec(statement)
    messages = result.all()

    # Count total messages for the conversation
    count_statement = select(Message).where(Message.conversation_id == conversation_id)
    count_result = await db_session.exec(count_statement)
    total_count = len(count_result.all())

    # Format response
    messages_data = []
    for msg in messages:
        # Get associated tool calls for this message
        tool_calls_statement = select(ToolCall).where(ToolCall.message_id == msg.id)
        tool_calls_result = await db_session.exec(tool_calls_statement)
        tool_calls = tool_calls_result.all()

        tool_calls_data = [
            {
                "id": tc.id,
                "tool_name": tc.tool_name,
                "parameters": tc.parameters,
                "result": tc.result,
                "executed_at": tc.executed_at.isoformat() if tc.executed_at else None
            }
            for tc in tool_calls
        ]

        messages_data.append({
            "id": msg.id,
            "sender_type": msg.sender_type,
            "content": msg.content,
            "timestamp": msg.timestamp.isoformat(),
            "tool_calls": tool_calls_data
        })

    return {
        "messages": messages_data,
        "total_count": total_count,
        "conversation_context": conversation.context_data  # Include conversation context
    }


