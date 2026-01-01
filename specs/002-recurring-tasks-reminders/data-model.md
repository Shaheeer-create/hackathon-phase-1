# Data Model Design: Recurring Tasks and Reminders

**Feature**: Recurring Tasks and Reminders
**Date**: 2026-01-01
**Status**: Complete

## Overview

This document defines the data model extensions required to support recurring tasks and time-based reminders. The design maintains immutability (per constitution), uses Python `dataclasses`, and integrates seamlessly with the existing `Task` model.

---

## New Enums

### RecurrencePattern

```python
from enum import Enum
from typing import Literal

class RecurrencePattern(Enum):
    """Defines the recurrence frequency pattern for tasks."""
    DAILY: Literal["daily"] = "daily"
    WEEKLY: Literal["weekly"] = "weekly"
    MONTHLY: Literal["monthly"] = "monthly"
```

**Purpose**: Encapsulates the three supported recurrence patterns defined in spec (FR-001).

**Values**:
- `DAILY`: Task repeats every day (next occurrence = current date + 1 day)
- `WEEKLY`: Task repeats every week (next occurrence = current date + 7 days)
- `MONTHLY`: Task repeats every month (next occurrence = current date + 1 month)

**Invariants**:
- Only three patterns supported (custom intervals out of scope per spec)
- String values match user-facing display in CLI

---

## New Dataclasses

### RecurrenceRule

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .enums import RecurrencePattern

@dataclass(frozen=True)
class RecurrenceRule:
    """Defines a recurring task's repetition schedule.

    Attributes:
        pattern: Recurrence frequency (daily/weekly/monthly)
        base_date: The original due date that started the recurrence
        next_occurrence_date: When the next instance should appear
        max_instances: Maximum number of instances to generate (100 per spec)
    """

    pattern: RecurrencePattern
    base_date: datetime
    next_occurrence_date: datetime
    max_instances: Optional[int] = 100

    def __post_init__(self) -> None:
        """Validate recurrence rule after initialization."""
        if self.max_instances is not None and self.max_instances < 1:
            raise ValueError("max_instances must be at least 1")
        if self.max_instances and self.max_instances > 100:
            raise ValueError("max_instances cannot exceed 100")
        if self.next_occurrence_date < datetime.now():
            raise ValueError("next_occurrence_date cannot be in the past")
```

**Purpose**: Stores recurrence metadata for a task, enabling automatic generation of next instances upon completion (FR-002).

**Key Attributes**:
- `pattern`: Enum for recurrence type (daily/weekly/monthly)
- `base_date`: Anchors the recurrence cycle (used for month-day calculations)
- `next_occurrence_date`: When to generate the next task instance
- `max_instances`: Safety limit to prevent excessive task generation (FR-015)

**Invariants**:
- Frozen (immutable): Cannot be modified after creation (constitution compliance)
- `next_occurrence_date` must be in the future
- `max_instances` defaults to 100, min value is 1, max value is 100

**Relationships**:
- One-to-one with `Task` (each task can have at most one recurrence rule)
- Related to `Reminder` entity through task association

---

### Reminder

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum

class ReminderStatus(Enum):
    """Status of a reminder notification."""
    SCHEDULED: str = "scheduled"
    SNOOZED: str = "snoozed"
    DISMISSED: str = "dismissed"

@dataclass(frozen=True)
class Reminder:
    """Represents a scheduled notification for a task.

    Attributes:
        task_id: The task ID this reminder is for
        reminder_time: When the reminder should trigger
        status: Current state of the reminder
        offset_hours: How many hours before due date to remind (24 default)
    """

    task_id: int
    reminder_time: datetime
    status: ReminderStatus = ReminderStatus.SCHEDULED
    offset_hours: int = 24

    def __post_init__(self) -> None:
        """Validate reminder after initialization."""
        if self.task_id < 1:
            raise ValueError("task_id must be positive")
        if self.reminder_time < datetime.now():
            raise ValueError("reminder_time cannot be in the past")
        if self.offset_hours < 0 or self.offset_hours > 168:  # 168 hours = 1 week
            raise ValueError("offset_hours must be between 0 and 168 (7 days)")
```

**Purpose**: Schedules and tracks notification state for time-sensitive tasks (FR-008, FR-009).

**Key Attributes**:
- `task_id`: References the associated task
- `reminder_time`: When to trigger the notification
- `status`: Tracks if reminder was scheduled, snoozed, or dismissed (FR-010)
- `offset_hours`: Defaults to 24 hours before due (per spec assumption)

**Invariants**:
- Frozen (immutable): Cannot be modified after creation (constitution compliance)
- `task_id` must be positive
- `reminder_time` must be in the future
- `offset_hours` must be between 0 and 168 (reasonable reminder window)

**Relationships**:
- Many-to-one with `Task` (multiple reminders could exist for one task in future, but initial implementation supports one)
- Independent from `RecurrenceRule` (reminders track notification state, recurrence tracks task generation)

---

## Extended Dataclass: Task

The existing `Task` model requires optional fields for recurrence and reminder support:

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

@dataclass(frozen=True)
class Task:
    """Represents a single task in the todo list.

    Attributes:
        id: Unique sequential identifier
        title: Task title (required)
        description: Optional detailed description
        completed: Whether task is done
        due_date: Optional due date in YYYY-MM-DD format (string)
        due_time: NEW - Optional due time in HH:MM format
        priority: Task priority level
        tags: List of category labels
        recurrence_rule: NEW - Optional recurrence pattern for automatic rescheduling
    """

    id: int
    title: str
    description: str = ""
    completed: bool = False
    due_date: Optional[str] = None
    due_time: Optional[str] = None  # NEW
    priority: Priority = Priority.MEDIUM
    tags: List[str] = field(default_factory=list)
    recurrence_rule: Optional[RecurrenceRule] = None  # NEW
```

**New Fields**:
- `due_time`: Optional string in HH:MM format for precise scheduling (FR-004)
- `recurrence_rule`: Optional `RecurrenceRule` for recurring tasks (FR-001)

**Invariants Maintained**:
- Frozen (immutable): Unchanged from existing model
- All fields have clear types (constitution compliance)
- Optional fields default to appropriate falsy values

---

## Relationships Diagram

```
┌─────────────┐         ┌──────────────────┐         ┌─────────────┐
│   Task      │◄───────►│ RecurrenceRule  │         │  Reminder    │
│ (existing)  │         │ (new)          │         │ (new)      │
└──────┬──────┘         └──────────────────┘         └──────┬──────┘
       │                                            │
       │◄──────────────────────────────────────────┤
       │                                            │
       │          ┌──────────────────┐         │
       └─────────►│ TaskManager      │◄──────┘
                  │ (controller)     │
                  │                  │
                  └──────────────────┘
```

**Relationships**:
1. **Task → RecurrenceRule**: One-to-one (task either has recurrence or doesn't)
2. **Task → Reminder**: Many-to-one (initially one reminder per task)
3. **TaskManager → Task**: Aggregates all tasks, handles recurrence logic, manages reminder scheduling

---

## Storage Strategy

### In-Memory List (Existing)

The existing `TaskManager` uses an in-memory list for task storage. This approach continues for recurrence and reminder data:

```python
class TaskManager:
    def __init__(self) -> None:
        self._tasks: List[Task] = []              # Existing
        self._reminders: List[Reminder] = []          # NEW
        self._recurrence_rules: List[RecurrenceRule] = [] # NEW
        self._next_id: int = 1                      # Existing
```

**Rationale**:
- Continues existing architecture (simple, maintainable)
- No file I/O overhead for fast access (aligns with performance goals)
- Per-session storage (spec constraint: no cross-device sync)

**Future Enhancement**:
- If persistence is added later (JSON file), `RecurrenceRule` and `Reminder` can be serialized similarly to existing `Task` storage approach

---

## Data Validations

### RecurrencePattern Validation

| Input | Valid | Reason |
|--------|--------|---------|
| "daily" | Yes | Matches enum DAILY |
| "DAILY" | Yes | Case-insensitive match |
| "d" | No | Not in enum (user must specify full word) |

### RecurrenceRule Validation

| Scenario | Expected Behavior |
|-----------|------------------|
| `max_instances = 0` | Raise ValueError (must be ≥ 1) |
| `max_instances = 101` | Raise ValueError (must be ≤ 100 per FR-015) |
| `next_occurrence_date` in past | Raise ValueError (must be future) |

### Reminder Validation

| Scenario | Expected Behavior |
|-----------|------------------|
| `task_id = 0` | Raise ValueError (must be positive) |
| `offset_hours = -1` | Raise ValueError (must be ≥ 0) |
| `offset_hours = 169` | Raise ValueError (must be ≤ 168) |
| `reminder_time` in past | Raise ValueError (must be future) |

---

## Type Hints and Imports

```python
from dataclasses import dataclass, field, frozen
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, List
```

All new models use type hints as required by constitution.

---

## Immutability Strategy

All new dataclasses use `@dataclass(frozen=True)` to ensure:
1. **No direct field mutation** after creation
2. **Deep immutability** for nested objects (enums are immutable by default)
3. **Hashable** for use in sets/dicts if needed

When a task needs modification, create a new instance with updated fields (existing pattern).

---

## Integration with Existing Models

### Backward Compatibility

Existing `Task` model is extended, not replaced:
- New fields `due_time` and `recurrence_rule` are optional
- Existing tests and code continue to work with tasks that don't use recurrence or reminders
- Default values ensure backward compatibility

### Migration Path

No database migration needed (in-memory storage). When loading from JSON persistence (if added):
- Missing `due_time` or `recurrence_rule` fields default to `None`
- Old JSON files parse correctly without errors
