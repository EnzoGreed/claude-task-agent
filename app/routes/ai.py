from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_service import AIService
from app.services.task_service import TaskService

router = APIRouter(prefix="/ai", tags=["ai"])


class ChatMessage(BaseModel):
    message: str
    include_context: bool = True


@router.get("/daily-briefing")
def get_daily_briefing():
    """Get AI-generated daily briefing"""
    try:
        tasks = TaskService.get_all_tasks()
        ai_service = AIService()
        briefing = ai_service.get_daily_briefing(tasks)
        return {"briefing": briefing}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/organize-tasks")
def organize_tasks():
    """Get AI-organized task plan"""
    try:
        tasks = TaskService.get_all_tasks()
        if not tasks:
            return {"message": "No tasks to organize"}

        ai_service = AIService()
        organization = ai_service.organize_tasks(tasks)
        return {"organization": organization}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/suggest/{task_id}")
def suggest_improvements(task_id: int):
    """Get AI suggestions for task improvement"""
    try:
        task = TaskService.get_task(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        ai_service = AIService()
        suggestion = ai_service.suggest_task_improvements(task)

        # Save suggestion to task
        TaskService.add_ai_suggestion(task_id, suggestion)

        return {"suggestion": suggestion}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat")
def chat(msg: ChatMessage):
    """Chat with AI for task management assistance"""
    try:
        context_tasks = None
        if msg.include_context:
            context_tasks = TaskService.get_all_tasks()

        ai_service = AIService()
        response = ai_service.chat(msg.message, context_tasks)

        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/clear")
def clear_chat_history():
    """Clear AI chat history"""
    try:
        ai_service = AIService()
        ai_service.clear_history()
        return {"message": "Chat history cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
