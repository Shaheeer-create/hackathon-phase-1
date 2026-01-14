# Data Model: Enhanced CLI Todo Application

**Date**: 2025-12-31
**Purpose**: Define data structures for enhanced Todo application

## Core Entities

### 1. Priority Enum

**File**: `src/models/enums.py`

```python
from enum import Enum

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
```

**Attributes**:
- `HIGH`: Most urgent tasks (sorting: first)
- `MEDIUM`: Normal urgency (sorting: middle)
- `LOW`: Least urgent (sorting: last)

**Invariant**: Enum member order determines sort order (natural ordering)

---

### 2. Sort Order Enum

**File**: `src/models/enums.py`

```python
class SortOrder(Enum):
    """Options for sorting task display."""
    DUE_DATE = "due_date"
    PRIORITY = "priority"
    ALPHABETICAL = "alphabetical"
    DEFAULT = "default"
```

**Attributes**:
- `DUE_DATE`: Sort chronologically (earliest first, tasks without due date last)
- `PRIORITY`: Sort by priority (High → Medium → Low)
- `ALPHABETICAL`: Sort case-insensitive by title
- `DEFAULT`: No sorting (maintain stored order)

---

### 3. Filter Date Category Enum

**File**: `src/models/enums.py`

```python
class DueDateCategory(Enum):
    """Due date filter categories."""
    TODAY = "today"
    UPCOMING = "upcoming"
    OVERDUE = "overdue"
```

**Attributes**:
- `TODAY`: Tasks with due_date == today's date
- `UPCOMING`: Tasks with due_date > today's date
- `OVERDUE`: Tasks with due_date < today's date AND not completed

---

### 4. Task Dataclass

**File**: `src/models/task.py`

```python
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass(frozen=True)
class Task:
    """Immutable todo item with enhanced attributes.

    Attributes:
        id: Unique sequential identifier (1, 2, 3...)
        title: Task title/name (required, must not be empty)
        description: Task description (optional, default empty)
        completed: Task completion status (False=pending, True=completed)
        due_date: Due date in YYYY-MM-DD format (optional, None for no due date)
        priority: Task priority (High/Medium/Low, default Medium)
        tags: List of categorization tags (default empty list, case-sensitive)

    Invariants:
        - id >= 1
        - title is not empty (after strip)
        - tags list contains no duplicates
        - due_date format is YYYY-MM-DD if not None
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False
    due_date: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    tags: List[str] = field(default_factory=list)
```

**Attributes**:
- `id: int`: Unique sequential identifier starting from 1
- `title: str`: Task title/name (required, must not be empty)
- `description: str`: Optional description (default empty string)
- `completed: bool`: Completion status (False=pending, True=completed)
- `due_date: Optional[str]`: Due date in YYYY-MM-DD format (None for no due date)
- `priority: Priority`: Priority level (default MEDIUM)
- `tags: List[str]`: Categorization tags (default empty list, case-sensitive)

**Invariants**:
- Task is immutable (frozen=True)
- ID is sequential (1, 2, 3...)
- Title is non-empty
- Tags contain no duplicates (enforced by service layer)
- Due date format validated before Task creation

**Examples**:
```python
# Basic task
task = Task(id=1, title="Buy groceries")

# Full-featured task
task = Task(
    id=2,
    title="Complete project documentation",
    description="Write detailed docs for each feature",
    completed=False,
    due_date="2025-01-05",
    priority=Priority.HIGH,
    tags=["Work", "Documentation"]
)
```

---

### 5. Task Filter Dataclass

**File**: `src/models/task.py` (or `src/models/filters.py`)

```python
from dataclasses import dataclass, field
from typing import Optional

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
```

**Attributes**:
- `keyword: Optional[str]`: Search term for title/description (case-insensitive)
- `status: Optional[bool]`: Filter by completion (None=All, True=Completed, False=Pending)
- `priority: Optional[Priority]`: Filter by priority level (None=All)
- `due_date_category: Optional[DueDateCategory]`: Filter by due date (None=All)

**Filter Behavior**:
- Multiple filters apply AND logic (all must match)
- None values exclude that criterion from filtering
- Keyword: Empty string or None returns all tasks
- Status: None returns both completed and pending
- Priority: None returns all priority levels
- Due date: None includes all tasks (including those without due date)

**Examples**:
```python
# No filters (return all tasks)
filter_all = TaskFilter()

# Filter for pending High priority tasks
filter_pending_high = TaskFilter(
    status=False,
    priority=Priority.HIGH
)

# Search for "meeting" in upcoming tasks
filter_meeting = TaskFilter(
    keyword="meeting",
    due_date_category=DueDateCategory.UPCOMING
)
```

---

## Data Relationships

### Task Lifecycle

```
[User Input]
    ↓
[Validate] → title not empty, date format valid
    ↓
[Create Task] → Immutable Task instance
    ↓
[Add to TaskManager] → Store in internal list
    ↓
[Save to Storage] → Persist to JSON file
```

### Task Update Flow

```
[Existing Task]
    ↓
[Get by ID]
    ↓
[Create New Task] → New immutable instance with updated fields
    ↓
[Replace in TaskManager] → Update internal list
    ↓
[Save to Storage] → Persist changes
```

### Filter Chain

```
[All Tasks]
    ↓
[Keyword Filter] → Keep if keyword in title or description
    ↓
[Status Filter] → Keep if status matches
    ↓
[Priority Filter] → Keep if priority matches
    ↓
[Due Date Filter] → Keep if due date category matches
    ↓
[Filtered Tasks]
```

---

## Storage Format

### JSON File Structure

**File**: `todo.json`

```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Complete project documentation",
      "description": "Write detailed docs for each feature",
      "completed": false,
      "due_date": "2025-01-05",
      "priority": "High",
      "tags": ["Work", "Documentation"]
    },
    {
      "id": 2,
      "title": "Buy groceries",
      "description": "",
      "completed": true,
      "due_date": "2025-01-01",
      "priority": "Medium",
      "tags": ["Home"]
    }
  ]
}
```

### Serialization Rules

- **Priority**: Stored as string ("High", "Medium", "Low")
- **Due Date**: Stored as YYYY-MM-DD string or `null`
- **Tags**: Stored as JSON array of strings
- **Boolean**: Stored as `true` or `false` (JSON boolean)
- **Empty Fields**: Stored with default values (empty string, empty array, null)

---

## Data Integrity Rules

### TaskManager Invariants

1. **Sequential IDs**: Tasks are numbered 1, 2, 3... with no gaps
2. **No Duplicates**: Each ID appears exactly once
3. **Tag Uniqueness**: No duplicate tags within a single task
4. **Date Format**: All due dates are valid YYYY-MM-DD or null

### Filter Invariants

1. **Empty Filter**: Returns all tasks (no filtering)
2. **Multiple Filters**: All must match (AND logic)
3. **Case Insensitivity**: Keyword search is case-insensitive

### Sort Invariants

1. **Stable Sort**: Equal keys maintain original relative order
2. **Non-Destructive**: Sorting returns new list, doesn't modify stored order
3. **None Handling**: Tasks without sort key placed last

---

**Document Status**: Complete | Ready for: Implementation
