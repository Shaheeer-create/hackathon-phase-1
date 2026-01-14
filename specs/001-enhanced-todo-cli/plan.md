# Implementation Plan: Enhanced CLI Todo Application

**Branch**: `001-enhanced-todo-cli` | **Date**: 2025-12-31 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-enhanced-todo-cli/spec.md`

**Note**: This template is filled in by `/sp.plan` command. See `.specify/templates/commands/plan.md` for execution workflow.

## Summary

Build an enhanced CLI-based Todo application with task management, priority/tag organization, search/filtering, and sorting capabilities. The implementation extends the existing basic Todo CLI with new features while maintaining the current MVC architecture and test-first approach. All functionality uses Python standard library only (no external dependencies) with JSON-based local persistence for data storage across sessions.

## Technical Context

**Language/Version**: Python 3.12+ (per constitution requirement)
**Primary Dependencies**: Standard library only (`json` for persistence, `dataclasses` for models, `unittest` for testing)
**Storage**: Local JSON file (todo.json) for persistent task storage
**Testing**: `unittest` framework with 100% code coverage requirement
**Target Platform**: Cross-platform CLI (Windows, Linux, macOS)
**Project Type**: Single project (standalone CLI application)
**Performance Goals**: Handle 100+ tasks with under 1 second display, search/filter in under 3 seconds
**Constraints**: No external dependencies, immutable models, in-memory operations with JSON persistence, 5-7 implementation tasks
**Scale/Scope**: ~500-700 LOC across 4 modules (models, services, cli, storage)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence/Notes |
|-----------|---------|----------------|
| Test-First Accuracy | ✅ PASS | Plan specifies test-first development for all features |
| Clear CLI | ✅ PASS | Menu-based CLI with intuitive navigation and help text |
| Reproducible | ✅ PASS | Spec-driven with 100% test coverage requirement |
| Tech Standards (Python 3.12+) | ✅ PASS | Using Python 3.12+ with standard library only |
| MVC Architecture | ✅ PASS | Existing code follows MVC, extending the same pattern |
| Code Style (PEP 8, Type Hints) | ✅ PASS | Type hints on all signatures, PEP 8 compliance |
| AI-Native Workflow | ✅ PASS | Following spec → plan → tasks → implement → validate sequence |
| Test Coverage | ✅ PASS | 100% coverage requirement with unittest framework |
| Immutability | ✅ PASS | Task model uses frozen dataclass, explicit state changes |
| Input Validation | ✅ PASS | All user inputs validated with clean error messages |

**Gate Result**: ✅ PASS - All constitution principles satisfied. Proceed to implementation.

## Project Structure

### Documentation (this feature)

```text
specs/001-enhanced-todo-cli/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── task_service_contract.md
│   ├── storage_contract.md
│   └── filter_sort_contract.md
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── models/
│   ├── __init__.py
│   ├── task.py          # Enhanced Task model with priority and tags
│   └── enums.py         # New: Priority enum, Filter/Sort enums
├── services/
│   ├── __init__.py
│   ├── task_manager.py   # Enhanced with search, filter, sort
│   └── storage.py       # New: JSON persistence layer
├── cli/
│   ├── __init__.py
│   ├── main.py           # Enhanced menu with new features
│   └── display.py       # New: Table formatting and display utilities
├── utils/
│   ├── __init__.py       # New: Utility package
│   └── validators.py    # New: Date validation, priority validation
└── exceptions/
    ├── __init__.py
    └── errors.py         # New: Storage errors, validation errors

tests/
├── contract/
│   ├── __init__.py
│   ├── test_task_operations.py
│   ├── test_storage_contract.py
│   └── test_filter_sort_contract.py
├── integration/
│   ├── __init__.py
│   └── test_cli_workflows.py
└── unit/
    ├── __init__.py
    ├── test_task_model.py
    ├── test_task_manager.py
    ├── test_storage.py
    ├── test_validators.py
    └── test_display.py
```

**Structure Decision**: Single project structure extending existing MVC pattern. New files added: `src/models/enums.py`, `src/services/storage.py`, `src/cli/display.py`, `src/utils/` package, and corresponding tests. This maintains the existing architecture while cleanly separating concerns.

## Complexity Tracking

> No constitution violations requiring justification. All design choices align with established principles.

## Phase 0: Research

**Objective**: Investigate CLI patterns, JSON persistence, and search/filtering techniques to inform implementation decisions.

### Research Questions

1. **CLI Table Formatting**:
   - How to format tables with variable-width content in standard terminals?
   - Best practices for column alignment and truncation?
   - ASCII/Unicode character compatibility?

2. **JSON Persistence Patterns**:
   - Best practices for reading/writing JSON files safely?
   - How to handle file corruption or invalid JSON?
   - Backup strategies for data integrity?

3. **Search and Filtering Algorithms**:
   - Efficient in-memory filtering for 100+ tasks?
   - Case-insensitive search implementation?
   - Date comparison for Today/Upcoming/Overdue filtering?

4. **Priority Representation**:
   - Enum vs string constants for priority levels?
   - Sorting efficiency comparison?

5. **Tag Management**:
   - Case-sensitive vs case-insensitive tags?
   - Tag deduplication strategies?

### Research Outputs

1. `specs/001-enhanced-todo-cli/research.md` - Summary of findings with code examples
2. Recommendations for each research question
3. Technology selection rationale

---

## Phase 1: Design

**Objective**: Design data models, service interfaces, and code organization.

### 1.1 Data Model Design

**Output**: `specs/001-enhanced-todo-cli/data-model.md`

#### Task Entity

```python
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum

class Priority(Enum):
    """Task priority levels for sorting and filtering."""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

@dataclass(frozen=True)
class Task:
    """Immutable todo item with enhanced attributes.

    Attributes:
        id: Unique sequential identifier (1, 2, 3...)
        title: Task title/name (required, must not be empty)
        description: Task description (optional, default empty)
        completed: Task completion status (False=pending, True=completed)
        due_date: Due date in YYYY-MM-DD format (optional)
        priority: Task priority (High/Medium/Low, default Medium)
        tags: List of categorization tags (default empty list)
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False
    due_date: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    tags: List[str] = field(default_factory=list)
```

**Key Decisions**:
- **Priority as Enum**: Type-safe, sortable, prevents invalid values
- **Tags as List[str]**: Simple, flexible, case-sensitive (per spec assumption)
- **Frozen dataclass**: Enforces immutability (constitution requirement)

#### Filter Criteria

```python
@dataclass(frozen=True)
class TaskFilter:
    """Criteria for filtering task display."""
    keyword: Optional[str] = None          # Search keyword
    status: Optional[bool] = None            # None=All, True=Completed, False=Pending
    priority: Optional[Priority] = None        # None=All, or specific priority
    due_date_category: Optional[str] = None   # None=All, "today", "upcoming", "overdue"
```

#### Sort Criteria

```python
class SortOrder(Enum):
    """Options for sorting task display."""
    DUE_DATE = "due_date"           # Chronological
    PRIORITY = "priority"             # High → Medium → Low
    ALPHABETICAL = "alphabetical"     # By title
    DEFAULT = "default"               # Stored order
```

### 1.2 Service Contracts

**Output Directory**: `specs/001-enhanced-todo-cli/contracts/`

#### Task Service Contract

**File**: `contracts/task_service_contract.md`

```
Interface: TaskManager

Operations:
- add_task(title, description, due_date, priority, tags) -> Task
- get_task(task_id) -> Task
- list_tasks() -> List[Task]
- update_task(task_id, title, description, due_date, priority, tags) -> Task
- delete_task(task_id) -> None
- toggle_complete(task_id) -> Task
- search_tasks(keyword) -> List[Task]
- filter_tasks(filter: TaskFilter) -> List[Task]
- sort_tasks(tasks: List[Task], sort_order: SortOrder) -> List[Task]

Invariants:
- Task IDs are sequential starting from 1
- Deleting a task reindexes remaining tasks
- Sorting operations do not modify stored order
- Empty task list returns empty list for all operations
```

#### Storage Service Contract

**File**: `contracts/storage_contract.md`

```
Interface: JSONStorage

Operations:
- save_tasks(tasks: List[Task]) -> None
- load_tasks() -> List[Task]

Behavior:
- Creates backup file before overwriting (todo.json.bak)
- Raises StorageError on I/O failures
- Returns empty list if file doesn't exist (first run)
- Validates JSON structure on load

File Format:
{
  "tasks": [
    {
      "id": 1,
      "title": "...",
      "description": "...",
      "completed": false,
      "due_date": "2025-01-01",
      "priority": "High",
      "tags": ["Work", "Urgent"]
    }
  ]
}
```

#### Filter/Sort Contract

**File**: `contracts/filter_sort_contract.md`

```
Filter Behavior:

Keyword Search:
- Case-insensitive substring matching
- Searches both title and description fields
- Empty keyword returns all tasks (no filtering)

Status Filter:
- None: Return all tasks
- True: Return only completed tasks
- False: Return only pending tasks

Priority Filter:
- None: Return all tasks
- Priority.HIGH: Return only High priority tasks
- Priority.MEDIUM: Return only Medium priority tasks
- Priority.LOW: Return only Low priority tasks

Due Date Filter:
- None: Return all tasks
- "today": Tasks with due_date == today's date (YYYY-MM-DD)
- "upcoming": Tasks with due_date > today's date
- "overdue": Tasks with due_date < today's date and completed == False
- Tasks with no due_date are excluded from all date filters

Sort Behavior:

SortOrder.DUE_DATE:
- Tasks with due_date sorted ascending (earliest first)
- Tasks without due_date placed last
- Equal due dates maintain original relative order

SortOrder.PRIORITY:
- Order: High → Medium → Low
- Same priority maintains original relative order

SortOrder.ALPHABETICAL:
- Case-insensitive sort by title
- Same title maintains original relative order

SortOrder.DEFAULT:
- Returns tasks in stored order (no sorting)
```

### 1.3 Quickstart Guide

**Output**: `specs/001-enhanced-todo-cli/quickstart.md`

```
# Quickstart: Enhanced Todo CLI

## Installation

```bash
# Clone repository
git clone <repo-url>
cd phase-1

# Run application
python -m src.cli.main
```

## Basic Usage

```
==================================================
Todo Application - Enhanced Task Management
==================================================

Main Menu:
1. Add Task
2. List Tasks
3. Complete Task
4. Delete Task
5. Update Task
6. Search Tasks         [NEW]
7. Filter Tasks         [NEW]
8. Sort Tasks           [NEW]
9. Exit
==================================================

Enter choice (1-9): 1

----------------------------------------
Add Task
----------------------------------------
Task title: Complete project documentation
Description (optional): Write detailed docs for each feature
Due date (YYYY-MM-DD, optional): 2025-01-05
Priority (High/Medium/Low) [Medium]: High
Tags (comma-separated, optional): Work, Documentation

Task added: [1] Complete project documentation
  Description: Write detailed docs for each feature
  Due: 2025-01-05
  Priority: High
  Tags: Work, Documentation
```

## Search and Filter

```
Main Menu:
1. Add Task
...
6. Search Tasks         [NEW]

Enter choice (1-9): 6

----------------------------------------
Search Tasks
----------------------------------------
Enter keyword: documentation

Found 2 tasks:

ID  | Status | Priority | Tags       | Title    | Due Date
----+---------+-----------+------------+----------+------------
1   | [ ]     | High      | Work, Doc  | Complete | 2025-01-05
5   | [✓]     | Medium    | Home       | Review    | 2025-01-02
```

## Filtering by Priority and Status

```
Main Menu:
...
7. Filter Tasks         [NEW]

Enter choice (1-9): 7

----------------------------------------
Filter Tasks
----------------------------------------
Status filter (All/Completed/Pending) [All]: Pending
Priority filter (All/High/Medium/Low) [All]: High
Due date filter (All/Today/Upcoming/Overdue) [All]: Upcoming

Filtered tasks (3 total):

ID  | Status | Priority | Tags       | Title       | Due Date
----+---------+-----------+------------+-------------+------------
1   | [ ]     | High      | Work       | Complete    | 2025-01-05
3   | [ ]     | High      | Urgent     | Fix bug     | 2025-01-07
```

## Sorting Tasks

```
Main Menu:
...
8. Sort Tasks           [NEW]

Enter choice (1-9): 8

----------------------------------------
Sort Tasks
----------------------------------------
Sort by (1: Due Date, 2: Priority, 3: Alphabetical, 4: Default) [1]: 2

Tasks (5 total), sorted by Priority:

ID  | Status | Priority | Tags       | Title       | Due Date
----+---------+-----------+------------+-------------+------------
1   | [ ]     | High      | Work       | Complete    | 2025-01-05
3   | [ ]     | High      | Urgent     | Fix bug     | 2025-01-07
2   | [✓]     | Medium    | Home       | Buy groceries| 2025-01-03
```

## Data Persistence

Tasks are automatically saved to `todo.json` after each operation.
A backup file `todo.json.bak` is created before overwriting.

First run: `todo.json` is created automatically.
```

---

## Phase 2: Implementation

**Objective**: Implement the feature incrementally with test-first development.

### Implementation Tasks

Output: `specs/001-enhanced-todo-cli/tasks.md` (created by `/sp.tasks`)

### Task Organization

1. **Task 1**: Enhance Task Model with Priority and Tags
   - Add Priority enum
   - Update Task dataclass with priority and tags fields
   - Write unit tests
   - Update existing tests

2. **Task 2**: Implement JSON Storage Layer
   - Create Storage service
   - Implement save/load operations with backup
   - Write unit and integration tests
   - Handle file errors and corruption

3. **Task 3**: Add Search and Filter Logic to TaskManager
   - Add TaskFilter dataclass
   - Implement search_tasks() method
   - Implement filter_tasks() method
   - Write unit tests for all filter combinations

4. **Task 4**: Add Sort Logic to TaskManager
   - Add SortOrder enum
   - Implement sort_tasks() method
   - Implement all sort criteria
   - Write unit tests for each sort type

5. **Task 5**: Integrate Storage with TaskManager
   - Modify TaskManager to use Storage
   - Auto-save after each mutation
   - Auto-load on initialization
   - Write integration tests

6. **Task 6**: Enhanced CLI Display
   - Create display utilities (table formatting)
   - Add Search menu option
   - Add Filter menu option
   - Add Sort menu option
   - Update task list display to show priority and tags
   - Write integration tests for CLI workflows

### Development Approach

**Incremental Feature Delivery**:
- Each task is independently testable
- Tasks can be committed individually
- Features build on each other (foundation first)

**Test-First Discipline**:
- Write failing test first
- Implement minimal code to pass test
- Refactor if needed
- Move to next test

**Example Implementation Flow** (Task 1 - Task Model):

```python
# 1. Write failing test (test_task_model.py)
def test_task_with_priority_and_tags():
    task = Task(
        id=1,
        title="Test",
        priority=Priority.HIGH,
        tags=["Work", "Urgent"]
    )
    assert task.priority == Priority.HIGH
    assert task.tags == ["Work", "Urgent"]

# 2. Run test (fails - Task model doesn't have priority/tags)
# 3. Implement Task model enhancement
# 4. Run test (passes)
# 5. Write edge case tests
def test_task_tags_empty_by_default():
    task = Task(id=1, title="Test")
    assert task.tags == []

# 6. Implement, test passes, move to next test
```

---

## Phase 3: Validation

**Objective**: Ensure correctness, usability, and data consistency across all features.

### Validation Checklist

#### Functional Validation

- [ ] **Add Task**: Task created with title, priority, tags, due date persisted
- [ ] **Update Task**: Modifications persist correctly, validation works
- [ ] **Delete Task**: Removal updates display and storage correctly
- [ ] **View Task List**: All tasks display with status, priority, tags, due date
- [ ] **Mark as Complete**: Status toggles accurately, saves to storage
- [ ] **Search Tasks**: Keyword search returns matching tasks
- [ ] **Filter Tasks**: All filter criteria work independently and combined
- [ ] **Sort Tasks**: Correct ordering by due date, priority, alphabetical

#### Edge Case Validation

- [ ] Empty task list handled gracefully
- [ ] Invalid user input (non-numeric, invalid dates, invalid priorities)
- [ ] Duplicate task titles allowed (different IDs)
- [ ] Duplicate tags on same task prevented
- [ ] Empty search keyword returns all tasks with hint
- [ ] Filter results empty shows "No tasks match current filters"
- [ ] Corrupted JSON file shows error message, doesn't crash
- [ ] Special characters in titles/descriptions/tags display correctly
- [ ] Tasks without due date display as "None"
- [ ] Sorting doesn't affect stored order (temporary view)

#### Performance Validation

- [ ] Create task completes in under 10 seconds
- [ ] Full CRUD cycle (create, view, update, delete) under 30 seconds
- [ ] Search among 100 tasks in under 3 seconds
- [ ] Apply filters and view results in under 3 seconds
- [ ] Display 100 tasks without noticeable delay (<1 second)
- [ ] Load tasks from storage in under 2 seconds (100 tasks)

#### Data Consistency Validation

- [ ] 95%+ tasks persist correctly across restarts
- [ ] Backup file created before overwriting storage
- [ ] No data loss on application crash (during save)
- [ ] Sequential IDs maintained after deletes
- [ ] Priority and tag case sensitivity handled correctly

#### Usability Validation

- [ ] Clear menu options with numbers 1-9
- [ ] Helpful error messages for invalid input
- [ ] Intuitive navigation between views
- [ ] Table formatting fits in 80-column terminal
- [ ] Consistent input patterns (press Enter to skip optional fields)

### Test Coverage Validation

```bash
# Run coverage check
python -m coverage run -m unittest discover
python -m coverage report

# Must achieve 100% coverage with no missing lines
```

### Manual CLI Testing

**Test Scenario 1: End-to-End Workflow**
```
1. Start application
2. Add 3 tasks with different priorities and tags
3. View task list (verify all displayed correctly)
4. Update task 2 priority and tags
5. Mark task 1 complete
6. Search for keyword from task 3
7. Filter by High priority
8. Sort by due date
9. Delete task 2
10. Exit and restart
11. Verify tasks 1 and 3 persisted with correct status
```

**Test Scenario 2: Error Handling**
```
1. Try to add task without title (rejected)
2. Try to add task with invalid date (rejected)
3. Try to update non-existent task ID (error message)
4. Try to add duplicate tag (rejected)
5. Try to filter with invalid date category (rejected)
```

**Test Scenario 3: Data Persistence**
```
1. Create tasks with all attributes
2. Delete todo.json file
3. Start application (should create empty file)
4. Add tasks and exit
5. Verify todo.json exists with correct structure
6. Corrupt todo.json manually
7. Start application (should show error, not crash)
```

---

## Risk Analysis and Mitigation

| Risk | Impact | Probability | Mitigation |
|-------|---------|--------------|------------|
| JSON file corruption | High | Low | Backup file created before overwriting, error handling |
| Performance degradation with 100+ tasks | Medium | Low | In-memory operations, efficient filtering algorithms |
| User input errors (invalid dates/priorities) | Low | High | Input validation with clear error messages |
| Table formatting overflow on narrow terminals | Low | Medium | Truncate long text, ensure 80-column minimum |
| Concurrent writes (rare edge case) | High | Very Low | Single-user application, not in scope |

---

## Architectural Decision Records (ADRs)

Significant architectural decisions from plan:

### ADR-001: Priority as Enum
**Decision**: Represent priority levels as `Priority` enum (HIGH, MEDIUM, LOW)
**Rationale**:
- Type safety prevents invalid values
- Natural ordering for sorting (enum members maintain order)
- Self-documenting code
**Alternatives Considered**:
- Numeric values (1, 2, 3): Less readable
- String constants: No type safety, error-prone
**Trade-offs**: Slightly more verbose than strings, but safer and more maintainable

### ADR-002: JSON Storage with Backup
**Decision**: Use JSON file storage with automatic backup before overwriting
**Rationale**:
- Simple, no external dependencies
- Human-readable for debugging
- Backup prevents catastrophic data loss
**Alternatives Considered**:
- SQLite: Overkill, adds external dependency
- Pickle: Not human-readable, security concerns
**Trade-offs**: JSON is slower than binary formats, but sufficient for 100+ tasks

### ADR-003: Temporary Sorting (View-Only)
**Decision**: Sorting operations return new ordered list, don't modify stored order
**Rationale**:
- Preserves data integrity
- Multiple sort views without affecting underlying data
- User can switch between views freely
**Alternatives Considered**:
- Persistent sorting: Changes stored order, harder to undo
**Trade-offs**: Users lose custom sort persistence, but data integrity is prioritized

---

## Success Metrics

From specification, validated in implementation:

- ✅ Users can create task with all attributes in under 10 seconds
- ✅ Full CRUD cycle completes in under 30 seconds
- ✅ Search 100 tasks in under 3 seconds
- ✅ Filter and view results in under 3 seconds
- ✅ Display 100 tasks with under 1 second delay
- ✅ Assign/modify priorities and tags without errors
- ✅ 95%+ tasks persist correctly across restarts
- ✅ Special characters display correctly
- ✅ Navigate between views without losing unsaved changes

---

## Next Steps

After plan approval:

1. Run `/sp.tasks` to generate actionable task list with dependency ordering
2. Begin implementation following test-first approach
3. Complete tasks incrementally with commits
4. Run validation checklist after each task
5. Final integration testing before merge

---

**Document Status**: Draft | Ready for: `/sp.tasks` command
