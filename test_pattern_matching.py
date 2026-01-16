import re

def test_pattern_matching():
    message_lower = "complete task dentist appointment"
    
    # Complete task command - supports various ways to complete a task
    complete_patterns = [
        # Pattern for completing by ID
        r'(complete|finish|done|mark.*as.*done|mark.*as.*completed)\s+(task\s+|#)?([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}|\d+)',
        r'mark\s+(task\s+|#)?([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}|\d+)\s+(as\s+)?(complete|done|finished)',
        r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}|\d+)\s+(is\s+)?(complete|done|finished)',
        # Pattern for completing by title/description
        r'(complete|finish|done|mark.*as.*done|mark.*as.*completed)\s+(task\s+)?(.+)'
    ]
    
    for pattern in complete_patterns:
        match = re.search(pattern, message_lower)
        if match:
            print(f"Pattern matched: {pattern}")
            print(f"Match groups: {match.groups()}")
            
            # Check if this is the pattern that captures by ID
            id_match = next((g for g in match.groups() if g and (g.replace('-', '').isdigit() or 
                       re.match(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', g))), None)
            
            print(f"ID match found: {id_match}")
            
            if not id_match:
                # This might be a match by title/description
                title_match = next((g for g in match.groups() if g and 
                                  g not in ['complete', 'finish', 'done', 'task', 'as', 'is', 'by', 'the', 'a', 'an']), None)
                print(f"Title match candidate: {title_match}")
                
                if title_match and len(title_match.strip()) > 2:  # At least 3 characters to avoid matching short words
                    print(f"Title keyword: {title_match.strip()}")
                    break
        else:
            print(f"Pattern did not match: {pattern}")

if __name__ == "__main__":
    test_pattern_matching()