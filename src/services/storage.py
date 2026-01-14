"""JSON Storage service for persistent task storage."""

import json
import os
import shutil
from typing import List, Dict, Any
from datetime import datetime

from ..models.task import Task
from ..models.enums import Priority
from ..exceptions import StorageError


class JSONStorage:
    """Manages persistent storage of tasks using JSON file.

    Attributes:
        filepath: Path to JSON storage file
        backup_filepath: Path to backup file
    """

    def __init__(self, filepath: str = "todo.json"):
        """Initialize JSONStorage with specified filepath.

        Args:
            filepath: Path to JSON storage file (default: "todo.json")
        """
        self.filepath = filepath
        self.backup_filepath = f"{filepath}.bak"

    def save_tasks(self, tasks: List[Task]) -> None:
        """Save tasks to JSON file with automatic backup.

        Args:
            tasks: List of Task objects to save

        Raises:
            StorageError: On I/O failures, permission errors
        """
        # Create backup if file exists
        if os.path.exists(self.filepath):
            shutil.copy2(self.filepath, self.backup_filepath)

        # Convert Task objects to dictionaries
        tasks_dict = {"tasks": [self._task_to_dict(task) for task in tasks]}

        # Write to temporary file first (atomic operation)
        temp_path = f"{self.filepath}.tmp"
        try:
            with open(temp_path, "w") as f:
                json.dump(tasks_dict, f, indent=2)
        except (IOError, PermissionError) as e:
            raise StorageError(f"Cannot write file: {e}")

        # Rename to final filename (atomic operation)
        try:
            os.replace(temp_path, self.filepath)
        except OSError as e:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise StorageError(f"Cannot save file: {e}")

    def load_tasks(self) -> List[Task]:
        """Load tasks from JSON file.

        Returns:
            List of Task objects

        Raises:
            StorageError: On file corruption or I/O failures
        """
        # Return empty list if file doesn't exist
        if not os.path.exists(self.filepath):
            return []

        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)

            # Validate JSON structure
            if not isinstance(data, dict) or "tasks" not in data:
                raise StorageError("Invalid file format: missing 'tasks' key")

            if not isinstance(data["tasks"], list):
                raise StorageError("Invalid file format: 'tasks' must be an array")

            # Convert dictionaries to Task objects
            return [self._dict_to_task(task_dict) for task_dict in data["tasks"]]

        except json.JSONDecodeError as e:
            raise StorageError(f"Corrupted data file: {e}")
        except (IOError, PermissionError) as e:
            raise StorageError(f"Cannot read file: {e}")

    def _task_to_dict(self, task: Task) -> Dict[str, Any]:
        """Convert Task object to dictionary for JSON serialization.

        Args:
            task: Task object to convert

        Returns:
            Dictionary representation of task
        """
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "due_date": task.due_date,
            "priority": task.priority.value,
            "tags": task.tags
        }

    def _dict_to_task(self, task_dict: Dict[str, Any]) -> Task:
        """Convert dictionary to Task object.

        Args:
            task_dict: Dictionary to convert

        Returns:
            Task object

        Raises:
            ValueError: If required fields are missing or invalid
        """
        # Map priority string to enum
        priority_map = {"High": Priority.HIGH, "Medium": Priority.MEDIUM, "Low": Priority.LOW}
        priority_str = task_dict.get("priority", "Medium")
        priority = priority_map.get(priority_str, Priority.MEDIUM)

        return Task(
            id=task_dict["id"],
            title=task_dict["title"],
            description=task_dict.get("description", ""),
            completed=task_dict.get("completed", False),
            due_date=task_dict.get("due_date"),
            priority=priority,
            tags=task_dict.get("tags", [])
        )
