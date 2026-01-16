#!/usr/bin/env python3
"""
Test script to check if the server can start and write to a file
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

with open('startup_test.log', 'w') as log_file:
    try:
        log_file.write("Starting import tests...\n")
        
        # Test basic imports
        import fastapi
        log_file.write("✓ FastAPI imported\n")
        
        import sqlmodel
        log_file.write("✓ SQLModel imported\n")
        
        # Test main imports
        from main import app
        log_file.write("✓ Main app imported\n")
        
        # Test specific modules
        from api.chat import router, anonymous_router
        log_file.write("✓ Chat routers imported\n")
        
        # Test database connection setup
        from database import create_db_and_tables, engine
        log_file.write("✓ Database modules imported\n")
        
        log_file.write("All imports successful!\n")
        
        # Now try to start the app
        import uvicorn
        log_file.write("Attempting to start Uvicorn server...\n")
        
    except Exception as e:
        log_file.write(f"Error occurred: {e}\n")
        import traceback
        traceback.print_exc(file=log_file)
