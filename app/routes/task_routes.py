from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.services.task_service import TaskService
from app.models.task import TaskCreate, TaskUpdate, TaskResponse, PriorityResponse

router = APIRouter()
task_service = TaskService()

@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(task: TaskCreate):
    """Create a new task"""
    try:
        return task_service.create_task(task)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create task: {str(e)}")

@router.get("/", response_model=List[TaskResponse])
async def get_tasks():
    """Get all tasks"""
    try:
        return task_service.get_all_tasks()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch tasks: {str(e)}")

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_by_id(task_id: int):
    """Get a specific task by ID"""
    task = task_service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_update: TaskUpdate):
    """Update an existing task"""
    updated_task = task_service.update_task(task_id, task_update)
    if not updated_task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    return updated_task

@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: int):
    """Delete a task by ID"""
    success = task_service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    return None

@router.get("/{task_id}/priority", response_model=PriorityResponse)
async def fetch_priority(task_id: int):
    """Fetch priority score for a task using OpenAI"""
    priority = await task_service.fetch_priority(task_id)
    if not priority:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    return priority

