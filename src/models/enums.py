"""Enums and dataclasses for Todo CLI."""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional


class Priority(Enum):
    """Task priority levels for sorting and filtering.

    Enum members maintain definition order for natural sorting:
    HIGH > MEDIUM > LOW
    """
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

    def __str__(self) -> str:
        """Return string representation of priority."""
        return self.value


class SortOrder(Enum):
    """Options for sorting task display."""
    DUE_DATE = "due_date"
    PRIORITY = "priority"
    ALPHABETICAL = "alphabetical"
    DEFAULT = "default"


class DueDateCategory(Enum):
    """Due date filter categories."""
    TODAY = "today"
    UPCOMING = "upcoming"
    OVERDUE = "overdue"


@dataclass(frozen=True)
class TaskFilter:
    """Criteria for filtering task display.

    All attributes are optional. Any None value means "apply no filter"
    for that criterion.

    Attributes:
        keyword: Search keyword (case-insensitive, matches title or description)
        status: Completion status (None=All, True=Completed, False=Pending)
        priority: Priority level filter (None=All, or specific priority)
        due_date_category: Due date category (None=All, or "today"/"upcoming"/"overdue")
    """
    keyword: Optional[str] = None
    status: Optional[bool] = None
    priority: Optional[Priority] = None
    due_date_category: Optional[DueDateCategory] = None
