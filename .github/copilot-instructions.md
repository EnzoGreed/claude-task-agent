# Copilot Instructions for AI Task Management Agent

## Project Overview
This is an AI-powered task management system built with FastAPI, Claude AI, and SQLite. It helps users organize daily tasks, get AI-powered recommendations, receive intelligent reminders, and maintain productivity through daily briefings.

## Key Technologies
- **Backend:** FastAPI with Python 3.8+
- **Database:** SQLite with SQLAlchemy ORM
- **AI Engine:** Claude API (Anthropic)
- **Scheduling:** APScheduler for background tasks
- **Frontend:** HTML/CSS/JavaScript with vanilla JS

## Project Structure
```
├── main.py                 # FastAPI application entry point
├── app/
│   ├── models/            # Pydantic & SQLAlchemy models (tasks, reminders)
│   ├── routes/            # API route handlers
│   ├── services/          # Business logic (TaskService, AIService, ReminderService)
│   ├── scheduler.py       # Background scheduler for reminders
│   └── utils/database.py  # Database configuration
├── frontend/index.html    # Web UI
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # Complete documentation
```

## Core Features Implementation

### 1. Task Management
- CRUD operations for tasks
- Priority levels (low/medium/high)
- Status tracking (todo/in_progress/completed)
- Automatic reminder creation on task creation
- AI suggestion storage

### 2. AI Integration
- **Task Organization**: Analyzes and prioritizes task queue
- **Daily Briefing**: Generates motivational daily overview
- **Task Suggestions**: Provides improvements and breakdowns
- **Chat Assistant**: Multi-turn conversation with context

### 3. Smart Reminders
- Automatic 2-reminder system (1 day before + 1 hour before)
- Background scheduler runs every minute
- Console/notification-based delivery
- Sent status tracking

### 4. Database Models
- **Task**: id, title, description, priority, status, due_date, timestamps, ai_suggestions
- **Reminder**: id, task_id, reminder_time, reminder_type, is_sent, timestamps

## Setup & Running

1. Create virtual environment: `python -m venv venv`
2. Activate: `source venv/bin/activate` (Windows: `venv\Scripts\activate`)
3. Install: `pip install -r requirements.txt`
4. Set ANTHROPIC_API_KEY in `.env`
5. Run: `python main.py`
6. Access: `http://localhost:8000`

## Development Guidelines

### Adding New Features
1. Create model in `app/models/` if needed
2. Add service logic in `app/services/`
3. Add route handler in `app/routes/`
4. Update frontend UI in `frontend/index.html`
5. Test via Swagger UI at `/docs`

### Modifying AI Behavior
- Edit prompts in `app/services/ai_service.py`
- Adjust model in API calls (currently: claude-3-5-sonnet-20241022)
- Modify system prompt in `chat()` method

### Adding New Reminder Types
1. Update `ReminderType` enum in `app/models/reminder.py`
2. Add handling in `check_and_send_reminders()` in `app/scheduler.py`
3. Update frontend reminder display logic if needed

## Important Notes

- Database file (`tasks.db`) is auto-created on first run
- Scheduler automatically starts/stops with the app
- Frontend uses vanilla JS for maximum compatibility
- CORS is enabled for all origins (update for production)
- API documentation auto-generates via Swagger UI

## Common Tasks

### Reset Database
Delete `tasks.db` and restart the application

### Change API Port
Edit line in `main.py`: `uvicorn.run(..., port=8000, ...)`

### Disable Auto-Reminders
Comment out `ReminderService.auto_create_reminders()` in `app/routes/tasks.py`

### Add Email Notifications
Update `check_and_send_reminders()` in `app/scheduler.py` with email logic
