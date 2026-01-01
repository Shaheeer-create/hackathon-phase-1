"""Task dataclass model."""

from dataclasses import dataclass, field
from typing import List, Optional

try:
    from .enums import Priority
except ImportError:
    Priority = None

try:
    from .recurrence import RecurrenceRule, Reminder
except ImportError:
    RecurrenceRule = None
    Reminder = None


@dataclass(frozen=True)
class Task:
    """Immutable todo item with unique identifier and completion status.

    Attributes:
        id: Unique sequential identifier (1, 2, 3...)
        title: Task title/name (required, must not be empty)
        description: Task description (optional, default empty)
        completed: Task completion status (False=pending, True=completed)
        due_date: Due date in YYYY-MM-DD format (optional)
        due_time: Due time in HH:MM format (optional)
        priority: Task priority (High/Medium/Low, default Medium)
        tags: List of categorization tags (default empty list)
        recurrence_rule: Recurrence schedule for recurring tasks (optional)
        reminder: Scheduled notification for this task (optional)
    """

    id: int
    title: str
    description: str = ""
    completed: bool = False
    due_date: Optional[str] = None
    due_time: Optional[str] = None

    # New fields for enhanced features
    if Priority is not None:
        priority: Priority = Priority.MEDIUM
    else:
        # Fallback if enum not available yet (during initialization)
        priority: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    # Recurrence and reminder fields (optional)
    recurrence_rule: Optional[RecurrenceRule] = None
    reminder: Optional[Reminder] = None
