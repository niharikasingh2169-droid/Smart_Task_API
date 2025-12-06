from typing import List, Optional
from app.repository.task_repository import TaskRepository
from app.models.task import TaskCreate, TaskUpdate, TaskResponse, PriorityResponse
from app.services.openai_service import OpenAIService

class TaskService:
    """Business logic layer for Task operations"""
    
    def __init__(self):
        self.repository = TaskRepository()
        self._openai_service = None
    
    @property
    def openai_service(self):
        """Lazy load OpenAI service"""
        if self._openai_service is None:
            self._openai_service = OpenAIService()
        return self._openai_service
    
    def create_task(self, task: TaskCreate) -> TaskResponse:
        """Create a new task"""
        task_id = self.repository.create_task(task)
        created_task = self.repository.get_task_by_id(task_id)
        return TaskResponse(**created_task)
    
    def get_all_tasks(self) -> List[TaskResponse]:
        """Get all tasks"""
        tasks = self.repository.get_all_tasks()
        return [TaskResponse(**task) for task in tasks]
    
    def get_task_by_id(self, task_id: int) -> Optional[TaskResponse]:
        """Get a task by ID"""
        task = self.repository.get_task_by_id(task_id)
        if task:
            return TaskResponse(**task)
        return None
    
    def update_task(self, task_id: int, task_update: TaskUpdate) -> Optional[TaskResponse]:
        """Update an existing task"""
        # Check if task exists
        existing_task = self.repository.get_task_by_id(task_id)
        if not existing_task:
            return None
        
        # Update task
        success = self.repository.update_task(task_id, task_update)
        if not success:
            return None
        
        # Return updated task
        updated_task = self.repository.get_task_by_id(task_id)
        return TaskResponse(**updated_task)
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        return self.repository.delete_task(task_id)
    
    async def fetch_priority(self, task_id: int) -> Optional[PriorityResponse]:
        """Fetch priority score for a task using OpenAI"""
        task = self.repository.get_task_by_id(task_id)
        if not task:
            return None
        
        priority_score, reasoning = await self.openai_service.get_priority_score(
            title=task["Title"],
            description=task.get("Description", ""),
            due_date=task["Due_Date"]
        )
        
        return PriorityResponse(
            task_id=task_id,
            priority_score=priority_score,
            reasoning=reasoning
        )

