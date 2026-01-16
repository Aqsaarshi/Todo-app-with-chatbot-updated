# Simple rule-based processor for task commands
import re
import json

def process_task_command(message):
    """
    Process task commands using simple rules instead of AI
    """
    message_lower = message.lower().strip()
    
    # Add task command
    if re.match(r'(add|create)\s+task\s+', message_lower):
        # Extract task title
        match = re.search(r'(?:add|create)\s+task\s+(.+)', message_lower)
        if match:
            task_title = match.group(1).strip()
            return {
                "action": "add_task",
                "parameters": {"title": task_title}
            }
        else:
            return {
                "action": "reply",
                "parameters": {},
                "response": "Please specify a task title. Example: 'add task cooking'"
            }
    
    # List tasks command
    elif re.match(r'(list|show|display)\s+tasks?', message_lower):
        return {
            "action": "list_tasks",
            "parameters": {}
        }
    
    # Complete task command
    elif re.match(r'(complete|finish|done)\s+task\s+(\d+)', message_lower):
        match = re.search(r'(?:complete|finish|done)\s+task\s+(\d+)', message_lower)
        if match:
            task_id = int(match.group(1))
            return {
                "action": "complete_task",
                "parameters": {"task_id": task_id}
            }
    
    # Update task command
    elif re.match(r'(update|modify|change)\s+task\s+(\d+)', message_lower):
        match = re.search(r'(?:update|modify|change)\s+task\s+(\d+)(?:\s+to\s+(.+)|\s+(.+))', message_lower)
        if match:
            task_id = int(match.group(1))
            new_title = (match.group(2) or match.group(3)).strip() if (match.group(2) or match.group(3)) else ""
            return {
                "action": "update_task",
                "parameters": {"task_id": task_id, "title": new_title}
            }
    
    # Delete task command
    elif re.match(r'(delete|remove)\s+task\s+(\d+)', message_lower):
        match = re.search(r'(?:delete|remove)\s+task\s+(\d+)', message_lower)
        if match:
            task_id = int(match.group(1))
            return {
                "action": "delete_task",
                "parameters": {"task_id": task_id}
            }
    
    # Default response
    else:
        return {
            "action": "reply",
            "parameters": {},
            "response": f"Sorry, I didn't understand that command: '{message}'. You can say things like 'add task cooking', 'list tasks', 'complete task 1', etc."
        }

# Test the processor
if __name__ == "__main__":
    test_commands = [
        "add task cooking",
        "create task shopping",
        "list tasks",
        "complete task 1",
        "update task 1 to new title",
        "delete task 2",
        "hello"
    ]
    
    for cmd in test_commands:
        result = process_task_command(cmd)
        print(f"Input: '{cmd}' -> Output: {result}")