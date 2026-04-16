# 🤖 AI Task Management Agent

An intelligent, AI-powered task management system that helps you organize, prioritize, and execute your daily tasks with timely reminders and smart scheduling powered by Claude AI.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### 📋 Task Management
- **Create, Read, Update, Delete** tasks with full lifecycle management
- **Priority Levels:** Low, Medium, High
- **Task Status Tracking:** Todo, In Progress, Completed
- **Due Date Management** with ISO 8601 datetime support
- **AI Suggestions Storage** for task improvements

### 🤖 AI-Powered Features
- **Daily Briefing** - AI generates motivational daily overview with focus areas and time management tips
- **Task Organization** - Claude analyzes and suggests optimal execution order based on priority and deadlines
- **Task Suggestions** - AI recommends task improvements, subtasks, and time estimates
- **Chat Assistant** - Multi-turn conversation with context-aware assistance for productivity guidance

### 🔔 Smart Reminders
- **Automatic Reminder Creation** - 2 reminders per task (1 day before + 1 hour before deadline)
- **Background Scheduler** - Checks and sends reminders every minute
- **Reminder Tracking** - Monitor which reminders have been sent
- **Console Notifications** - Real-time reminder notifications in terminal

### 📊 Dashboard & Analytics
- **Today's Tasks** - Quick view of today's commitments
- **Overdue Tasks** - Identify missed deadlines
- **All Tasks View** - Complete task history with filtering
- **Task Status Overview** - Visual status indicators and color-coded priorities
- **Web-Based UI** - Modern, responsive interface with smooth animations

## 🏗️ Architecture

```
AI Task Management Agent/
├── main.py                          # FastAPI application entry point
├── app/
│   ├── models/                      # Pydantic data models
│   │   ├── task.py                  # Task and TaskPriority/Status enums
│   │   ├── reminder.py              # Reminder and ReminderType enums
│   │   └── __init__.py
│   ├── routes/                      # API endpoint handlers
│   │   ├── tasks.py                 # Task CRUD endpoints
│   │   ├── reminders.py             # Reminder management endpoints
│   │   ├── ai.py                    # AI feature endpoints
│   │   └── __init__.py
│   ├── services/                    # Business logic layer
│   │   ├── task_service.py          # Task operations (JSON storage)
│   │   ├── reminder_service.py      # Reminder operations
│   │   ├── ai_service.py            # Claude AI integration
│   │   └── __init__.py
│   ├── scheduler.py                 # APScheduler background jobs
│   ├── utils/
│   │   ├── database.py              # JSON file storage utility
│   │   └── __init__.py
│   └── __init__.py
├── frontend/
│   └── index.html                   # Web UI (400+ lines)
├── data/                            # JSON data storage
│   ├── tasks.json                   # Tasks database
│   └── reminders.json               # Reminders database
├── .env.example                     # Environment variables template
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Claude API Key from [Anthropic Console](https://console.anthropic.com)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ai-task-management-agent.git
   cd ai-task-management-agent
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your Anthropic API key
   ANTHROPIC_API_KEY=sk-ant-xxxxx
   ```

5. **Run the application:**
   ```bash
   python main.py
   ```

6. **Access the application:**
   - Web UI: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## 📖 Usage Guide

### Creating a Task

**Via Web UI:**
1. Navigate to http://localhost:8000
2. Fill in the task form:
   - **Title:** Task name (e.g., "Write project proposal")
   - **Description:** Task details
   - **Priority:** Low, Medium, or High
   - **Due Date:** When you need to complete it
3. Click "Create Task"
4. Task is automatically saved with 2 reminders created

**Via API:**
```bash
curl -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete quarterly report",
    "description": "Analyze Q1 metrics and prepare presentation",
    "priority": "high",
    "due_date": "2026-04-20T10:00:00"
  }'
```

### Getting AI Assistance

**Daily Briefing:**
```bash
curl http://localhost:8000/ai/daily-briefing
```
Generates a motivational overview of your day with focus areas and tips.

**Organize Tasks:**
```bash
curl -X POST http://localhost:8000/ai/organize-tasks
```
Claude analyzes your tasks and suggests optimal execution order.

**Get Task Suggestions:**
```bash
curl -X POST http://localhost:8000/ai/suggest/1 \
  -H "Content-Type: application/json"
```
Get improvements for task structure, time estimates, and subtasks.

**Chat with Assistant:**
```bash
curl -X POST http://localhost:8000/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Help me prioritize my tasks", "include_context": true}'
```
Have a multi-turn conversation about task management.

### Managing Tasks

**View All Tasks:**
```bash
curl http://localhost:8000/tasks/
```

**View Today's Tasks:**
```bash
curl http://localhost:8000/tasks/today
```

**View Overdue Tasks:**
```bash
curl http://localhost:8000/tasks/overdue
```

**Update a Task:**
```bash
curl -X PATCH http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress", "priority": "high"}'
```

**Delete a Task:**
```bash
curl -X DELETE http://localhost:8000/tasks/1
```

## 🔌 API Endpoints

### Tasks
- `POST /tasks/` - Create a new task
- `GET /tasks/` - Get all tasks (optional: filter by status)
- `GET /tasks/{task_id}` - Get a specific task
- `GET /tasks/today` - Get today's tasks
- `GET /tasks/overdue` - Get overdue tasks
- `PATCH /tasks/{task_id}` - Update a task
- `DELETE /tasks/{task_id}` - Delete a task

### Reminders
- `POST /reminders/` - Create a reminder
- `GET /reminders/task/{task_id}` - Get reminders for a task
- `GET /reminders/{reminder_id}` - Get a specific reminder
- `PATCH /reminders/{reminder_id}/mark-sent` - Mark reminder as sent
- `DELETE /reminders/{reminder_id}` - Delete a reminder

### AI Features
- `GET /ai/daily-briefing` - Generate daily briefing
- `POST /ai/organize-tasks` - Organize and prioritize all tasks
- `POST /ai/suggest/{task_id}` - Get suggestions for task improvement
- `POST /ai/chat` - Chat with AI assistant
- `POST /ai/chat/clear` - Clear chat history

### System
- `GET /` - Application info
- `GET /health` - Health check

### API Documentation
- Swagger UI: `GET /docs`
- ReDoc: `GET /redoc`

## 💾 Data Storage

The application uses JSON file-based storage for simplicity:

- **tasks.json** - All task records with timestamps and AI suggestions
- **reminders.json** - Reminder schedules with sent status

Data files are automatically created in the `data/` directory on first run.

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following:

```env
# Required: Anthropic API Key
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx

# Optional: Debug mode
DEBUG=True

# Optional: Database URL (compatibility)
DATABASE_URL=sqlite:///./tasks.db
```

### Application Settings

Edit `main.py` to customize:
- **Port:** Default is 8000
- **Host:** Default is 0.0.0.0
- **Reload:** Set to False for production

## 🔄 Background Scheduler

The application includes an APScheduler instance that:
- Runs in the background continuously
- Checks for pending reminders every minute
- Automatically sends notifications to console
- Starts on application startup
- Stops on application shutdown

## 📚 Dependencies

```
FastAPI==0.104.1
uvicorn==0.24.0
python-dotenv==1.0.0
pydantic==2.5.0
anthropic==0.7.1
apscheduler==3.10.4
pytz==2023.3
python-multipart==0.0.6
aiofiles==23.2.1
```

## 🛠️ Development

### Project Structure

- **Models** - Pydantic data validation models
- **Services** - Business logic layer with JSON storage
- **Routes** - FastAPI endpoint handlers
- **Scheduler** - Background job management
- **Frontend** - Single-page HTML/CSS/JavaScript UI

### Adding New Features

1. **Define Model** - Add Pydantic model in `app/models/`
2. **Create Service** - Implement business logic in `app/services/`
3. **Add Route** - Create endpoint handler in `app/routes/`
4. **Update Frontend** - Add UI elements in `frontend/index.html`
5. **Test via Swagger** - Access /docs to test new endpoints

### Code Style

- Use type hints for all functions
- Follow PEP 8 naming conventions
- Include docstrings for complex functions
- Keep service methods stateless where possible

## 🐛 Troubleshooting

### Application Won't Start

**Issue:** `ModuleNotFoundError: No module named 'app'`
- **Solution:** Ensure you're running from the project root directory
- Verify the virtual environment is activated

**Issue:** `ANTHROPIC_API_KEY not set`
- **Solution:** Add your API key to `.env` file
- Restart the application after changes

### Reminders Not Sending

**Issue:** No reminder notifications in console
- **Solution:** Check that the application has been running for more than 1 minute
- Verify due dates are in the future for reminders to be created
- Check that `DEBUG=True` in `.env` for verbose logging

### API Returns 404 Errors

**Issue:** Task or reminder not found
- **Solution:** Verify the ID is correct and exists
- Check data files exist in `data/` directory
- Ensure task was created successfully

### Port Already in Use

**Issue:** `Address already in use`
- **Solution:** Change port in `main.py` or kill process using port 8000
- Or restart the application

## 🚀 Production Deployment

For production deployment:

1. **Set `DEBUG=False`** in `.env`
2. **Use a production ASGI server** like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
   ```
3. **Use a database** like PostgreSQL instead of JSON files
4. **Add authentication** for multi-user scenarios
5. **Configure CORS** appropriately for your domain
6. **Use environment-specific configs** for secrets

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 💬 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review API documentation at `/docs`

## 📄 Changelog

### v1.0.0 (Initial Release)
- ✅ Core task management system
- ✅ AI-powered organization and suggestions
- ✅ Smart reminder system with background scheduler
- ✅ Daily briefing generation
- ✅ Multi-turn chat assistant
- ✅ Web-based dashboard
- ✅ RESTful API with Swagger documentation
- ✅ JSON file-based storage

## 🎯 Roadmap

- [ ] Email notifications for reminders
- [ ] SMS notifications via Twilio
- [ ] Task analytics and productivity insights
- [ ] User authentication and multi-user support
- [ ] PostgreSQL database integration
- [ ] Mobile app (React Native)
- [ ] Task templates and recurring tasks
- [ ] Team collaboration features
- [ ] Integration with calendar apps (Google Calendar, Outlook)
- [ ] Advanced filtering and search

## 👨‍💻 Author

Created with ❤️ using FastAPI, Claude AI, and Python

---

**⭐ If you find this project helpful, please star it on GitHub!**

**Built with ❤️ using FastAPI, Claude AI, and Python**

**Port Already in Use:**
- Change the port in `main.py` (default: 8000)
- Or kill the process using the port

**Reminders Not Showing:**
- Check that the scheduler started (logs should show "✓ Task scheduler started")
- Ensure task due dates are set correctly
- Check console output for reminder logs

## Project Structure

```
AI Agentic Enve/
├── main.py                 # FastAPI application entry point
├── app/
│   ├── models/            # Database models
│   │   ├── task.py
│   │   └── reminder.py
│   ├── routes/            # API endpoints
│   │   ├── tasks.py
│   │   ├── reminders.py
│   │   └── ai.py
│   ├── services/          # Business logic
│   │   ├── task_service.py
│   │   ├── reminder_service.py
│   │   └── ai_service.py
│   ├── scheduler.py       # Background scheduler
│   └── utils/
│       └── database.py
├── frontend/
│   └── index.html         # Web interface
├── requirements.txt       # Dependencies
├── .env.example          # Environment template
└── README.md             # This file
```

## Contributing

Feel free to extend the system with:
- Email notification support
- Slack/Discord integration
- Calendar sync (Google Calendar, Outlook)
- Mobile app
- Advanced analytics
- Team collaboration features

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions:
1. Check the troubleshooting section
2. Review API documentation at `/docs`
3. Check console logs for error messages

## Future Enhancements

- 📱 Mobile app (React Native)
- 🔗 Calendar integration
- 👥 Team collaboration
- 📊 Advanced analytics dashboard
- 🔐 User authentication
- 🌍 Multi-language support
- 🎨 Theme customization
- 📧 Email integration

---

**Built with ❤️ using Claude AI and FastAPI**
