---

description: "Task list for feature implementation"
---

# Tasks: Todo CLI - Basic Task Management

**Input**: Design documents from `/specs/001-todo-cli/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are REQUIRED (constitution requires 100% unittest coverage). Test tasks are included for each user story.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project directory structure per implementation plan (src/, src/models/, src/services/, src/cli/, tests/ and subdirectories)
- [ ] T002 [P] Create all __init__.py files for src/, src/models/, src/services/, src/cli/, tests/, tests/contract/, tests/integration/, tests/unit/
- [ ] T003 [P] Create custom exception classes in src/exceptions/__init__.py (TaskNotFoundError, InvalidTaskError) as defined in data-model.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Tests for Foundational Components (REQUIRED - Constitution mandates 100% coverage) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T004 [P] Create unit test for Task model in tests/unit/test_task_model.py
- [ ] T005 [P] Create unit test for TaskManager service in tests/unit/test_task_manager.py

### Implementation of Foundational Components

- [ ] T006 [P] Implement Task dataclass (immutable, frozen=True) in src/models/task.py with all fields: id, title, description, completed, due_date
- [ ] T007 [P] Implement TaskManager class in src/services/task_manager.py with methods: add_task, get_task, list_tasks, update_task, delete_task, toggle_complete
- [ ] T008 [P] Implement input validation in TaskManager: validate title not empty, validate date format YYYY-MM-DD, validate task ID exists
- [ ] T009 [P] Implement error handling in TaskManager: raise TaskNotFoundError for invalid IDs, raise ValueError for invalid dates, raise InvalidTaskError for invalid titles
- [ ] T010 [P] Implement re-indexing logic in TaskManager.delete_task to maintain sequential IDs after deletion

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new tasks to the todo list and view all tasks

**Independent Test**: Can be fully tested by running add and list commands with various task configurations (title only, title+description, title+due_date, all fields)

### Tests for User Story 1 (REQUIRED - Constitution mandates 100% coverage) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T011 [P] [US1] Contract test for add_task operation in tests/contract/test_task_operations.py (validate task creation with sequential ID)
- [ ] T012 [P] [US1] Contract test for list_tasks operation in tests/contract/test_task_operations.py (validate correct listing with all fields)
- [ ] T013 [P] [US1] Integration test for add→list workflow in tests/integration/test_cli_workflows.py (add task, then list to verify appearance)
- [ ] T014 [P] [US1] Integration test for empty list in tests/integration/test_cli_workflows.py (list with no tasks shows "No tasks found")

### Implementation for User Story 1

- [ ] T015 [P] [US1] Implement add command argument parser in src/cli/main.py (argparse subcommand with --title, --desc, --due flags)
- [ ] T016 [P] [US1] Implement list command argument parser in src/cli/main.py (argparse subcommand with no arguments)
- [ ] T017 [P] [US1] Implement add command handler in src/cli/main.py (calls TaskManager.add_task, validates inputs, displays success message)
- [ ] T018 [P] [US1] Implement list command handler in src/cli/main.py (calls TaskManager.list_tasks, formats display with [ ] status indicator)
- [ ] T019 [US1] Implement task display formatting in src/cli/main.py (format individual tasks with [ ] or [✓], show description and due_date if present)
- [ ] T020 [US1] Implement empty list message in src/cli/main.py (display "No tasks found" message when list is empty)
- [ ] T021 [US1] Add validation error messages in src/cli/main.py (display clear errors for empty title, invalid date format)

**Checkpoint**: At this point, users can add tasks and view the task list - MVP functionality complete

---

## Phase 4: User Story 2 - Complete and Delete Tasks (Priority: P1)

**Goal**: Enable users to mark tasks as completed and remove tasks from the list

**Independent Test**: Can be fully tested by creating tasks, marking them complete, toggling status, and deleting with re-indexing verification

### Tests for User Story 2 (REQUIRED - Constitution mandates 100% coverage) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T022 [P] [US2] Contract test for toggle_complete operation in tests/contract/test_task_operations.py (validate status toggle between pending and completed)
- [ ] T023 [P] [US2] Contract test for delete_task operation in tests/contract/test_task_operations.py (validate deletion and re-indexing)
- [ ] T024 [P] [US2] Integration test for complete→list workflow in tests/integration/test_cli_workflows.py (complete task, then list to verify [✓] indicator)
- [ ] T025 [P] [US2] Integration test for delete→list workflow in tests/integration/test_cli_workflows.py (delete task, then list to verify removal and re-indexing)
- [ ] T026 [P] [US2] Integration test for error cases in tests/integration/test_cli_workflows.py (attempt complete/delete on non-existent task ID)

### Implementation for User Story 2

- [ ] T027 [P] [US2] Implement complete command argument parser in src/cli/main.py (argparse subcommand with positional task_id argument)
- [ ] T028 [P] [US2] Implement delete command argument parser in src/cli/main.py (argparse subcommand with positional task_id argument)
- [ ] T029 [P] [US2] Implement complete command handler in src/cli/main.py (calls TaskManager.toggle_complete, displays updated status with [✓] or [ ])
- [ ] T030 [P] [US2] Implement delete command handler in src/cli/main.py (calls TaskManager.delete_task, displays success message and remaining task count)
- [ ] T031 [US2] Implement task ID validation in src/cli/main.py (validate task_id is positive integer, catch TaskNotFoundError)
- [ ] T032 [US2] Add error messages for not-found tasks in src/cli/main.py (display "Task with ID {n} not found" for complete/delete commands)

**Checkpoint**: At this point, User Stories 1 AND 2 are fully functional - complete CRUD lifecycle

---

## Phase 5: User Story 3 - Update Task Details (Priority: P2)

**Goal**: Enable users to modify existing task details (title, description, due date)

**Independent Test**: Can be fully tested by creating a task, updating each field individually and in combination, verifying changes persist

### Tests for User Story 3 (REQUIRED - Constitution mandates 100% coverage) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T033 [P] [US3] Contract test for update_task operation in tests/contract/test_task_operations.py (validate updates to title, description, due_date individually and in combination)
- [ ] T034 [P] [US3] Integration test for update→list workflow in tests/integration/test_cli_workflows.py (update task, then list to verify changes)
- [ ] T035 [P] [US3] Integration test for update error cases in tests/integration/test_cli_workflows.py (attempt update on non-existent task ID, attempt update with empty title, invalid date)

### Implementation for User Story 3

- [ ] T036 [P] [US3] Implement update command argument parser in src/cli/main.py (argparse subcommand with positional task_id and optional --title, --desc, --due flags)
- [ ] T037 [P] [US3] Implement update command handler in src/cli/main.py (calls TaskManager.update_task with provided fields, displays updated task)
- [ ] T038 [P] [US3] Implement partial update logic in src/cli/main.py (only update fields that are provided, preserve existing values for unspecified fields)
- [ ] T039 [P] [US3] Add update validation error messages in src/cli/main.py (validate task exists, validate non-empty title if provided, validate date format if provided)

**Checkpoint**: All three user stories are now independently functional - full CRUD and lifecycle management

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and ensure constitution compliance

- [ ] T040 [P] Implement help command in src/cli/main.py (display all commands with brief descriptions)
- [ ] T041 [P] Implement command-specific help in src/cli/main.py (display detailed help for each command with examples)
- [ ] T042 [P] Add type hints to all functions in src/models/task.py, src/services/task_manager.py, src/cli/main.py (PEP 8 requirement)
- [ ] T043 [P] Add docstrings to all classes and methods (Task, TaskManager, CLI handlers)
- [ ] T044 Ensure PEP 8 compliance across all code (line length < 88 chars, proper spacing)
- [ ] T045 Run contract test suite to validate all operations (tests/contract/test_task_operations.py)
- [ ] T046 Run unit test suite to validate model and service logic (tests/unit/test_task_model.py, tests/unit/test_task_manager.py)
- [ ] T047 Run integration test suite to validate end-to-end workflows (tests/integration/test_cli_workflows.py)
- [ ] T048 Verify 100% test coverage using unittest discovery (python -m unittest discover -v tests/)
- [ ] T049 Performance testing: Create 100 tasks and verify operations complete within 1 second

**Final Checkpoint**: All requirements met, 100% test coverage achieved, ready for deployment

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User Story 1 (Phase 3): Can start after Foundational - No dependencies on other stories
  - User Story 2 (Phase 4): Can start after Foundational - Integrates with US1 components
  - User Story 3 (Phase 5): Can start after Foundational - Integrates with US1/US2 components
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Uses Task model and TaskManager from US1, but independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Uses Task model and TaskManager from US1, but independently testable

### Within Each User Story

- Tests MUST be written and FAIL before implementation (Constitution: Test-First Accuracy)
- Model implementation before service implementation
- Service implementation before CLI handler implementation
- CLI handlers before validation/error handling
- Story complete before moving to next priority

### Parallel Opportunities

- **Setup (Phase 1)**: All [P] tasks (T002, T003) can run in parallel with T001
- **Foundational (Phase 2)**: All [P] tests (T004, T005) can run in parallel
- **Foundational (Phase 2)**: All [P] implementation tasks (T006, T007, T008, T009, T010) can run in parallel
- **User Story 1**: All [P] tests (T011, T012, T013, T014) can run in parallel; all [P] CLI tasks (T015, T016, T017, T018, T019, T020, T021) can run in parallel
- **User Story 2**: All [P] tests (T022, T023, T024, T025, T026) can run in parallel; all [P] CLI tasks (T027, T028, T029, T030, T031, T032) can run in parallel
- **User Story 3**: All [P] tests (T033, T034, T035) can run in parallel; all [P] CLI tasks (T036, T037, T038, T039) can run in parallel
- **Polish (Phase 6)**: All [P] tasks (T040, T041, T042, T043, T044) can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Contract test for add_task operation in tests/contract/test_task_operations.py"
Task: "Contract test for list_tasks operation in tests/contract/test_task_operations.py"
Task: "Integration test for add→list workflow in tests/integration/test_cli_workflows.py"
Task: "Integration test for empty list in tests/integration/test_cli_workflows.py"

# Launch all CLI implementations for User Story 1 together:
Task: "Implement add command argument parser in src/cli/main.py"
Task: "Implement list command argument parser in src/cli/main.py"
Task: "Implement task display formatting in src/cli/main.py"
Task: "Implement empty list message in src/cli/main.py"
Task: "Add validation error messages in src/cli/main.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Run all tests, verify add and list commands work correctly
5. Demo: Show adding tasks and listing them

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Demo (MVP!)
3. Add User Story 2 → Test independently → Demo
4. Add User Story 3 → Test independently → Demo
5. Polish Phase → Full validation
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (tests + implementation)
   - Developer B: User Story 2 (tests + implementation)
   - Developer C: User Story 3 (tests + implementation)
3. Stories complete and integrate independently

---

## Summary

**Total Task Count**: 49 tasks

**Task Count by Phase**:
- Phase 1 (Setup): 3 tasks
- Phase 2 (Foundational): 7 tasks (5 tests + 2 implementation)
- Phase 3 (User Story 1): 11 tasks (4 tests + 7 implementation)
- Phase 4 (User Story 2): 11 tasks (5 tests + 6 implementation)
- Phase 5 (User Story 3): 7 tasks (3 tests + 4 implementation)
- Phase 6 (Polish): 10 tasks

**Task Count by User Story**:
- User Story 1 (P1): 11 tasks - MVP scope
- User Story 2 (P1): 11 tasks - Complete task lifecycle
- User Story 3 (P2): 7 tasks - Task updates

**Parallel Opportunities**: 40 tasks marked [P] for parallel execution (82% of tasks)

**Independent Test Criteria**:
- US1: Can add tasks and list all tasks without other stories
- US2: Can complete/delete tasks independently of other operations
- US3: Can update task details independently of other stories

**Suggested MVP Scope**: User Story 1 only (T001-T021) - provides add and list functionality
