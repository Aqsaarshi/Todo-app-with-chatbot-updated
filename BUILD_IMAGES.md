# Building Docker Images for Todo App

This document explains how to build the Docker images for the new backend and frontend services.

## Building the Images

### Windows
Run the batch script to build both images:
```cmd
build-images.bat
```

### Linux/Mac
Run the shell script to build both images:
```bash
./build-images.sh
```

### Manual Build
Alternatively, you can build the images manually:

```bash
# Build the new backend image
docker build -t todo-new-backend ./backend

# Build the new frontend image
docker build -t todo-new-frontend ./frontend
```

## Built Images

After running the build script, you will have two new Docker images:

- `todo-new-backend` - The backend API service
- `todo-new-frontend` - The frontend web application

## Running the Containers

Once built, you can run the containers individually:

```bash
# Run the backend container
docker run -d -p 8000:8000 --name todo-backend-app todo-new-backend

# Run the frontend container
docker run -d -p 3000:3000 --name todo-frontend-app todo-new-frontend
```

## Orchestration with Docker Compose

To run both services together with proper networking, use the provided docker-compose file:

```bash
docker-compose -f docker-compose.new-images.yml up -d
```

This will:
- Start a PostgreSQL database container
- Start the backend container (on port 8000)
- Start the frontend container (on port 3000)
- Set up proper networking between services
- Configure the frontend to communicate with the backend

## Accessing the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend API Documentation: http://localhost:8000/docs

## Verification

To verify the images were built successfully:
```bash
docker images | grep todo-new
```

You should see both `todo-new-backend` and `todo-new-frontend` images listed.