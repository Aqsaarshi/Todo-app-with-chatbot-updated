# AI Todo Chatbot Integration - User Guide

## Overview
The AI Todo Chatbot Integration allows users to manage their tasks using natural language commands. The chatbot understands user intents and performs corresponding task operations such as adding, listing, completing, updating, and deleting tasks.

## Features
- Natural language task management
- Context-aware conversations
- Persistent conversation history
- Secure authentication
- Real-time task synchronization

## How to Use

### Accessing the Chatbot
1. Navigate to the dashboard page
2. Click on the floating chatbot icon in the bottom-right corner
3. The chat interface will appear

### Supported Commands
The chatbot supports various natural language commands:

#### Adding Tasks
- "Add a task to buy groceries"
- "Create a task to finish the report"
- "Add task: Call John tomorrow"

#### Listing Tasks
- "Show my tasks"
- "What tasks do I have?"
- "List all pending tasks"
- "Show completed tasks"

#### Completing Tasks
- "Mark the grocery task as complete"
- "Complete the report task"
- "Finish the task with ID 123"

#### Updating Tasks
- "Update the grocery task to buy milk and bread"
- "Change the title of task 123 to 'Updated Title'"
- "Edit the description of the report task"

#### Deleting Tasks
- "Delete the grocery task"
- "Remove task 123"
- "Cancel the meeting task"

### Starting a New Conversation
- Click the "New" button in the conversation list to start a fresh conversation
- Alternatively, close the current chat and reopen it

### Switching Between Conversations
- Click the ≡ button in the chat header to view your conversation history
- Select any previous conversation to continue where you left off

## Technical Architecture

### Backend Components
- **Cohere Service**: Handles natural language processing and response generation
- **MCP Tools**: Provides structured function calling for task operations
- **Database Models**: Conversation, Message, and ToolCall entities
- **API Endpoints**: RESTful endpoints for chat interactions

### Frontend Components
- **ChatBotIcon**: Floating icon to open the chat interface
- **ChatInterface**: Main chat component with conversation history
- **ApiClient**: Service for communicating with backend APIs

## Security
- All chat requests require JWT authentication
- User data is isolated by user_id in all database queries
- Input validation is performed on all user inputs

## Troubleshooting

### Common Issues
- **Chatbot not responding**: Check your internet connection and refresh the page
- **Commands not recognized**: Try rephrasing your command using simpler language
- **Authentication errors**: Log out and log back in to refresh your session

### Getting Help
If you encounter issues not covered here, please contact support or check the application logs for more details.