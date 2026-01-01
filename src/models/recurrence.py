"""Recurrence and reminder models for Todo CLI application."""

from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


class RecurrencePattern(Enum):
    """Defines recurrence frequency pattern for tasks."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

    def __str__(self) -> str:
        """Return string representation of pattern."""
        return self.value


@dataclass(frozen=True)
class RecurrenceRule:
    """Defines a recurring task's repetition schedule.

    Attributes:
        pattern: Recurrence frequency (daily/weekly/monthly)
        base_date: The original due date that anchors recurrence cycle
        next_occurrence_date: When to next instance
        max_instances: Maximum number of instances to generate (100 per spec)
    """

    pattern: RecurrencePattern
    base_date: datetime
    next_occurrence_date: datetime
    max_instances: int = 100

    def __post_init__(self) -> None:
        """Validate recurrence rule after initialization."""
        if self.max_instances < 1:
            raise ValueError("max_instances must be at least 1")
        if self.max_instances > 100:
            raise ValueError("max_instances cannot exceed 100")
        if self.next_occurrence_date < datetime.now():
            raise ValueError("next_occurrence_date cannot be in the past")


@dataclass(frozen=True)
class Reminder:
    """Represents a scheduled notification for a task.

    Attributes:
        task_id: The task ID this reminder is for
        reminder_time: When to reminder should trigger
        status: Current state of reminder (scheduled/snoozed/dismissed)
        offset_hours: How many hours before due date to remind (24 default)
    """

    task_id: int
    reminder_time: datetime
    status: str = "scheduled"
    offset_hours: int = 24

    def __post_init__(self) -> None:
        """Validate reminder after initialization."""
        if self.task_id < 1:
            raise ValueError("task_id must be positive")
        if self.reminder_time < datetime.now():
            raise ValueError("reminder_time cannot be in the past")
        if self.offset_hours < 0 or self.offset_hours > 168:
            raise ValueError("offset_hours must be between 0 and 168 (7 days)")
