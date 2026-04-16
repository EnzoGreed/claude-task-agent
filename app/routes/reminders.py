from fastapi import APIRouter, HTTPException
from app.models.reminder import ReminderCreate, ReminderResponse
from app.services.reminder_service import ReminderService
from typing import List

router = APIRouter(prefix="/reminders", tags=["reminders"])


@router.post("/", response_model=ReminderResponse)
def create_reminder(reminder: ReminderCreate):
    """Create a new reminder"""
    db_reminder = ReminderService.create_reminder(reminder)
    return db_reminder


@router.get("/task/{task_id}", response_model=List[ReminderResponse])
def get_task_reminders(task_id: int):
    """Get all reminders for a task"""
    reminders = ReminderService.get_task_reminders(task_id)
    return reminders


@router.get("/{reminder_id}", response_model=ReminderResponse)
def get_reminder(reminder_id: int):
    """Get a specific reminder"""
    reminder = ReminderService.get_reminder(reminder_id)
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return reminder


@router.patch("/{reminder_id}/mark-sent")
def mark_reminder_sent(reminder_id: int):
    """Mark a reminder as sent"""
    reminder = ReminderService.mark_reminder_sent(reminder_id)
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return {"message": "Reminder marked as sent"}


@router.delete("/{reminder_id}")
def delete_reminder(reminder_id: int):
    """Delete a reminder"""
    reminder = ReminderService.delete_reminder(reminder_id)
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return {"message": "Reminder deleted successfully"}
