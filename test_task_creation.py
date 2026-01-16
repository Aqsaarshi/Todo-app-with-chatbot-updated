#!/usr/bin/env python3
"""
Test script to verify that the task creation functionality works properly.
This addresses the issue where the AI chatbot says "task created" but doesn't actually create a real task.
"""
import asyncio
from uuid import uuid4
from sqlmodel import SQLModel, Field, create_engine, Session, select
from backend.src.models.task import Task, TaskCreate
from backend.src.database import create_db_and_tables, engine
from backend.src.services.task_service import create_task
from backend.src.tools.mcp_tools import MCPTaskTools


def test_direct_task_creation():
    """Test direct task creation using the task service"""
    print("Testing direct task creation using task service...")
    
    # Create a new database session
    with Session(engine) as session:
        # Create a sample user ID
        user_id = str(uuid4())
        
        # Create a task using the task service
        task_create = TaskCreate(
            title="Test Cooking Task",
            description="This is a test task for cooking"
        )
        
        # Create the task
        created_task = asyncio.run(create_task(session, user_id, task_create))
        
        print(f"Task created successfully: {created_task.title}")
        print(f"Task ID: {created_task.id}")
        print(f"User ID: {created_task.user_id}")
        print(f"Completed: {created_task.completed}")
        
        # Verify the task exists in the database
        retrieved_task = session.get(Task, created_task.id)
        assert retrieved_task is not None, "Task should exist in database"
        assert retrieved_task.title == "Test Cooking Task", "Task title should match"
        assert retrieved_task.user_id == user_id, "Task user_id should match"
        
        print("✓ Direct task creation test passed!")
        return True


def test_mcp_tools_task_creation():
    """Test task creation using MCP tools"""
    print("\nTesting task creation using MCP tools...")
    
    # Create a new database session
    with Session(engine) as session:
        # Create a sample user ID
        user_id = str(uuid4())
        
        # Create MCP tools instance
        mcp_tools = MCPTaskTools(session)
        
        # Create a task using MCP tools
        result = mcp_tools.add_task(
            user_id=user_id,
            title="Test MCP Cooking Task",
            description="This is a test task created via MCP tools"
        )
        
        print(f"MCP Task created successfully: {result['title']}")
        print(f"Task ID: {result['task_id']}")
        print(f"Completed: {result['completed']}")
        
        # Verify the task exists in the database
        statement = select(Task).where(Task.id == result['task_id'])
        retrieved_task = session.exec(statement).first()
        assert retrieved_task is not None, "Task should exist in database"
        assert retrieved_task.title == "Test MCP Cooking Task", "Task title should match"
        assert retrieved_task.user_id == user_id, "Task user_id should match"
        
        print("✓ MCP tools task creation test passed!")
        return True


def run_tests():
    """Run all tests"""
    print("Running task creation tests...\n")
    
    # Initialize the database
    asyncio.run(create_db_and_tables())
    
    success = True
    
    try:
        success &= test_direct_task_creation()
        success &= test_mcp_tools_task_creation()
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        success = False
    
    if success:
        print("\n🎉 All tests passed! Task creation functionality is working correctly.")
    else:
        print("\n❌ Some tests failed. Task creation functionality needs to be fixed.")
    
    return success


if __name__ == "__main__":
    run_tests()