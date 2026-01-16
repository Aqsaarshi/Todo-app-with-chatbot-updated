import sys
sys.path.insert(0, './src')

from src.main import app

print('Available routes:')
for route in app.routes:
    if hasattr(route, 'methods') and hasattr(route, 'path'):
        print(f'{route.methods} {route.path}')
    else:
        print(f'Route object: {route}')

print("\nChecking for chat routes specifically...")
found_chat = False
for route in app.routes:
    if hasattr(route, 'path') and 'chat' in route.path:
        print(f"Found chat route: {route.methods} {route.path}")
        found_chat = True

if not found_chat:
    print("No chat routes found!")
    
# Also check for conversation routes
found_conv = False
for route in app.routes:
    if hasattr(route, 'path') and 'conversation' in route.path:
        print(f"Found conversation route: {route.methods} {route.path}")
        found_conv = True

if not found_conv:
    print("No conversation routes found!")

print("Done checking routes.")