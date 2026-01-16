import re

def test_all_patterns():
    # Test message
    message_lower = "complete task fbb57543-a65b-4040-84de-1c23324f03cc"
    
    print(f"Testing message: '{message_lower}'")
    
    # Add task command - supports various ways to add a task
    add_task_patterns = [
        r'(add|create|make|new)\s+(a\s+)?task\s+(.+)',
        r'(add|create|make|new)\s+(.+)\s+(as\s+)?a\s+task',
        r'(add|create|make|new)\s+(.+)',
        r'(.+)\s+(please|pls|now|today)'
    ]

    for pattern in add_task_patterns:
        match = re.search(pattern, message_lower)
        if match:
            print(f"Add task pattern matched: {pattern}")
            print(f"Groups: {match.groups()}")
            break
    else:
        print("No add task pattern matched")

    # List tasks command - supports various ways to list tasks
    list_patterns = [
        r'(list|show|display|view|see|get)\s+(my\s+)?(all\s+)?tasks?',
        r'what\s+(are|is)\s+(my|the)\s+(current\s+)?tasks?',
        r'do\s+i\s+have\s+any\s+tasks?',
        r'(my\s+)?tasks?(\?)?'
    ]

    for pattern in list_patterns:
        match = re.search(pattern, message_lower)
        if match:
            print(f"List tasks pattern matched: {pattern}")
            print(f"Groups: {match.groups()}")
            break
    else:
        print("No list tasks pattern matched")

    # Complete task command - supports various ways to complete a task
    complete_patterns = [
        r'(complete|finish|done|mark.*as.*done|mark.*as.*completed)\s+(task\s+|#)?([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}|\d+)',
        r'mark\s+(task\s+|#)?([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}|\d+)\s+(as\s+)?(complete|done|finished)',
        r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}|\d+)\s+(is\s+)?(complete|done|finished)'
    ]

    for pattern in complete_patterns:
        match = re.search(pattern, message_lower)
        if match:
            print(f"Complete task pattern matched: {pattern}")
            print(f"Groups: {match.groups()}")
            # Extract task ID (it could be in different groups depending on the pattern)
            task_id_str = next((g for g in match.groups() if g and (g.replace('-', '').isdigit() or 
                           re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', g))), None)
            print(f"Task ID found: {task_id_str}")
            break
    else:
        print("No complete task pattern matched")

    # Update/edit task command - supports various ways to update a task
    update_patterns = [
        r'(update|edit|change|modify|rename)\s+(task\s+|#)?([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}|\d+)\s+(to|as|with)\s+(.+)',
        r'(update|edit|change|modify|rename)\s+(task\s+|#)?([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}|\d+):\s*(.+)',
        r'(update|edit|change|modify|rename)\s+(task\s+|#)?([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}|\d+)\s+(.+)'
    ]

    for pattern in update_patterns:
        match = re.search(pattern, message_lower)
        if match:
            print(f"Update task pattern matched: {pattern}")
            print(f"Groups: {match.groups()}")
            break
    else:
        print("No update task pattern matched")

    # Delete/remove task command - supports various ways to delete a task
    delete_patterns = [
        r'(delete|remove|erase|cancel)\s+(task\s+|#)?([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}|\d+)',
        r'remove\s+(task\s+|#)?([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}|\d+)\s+(please|pls|now)?',
        r'(delete|remove|erase|cancel)\s+(this|the)\s+(task\s+|#)?([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}|\d+)'
    ]

    for pattern in delete_patterns:
        match = re.search(pattern, message_lower)
        if match:
            print(f"Delete task pattern matched: {pattern}")
            print(f"Groups: {match.groups()}")
            break
    else:
        print("No delete task pattern matched")

if __name__ == "__main__":
    test_all_patterns()