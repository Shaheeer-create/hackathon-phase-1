# Research Findings: Enhanced CLI Todo Application

**Date**: 2025-12-31
**Objective**: Investigate CLI patterns, JSON persistence, and search/filtering techniques

## 1. CLI Table Formatting

### Question: How to format tables with variable-width content in standard terminals?

**Findings**:
- Python's `str.format()` with alignment specifiers: `"{:<10} {:>5}".format(left, right)`
- Column widths calculated dynamically based on content
- Truncation needed for long text: `text[:max_width] + "..."`

**Best Practices**:
- Right-align numeric columns (ID)
- Left-align text columns (Title, Description, Tags)
- Add padding for readability (2 spaces minimum between columns)
- Handle terminal width (80 columns minimum per spec)

**Code Example**:
```python
def format_table(tasks: List[Task]) -> List[str]:
    """Format tasks as CLI table."""
    # Calculate column widths based on content
    max_title = max((len(task.title) for task in tasks), default=10)
    max_tags = max((len(", ".join(task.tags)) for task in tasks), default=4)

    # Header
    header = f"{'ID':<4} | {'Status':<7} | {'Priority':<9} | {'Tags':<{max_tags}} | {'Title':<{max_title}} | {'Due':<10}"
    separator = "-" * len(header)

    rows = [header, separator]

    for task in tasks:
        status = "[✓]" if task.completed else "[ ]"
        tags_str = ", ".join(task.tags)
        due_str = task.due_date or "None"
        row = f"{task.id:<4} | {status:<7} | {task.priority.value:<9} | {tags_str:<{max_tags}} | {task.title:<{max_title}} | {due_str:<10}"
        rows.append(row)

    return rows
```

**Decision**: Use format strings with dynamic width calculation, truncate at 25 chars for title, 20 for tags

---

## 2. JSON Persistence Patterns

### Question: Best practices for reading/writing JSON files safely?

**Findings**:
- Use `json.dump()` with `indent=2` for readable files
- Use `json.load()` for reading (raises `json.JSONDecodeError` on corruption)
- Atomic writes: Write to temp file, then rename (prevents partial writes on crash)
- Backup strategy: Copy existing to `.bak` before overwriting

**Best Practices**:
- Always validate file existence before loading
- Handle `JSONDecodeError` with user-friendly message
- Use `shutil.copy2()` for backup (preserves metadata)
- Catch `IOError` and `PermissionError` for file operations

**Code Example**:
```python
import json
import os
import shutil

class JSONStorage:
    def save(self, tasks: List[dict], filepath: str):
        """Save tasks to JSON file with backup."""
        # Create backup if file exists
        if os.path.exists(filepath):
            shutil.copy2(filepath, filepath + ".bak")

        # Write to temp file first (atomic)
        temp_path = filepath + ".tmp"
        with open(temp_path, "w") as f:
            json.dump({"tasks": tasks}, f, indent=2)

        # Rename to final (atomic operation)
        os.replace(temp_path, filepath)

    def load(self, filepath: str) -> List[dict]:
        """Load tasks from JSON file."""
        if not os.path.exists(filepath):
            return []

        try:
            with open(filepath, "r") as f:
                data = json.load(f)
                return data.get("tasks", [])
        except json.JSONDecodeError as e:
            raise StorageError(f"Corrupted data file: {e}")
        except (IOError, PermissionError) as e:
            raise StorageError(f"Cannot read file: {e}")
```

**Decision**: JSON with atomic writes + backup strategy, error handling for corruption and permissions

---

## 3. Search and Filtering Algorithms

### Question: Efficient in-memory filtering for 100+ tasks?

**Findings**:
- For 100 tasks, O(n) filtering is negligible (<1ms)
- List comprehension is most Pythonic and readable
- Case-insensitive search: `keyword.lower() in text.lower()`
- Date comparison: Parse to `datetime.date()` objects for comparison

**Best Practices**:
- Filter sequentially applying each criterion
- Short-circuit: If any filter criterion fails, skip task
- Date comparison: Use `datetime.date.today()` for "today"
- Empty keyword = no filtering (return all tasks)

**Code Example**:
```python
from datetime import date

def filter_tasks(tasks: List[Task], keyword: str, status: bool, priority: Priority, due_cat: str) -> List[Task]:
    """Filter tasks by multiple criteria."""
    today = date.today()

    filtered = []
    for task in tasks:
        # Keyword search
        if keyword:
            keyword_lower = keyword.lower()
            title_match = keyword_lower in task.title.lower()
            desc_match = keyword_lower in task.description.lower()
            if not (title_match or desc_match):
                continue

        # Status filter
        if status is not None and task.completed != status:
            continue

        # Priority filter
        if priority is not None and task.priority != priority:
            continue

        # Due date filter
        if due_cat and task.due_date:
            due_date = datetime.strptime(task.due_date, "%Y-%m-%d").date()

            if due_cat == "today" and due_date != today:
                continue
            if due_cat == "upcoming" and due_date <= today:
                continue
            if due_cat == "overdue" and (due_date >= today or task.completed):
                continue
        elif due_cat:  # Filter category specified but task has no due date
            continue

        filtered.append(task)

    return filtered
```

**Decision**: O(n) sequential filtering, case-insensitive search, date objects for comparison

---

## 4. Priority Representation

### Question: Enum vs string constants for priority levels?

**Findings**:
- **Enum Advantages**:
  - Type safety (prevents invalid values)
  - Natural ordering for sorting (`enum members maintain definition order`)
  - Self-documenting code
  - IDE autocomplete support
  - Can convert to string via `.value`

- **String Constants Advantages**:
  - Simpler implementation
  - Direct comparison

**Sorting Efficiency**:
- Enum sorting: Uses enum member order (faster due to identity comparison)
- String sorting: Lexicographic (alphabetical), but "High" > "Medium" > "Low" works
- Both are O(n log n), negligible difference for 100 tasks

**Code Comparison**:
```python
# Using Enum (RECOMMENDED)
from enum import Enum

class Priority(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

# Sort by priority (uses enum order)
sorted(tasks, key=lambda t: t.priority)

# Using String Constants (NOT RECOMMENDED)
HIGH = "High"
MEDIUM = "Medium"
LOW = "Low"

# Sort by priority (needs mapping)
priority_order = {"High": 0, "Medium": 1, "Low": 2}
sorted(tasks, key=lambda t: priority_order[t.priority])
```

**Decision**: Use `Priority` enum for type safety, natural ordering, and better code maintainability

---

## 5. Tag Management

### Question: Case-sensitive vs case-insensitive tags?

**Findings**:
- **Case-Sensitive**:
  - "Work" and "work" are different tags
  - Simpler implementation (direct string comparison)
  - Per spec assumption: "Tags are case-sensitive for simplicity"

- **Case-Insensitive**:
  - "Work" and "work" are the same tag
  - Requires normalization (lowercase) for storage
  - More user-friendly (avoids duplicates from capitalization)

**Deduplication**:
- Check if tag already exists before adding
- Use `if tag not in task.tags:` (case-sensitive)

**Code Example**:
```python
def add_tags(task: Task, tags: List[str]) -> Task:
    """Add tags to task with deduplication."""
    existing_tags = set(task.tags)
    unique_tags = [tag for tag in tags if tag not in existing_tags]

    # Create updated task with new tags
    return Task(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        due_date=task.due_date,
        priority=task.priority,
        tags=task.tags + unique_tags
    )
```

**Decision**: Case-sensitive (per spec assumption), deduplication on add

---

## 6. Date Validation

### Question: How to validate YYYY-MM-DD format?

**Findings**:
- Regex pattern: `r"^\d{4}-\d{2}-\d{2}$"` validates format only
- For semantic validation (e.g., 2025-13-45), use `datetime.strptime()`
- `strptime()` raises `ValueError` for invalid dates

**Code Example**:
```python
import re
from datetime import datetime

def is_valid_date(date_str: str) -> bool:
    """Validate YYYY-MM-DD format."""
    # Check format
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        return False

    # Check semantic validity
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
```

**Decision**: Regex + `strptime()` for comprehensive validation

---

## Summary of Recommendations

| Research Question | Recommendation | Rationale |
|------------------|----------------|------------|
| CLI Table Formatting | Dynamic width calculation with truncation | Adapts to content, fits terminal |
| JSON Persistence | Atomic writes + backup | Safe crash recovery |
| Search/Filtering | O(n) sequential, case-insensitive | Sufficient for 100+ tasks |
| Priority Representation | Enum | Type safety, natural ordering |
| Tag Management | Case-sensitive, deduplicate on add | Per spec assumption |
| Date Validation | Regex + strptime | Format + semantic validation |

---

**Document Status**: Complete | Ready for: Phase 1 Design
