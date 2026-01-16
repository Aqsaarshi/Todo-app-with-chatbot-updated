#!/usr/bin/env python3
"""
Robust test script to verify the backend functionality
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

with open('verification_output_detailed.txt', 'w') as f:
    f.write("Starting verification...\n")
    try:
        f.write("Testing main app import...\n")
        # Test main imports
        from main import app
        f.write("SUCCESS: Main app imported\n")
        
        f.write("Testing chat routers import...\n")
        # Test specific modules
        from api.chat import router, anonymous_router
        f.write("SUCCESS: Chat routers imported\n")
        
        f.write("Testing database modules import...\n")
        # Test database connection setup
        from database import create_db_and_tables, engine
        f.write("SUCCESS: Database modules imported\n")
        
        f.write("All imports successful!\n")
        
        # Verify that our changes are in place
        f.write("Checking for anonymous routes in main app...\n")
        # Check if the anonymous router is properly included in main
        router_names = [str(route) for route in app.routes]
        anonymous_routes = [route for route in app.routes if 'anonymous' in str(route).lower()]
        f.write(f"Found {len(anonymous_routes)} anonymous routes\n")
        
        # Check for specific endpoints
        endpoint_paths = [str(route.path) for route in app.routes]
        f.write(f"All endpoint paths: {endpoint_paths}\n")
        
        if '/api/anonymous/chat' in endpoint_paths:
            f.write("SUCCESS: Anonymous chat endpoint is registered\n")
        else:
            f.write("ERROR: Anonymous chat endpoint is not registered\n")
            
        if '/api/anonymous/conversations' in endpoint_paths:
            f.write("SUCCESS: Anonymous conversations endpoint is registered\n")
        else:
            f.write("ERROR: Anonymous conversations endpoint is not registered\n")

        f.write("Verification completed.\n")
        
    except Exception as e:
        f.write(f"ERROR: {str(e)}\n")
        import traceback
        traceback.print_exc(file=f)