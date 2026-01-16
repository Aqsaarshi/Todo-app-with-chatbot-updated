print("Testing basic output")
with open("test_output.txt", "w") as f:
    f.write("Basic output test\n")
    
try:
    from src.api import chat
    with open("test_output.txt", "a") as f:
        f.write("Chat module imported successfully\n")
except Exception as e:
    with open("test_output.txt", "a") as f:
        f.write(f"Error importing chat module: {e}\n")
        import traceback
        f.write(traceback.format_exc())

try:
    from src.main import app
    with open("test_output.txt", "a") as f:
        f.write("Main app imported successfully\n")
        
    # Write routes to file
    with open("test_output.txt", "a") as f:
        f.write('\nAvailable routes:\n')
        for route in app.routes:
            if hasattr(route, 'methods') and hasattr(route, 'path'):
                f.write(f'{route.methods} {route.path}\n')
            else:
                f.write(f'Route object: {route}\n')
                
        f.write("\nChecking for chat routes specifically...\n")
        found_chat = False
        for route in app.routes:
            if hasattr(route, 'path') and 'chat' in route.path:
                f.write(f"Found chat route: {route.methods} {route.path}\n")
                found_chat = True

        if not found_chat:
            f.write("No chat routes found!\n")
            
except Exception as e:
    with open("test_output.txt", "a") as f:
        f.write(f"Error with main app: {e}\n")
        import traceback
        f.write(traceback.format_exc())