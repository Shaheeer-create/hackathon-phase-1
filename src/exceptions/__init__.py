"""Todo CLI exceptions package."""

import sys
import os

# Support both module and script execution
try:
    from ..models.task import Task
    from ..services.task_manager import TaskManager
except (ImportError, ValueError):
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    from models.task import Task
    from services.task_manager import TaskManager


class TaskNotFoundError(Exception):
    """Exception raised when a task with given ID is not found."""

    def __init__(self, task_id: int) -> None:
        """Initialize TaskNotFoundError.

        Args:
            task_id: The task ID that was not found
        """
        super().__init__(f"Task with ID {task_id} not found")


class InvalidTaskError(Exception):
    """Exception raised when task validation fails."""

    def __init__(self, message: str) -> None:
        """Initialize InvalidTaskError.

        Args:
            message: The validation error message
        """
        super().__init__(message)
