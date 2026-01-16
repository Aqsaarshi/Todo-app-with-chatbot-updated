#!/usr/bin/env python3
"""
Simple test script to verify the backend functionality
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    # Test main imports
    from main import app
    print("SUCCESS: Main app imported")
    
    # Test specific modules
    from api.chat import router, anonymous_router
    print("SUCCESS: Chat routers imported")
    
    # Test database connection setup
    from database import create_db_and_tables, engine
    print("SUCCESS: Database modules imported")
    
    print("All imports successful!")
    
    # Verify that our changes are in place
    # Check if the anonymous router is properly included in main
    router_names = [route.name for route in app.routes]
    if any('anonymous' in str(route).lower() for route in app.routes):
        print("SUCCESS: Anonymous routes are included in the main app")
    else:
        print("WARNING: Could not find anonymous routes in main app")
        
    # Check for specific endpoints
    endpoint_paths = [str(route.path) for route in app.routes]
    if '/api/anonymous/chat' in endpoint_paths:
        print("SUCCESS: Anonymous chat endpoint is registered")
    else:
        print("ERROR: Anonymous chat endpoint is not registered")
        
    if '/api/anonymous/conversations' in endpoint_paths:
        print("SUCCESS: Anonymous conversations endpoint is registered")
    else:
        print("ERROR: Anonymous conversations endpoint is not registered")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()