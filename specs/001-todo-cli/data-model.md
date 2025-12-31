# Data Model: Todo CLI - Basic Task Management

**Date**: 2025-12-31
**Purpose**: Define data entities, validation rules, and state transitions for Task application

## Entities

### Task

**Purpose**: Represents a single todo item with all required and optional attributes

**Fields**:

| Field | Type | Required | Description | Validation |
|--------|--------|-----------|-------------|
| id | int | Yes | Unique sequential identifier (1, 2, 3...) | Must be positive integer, assigned by TaskManager |
| title | str | Yes | Task title/name | Must not be empty or whitespace-only |
| description | str | No | Additional task details | Can be empty, accepts any characters including special characters |
| completed | bool | No | Task completion status | True = completed, False = pending (default False) |
| due_date | Optional[str] | No | Task due date in YYYY-MM-DD format | Must match YYYY-MM-DD regex if provided |

**Type Definition**:
```python
@dataclass(frozen=True)
class Task:
    """Immutable todo item with unique identifier and completion status."""
    id: int
    title: str
    description: str = ""
    completed: bool = False
    due_date: Optional[str] = None
```

**Validation Rules**:
- V001: `id` MUST be positive integer (>= 1)
- V002: `title` MUST NOT be empty or whitespace-only
- V003: `description` accepts any string (including empty, special characters)
- V004: `completed` defaults to False (pending state)
- V005: `due_date` MUST match YYYY-MM-DD format if provided, otherwise None

**State Transitions**:
```
Pending (completed=False) → Complete (completed=True)
Complete (completed=True) → Pending (completed=False)
```

**Invariants**:
- Task is immutable (frozen=True) - cannot modify after creation
- All tasks created with unique sequential ID

---

### TaskList

**Purpose**: In-memory collection of all tasks, managing unique sequential IDs and CRUD operations

**Structure**:
```python
class TaskManager:
    """Manages in-memory collection of Task objects with CRUD operations."""
    _tasks: List[Task]  # Internal list (private)
    _next_id: int  # Next ID to assign (starts at 1)
```

**Operations**:

| Operation | Input | Output | Side Effects |
|-----------|--------|--------|--------------|
| add_task(title, description, due_date) | title (str), description (str), due_date (str) | Task | Creates task with next ID, increments _next_id |
| get_task(task_id) | task_id (int) | Task | No side effects |
| list_tasks() | None | List[Task] | No side effects |
| update_task(task_id, **kwargs) | task_id (int), title/description/due_date | Task | Replaces task with new immutable instance |
| delete_task(task_id) | task_id (int) | None | Removes task, re-indexes all remaining tasks |
| toggle_complete(task_id) | task_id (int) | Task | Flips completed status, returns updated task |

**Invariants**:
- All task IDs are unique and sequential starting from 1
- After deletion, all remaining tasks are re-indexed to maintain sequence
- _next_id always points to next available ID
- All operations return Task objects (except delete_task which returns None)

**Validation Rules**:
- V006: `get_task(task_id)` raises TaskNotFoundError if ID not found
- V007: `update_task(task_id)` raises TaskNotFoundError if ID not found
- V008: `delete_task(task_id)` raises TaskNotFoundError if ID not found
- V009: `toggle_complete(task_id)` raises TaskNotFoundError if ID not found
- V010: `add_task` raises ValueError if title is empty or whitespace

**Re-indexing Logic**:
When task is deleted, all subsequent tasks shift down:
```
Before: [Task(id=1), Task(id=2), Task(id=3), Task(id=4), Task(id=5)]
Delete task ID 3
After: [Task(id=1), Task(id=2), Task(id=1→3), Task(id=2→4), Task(id=3→5)]
Result: [Task(id=1), Task(id=2), Task(id=3), Task(id=4)]
```

---

## Relationships

**Task → TaskList**: Aggregation
- TaskList contains zero or more Task objects
- Task does not know about TaskList
- TaskList manages Task lifecycle (creation, deletion)

**Cardinality**:
- TaskList: 0..* Task (zero to many tasks)
- Task: Exactly one TaskList (belongs to TaskManager)

---

## Data Flow

### Add Task Flow
```
User Input → validate title → create Task(id=_next_id) → append to _tasks → increment _next_id → return Task
```

### List Tasks Flow
```
User Request → return copy of _tasks list (immutable iteration)
```

### Update Task Flow
```
User Input + task_id → find task → create new Task instance → replace at index → return new Task
```

### Delete Task Flow
```
User Input + task_id → find task → remove from _tasks → re-index remaining tasks → decrement _next_id → return None
```

### Toggle Complete Flow
```
User Input + task_id → find task → create new Task(completed=not completed) → replace at index → return new Task
```

---

## Error Types

### TaskNotFoundError
**Trigger**: Task ID not found in TaskList
**Usage**: get_task, update_task, delete_task, toggle_complete
**Message**: "Task with ID {task_id} not found"

### InvalidTaskError
**Trigger**: Task validation failure
**Usage**: add_task, update_task
**Message**: Specific to validation rule (e.g., "Task title cannot be empty")

### ValueError
**Trigger**: Invalid date format
**Usage**: add_task, update_task (when due_date provided)
**Message**: "Invalid date format. Expected YYYY-MM-DD"
