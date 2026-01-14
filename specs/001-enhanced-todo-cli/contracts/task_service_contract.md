# Task Service Contract

**Interface**: `TaskManager`
**Purpose**: Manage task collection with CRUD, search, filter, and sort operations

## Operations

### Core CRUD

#### `add_task(title, description, due_date, priority, tags) -> Task`

Create a new task with specified attributes.

**Parameters**:
- `title: str` (required): Task title, must not be empty after strip
- `description: str` (optional): Task description, default ""
- `due_date: Optional[str]` (optional): Due date in YYYY-MM-DD format, default None
- `priority: Priority` (optional): Task priority, default Priority.MEDIUM
- `tags: List[str]` (optional): List of tags, default []

**Returns**: Newly created `Task` object

**Raises**:
- `ValueError`: If title is empty/whitespace-only or due_date format is invalid
- `InvalidTaskError`: If priority value is invalid

**Behavior**:
- Assigns next sequential ID starting from 1
- Strips whitespace from title and description
- Validates date format using regex + strptime
- Validates priority against allowed values
- Deduplicates tags (case-sensitive)
- Stores task in internal list
- Increments next ID

**Example**:
```python
task = manager.add_task(
    title="Complete documentation",
    description="Write detailed docs",
    due_date="2025-01-05",
    priority=Priority.HIGH,
    tags=["Work", "Urgent"]
)
# task.id == 1
```

---

#### `get_task(task_id) -> Task`

Retrieve a task by its ID.

**Parameters**:
- `task_id: int` (required): Sequential task ID to retrieve

**Returns**: `Task` object with matching ID

**Raises**:
- `TaskNotFoundError`: If task ID does not exist

**Behavior**:
- Converts task_id to 0-based index (index = task_id - 1)
- Returns task at that index
- Does not modify task list

**Example**:
```python
task = manager.get_task(task_id=1)
# Returns Task with id=1
```

---

#### `list_tasks() -> List[Task]`

Return all tasks in the task list.

**Returns**: List of all `Task` objects (empty list if no tasks)

**Behavior**:
- Returns copy of internal list (caller cannot modify internal state)
- Returns empty list if no tasks exist
- Tasks are in stored order (no sorting)

**Example**:
```python
tasks = manager.list_tasks()
# Returns copy of internal task list
```

---

#### `update_task(task_id, title, description, due_date, priority, tags) -> Task`

Update an existing task with new values.

**Parameters**:
- `task_id: int` (required): Sequential task ID to update
- `title: Optional[str]` (optional): New title, must not be empty if provided
- `description: Optional[str]` (optional): New description
- `due_date: Optional[str]` (optional): New due date in YYYY-MM-DD format
- `priority: Optional[Priority]` (optional): New priority
- `tags: Optional[List[str]]` (optional): New list of tags

**Returns**: Updated `Task` object (new immutable instance)

**Raises**:
- `TaskNotFoundError`: If task ID does not exist
- `ValueError`: If title is empty/whitespace-only or due_date format is invalid

**Behavior**:
- Validates new title if provided (non-empty after strip)
- Validates new date format if provided
- Replaces provided fields, keeps existing values for None parameters
- Creates new immutable Task instance
- Replaces task in internal list
- Does not modify task ID

**Example**:
```python
updated_task = manager.update_task(
    task_id=1,
    priority=Priority.LOW,
    tags=["Work"]  # Replaces existing tags
)
```

---

#### `delete_task(task_id) -> None`

Delete a task from the task list and re-index remaining tasks.

**Parameters**:
- `task_id: int` (required): Sequential task ID to delete

**Returns**: None

**Raises**:
- `TaskNotFoundError`: If task ID does not exist

**Behavior**:
- Removes task from internal list
- Reindexes remaining tasks to maintain sequential IDs (1, 2, 3...)
- Decrements next ID
- All IDs after deleted task shift down by 1

**Example**:
```python
manager.delete_task(task_id=1)
# Tasks 2, 3, 4 become tasks 1, 2, 3
```

---

#### `toggle_complete(task_id) -> Task`

Toggle task completion status between pending and completed.

**Parameters**:
- `task_id: int` (required): Sequential task ID to toggle

**Returns**: Updated `Task` object with toggled completion status

**Raises**:
- `TaskNotFoundError`: If task ID does not exist

**Behavior**:
- Flips `completed` boolean (True → False, False → True)
- Creates new immutable Task instance
- Replaces task in internal list
- All other fields remain unchanged

**Example**:
```python
# task.completed == False
updated_task = manager.toggle_complete(task_id=1)
# updated_task.completed == True
```

---

### Search and Filter

#### `search_tasks(keyword) -> List[Task]`

Search tasks by keyword in title and description.

**Parameters**:
- `keyword: str` (required): Search term

**Returns**: List of matching `Task` objects

**Behavior**:
- Case-insensitive search
- Matches keyword in title OR description
- Empty or whitespace-only keyword returns all tasks (with hint)
- Returns copy of filtered list

**Example**:
```python
tasks = manager.search_tasks(keyword="meeting")
# Returns tasks with "meeting" in title or description
```

---

#### `filter_tasks(filter: TaskFilter) -> List[Task]`

Filter tasks by multiple criteria.

**Parameters**:
- `filter: TaskFilter` (required): Filter criteria object

**Returns**: List of matching `Task` objects

**Behavior**:
- Applies all filter criteria (AND logic)
- Each None value in filter excludes that criterion
- Keyword: Case-insensitive substring match
- Status: Exact boolean match (None=All)
- Priority: Exact enum match (None=All)
- Due date category:
  - TODAY: due_date == today's date
  - UPCOMING: due_date > today's date
  - OVERDUE: due_date < today's date AND completed == False
  - Tasks without due_date excluded from date filters
- Returns copy of filtered list
- Empty filter returns all tasks

**Example**:
```python
filter_obj = TaskFilter(
    status=False,  # Pending only
    priority=Priority.HIGH
)
tasks = manager.filter_tasks(filter_obj)
# Returns pending High priority tasks
```

---

### Sorting

#### `sort_tasks(tasks: List[Task], sort_order: SortOrder) -> List[Task]`

Sort tasks by specified criteria.

**Parameters**:
- `tasks: List[Task]` (required): List of tasks to sort
- `sort_order: SortOrder` (required): Sort criterion

**Returns**: New sorted list of `Task` objects

**Behavior**:
- Returns new list, does not modify input list or internal state
- SortOrder.DUE_DATE:
  - Tasks with due_date sorted ascending (earliest first)
  - Tasks without due_date placed last
  - Equal due dates maintain original relative order (stable sort)
- SortOrder.PRIORITY:
  - Order: HIGH → MEDIUM → LOW
  - Same priority maintains original relative order
- SortOrder.ALPHABETICAL:
  - Case-insensitive sort by title
  - Same title maintains original relative order
- SortOrder.DEFAULT:
  - Returns tasks in original order (no sorting)

**Example**:
```python
tasks = manager.list_tasks()
sorted_tasks = manager.sort_tasks(tasks, SortOrder.DUE_DATE)
# Returns tasks sorted by due date
```

---

## Invariants

1. **Sequential IDs**: Tasks are numbered 1, 2, 3... with no gaps
2. **No ID Duplicates**: Each ID appears exactly once
3. **Immutable Tasks**: Task objects are never modified (new instances created)
4. **List Copies**: `list_tasks()` and filter methods return copies (caller can't modify internal state)
5. **Delete Reindex**: Deleting a task reindexes all remaining tasks
6. **Sort Non-Destructive**: Sorting returns new list, doesn't affect stored order
7. **Empty Handling**: Empty task list returns empty list for all operations
8. **Validation**: All inputs are validated before processing
