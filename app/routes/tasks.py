from fastapi import APIRouter, HTTPException
from app.models.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import TaskService
from app.services.reminder_service import ReminderService
from typing import List

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate):
    """Create a new task"""
    db_task = TaskService.create_task(task)
    # Auto-create reminders
    ReminderService.auto_create_reminders(db_task)
    return db_task


@router.get("/", response_model=List[TaskResponse])
def get_all_tasks(status: str = None):
    """Get all tasks, optionally filtered by status"""
    tasks = TaskService.get_all_tasks(status)
    return tasks


@router.get("/today", response_model=List[TaskResponse])
def get_today_tasks():
    """Get tasks due today"""
    tasks = TaskService.get_today_tasks()
    return tasks


@router.get("/overdue", response_model=List[TaskResponse])
def get_overdue_tasks():
    """Get overdue tasks"""
    tasks = TaskService.get_overdue_tasks()
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    """Get a specific task"""
    task = TaskService.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate):
    """Update a task"""
    task = TaskService.update_task(task_id, task_update)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int):
    """Delete a task"""
    task = TaskService.delete_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}
