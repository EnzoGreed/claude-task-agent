from app.models.reminder import ReminderCreate
from app.utils.database import DataStore, REMINDERS_FILE
from datetime import datetime, timedelta
from typing import List, Optional


class ReminderService:

    @staticmethod
    def create_reminder(reminder: ReminderCreate) -> dict:
        """Create a new reminder"""
        reminders = DataStore.load_json(REMINDERS_FILE)
        reminder_id = DataStore.get_next_id(REMINDERS_FILE)

        new_reminder = {
            "id": reminder_id,
            "task_id": reminder.task_id,
            "reminder_time": reminder.reminder_time.isoformat(),
            "reminder_type": reminder.reminder_type.value,
            "is_sent": False,
            "created_at": datetime.now().isoformat(),
            "sent_at": None
        }

        reminders.append(new_reminder)
        DataStore.save_json(REMINDERS_FILE, reminders)
        return new_reminder

    @staticmethod
    def get_reminder(reminder_id: int) -> Optional[dict]:
        """Get a reminder by ID"""
        reminders = DataStore.load_json(REMINDERS_FILE)
        return next((r for r in reminders if r["id"] == reminder_id), None)

    @staticmethod
    def get_task_reminders(task_id: int) -> List[dict]:
        """Get all reminders for a task"""
        reminders = DataStore.load_json(REMINDERS_FILE)
        return [r for r in reminders if r["task_id"] == task_id]

    @staticmethod
    def get_pending_reminders() -> List[dict]:
        """Get reminders that should be sent now"""
        reminders = DataStore.load_json(REMINDERS_FILE)
        now = datetime.now()

        pending = []
        for reminder in reminders:
            if not reminder.get("is_sent"):
                try:
                    reminder_time = datetime.fromisoformat(
                        reminder.get("reminder_time", ""))
                    if reminder_time <= now:
                        pending.append(reminder)
                except:
                    pass

        return pending

    @staticmethod
    def mark_reminder_sent(reminder_id: int) -> Optional[dict]:
        """Mark a reminder as sent"""
        reminders = DataStore.load_json(REMINDERS_FILE)

        for reminder in reminders:
            if reminder["id"] == reminder_id:
                reminder["is_sent"] = True
                reminder["sent_at"] = datetime.now().isoformat()
                DataStore.save_json(REMINDERS_FILE, reminders)
                return reminder

        return None

    @staticmethod
    def delete_reminder(reminder_id: int) -> Optional[dict]:
        """Delete a reminder"""
        reminders = DataStore.load_json(REMINDERS_FILE)

        for i, reminder in enumerate(reminders):
            if reminder["id"] == reminder_id:
                deleted = reminders.pop(i)
                DataStore.save_json(REMINDERS_FILE, reminders)
                return deleted

        return None

    @staticmethod
    def auto_create_reminders(task: dict) -> List[dict]:
        """Automatically create reminders for a task based on due date"""
        if not task.get("due_date"):
            return []

        reminders = []
        try:
            due_date = datetime.fromisoformat(task.get("due_date"))

            # Create reminder 1 day before
            reminder_1day = due_date - timedelta(days=1)

            # Create reminder 1 hour before
            reminder_1hour = due_date - timedelta(hours=1)

            now = datetime.now()

            for reminder_time in [reminder_1day, reminder_1hour]:
                if reminder_time > now:
                    reminder_obj = ReminderCreate(
                        task_id=task["id"],
                        reminder_time=reminder_time
                    )
                    db_reminder = ReminderService.create_reminder(reminder_obj)
                    reminders.append(db_reminder)
        except:
            pass

        return reminders
