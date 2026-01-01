# Filter and Sort Behavior Specification

**Purpose**: Define exact behavior for filtering and sorting tasks

## Filter Behavior

### Filter Application Rules

1. **AND Logic**: All filter criteria must match for task to be included
2. **None Exclusion**: Any None value in filter excludes that criterion from evaluation
3. **Order Independent**: Filter results are the same regardless of criterion evaluation order

### Keyword Search

**Filter Field**: `keyword: Optional[str]`

**Behavior**:
- Case-insensitive substring matching
- Searches both `title` and `description` fields
- Empty string or None → no filtering (return all tasks)
- Whitespace-only string → no filtering (treated as empty)

**Matching Rules**:
- Keyword "meeting" matches:
  - Title: "Attend team meeting" → YES
  - Title: "Meeting notes review" → YES
  - Description: "Prepare for meeting" → YES
  - Title: "Meat" → NO (partial "meet" but not "meeting")

**Implementation**:
```python
keyword_lower = keyword.lower()
title_match = keyword_lower in task.title.lower()
desc_match = keyword_lower in task.description.lower()
if not (title_match or desc_match):
    continue  # Skip this task
```

**Examples**:
```python
# Return tasks with "doc" in title or description
filter = TaskFilter(keyword="doc")

# Matches: "Documentation", "docs", "DOC" (case-insensitive)
# Doesn't match: "Project"
```

---

### Status Filter

**Filter Field**: `status: Optional[bool]`

**Behavior**:
- `None` → Return all tasks (both completed and pending)
- `True` → Return only completed tasks
- `False` → Return only pending tasks

**Matching Rules**:
- Exact boolean comparison with `task.completed`

**Examples**:
```python
# Return all tasks
filter_all = TaskFilter(status=None)

# Return only completed tasks
filter_completed = TaskFilter(status=True)

# Return only pending tasks
filter_pending = TaskFilter(status=False)
```

---

### Priority Filter

**Filter Field**: `priority: Optional[Priority]`

**Behavior**:
- `None` → Return all tasks (all priority levels)
- `Priority.HIGH` → Return only High priority tasks
- `Priority.MEDIUM` → Return only Medium priority tasks
- `Priority.LOW` → Return only Low priority tasks

**Matching Rules**:
- Exact enum comparison with `task.priority`

**Examples**:
```python
# Return all priorities
filter_all = TaskFilter(priority=None)

# Return only High priority tasks
filter_high = TaskFilter(priority=Priority.HIGH)

# Return only Medium priority tasks
filter_medium = TaskFilter(priority=Priority.MEDIUM)
```

---

### Due Date Filter

**Filter Field**: `due_date_category: Optional[DueDateCategory]`

**Behavior**:
- `None` → Return all tasks (including those without due date)
- `DueDateCategory.TODAY` → Tasks with due_date == today's date
- `DueDateCategory.UPCOMING` → Tasks with due_date > today's date
- `DueDateCategory.OVERDUE` → Tasks with due_date < today's date AND completed == False

**Matching Rules**:
- Tasks **without** due date are excluded from all date filters (TODAY, UPCOMING, OVERDUE)
- Date comparison uses `datetime.date.today()`
- OVERDUE filter excludes completed tasks (even if due date is past)

**Date Comparison**:
```python
today = datetime.date.today()
task_due_date = datetime.strptime(task.due_date, "%Y-%m-%d").date()

# TODAY: task_due_date == today
# UPCOMING: task_due_date > today
# OVERDUE: task_due_date < today AND task.completed == False
```

**Examples**:
```python
# Return all tasks (including no due date)
filter_all = TaskFilter(due_date_category=None)

# Return tasks due today (today is 2025-01-05)
filter_today = TaskFilter(due_date_category=DueDateCategory.TODAY)
# Matches: Task with due_date="2025-01-05"
# Doesn't match: Task with due_date="2025-01-06", or None

# Return upcoming tasks (today is 2025-01-05)
filter_upcoming = TaskFilter(due_date_category=DueDateCategory.UPCOMING)
# Matches: Task with due_date="2025-01-06", "2025-01-10"
# Doesn't match: Task with due_date="2025-01-05", "2025-01-04", or None

# Return overdue tasks (today is 2025-01-05)
filter_overdue = TaskFilter(due_date_category=DueDateCategory.OVERDUE)
# Matches: Pending task with due_date="2025-01-04"
# Doesn't match: Completed task with due_date="2025-01-04"
# Doesn't match: Task with due_date=None
```

---

### Combined Filters

**Behavior**: All filters apply with AND logic

**Example**:
```python
# Filter: Pending AND High priority AND keyword "urgent"
filter = TaskFilter(
    keyword="urgent",
    status=False,  # Pending
    priority=Priority.HIGH,
    due_date_category=None
)

# Task included only if:
# - "urgent" in title or description (case-insensitive)
# - completed == False
# - priority == Priority.HIGH
# - Due date doesn't matter (None filter)
```

**Truth Table** (Keyword="urgent", Status=Pending, Priority=High, Due=None):

| Task | Keyword | Status | Priority | Due Date | Included? |
|------|----------|---------|-----------|-----------|-----------|
| A: Urgent meeting, Pending, High | YES | YES | YES | N/A | ✅ YES |
| B: Urgent task, Completed, High | YES | NO | YES | N/A | ❌ NO |
| C: Urgent fix, Pending, Medium | YES | YES | NO | N/A | ❌ NO |
| D: Regular meeting, Pending, High | NO | YES | YES | N/A | ❌ NO |

---

## Sort Behavior

### Sort Rules

1. **Stable Sort**: Tasks with equal sort keys maintain original relative order
2. **Non-Destructive**: Sorting returns new list, doesn't modify stored order
3. **None Handling**: Tasks without sort key placed last (except DEFAULT sort)

### SortOrder.DUE_DATE

**Behavior**:
- Sorts tasks by `due_date` field in ascending order (earliest first)
- Tasks **with** due date sorted chronologically
- Tasks **without** due date placed last
- Tasks with same due date maintain original relative order

**Sort Key**:
```python
def due_date_sort_key(task: Task):
    # Tasks with due date: use date
    # Tasks without due date: use max date (placed last)
    if task.due_date:
        return datetime.strptime(task.due_date, "%Y-%m-%d").date()
    else:
        return datetime.date.max
```

**Examples**:
```python
tasks = [
    Task(id=1, title="A", due_date="2025-01-10"),
    Task(id=2, title="B", due_date=None),
    Task(id=3, title="C", due_date="2025-01-05"),
    Task(id=4, title="D", due_date="2025-01-07")
]

sorted = sort_tasks(tasks, SortOrder.DUE_DATE)
# Result order: [3, 4, 1, 2]
# 3: 2025-01-05 (earliest)
# 4: 2025-01-07
# 1: 2025-01-10
# 2: None (placed last)
```

---

### SortOrder.PRIORITY

**Behavior**:
- Sorts by `priority` field in order: HIGH → MEDIUM → LOW
- Uses enum member order for sorting
- Tasks with same priority maintain original relative order

**Sort Key**:
```python
def priority_sort_key(task: Task):
    # Use enum member order: HIGH=0, MEDIUM=1, LOW=2
    return task.priority.value  # Or enum member index
```

**Enum Order**:
```python
class Priority(Enum):
    HIGH = "High"     # Order: 0
    MEDIUM = "Medium"  # Order: 1
    LOW = "Low"       # Order: 2
```

**Examples**:
```python
tasks = [
    Task(id=1, title="A", priority=Priority.MEDIUM),
    Task(id=2, title="B", priority=Priority.HIGH),
    Task(id=3, title="C", priority=Priority.LOW),
    Task(id=4, title="D", priority=Priority.HIGH)
]

sorted = sort_tasks(tasks, SortOrder.PRIORITY)
# Result order: [2, 4, 1, 3]
# 2: HIGH
# 4: HIGH (maintains original order relative to 2)
# 1: MEDIUM
# 3: LOW
```

---

### SortOrder.ALPHABETICAL

**Behavior**:
- Sorts by `title` field case-insensitively
- Uses string comparison (lexicographic order)
- Tasks with same title maintain original relative order

**Sort Key**:
```python
def alphabetical_sort_key(task: Task):
    return task.title.lower()
```

**Examples**:
```python
tasks = [
    Task(id=1, title="Zebra"),
    Task(id=2, title="Apple"),
    Task(id=3, title="banana"),
    Task(id=4, title="Apple")  # Duplicate title
]

sorted = sort_tasks(tasks, SortOrder.ALPHABETICAL)
# Result order: [2, 4, 3, 1]
# 2: "Apple" (lowercase: "apple")
# 4: "Apple" (lowercase: "apple", maintains order after 2)
# 3: "banana"
# 1: "Zebra"
```

---

### SortOrder.DEFAULT

**Behavior**:
- Returns tasks in stored order (no sorting)
- Preserves internal task list order
- Used to exit sort view and return to default display

**Examples**:
```python
tasks = [Task(id=3), Task(id=1), Task(id=2)]

sorted = sort_tasks(tasks, SortOrder.DEFAULT)
# Result order: [3, 1, 2] (same as input)
```

---

## Sort+Filter Interaction

**Workflow**:
1. Filter tasks first (apply all filter criteria)
2. Sort filtered results (apply sort order)
3. Display sorted, filtered tasks

**Important**: Sorting does not modify stored order. Only displayed order changes.

**Example**:
```python
# All tasks (stored order: 1, 2, 3, 4)
all_tasks = [
    Task(id=1, title="A", priority=Priority.LOW, due_date="2025-01-10"),
    Task(id=2, title="B", priority=Priority.HIGH, due_date="2025-01-05"),
    Task(id=3, title="C", priority=Priority.MEDIUM, due_date=None),
    Task(id=4, title="D", priority=Priority.HIGH, due_date="2025-01-07")
]

# Filter: High priority only
filtered = filter_tasks(all_tasks, TaskFilter(priority=Priority.HIGH))
# Result: [2, 4] (preserves stored order)

# Sort: By due date
sorted = sort_tasks(filtered, SortOrder.DUE_DATE)
# Result: [2, 4]
# 2: 2025-01-05 (earlier)
# 4: 2025-01-07 (later)

# Original stored order remains: [1, 2, 3, 4]
```

---

## Edge Cases

### Empty Filter

```python
filter = TaskFilter()  # All fields None
tasks = filter_tasks(all_tasks, filter)
# Result: All tasks returned (no filtering)
```

---

### No Matching Tasks

```python
filter = TaskFilter(keyword="nonexistent")
tasks = filter_tasks(all_tasks, filter)
# Result: Empty list []
# UI should show: "No tasks match the current filters"
```

---

### All Tasks Filtered Out

```python
# Task 1: Completed, High priority
# Task 2: Pending, Medium priority

# Filter for Pending High priority
filter = TaskFilter(status=False, priority=Priority.HIGH)
tasks = filter_tasks(all_tasks, filter)
# Result: Empty list []
```

---

### Single Task in List

```python
tasks = [Task(id=1, title="Only task")]

sorted = sort_tasks(tasks, SortOrder.PRIORITY)
# Result: [1] (unchanged, single element)
```

---

### All Tasks Have Same Sort Key

```python
tasks = [
    Task(id=1, title="A", priority=Priority.HIGH),
    Task(id=2, title="B", priority=Priority.HIGH),
    Task(id=3, title="C", priority=Priority.HIGH)
]

sorted = sort_tasks(tasks, SortOrder.PRIORITY)
# Result: [1, 2, 3] (maintains original relative order)
```

---

## Performance Characteristics

### Filter Performance

- **Keyword Search**: O(n * (len(title) + len(description))) where n = number of tasks
- **Status Filter**: O(n) - simple boolean comparison
- **Priority Filter**: O(n) - simple enum comparison
- **Due Date Filter**: O(n * k) where k = date parsing cost
- **Combined Filter**: O(n * m) where m = number of active filter criteria

**Expected Performance**:
- 100 tasks: <1ms for any single filter
- 100 tasks: <5ms for combined filters
- Scales linearly with task count

### Sort Performance

- **All Sort Types**: O(n log n) using Python's Timsort
- **Stable**: Maintains relative order for equal keys

**Expected Performance**:
- 100 tasks: <1ms for any sort type
- 1000 tasks: <10ms for any sort type
- Scales as O(n log n)

### Combined Performance

- **Filter + Sort**: O(n * m + n log n) where m = filter criteria count
- **100 Tasks**: <10ms total (filter + sort)
- Well within performance requirements (under 3 seconds for search/filter)

---

## Implementation Validation

### Test Cases for Filter

1. **Keyword Filter**:
   - Match in title only
   - Match in description only
   - Match in both title and description
   - No match (keyword not present)
   - Empty keyword (return all)
   - Case-insensitive matching
   - Partial word matching

2. **Status Filter**:
   - Filter completed only
   - Filter pending only
   - No filter (return all)
   - All completed tasks
   - All pending tasks
   - Mixed completion status

3. **Priority Filter**:
   - Filter High priority only
   - Filter Medium priority only
   - Filter Low priority only
   - No filter (return all)
   - All same priority

4. **Due Date Filter**:
   - Filter today's tasks
   - Filter upcoming tasks
   - Filter overdue tasks
   - No filter (return all)
   - Tasks without due date excluded

5. **Combined Filters**:
   - Keyword + Status
   - Keyword + Priority
   - Keyword + Due Date
   - Status + Priority + Due Date
   - All filters combined
   - No matches (empty result)

### Test Cases for Sort

1. **Due Date Sort**:
   - Different dates
   - Same dates (stable sort)
   - Tasks without due date (placed last)
   - All tasks without due date
   - Single task

2. **Priority Sort**:
   - Different priorities
   - Same priority (stable sort)
   - All same priority
   - Single task

3. **Alphabetical Sort**:
   - Different titles
   - Same title (stable sort)
   - Case differences (case-insensitive)
   - Special characters
   - Single task

4. **Default Sort**:
   - Returns input order unchanged
   - Multiple tasks
   - Single task

### Test Cases for Filter+Sort Interaction

1. **Filter then Sort**:
   - Filter by status, sort by priority
   - Filter by keyword, sort by due date
   - Filter by priority, sort alphabetically

2. **Empty Results**:
   - Filter returns empty list
   - Sort of empty list returns empty list

3. **Stability**:
   - Sort stable across multiple calls
   - Filter order doesn't affect final sorted result

---

## Invariants

1. **Filter Returns Copy**: Returned list is independent of source
2. **Sort Returns Copy**: Returned list is independent of source
3. **No Side Effects**: Filter and sort don't modify input lists
4. **Stable Sort**: Equal keys maintain original relative order
5. **Filter AND Logic**: All criteria must match
6. **None Exclusion**: None values exclude that criterion
7. **Empty Filter**: Returns all tasks
8. **Empty Sort**: Returns tasks in input order
