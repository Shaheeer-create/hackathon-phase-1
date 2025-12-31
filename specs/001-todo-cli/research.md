# Research: Todo CLI - Basic Task Management

**Date**: 2025-12-31
**Purpose**: Document architectural decisions and technology choices for Python CLI Todo application

## Data Storage Method

### Decision: In-Memory List

**Rationale**:
- Constitution explicitly requires "in-memory list storage" for Basic level
- MVP scope is single-session task management without persistence requirements
- Spec acknowledges data resets on restart as "expected and documented behavior"
- Zero external dependencies (no file I/O complexity)
- Fastest performance for CRUD operations

**Alternatives Considered**:
- **JSON file persistence**: Better for long-term use, but violates constitution "in-memory" requirement and adds file I/O complexity
- **CSV file storage**: Simpler than JSON but still violates in-memory requirement and lacks flexibility
- **SQLite database**: Robust persistence but overkill for MVP, requires external dependency (sqlite3 is built-in but complex schema management)

**Trade-offs Accepted**:
- ✅ Simplicity and speed
- ✅ Zero dependencies
- ✅ Constitution compliance
- ❌ No data persistence across restarts (documented as expected behavior)

---

## Task Identification

### Decision: Index-Based Sequential IDs (1, 2, 3...)

**Rationale**:
- Spec explicitly requires "unique sequential identifier" and "re-index when deleted"
- User-friendly: Users refer to "task 1", "task 2" - easier than UUIDs
- Simple implementation with list indexing
- Natural for CLI interface (e.g., `todo complete 1` vs `todo complete 550e8400-e29b-41d4-a716-446655440000`)

**Alternatives Considered**:
- **UUIDs**: Globally unique but user-unfriendly for CLI, no re-indexing needed but violates spec requirement
- **Hash-based IDs**: Unique but non-sequential, harder for users to reference

**Trade-offs Accepted**:
- ✅ User-friendly CLI interaction
- ✅ Spec-compliant (sequential + re-indexing)
- ✅ Simple implementation
- ❌ Re-indexing overhead on delete (minimal for 100+ tasks)

---

## User Interaction Style

### Decision: Command-Based Input (argparse)

**Rationale**:
- Constitution explicitly requires "argparse" for CLI
- Commands follow standard CLI conventions: `todo add`, `todo list`, `todo delete 1`
- Extensible for future features (priorities, tags in Intermediate level)
- Shell-scriptable and pipe-friendly
- Clear help text via argparse (constitution requirement)

**Alternatives Considered**:
- **Menu-driven CLI**: User-friendly for beginners but less scriptable, harder to automate, doesn't align with constitution's "standard CLI conventions"
- **Interactive REPL**: Good for multi-step workflows but harder to script/test, argparse preferred for standard CLI tools

**Trade-offs Accepted**:
- ✅ Constitution compliant (argparse)
- ✅ Scriptable and automatable
- ✅ Standard CLI patterns
- ✅ Clear help text
- ❌ Slightly steeper learning curve than menu-driven (mitigated by help text)

---

## Error Handling Approach

### Decision: Robust Exception Handling

**Rationale**:
- Constitution requires "clean and actionable with helpful error messages"
- Spec requires "clear error messages for invalid commands or non-existent task IDs"
- Prevents application crashes (success criterion SC-001)
- User experience principle: "clear error messages" in edge cases

**Implementation Strategy**:
- Validate all user inputs before processing
- Catch specific exceptions (ValueError, IndexError, KeyError)
- Provide helpful error messages with expected format (e.g., "Invalid date format. Expected YYYY-MM-DD")
- Use argparse built-in validation for command-line arguments
- Custom exception types for domain-specific errors (TaskNotFoundError, InvalidTaskError)

**Alternatives Considered**:
- **Basic input validation only**: Faster to implement but crashes on edge cases, violates constitution's "clean error messages"
- **Silent failures**: Bad UX, users don't know what went wrong

**Trade-offs Accepted**:
- ✅ User-friendly error messages
- ✅ Constitution compliant
- ✅ Application stability
- ❌ Slightly more code than basic validation (mitigated by test coverage)

---

## CLI Command Structure

### Decision: Subcommand-Based Architecture

**Rationale**:
- Standard CLI pattern (e.g., `git commit`, `docker run`)
- Extensible for future features
- Clean separation of concerns per command
- argparse supports subcommands natively

**Commands**:
```
todo add [--title TITLE] [--desc DESCRIPTION] [--due YYYY-MM-DD]
todo list
todo complete <task_id>
todo delete <task_id>
todo update <task_id> [--title TITLE] [--desc DESCRIPTION] [--due YYYY-MM-DD]
todo help [command]
```

**Alternatives Considered**:
- **Single command with flags**: `todo --add --title "..."` (less intuitive for multiple operations)
- **Positional arguments only**: `todo add "Title" "Description" "YYYY-MM-DD"` (less flexible, requires all arguments)

**Trade-offs Accepted**:
- ✅ Intuitive CLI UX
- ✅ Extensible architecture
- ✅ Clear help text per command
- ❌ More argparse setup (one-time cost)

---

## Testing Strategy

### Decision: unittest with Contract/Integration/Unit Structure

**Rationale**:
- Constitution requires "unittest" and "100% coverage"
- Test structure mirrors implementation for discoverability
- Contract tests validate CRUD operations (add, list, update, delete, complete)
- Integration tests validate CLI workflows (user journeys from spec)
- Unit tests validate model and service logic

**Test Categories**:
- **Contract**: `test_task_operations.py` - Validates each CRUD operation behavior
- **Integration**: `test_cli_workflows.py` - Validates end-to-end CLI scenarios from spec
- **Unit**: `test_task_model.py`, `test_task_manager.py` - Validates model/service logic

**Alternatives Considered**:
- **pytest**: Popular but constitution explicitly requires unittest
- **Manual testing only**: Insufficient for 100% coverage, violates constitution

**Trade-offs Accepted**:
- ✅ Constitution compliant
- ✅ Comprehensive coverage
- ✅ Organized test structure
- ❌ More test files than minimal approach (necessary for 100% coverage)

---

## Architecture Patterns

### Decision: MVC with Immutable Dataclasses

**Rationale**:
- Constitution explicitly requires MVC pattern
- Constitution requires "immutable models" with dataclasses
- Clear separation: Model (Task), View (CLI display), Controller (TaskManager)

**Implementation**:
```python
@dataclass(frozen=True)
class Task:
    id: int
    title: str
    description: str
    completed: bool
    due_date: Optional[str]

class TaskManager:
    tasks: List[Task]

    def add_task(self, task: Task) -> Task
    def get_task(self, task_id: int) -> Task
    def list_tasks(self) -> List[Task]
    def update_task(self, task_id: int, **kwargs) -> Task
    def delete_task(self, task_id: int) -> None
    def toggle_complete(self, task_id: int) -> Task
```

**Alternatives Considered**:
- **Mutable models**: Violates constitution's "immutable models" requirement
- **Single-file script**: Simpler but violates MVC separation principle

**Trade-offs Accepted**:
- ✅ Constitution compliant
- ✅ Clear separation of concerns
- ✅ Immutable state
- ✅ Testable components
- ❌ More files than single-script approach (necessary for MVC)

---

## Summary of Key Decisions

| Decision | Rationale | Constitution Compliance |
|----------|-----------|----------------------|
| In-memory storage | MVP scope, zero deps | ✅ Required |
| Index-based sequential IDs | User-friendly CLI, spec requirement | ✅ Compatible |
| Command-based argparse | Standard CLI patterns | ✅ Required |
| Robust exception handling | Clean error messages | ✅ Required |
| Subcommand architecture | Extensible, intuitive | ✅ Compatible |
| unittest + 100% coverage | Explicitly required | ✅ Required |
| MVC with frozen dataclasses | Separation, immutability | ✅ Required |

All decisions align with constitution and spec requirements. No trade-offs violate constitution principles.
