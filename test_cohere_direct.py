import os
import sys
sys.path.insert(0, r'E:\hackathon-2TODOphase3 - Copy\backend')

from src.services.cohere_service import CohereService
from src.utils.logging import log_error

# Test the Cohere service directly
try:
    cohere_service = CohereService()
    
    # Test prompt similar to what's used in the chat endpoint
    test_prompt = """
    You are an AI assistant that helps users manage their todo tasks.
    Based on the user's message, determine the appropriate action to take.

    Conversation history:

    Current user message:
    add task aqsa

    Available actions:
    - add_task: When user wants to create/add a new task
      Example: "Add task driving" -> ACTION: add_task, PARAMETERS: {"title": "driving"}}
      Example: "Create a task to buy groceries" -> ACTION: add_task, PARAMETERS: {"title": "buy groceries"}}

    - list_tasks: When user wants to see their tasks
      Example: "Show my tasks" -> ACTION: list_tasks, PARAMETERS: {}}

    - complete_task: When user wants to mark a task as completed
      Example: "Complete task 1" -> ACTION: complete_task, PARAMETERS: {"task_id": 1}}

    - update_task: When user wants to modify a task
      Example: "Update task 1 to 'updated title'" -> ACTION: update_task, PARAMETERS: {"task_id": 1, "title": "updated title"}}

    - delete_task: When user wants to remove a task
      Example: "Delete task 1" -> ACTION: delete_task, PARAMETERS: {"task_id": 1}}

    - reply: For general conversation or when no task action is needed

    Respond in the following format:
    ACTION: [add_task|list_tasks|complete_task|update_task|delete_task|reply]
    PARAMETERS: {json_parameters}

    Examples:
    User: "create task driving"
    ACTION: add_task
    PARAMETERS: {"title": "driving"}

    User: "add task buy groceries"
    ACTION: add_task
    PARAMETERS: {"title": "buy groceries"}

    User: "list tasks"
    ACTION: list_tasks
    PARAMETERS: {}

    Now respond to the current user message:
    """
    
    print("Testing Cohere service with sample prompt...")
    response = cohere_service.generate_response(test_prompt)
    print(f"Cohere response: {response}")
    
except Exception as e:
    print(f"Error testing Cohere service: {e}")
    import traceback
    traceback.print_exc()