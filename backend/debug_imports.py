#!/usr/bin/env python3
"""
Debug script to check for import and database issues
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("Checking imports...")

try:
    # Test basic imports
    import fastapi
    print("✓ FastAPI imported")
    
    import sqlmodel
    print("✓ SQLModel imported")
    
    import asyncio
    print("✓ asyncio imported")
    
    # Test main imports
    from main import app
    print("✓ Main app imported")
    
    # Test specific modules
    from api.chat import router, anonymous_router
    print("✓ Chat routers imported")
    
    # Test database connection setup
    from database import create_db_and_tables, engine
    print("✓ Database modules imported")
    
    # Test model imports
    from models.user import User
    from models.conversation import Conversation
    from models.message import Message
    from models.task import Task
    print("✓ Model imports successful")
    
    # Test service imports
    from services.cohere_service import CohereService
    print("✓ Cohere service imported")
    
    print("\nAll imports successful! The issue might be with the database connection or startup dependencies.")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"✗ Other error: {e}")
    import traceback
    traceback.print_exc()