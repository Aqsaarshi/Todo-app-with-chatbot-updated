import re

def test_patterns():
    message_lower = "complete task 1a300d04-c330-49c8-bed6-89ace5cd7614"
    
    # Complete task command - supports various ways to complete a task
    complete_patterns = [
        r'(complete|finish|done|mark.*as.*done|mark.*as.*completed)\s+(task\s+|#)?([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}|\d+)',
        r'mark\s+(task\s+|#)?([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}|\d+)\s+(as\s+)?(complete|done|finished)',
        r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}|\d+)\s+(is\s+)?(complete|done|finished)'
    ]
    
    for pattern in complete_patterns:
        match = re.search(pattern, message_lower)
        if match:
            print(f"Pattern matched: {pattern}")
            print(f"Match groups: {match.groups()}")
            # Extract task ID (it could be in different groups depending on the pattern)
            task_id_str = next((g for g in match.groups() if g and (g.replace('-', '').isdigit() or 
                           re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', g))), None)
            print(f"Task ID found: {task_id_str}")
            break
    else:
        print("No pattern matched")

if __name__ == "__main__":
    test_patterns()