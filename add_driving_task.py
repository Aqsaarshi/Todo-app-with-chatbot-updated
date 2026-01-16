#!/usr/bin/env python3
"""
Script to add a 'driving' task to the todo list.
"""
import sys
import os

# Add the src directory to the Python path
src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_dir)

from src.services.todo_service import TodoService
from src.models.task import Task


def main():
    """Add a 'driving' task to the todo list."""
    # Create a new todo service instance
    service = TodoService()
    
    # Add the 'driving' task
    try:
        task = service.add_task("driving")
        print(f"Successfully added task: '{task.title}' with ID: {task.id}")
        
        # Show the current list of tasks
        print("\nCurrent tasks:")
        tasks = service.get_all_tasks()
        for task in tasks:
            status_indicator = "X" if task.status.name == "COMPLETE" else "O"
            print(f"[{status_indicator}] {task.id}. {task.title}")
            if task.description:
                print(f"      Description: {task.description}")
            print()
            
    except ValueError as e:
        print(f"Error adding task: {e}")


if __name__ == "__main__":
    main()