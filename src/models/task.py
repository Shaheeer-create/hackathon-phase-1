"""Task dataclass model."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Task:
    """Immutable todo item with unique identifier and completion status.

    Attributes:
        id: Unique sequential identifier (1, 2, 3...)
        title: Task title/name (required, must not be empty)
        description: Task description (optional, default empty)
        completed: Task completion status (False=pending, True=completed)
        due_date: Due date in YYYY-MM-DD format (optional)
    """

    id: int
    title: str
    description: str = ""
    completed: bool = False
    due_date: Optional[str] = None
