from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import task_routes
from app.database import init_db

app = FastAPI(
    title="Task Dashboard API",
    description="Enterprise-level Task Management API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Include routers
app.include_router(task_routes.router, prefix="/api/tasks", tags=["tasks"])

@app.get("/")
async def root():
    return {"message": "Task Dashboard API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

