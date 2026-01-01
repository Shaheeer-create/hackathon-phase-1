"""TaskManager service - manages in-memory task collection with CRUD operations."""

import re
import sys
import os
from typing import List, Optional

# Support both module and script execution
try:
    from ..models.task import Task
    from ..models.enums import Priority
    from ..exceptions import TaskNotFoundError, InvalidTaskError
    from ..utils.validators import validate_priority, validate_tags
except (ImportError, ValueError):
    # Running as script - add parent to path
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    from models.task import Task
    from models.enums import Priority
    from exceptions import TaskNotFoundError, InvalidTaskError
    from utils.validators import validate_priority, validate_tags


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
        self,
        title: str,
        description: str = "",
        due_date: Optional[str] = None,
        priority: Optional[Priority] = None,
        tags: Optional[List[str]] = None
    ) -> Task:
        """Add a new task to the task list.

        Args:
            title: Task title (required, must not be empty)
            description: Task description (optional)
            due_date: Due date in YYYY-MM-DD format (optional)
            priority: Task priority (optional, defaults to MEDIUM)
            tags: List of tags (optional, deduplicated)

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

        # Use validators for priority and tags
        valid_priority = validate_priority(priority.value if priority else None)
        deduplicated_tags = validate_tags(",".join(tags)) if tags else []

        # Create new task with next sequential ID
        task = Task(
            id=self._next_id,
            title=title,
            description=description.strip(),
            completed=False,
            due_date=due_date,
            priority=valid_priority if valid_priority else Priority.MEDIUM,
            tags=deduplicated_tags
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
        priority: Optional[Priority] = None,
        tags: Optional[List[str]] = None
    ) -> Task:
        """Update an existing task with new values.

        Args:
            task_id: Sequential task ID to update
            title: New title (optional, must not be empty if provided)
            description: New description (optional)
            due_date: New due date in YYYY-MM-DD format (optional)
            priority: New priority (optional)
            tags: New list of tags (optional, deduplicated)

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

        # Validate new priority if provided
        valid_priority = None
        if priority is not None:
            valid_priority = validate_priority(priority.value)
            if not valid_priority:
                raise ValueError("Invalid priority. Expected High, Medium, or Low")

        # Deduplicate tags if provided
        deduplicated_tags = None
        if tags is not None:
            deduplicated_tags = validate_tags(",".join(tags))

        # Update fields (keep existing values if not provided)
        updated_title = title if title is not None else existing_task.title
        updated_desc = description if description is not None else existing_task.description
        updated_due = due_date if due_date is not None else existing_task.due_date
        updated_priority = valid_priority if valid_priority else existing_task.priority
        updated_tags = deduplicated_tags if deduplicated_tags is not None else existing_task.tags

        # Create new immutable task instance
        updated_task = Task(
            id=existing_task.id,
            title=updated_title,
            description=updated_desc,
            completed=existing_task.completed,
            due_date=updated_due,
            priority=updated_priority,
            tags=updated_tags
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
            due_date=existing_task.due_date,
            priority=existing_task.priority,
            tags=existing_task.tags
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

    def search_tasks(self, keyword: str) -> List[Task]:
        """Search tasks by keyword in title, description, or tags.

        Args:
            keyword: Search keyword (case-insensitive)

        Returns:
            List of matching Task objects (empty list if no matches)
        """
        if not keyword:
            return []

        keyword_lower = keyword.lower()
        matching_tasks = []

        for task in self._tasks:
            # Search in title
            if keyword_lower in task.title.lower():
                matching_tasks.append(task)
                continue

            # Search in description
            if task.description and keyword_lower in task.description.lower():
                matching_tasks.append(task)
                continue

            # Search in tags
            for tag in task.tags:
                if keyword_lower in tag.lower():
                    matching_tasks.append(task)
                    break

        return matching_tasks

    def filter_tasks(
        self,
        status: Optional[str] = None,
        priority: Optional[Priority] = None,
        due_before: Optional[str] = None
    ) -> List[Task]:
        """Filter tasks by status, priority, or due date.

        Args:
            status: Filter by status ("completed" or "pending")
            priority: Filter by priority (Priority enum)
            due_before: Filter tasks due before this date (YYYY-MM-DD format)

        Returns:
            List of filtered Task objects (empty list if no matches)

        Raises:
            ValueError: If status is invalid or due_before has invalid format
        """
        filtered_tasks = self._tasks.copy()

        # Filter by status
        if status:
            status_lower = status.lower()
            if status_lower == "completed":
                filtered_tasks = [t for t in filtered_tasks if t.completed]
            elif status_lower == "pending":
                filtered_tasks = [t for t in filtered_tasks if not t.completed]
            else:
                raise ValueError("Invalid status. Must be 'completed' or 'pending'")

        # Filter by priority
        if priority:
            filtered_tasks = [t for t in filtered_tasks if t.priority == priority]

        # Filter by due date (tasks due before specified date)
        if due_before:
            if not self._is_valid_date(due_before):
                raise ValueError("Invalid date format. Expected YYYY-MM-DD")
            filtered_tasks = [
                t for t in filtered_tasks
                if t.due_date and t.due_date <= due_before
            ]

        return filtered_tasks

    def sort_tasks(self, by: str = "id") -> List[Task]:
        """Sort tasks by specified field.

        Args:
            by: Sort field - "id" (default), "due_date", "priority", or "title"

        Returns:
            List of sorted Task objects

        Raises:
            ValueError: If sort field is invalid
        """
        # Create a copy to avoid modifying original list
        tasks_to_sort = self._tasks.copy()

        if by == "id":
            # Sort by ID (already in order, but for consistency)
            return sorted(tasks_to_sort, key=lambda t: t.id)
        elif by == "due_date":
            # Sort by due date (tasks without due dates come last)
            return sorted(
                tasks_to_sort,
                key=lambda t: (t.due_date is None, t.due_date or "")
            )
        elif by == "priority":
            # Sort by priority (High > Medium > Low)
            priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
            return sorted(
                tasks_to_sort,
                key=lambda t: priority_order.get(t.priority, 1)
            )
        elif by == "title":
            # Sort alphabetically by title
            return sorted(tasks_to_sort, key=lambda t: t.title.lower())
        else:
            raise ValueError(
                "Invalid sort field. Must be 'id', 'due_date', 'priority', or 'title'"
            )

    def _reindex_tasks(self) -> None:
        """Re-index all tasks to maintain sequential IDs starting from 1."""
        for i, task in enumerate(self._tasks):
            # Create new task with updated ID
            self._tasks[i] = Task(
                id=i + 1,
                title=task.title,
                description=task.description,
                completed=task.completed,
                due_date=task.due_date,
                priority=task.priority,
                tags=task.tags
            )
