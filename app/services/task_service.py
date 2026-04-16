from app.models.task import TaskStatus, TaskCreate, TaskUpdate
from app.utils.database import DataStore, TASKS_FILE
from datetime import datetime
from typing import List, Optional


class TaskService:

    @staticmethod
    def create_task(task: TaskCreate) -> dict:
        """Create a new task"""
        tasks = DataStore.load_json(TASKS_FILE)
        task_id = DataStore.get_next_id(TASKS_FILE)

        new_task = {
            "id": task_id,
            **task.model_dump(),
            "status": "todo",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "completed_at": None,
            "ai_suggestions": None,
            "due_date": task.due_date.isoformat() if task.due_date else None
        }

        tasks.append(new_task)
        DataStore.save_json(TASKS_FILE, tasks)
        return new_task

    @staticmethod
    def get_task(task_id: int) -> Optional[dict]:
        """Get a task by ID"""
        tasks = DataStore.load_json(TASKS_FILE)
        return next((t for t in tasks if t["id"] == task_id), None)

    @staticmethod
    def get_all_tasks(status: str = None) -> List[dict]:
        """Get all tasks, optionally filtered by status"""
        tasks = DataStore.load_json(TASKS_FILE)

        if status:
            tasks = [t for t in tasks if t.get("status") == status]

        # Sort by due_date
        return sorted(tasks, key=lambda t: t.get("due_date") or "")

    @staticmethod
    def get_today_tasks() -> List[dict]:
        """Get tasks due today"""
        tasks = DataStore.load_json(TASKS_FILE)
        today = datetime.now().date()

        today_tasks = []
        for task in tasks:
            if task.get("status") == "completed":
                continue
            due_date_str = task.get("due_date")
            if due_date_str:
                try:
                    due_date = datetime.fromisoformat(due_date_str).date()
                    if due_date == today:
                        today_tasks.append(task)
                except:
                    pass

        return today_tasks

    @staticmethod
    def get_overdue_tasks() -> List[dict]:
        """Get overdue tasks"""
        tasks = DataStore.load_json(TASKS_FILE)
        now = datetime.now()

        overdue = []
        for task in tasks:
            if task.get("status") == "completed":
                continue
            due_date_str = task.get("due_date")
            if due_date_str:
                try:
                    due_date = datetime.fromisoformat(due_date_str)
                    if due_date < now:
                        overdue.append(task)
                except:
                    pass

        return overdue

    @staticmethod
    def update_task(task_id: int, task_update: TaskUpdate) -> Optional[dict]:
        """Update a task"""
        tasks = DataStore.load_json(TASKS_FILE)

        for task in tasks:
            if task["id"] == task_id:
                update_data = task_update.model_dump(exclude_unset=True)

                for field, value in update_data.items():
                    if field == "due_date" and value:
                        task[field] = value.isoformat()
                    elif field != "due_date":
                        task[field] = value

                task["updated_at"] = datetime.now().isoformat()

                if task_update.status == TaskStatus.COMPLETED:
                    task["completed_at"] = datetime.now().isoformat()

                DataStore.save_json(TASKS_FILE, tasks)
                return task

        return None

    @staticmethod
    def delete_task(task_id: int) -> Optional[dict]:
        """Delete a task"""
        tasks = DataStore.load_json(TASKS_FILE)

        for i, task in enumerate(tasks):
            if task["id"] == task_id:
                deleted = tasks.pop(i)
                DataStore.save_json(TASKS_FILE, tasks)
                return deleted

        return None

    @staticmethod
    def add_ai_suggestion(task_id: int, suggestion: str) -> Optional[dict]:
        """Add AI suggestion to a task"""
        tasks = DataStore.load_json(TASKS_FILE)

        for task in tasks:
            if task["id"] == task_id:
                task["ai_suggestions"] = suggestion
                task["updated_at"] = datetime.now().isoformat()
                DataStore.save_json(TASKS_FILE, tasks)
                return task

        return None
