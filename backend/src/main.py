from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from .api import auth , tasks,chat
from .database import create_db_and_tables, engine
from contextlib import asynccontextmanager

# Define the security scheme
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
    # Close the database engine on shutdown
    await engine.dispose()

app = FastAPI(
    title="Todo API",
    description="API for managing todo tasks with user authentication",
    version="1.0.0",
    lifespan=lifespan,
    # Add the security scheme to the OpenAPI spec
    root_path=""
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Todo API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include API routes
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
