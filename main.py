from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

from app.routes import tasks_router, reminders_router, ai_router
from app.scheduler import start_scheduler, stop_scheduler

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Task Management Agent",
    description="An intelligent task management system with AI-powered organization and reminders",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks_router)
app.include_router(reminders_router)
app.include_router(ai_router)

# Mount static files
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.on_event("startup")
async def startup_event():
    """Start scheduler on app startup"""
    start_scheduler()
    print("✓ Task scheduler started")


@app.on_event("shutdown")
async def shutdown_event():
    """Stop scheduler on app shutdown"""
    stop_scheduler()
    print("✓ Task scheduler stopped")


@app.get("/")
async def root():
    """Root endpoint - returns API info"""
    return {
        "message": "AI Task Management Agent",
        "version": "1.0.0",
        "docs": "/docs",
        "api_routes": {
            "tasks": "/tasks",
            "reminders": "/reminders",
            "ai": "/ai"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
