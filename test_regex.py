import re

# Test the regex patterns
user_message = "add task cooking"

print(f"Testing with user_message: '{user_message}'")

# Check for add task command
if re.search(r'\b(add|create)\s+task\b', user_message, re.IGNORECASE):
    print("Pattern matched: \\b(add|create)\\s+task\\b")
    # Extract the task title from the user message
    match = re.search(r'(?:add|create)\s+task\s+(.+)', user_message, re.IGNORECASE)
    if match:
        task_title = match.group(1).strip()
        print(f"Extracted task title: '{task_title}'")
        action = "add_task"
        params = {"title": task_title}
        print(f"Inferred action: {action} with params: {params}")
    else:
        print("Could not extract task title from user message")
else:
    print("Pattern did not match")

# Test other patterns
user_message2 = "list tasks"
if re.search(r'\b(list|show|display)\s+task', user_message2, re.IGNORECASE):
    print(f"'{user_message2}' matches list task pattern")
else:
    print(f"'{user_message2}' does not match list task pattern")