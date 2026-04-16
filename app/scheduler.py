from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.utils.database import DataStore, TASKS_FILE, REMINDERS_FILE
from app.services.reminder_service import ReminderService
from datetime import datetime
import logging

scheduler = BackgroundScheduler()
scheduler.start()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_and_send_reminders():
    """Check for pending reminders and send them"""
    try:
        pending_reminders = ReminderService.get_pending_reminders()
        tasks = DataStore.load_json(TASKS_FILE)

        for reminder in pending_reminders:
            task = next((t for t in tasks if t.get("id")
                        == reminder.get("task_id")), None)

            if task:
                # Send reminder based on type
                reminder_type = reminder.get("reminder_type", "console")
                if reminder_type == "console":
                    logger.info(
                        f"🔔 REMINDER: Task '{task.get('title')}' is due at {task.get('due_date')}")
                elif reminder_type == "notification":
                    logger.warning(
                        f"⏰ NOTIFICATION: Task '{task.get('title')}' is due at {task.get('due_date')}")
                elif reminder_type == "email":
                    logger.info(
                        f"📧 EMAIL REMINDER: Task '{task.get('title')}' is due at {task.get('due_date')}")

                # Mark reminder as sent
                ReminderService.mark_reminder_sent(reminder.get("id"))
                logger.info(f"✓ Reminder {reminder.get('id')} marked as sent")

    except Exception as e:
        logger.error(f"Error checking reminders: {e}")


def start_scheduler():
    """Start the background scheduler"""
    if not scheduler.running:
        # Add job to check reminders every minute
        scheduler.add_job(
            check_and_send_reminders,
            IntervalTrigger(minutes=1),
            id="check_reminders",
            name="Check and send reminders",
            replace_existing=True
        )
        logger.info("Scheduler started with reminder check job")


def stop_scheduler():
    """Stop the background scheduler"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler stopped")


def get_scheduler():
    """Get the scheduler instance"""
    return scheduler
