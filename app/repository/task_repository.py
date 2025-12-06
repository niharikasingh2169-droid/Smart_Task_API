from typing import List, Optional
from app.database.connection import get_db_connection
from app.models.task import TaskCreate, TaskUpdate

class TaskRepository:
    """Repository layer for Task database operations"""
    
    @staticmethod
    def create_task(task: TaskCreate) -> int:
        """Create a new task and return its ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO Task (Title, Description, Due_Date, Status, Created_At)
            VALUES (?, ?, ?, ?, datetime('now'))
        """, (task.Title, task.Description, task.Due_Date, task.Status))
        
        task_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return task_id
    
    @staticmethod
    def get_all_tasks() -> List[dict]:
        """Get all tasks from the database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM Task ORDER BY Created_At DESC")
        tasks = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return tasks
    
    @staticmethod
    def get_task_by_id(task_id: int) -> Optional[dict]:
        """Get a task by its ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM Task WHERE Id = ?", (task_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    @staticmethod
    def update_task(task_id: int, task_update: TaskUpdate) -> bool:
        """Update an existing task"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Build dynamic update query
        update_fields = []
        values = []
        
        if task_update.Title is not None:
            update_fields.append("Title = ?")
            values.append(task_update.Title)
        if task_update.Description is not None:
            update_fields.append("Description = ?")
            values.append(task_update.Description)
        if task_update.Due_Date is not None:
            update_fields.append("Due_Date = ?")
            values.append(task_update.Due_Date)
        if task_update.Status is not None:
            update_fields.append("Status = ?")
            values.append(task_update.Status)
        
        if not update_fields:
            conn.close()
            return False
        
        values.append(task_id)
        query = f"UPDATE Task SET {', '.join(update_fields)} WHERE Id = ?"
        
        cursor.execute(query, values)
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        
        return rows_affected > 0
    
    @staticmethod
    def delete_task(task_id: int) -> bool:
        """Delete a task by its ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM Task WHERE Id = ?", (task_id,))
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        
        return rows_affected > 0

