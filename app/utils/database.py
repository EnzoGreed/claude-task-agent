import json
import os
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

# Data storage paths
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

TASKS_FILE = DATA_DIR / "tasks.json"
REMINDERS_FILE = DATA_DIR / "reminders.json"


class DataStore:
    """Simple JSON-based data store"""

    @staticmethod
    def load_json(file_path: Path) -> List[Dict]:
        """Load data from JSON file"""
        if file_path.exists():
            try:
                with open(file_path, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    @staticmethod
    def save_json(file_path: Path, data: List[Dict]):
        """Save data to JSON file"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    @staticmethod
    def get_next_id(file_path: Path) -> int:
        """Get the next ID for a new record"""
        data = DataStore.load_json(file_path)
        if not data:
            return 1
        return max(item.get('id', 0) for item in data) + 1


class Session:
    """Mock session for compatibility"""
    pass


def get_db():
    """Dependency for FastAPI"""
    return Session()
