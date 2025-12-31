"""TaskManager service - manages in-memory task collection with CRUD operations."""

import re
import sys
import os
from typing import List, Optional

# Support both module and script execution
try:
    from ..models.task import Task
    from ..exceptions import TaskNotFoundError, InvalidTaskError
except (ImportError, ValueError):
    # Running as script - add parent to path
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    from models.task import Task
    from exceptions import TaskNotFoundError, InvalidTaskError


class TaskManager:
    """Manages in-memory collection of Task objects with CRUD operations.

    Attributes:
        _tasks: Internal list of Task objects (private)
        _next_id: Next ID to assign to new tasks (starts at 1)
    """

    def __init__(self) -> None:
        """Initialize TaskManager with empty task list."""
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def add_task(
        self, title: str, description: str = "", due_date: Optional[str] = None
    ) -> Task:
        """Add a new task to the task list.

        Args:
            title: Task title (required, must not be empty)
            description: Task description (optional)
            due_date: Due date in YYYY-MM-DD format (optional)

        Returns:
            Newly created Task object

        Raises:
            ValueError: If title is empty/whitespace-only or date format is invalid
        """
        # Validate title
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty")

        # Validate date format if provided
        if due_date and not self._is_valid_date(due_date):
            raise ValueError("Invalid date format. Expected YYYY-MM-DD")

        # Create new task with next sequential ID
        task = Task(
            id=self._next_id,
            title=title,
            description=description.strip(),
            completed=False,
            due_date=due_date
        )

        # Add to list and increment next ID
        self._tasks.append(task)
        self._next_id += 1

        return task

    def get_task(self, task_id: int) -> Task:
        """Get a task by its ID.

        Args:
            task_id: Sequential task ID to retrieve

        Returns:
            Task object with matching ID

        Raises:
            TaskNotFoundError: If task ID does not exist
        """
        # Find task by ID (convert to 0-based index)
        index = task_id - 1
        if index < 0 or index >= len(self._tasks):
            raise TaskNotFoundError(task_id)
        return self._tasks[index]

    def list_tasks(self) -> List[Task]:
        """Return all tasks in the task list.

        Returns:
            List of all Task objects (empty list if no tasks)
        """
        return self._tasks.copy()

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        due_date: Optional[str] = None,
    ) -> Task:
        """Update an existing task with new values.

        Args:
            task_id: Sequential task ID to update
            title: New title (optional, must not be empty if provided)
            description: New description (optional)
            due_date: New due date in YYYY-MM-DD format (optional)

        Returns:
            Updated Task object (new immutable instance)

        Raises:
            TaskNotFoundError: If task ID does not exist
            ValueError: If title is empty/whitespace-only or date format is invalid
        """
        # Get existing task
        existing_task = self.get_task(task_id)

        # Validate new title if provided
        if title is not None:
            title = title.strip()
            if not title:
                raise ValueError("Task title cannot be empty")

        # Validate new date format if provided
        if due_date is not None and not self._is_valid_date(due_date):
            raise ValueError("Invalid date format. Expected YYYY-MM-DD")

        # Update fields (keep existing values if not provided)
        updated_title = title if title is not None else existing_task.title
        updated_desc = description if description is not None else existing_task.description
        updated_due = due_date if due_date is not None else existing_task.due_date

        # Create new immutable task instance
        updated_task = Task(
            id=existing_task.id,
            title=updated_title,
            description=updated_desc,
            completed=existing_task.completed,
            due_date=updated_due
        )

        # Replace task in list
        index = task_id - 1
        self._tasks[index] = updated_task

        return updated_task

    def delete_task(self, task_id: int) -> None:
        """Delete a task from the task list and re-index remaining tasks.

        Args:
            task_id: Sequential task ID to delete

        Raises:
            TaskNotFoundError: If task ID does not exist
        """
        # Verify task exists
        self.get_task(task_id)

        # Remove task from list
        index = task_id - 1
        self._tasks.pop(index)

        # Re-index remaining tasks to maintain sequential IDs
        self._reindex_tasks()

        # Decrement next ID
        self._next_id -= 1

    def toggle_complete(self, task_id: int) -> Task:
        """Toggle task completion status between pending and completed.

        Args:
            task_id: Sequential task ID to toggle

        Returns:
            Updated Task object with toggled completion status

        Raises:
            TaskNotFoundError: If task ID does not exist
        """
        # Get existing task
        existing_task = self.get_task(task_id)

        # Toggle completion status
        updated_task = Task(
            id=existing_task.id,
            title=existing_task.title,
            description=existing_task.description,
            completed=not existing_task.completed,
            due_date=existing_task.due_date
        )

        # Replace task in list
        index = task_id - 1
        self._tasks[index] = updated_task

        return updated_task

    def _is_valid_date(self, date_str: str) -> bool:
        """Check if date string matches YYYY-MM-DD format.

        Args:
            date_str: Date string to validate

        Returns:
            True if format is YYYY-MM-DD, False otherwise
        """
        pattern = r"^\d{4}-\d{2}-\d{2}$"
        return bool(re.match(pattern, date_str))

    def _reindex_tasks(self) -> None:
        """Re-index all tasks to maintain sequential IDs starting from 1."""
        for i, task in enumerate(self._tasks):
            # Create new task with updated ID
            self._tasks[i] = Task(
                id=i + 1,
                title=task.title,
                description=task.description,
                completed=task.completed,
                due_date=task.due_date
            )
