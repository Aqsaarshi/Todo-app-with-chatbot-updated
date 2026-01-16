#!/usr/bin/env python3
"""
Simple test script to verify the backend server starts correctly
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    print("Attempting to import main app...")
    from main import app
    print("✓ Main app imported successfully")
    
    print("Attempting to import chat routes...")
    from api.chat import router, anonymous_router
    print("✓ Chat routes imported successfully")
    
    print("Starting Uvicorn server...")
    import uvicorn
    
    # Start the server
    uvicorn.run(app, host="127.0.0.1", port=8080, reload=False)
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"✗ Other error: {e}")
    import traceback
    traceback.print_exc()