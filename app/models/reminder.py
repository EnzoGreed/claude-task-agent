from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional


class ReminderType(str, Enum):
    EMAIL = "email"
    NOTIFICATION = "notification"
    CONSOLE = "console"


class ReminderBase(BaseModel):
    task_id: int
    reminder_time: datetime
    reminder_type: ReminderType = ReminderType.NOTIFICATION


class ReminderCreate(ReminderBase):
    pass


class ReminderResponse(ReminderBase):
    id: int
    is_sent: bool = False
    created_at: datetime
    sent_at: Optional[datetime] = None

    class Config:
        from_attributes = True
