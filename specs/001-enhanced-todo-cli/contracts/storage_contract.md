# Storage Service Contract

**Interface**: `JSONStorage`
**Purpose**: Persistent storage of tasks using JSON file with backup strategy

## Operations

#### `save_tasks(tasks: List[dict]) -> None`

Save tasks to JSON file with automatic backup.

**Parameters**:
- `tasks: List[dict]` (required): List of task dictionaries to save

**Returns**: None

**Raises**:
- `StorageError`: On I/O failures, permission errors, or write failures

**Behavior**:
- Creates backup file before overwriting (filename.json → filename.json.bak)
- Backup created using `shutil.copy2()` (preserves metadata)
- Writes to temporary file first (.tmp suffix)
- Renames temp file to final filename (atomic operation)
- Prevents data loss on crash during write
- Format: JSON with `{"tasks": [task_dicts]}` structure
- Indented with 2 spaces for human readability

**File Structure**:
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Task title",
      "description": "Description",
      "completed": false,
      "due_date": "2025-01-05",
      "priority": "High",
      "tags": ["Work", "Urgent"]
    }
  ]
}
```

**Example**:
```python
storage = JSONStorage("todo.json")
tasks = [
    {
        "id": 1,
        "title": "Complete documentation",
        "description": "",
        "completed": false,
        "due_date": "2025-01-05",
        "priority": "High",
        "tags": ["Work"]
    }
]
storage.save_tasks(tasks)
# Creates todo.json.bak (backup)
# Writes to todo.json
```

---

#### `load_tasks() -> List[dict]`

Load tasks from JSON file.

**Parameters**: None

**Returns**: List of task dictionaries

**Raises**:
- `StorageError`: On file corruption (invalid JSON), I/O failures, or permission errors

**Behavior**:
- Returns empty list if file doesn't exist (first run)
- Parses JSON and extracts `tasks` key
- Validates JSON structure (must be object with `tasks` array)
- Handles `json.JSONDecodeError` with descriptive error
- Handles `IOError` and `PermissionError` with descriptive error
- Returns copy of tasks list (caller modifications don't affect file)

**Example**:
```python
storage = JSONStorage("todo.json")

# First run (file doesn't exist)
tasks = storage.load_tasks()
# Returns []

# Subsequent run
tasks = storage.load_tasks()
# Returns list of task dicts from file
```

---

## File Format

### Structure

```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Task title",
      "description": "Task description",
      "completed": false,
      "due_date": "2025-01-05",
      "priority": "High",
      "tags": ["Work", "Urgent"]
    },
    {
      "id": 2,
      "title": "Another task",
      "description": "",
      "completed": true,
      "due_date": null,
      "priority": "Medium",
      "tags": []
    }
  ]
}
```

### Field Types

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `id` | integer | Yes | - | Sequential starting from 1 |
| `title` | string | Yes | - | Non-empty |
| `description` | string | No | "" | Can be empty |
| `completed` | boolean | Yes | - | false = pending, true = completed |
| `due_date` | string/null | No | null | YYYY-MM-DD format or null |
| `priority` | string | Yes | "Medium" | "High", "Medium", or "Low" |
| `tags` | array | Yes | [] | Array of strings |

### Validation Rules

1. **Root Level**: Must be JSON object with `tasks` key
2. **Tasks Key**: Must be an array (can be empty)
3. **Task Objects**: Each must be a JSON object with all required fields
4. **ID**: Must be positive integer
5. **Title**: Must be non-empty string
6. **Completed**: Must be boolean
7. **Due Date**: Must be YYYY-MM-DD string or null
8. **Priority**: Must be one of "High", "Medium", "Low"
9. **Tags**: Must be array of strings

---

## Backup Strategy

### When Backup is Created

1. Before every `save_tasks()` operation
2. If target file exists (not on first run)
3. Before overwriting, copy to `.bak` extension

### Backup File

- **Filename**: Original filename + `.bak` extension
- **Location**: Same directory as original file
- **Content**: Exact copy of original file
- **Method**: `shutil.copy2()` (preserves metadata)

### Backup Lifecycle

- Backup is always the previous version of the file
- Old backup is overwritten (single backup retained)
- If save fails, original file is preserved in backup

---

## Error Handling

### File Does Not Exist

**Scenario**: User runs application for first time

**Behavior**:
- `load_tasks()` returns empty list
- No error raised
- `save_tasks()` creates new file

**Example**:
```python
storage = JSONStorage("new_file.json")
tasks = storage.load_tasks()
# Returns [] (no file exists)
storage.save_tasks([])
# Creates new_file.json
```

---

### Invalid JSON (Corrupted File)

**Scenario**: File was manually edited or corrupted

**Raises**: `StorageError` with descriptive message

**Behavior**:
- Catches `json.JSONDecodeError`
- Provides error message: "Corrupted data file: <reason>"
- Does not crash application
- User can manually restore from `.bak` file

**Example**:
```python
storage = JSONStorage("corrupted.json")
try:
    tasks = storage.load_tasks()
except StorageError as e:
    print(f"Error: {e}")
    # Output: "Error: Corrupted data file: Expecting value: line 2 column 1 (char 1)"
```

---

### Permission Denied

**Scenario**: File is read-only or user lacks write permissions

**Raises**: `StorageError` with descriptive message

**Behavior**:
- Catches `PermissionError`
- Provides error message: "Cannot write file: Permission denied"

---

### Invalid Data Structure

**Scenario**: JSON structure is wrong format

**Raises**: `StorageError` with descriptive message

**Behavior**:
- Validates JSON structure after parsing
- Checks for `tasks` key
- Checks if `tasks` is array
- Provides error message describing the issue

**Example**:
```python
# File contains: {"invalid": "structure"}
storage = JSONStorage("bad_format.json")
try:
    tasks = storage.load_tasks()
except StorageError as e:
    print(f"Error: {e}")
    # Output: "Error: Invalid file format: missing 'tasks' key"
```

---

## Data Integrity Guarantees

1. **Atomic Writes**: File is either fully written or not at all (no partial writes)
2. **Backup Retention**: Previous version always preserved before overwriting
3. **Error Recovery**: Corrupted data doesn't crash application
4. **Format Validation**: Invalid structure is detected and reported
5. **Type Safety**: JSON types validated against expected schema

---

## Performance Characteristics

- **Load Time**: O(n) where n = number of tasks (for 100 tasks: <100ms)
- **Save Time**: O(n) where n = number of tasks (for 100 tasks: <100ms)
- **Backup Time**: O(f) where f = file size (file copy operation)
- **Memory Usage**: O(n) where n = number of tasks (in-memory list of dicts)

---

## File Locking (Not Implemented)

**Decision**: No file locking implemented

**Rationale**:
- Single-user application (per spec)
- No concurrent access expected
- File locking would add complexity without benefit

**Risk**: Very low risk of data corruption from concurrent writes

---

## Example Usage

```python
from services.storage import JSONStorage
from exceptions import StorageError

# Initialize storage
storage = JSONStorage("todo.json")

# Load tasks (first run returns empty list)
try:
    tasks = storage.load_tasks()
    print(f"Loaded {len(tasks)} tasks")
except StorageError as e:
    print(f"Failed to load: {e}")
    # Could restore from backup here

# Save tasks
try:
    tasks = [
        {
            "id": 1,
            "title": "First task",
            "description": "",
            "completed": False,
            "due_date": None,
            "priority": "Medium",
            "tags": []
        }
    ]
    storage.save_tasks(tasks)
    print("Tasks saved successfully")
except StorageError as e:
    print(f"Failed to save: {e}")
    # Original data preserved in .bak file
```

---

## StorageError Exception

**Definition**:
```python
class StorageError(Exception):
    """Exception raised when storage operations fail."""
    pass
```

**Raised When**:
- File is corrupted (invalid JSON)
- File has invalid structure
- Permission denied on read/write
- I/O error occurs

**Usage**:
```python
try:
    tasks = storage.load_tasks()
except StorageError as e:
    # Handle storage error gracefully
    print(f"Storage error: {e}")
    # Prompt user to restore from backup or recreate
```

---

## Invariants

1. **File Existence**: Load returns empty list if file doesn't exist
2. **Backup Before Write**: Backup created before every overwrite
3. **Atomic Writes**: Temporary file + rename (no partial writes)
4. **Type Consistency**: Loaded data matches expected schema
5. **Copy Return**: Methods return copies (caller modifications don't affect internal state)
