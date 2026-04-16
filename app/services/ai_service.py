import os
from anthropic import Anthropic
from datetime import datetime
import json


class AIService:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set in environment")
        self.client = Anthropic()
        self.conversation_history = []

    def organize_tasks(self, tasks):
        """Use Claude to organize and prioritize tasks"""
        task_list = "\n".join([
            f"- {task.get('title')} (Priority: {task.get('priority')}, Due: {task.get('due_date')})"
            for task in tasks
        ])

        prompt = f"""You are an expert task management assistant. I have the following tasks:

{task_list}

Please analyze these tasks and provide:
1. Optimal execution order based on priority and deadlines
2. Time estimates for each task
3. Potential dependencies between tasks
4. Recommendations for efficiency
5. Any tasks that could be combined or delegated

Provide your response in a structured JSON format."""

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.content[0].text

    def get_daily_briefing(self, tasks):
        """Generate a daily briefing for the user"""
        today = datetime.now().date()
        today_tasks = []
        upcoming_tasks = []

        for task in tasks:
            if task.get("status") == "completed":
                continue
            due_date_str = task.get("due_date")
            if due_date_str:
                try:
                    due_date = datetime.fromisoformat(due_date_str).date()
                    if due_date == today:
                        today_tasks.append(task)
                    elif due_date > today:
                        upcoming_tasks.append(task)
                except:
                    pass

        today_list = "\n".join(
            [f"- {t.get('title')} ({t.get('priority')})" for t in today_tasks]) or "No tasks today"
        upcoming_list = "\n".join(
            [f"- {t.get('title')} on {t.get('due_date', '').split('T')[0]}" for t in upcoming_tasks[:5]]) or "No upcoming tasks"

        prompt = f"""Generate a motivational and practical daily briefing for my task management:

TODAY'S TASKS:
{today_list}

UPCOMING TASKS:
{upcoming_list}

Please provide:
1. A motivational opening
2. Focus areas for today
3. Time management tips
4. Evening reflection prompts"""

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.content[0].text

    def suggest_task_improvements(self, task):
        """Suggest improvements for task description and breakdown"""
        prompt = f"""I have a task that needs improvement:

Task Title: {task.get('title')}
Description: {task.get('description')}

Please suggest:
1. A more specific and measurable task title
2. Better description with acceptance criteria
3. Potential subtasks if this is too big
4. Realistic time estimate
5. Any blockers or dependencies to consider"""

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.content[0].text

    def chat(self, user_message, context_tasks=None):
        """Multi-turn conversation for task management help"""
        context = ""
        if context_tasks:
            context = "\nCurrent tasks:\n" + "\n".join([
                f"- {t.get('title')} (Status: {t.get('status')}, Due: {t.get('due_date')})"
                for t in context_tasks
            ])

        full_message = user_message + context

        self.conversation_history.append({
            "role": "user",
            "content": full_message
        })

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            system="""You are an expert AI task management assistant. Help users:
- Organize and prioritize their tasks
- Break down complex tasks into subtasks
- Suggest execution strategies
- Provide time management advice
- Generate reminders and motivation
- Analyze productivity patterns
Be concise, practical, and encouraging.""",
            messages=self.conversation_history
        )

        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
