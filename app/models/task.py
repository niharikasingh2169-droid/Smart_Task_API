from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
import re

class TaskBase(BaseModel):
    Title: str = Field(..., description="Task title")
    Description: Optional[str] = Field(None, description="Task description")
    Due_Date: str = Field(..., description="Task due date (dd-mm-yyyy format)")
    Status: str = Field(..., description="Task status")
    
    @field_validator('Due_Date')
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        """Validate that date is in dd-mm-yyyy format"""
        if not v:
            raise ValueError("Due_Date is required")
        
        # Check format: dd-mm-yyyy
        pattern = r'^\d{2}-\d{2}-\d{4}$'
        if not re.match(pattern, v):
            raise ValueError("Due_Date must be in dd-mm-yyyy format (e.g., 25-12-2024)")
        
        # Validate that it's a valid date
        try:
            datetime.strptime(v, '%d-%m-%Y')
        except ValueError:
            raise ValueError("Invalid date. Please ensure the date is valid (e.g., 25-12-2024)")
        
        return v

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    Title: Optional[str] = None
    Description: Optional[str] = None
    Due_Date: Optional[str] = None
    Status: Optional[str] = None
    
    @field_validator('Due_Date')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        """Validate that date is in dd-mm-yyyy format"""
        if v is None:
            return v
        
        # Check format: dd-mm-yyyy
        pattern = r'^\d{2}-\d{2}-\d{4}$'
        if not re.match(pattern, v):
            raise ValueError("Due_Date must be in dd-mm-yyyy format (e.g., 25-12-2024)")
        
        # Validate that it's a valid date
        try:
            datetime.strptime(v, '%d-%m-%Y')
        except ValueError:
            raise ValueError("Invalid date. Please ensure the date is valid (e.g., 25-12-2024)")
        
        return v

class TaskResponse(TaskBase):
    Id: int
    Created_At: str
    
    class Config:
        from_attributes = True

class PriorityResponse(BaseModel):
    task_id: int
    priority_score: int = Field(..., ge=1, le=5, description="Priority score from 1 (highest) to 5 (lowest)")
    reasoning: Optional[str] = None

