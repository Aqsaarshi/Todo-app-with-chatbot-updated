try:
    from src.api import chat
    print("Chat module imported successfully")
except Exception as e:
    print(f"Error importing chat module: {e}")
    import traceback
    traceback.print_exc()

try:
    from src.main import app
    print("Main app imported successfully")
except Exception as e:
    print(f"Error importing main app: {e}")
    import traceback
    traceback.print_exc()