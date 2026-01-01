---
description: "Task list for Enhanced CLI Todo Application implementation"
---

# Tasks: Enhanced CLI Todo Application

**Input**: Design documents from `specs/001-enhanced-todo-cli/`

**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Following constitution's Test-First Accuracy principle, all tasks include corresponding test cases

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

**Single project**: `src/`, `tests/` at repository root

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create src/utils package directory and __init__.py in src/utils/__init__.py
- [ ] T002 Create tests/contract directory __init__.py in tests/contract/__init__.py
- [ ] T003 [P] Create tests/integration directory __init__.py in tests/integration/__init__.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 [P] Create StorageError exception in src/exceptions/__init__.py
- [ ] T005 [P] Create Priority enum in src/models/enums.py
- [ ] T006 [P] Create SortOrder enum in src/models/enums.py (depends on T005)
- [ ] T007 [P] Create DueDateCategory enum in src/models/enums.py
- [ ] T008 Implement JSONStorage class with save_tasks() method in src/services/storage.py
- [ ] T009 Implement JSONStorage class with load_tasks() method in src/services/storage.py (depends on T008)
- [ ] T010 [P] Write unit tests for JSONStorage save/load in tests/unit/test_storage.py
- [ ] T011 Update Task dataclass with priority and tags fields in src/models/task.py
- [ ] T012 Update existing unit tests for Task model in tests/unit/test_task_model.py (depends on T011)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Core Task Management (Priority: P1) 🎯 MVP

**Goal**: Extend existing CRUD operations to support priority and tags while maintaining core functionality

**Independent Test**: Can create, view, update, delete, and complete tasks with priority and tags through CLI commands. Delivers core value of enhanced task tracking.

### Tests for User Story 1 (REQUIRED) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T013 [P] [US1] Write contract test for add_task with priority and tags in tests/contract/test_task_operations.py
- [ ] T014 [P] [US1] Write contract test for update_task with priority and tags in tests/contract/test_task_operations.py
- [ ] T015 [P] [US1] Write integration test for create/view/update/delete cycle in tests/integration/test_cli_workflows.py

### Implementation for User Story 1

- [ ] T016 [P] [US1] Update TaskManager.add_task() to accept priority and tags in src/services/task_manager.py (depends on T011)
- [ ] T017 [US1] Update TaskManager.update_task() to accept priority and tags in src/services/task_manager.py (depends on T016)
- [ ] T018 [US1] Update TaskManager.add_task() tag deduplication logic in src/services/task_manager.py (depends on T016)
- [ ] T019 [US1] Update TaskManager.toggle_complete() with reindex for priority changes in src/services/task_manager.py (depends on T016)
- [ ] T020 [US1] Update CLI add_task_interactive() to prompt for priority and tags in src/cli/main.py (depends on T016, T017)
- [ ] T021 [US1] Update CLI update_task_interactive() to prompt for priority and tags in src/cli/main.py (depends on T020)
- [ ] T022 [US1] Update CLI list_tasks_interactive() to display priority and tags in src/cli/main.py (depends on T020)
- [ ] T023 [US1] Update CLI complete_task_interactive() to display updated priority in src/cli/main.py (depends on T019)
- [ ] T024 [US1] Update existing unit tests for TaskManager add/update in tests/unit/test_task_manager.py (depends on T016, T017)
- [ ] T025 [US1] Update existing integration tests for CLI workflows in tests/integration/test_cli_workflows.py (depends on T020, T021, T022, T023)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Organization (Priority: P2)

**Goal**: Enable users to assign and modify priority levels and multiple tags for task organization

**Independent Test**: Can assign priorities (High/Medium/Low) and multiple tags to tasks, update them, and view tasks sorted by priority. Delivers enhanced organization and focus capabilities.

### Tests for User Story 2 (REQUIRED) ⚠️

- [ ] T026 [P] [US2] Write unit test for priority validation (rejects invalid values) in tests/unit/test_validators.py
- [ ] T027 [P] [US2] Write unit test for tag deduplication in tests/unit/test_task_manager.py
- [ ] T028 [P] [US2] Write integration test for priority and tag CRUD workflows in tests/integration/test_cli_workflows.py

### Implementation for User Story 2

- [ ] T029 [P] [US2] Create validate_priority() utility function in src/utils/validators.py (depends on T005)
- [ ] T030 [P] [US2] Create validate_tags() utility function with deduplication in src/utils/validators.py
- [ ] T031 [US2] Update TaskManager.add_task() to validate priority using validators in src/services/task_manager.py (depends on T029)
- [ ] T032 [US2] Update TaskManager.add_task() to deduplicate tags using validators in src/services/task_manager.py (depends on T030, T031)
- [ ] T033 [US2] Update TaskManager.update_task() to validate new priority in src/services/task_manager.py (depends on T029)
- [ ] T034 [US2] Update TaskManager.update_task() to deduplicate new tags in src/services/task_manager.py (depends on T030, T033)
- [ ] T035 [US2] Add CLI priority input validation with helpful error messages in src/cli/main.py (depends on T029)
- [ ] T036 [US2] Add CLI tag input validation with helpful error messages in src/cli/main.py (depends on T030)
- [ ] T037 [US2] Write unit tests for validators in tests/unit/test_validators.py (depends on T029, T030)
- [ ] T038 [US2] Update TaskManager tests for priority validation in tests/unit/test_task_manager.py (depends on T031, T033)
- [ ] T039 [US2] Update TaskManager tests for tag deduplication in tests/unit/test_task_manager.py (depends on T032, T034)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Task Discovery (Priority: P3)

**Goal**: Enable users to quickly find specific tasks by searching keywords and filtering by status, priority, and due date

**Independent Test**: Can search tasks by keyword and filter by status, priority, and due date. Delivers ability to quickly locate and focus on relevant tasks.

### Tests for User Story 3 (REQUIRED) ⚠️

- [ ] T040 [P] [US3] Write contract test for search_tasks() in tests/contract/test_task_operations.py
- [ ] T041 [P] [US3] Write contract test for filter_tasks() with TaskFilter in tests/contract/test_task_operations.py
- [ ] T042 [P] [US3] Write integration test for search and filter workflows in tests/integration/test_cli_workflows.py

### Implementation for User Story 3

- [ ] T043 [P] [US3] Create TaskFilter dataclass in src/models/task.py (depends on T007)
- [ ] T044 [P] [US3] Implement TaskManager.search_tasks() method in src/services/task_manager.py
- [ ] T045 [US3] Implement TaskManager.filter_tasks() with keyword filter in src/services/task_manager.py (depends on T043, T044)
- [ ] T046 [US3] Implement TaskManager.filter_tasks() with status filter in src/services/task_manager.py (depends on T043, T045)
- [ ] T047 [US3] Implement TaskManager.filter_tasks() with priority filter in src/services/task_manager.py (depends on T005, T045)
- [ ] T048 [P] [US3] Implement TaskManager.filter_tasks() with due date filter in src/services/task_manager.py (depends on T007, T045)
- [ ] T049 [US3] Create is_valid_date() validator utility in src/utils/validators.py
- [ ] T050 [US3] Implement date comparison helpers (today, upcoming, overdue) in src/utils/validators.py (depends on T049)
- [ ] T051 [US3] Add CLI search menu option and handler in src/cli/main.py (depends on T044)
- [ ] T052 [US3] Add CLI filter menu option and handler in src/cli/main.py (depends on T045, T046, T047, T048)
- [ ] T053 [US3] Update CLI to display filtered tasks with message when empty in src/cli/main.py (depends on T051, T052)
- [ ] T054 [US3] Write unit tests for search_tasks() in tests/unit/test_task_manager.py (depends on T044)
- [ ] T055 [US3] Write unit tests for filter_tasks() all criteria in tests/unit/test_task_manager.py (depends on T045, T046, T047, T048)
- [ ] T056 [US3] Write unit tests for date validators in tests/unit/test_validators.py (depends on T049, T050)
- [ ] T057 [US3] Write integration tests for CLI search workflows in tests/integration/test_cli_workflows.py (depends on T051)
- [ ] T058 [US3] Write integration tests for CLI filter workflows in tests/integration/test_cli_workflows.py (depends on T052, T053)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Flexible Task Ordering (Priority: P4)

**Goal**: Enable users to view tasks in different orders (due date, priority, alphabetical) depending on context

**Independent Test**: Can sort tasks by due date, priority, and alphabetical title. Each sort type maintains stability and doesn't affect stored order. Delivers ability to view tasks in most useful order for any given context.

### Tests for User Story 4 (REQUIRED) ⚠️

- [ ] T059 [P] [US4] Write contract test for sort_tasks() with SortOrder enum in tests/contract/test_task_operations.py
- [ ] T060 [P] [US4] Write integration test for sort workflows in tests/integration/test_cli_workflows.py

### Implementation for User Story 4

- [ ] T061 [P] [US4] Implement TaskManager.sort_tasks() with DUE_DATE sort in src/services/task_manager.py (depends on T006, T049)
- [ ] T062 [P] [US4] Implement TaskManager.sort_tasks() with PRIORITY sort in src/services/task_manager.py (depends on T005)
- [ ] T063 [P] [US4] Implement TaskManager.sort_tasks() with ALPHABETICAL sort in src/services/task_manager.py
- [ ] T064 [P] [US4] Implement TaskManager.sort_tasks() with DEFAULT (no-sort) in src/services/task_manager.py
- [ ] T065 [P] [US4] Ensure stable sorting for equal keys in all sort methods in src/services/task_manager.py
- [ ] T066 [P] [US4] Add CLI sort menu option and handler in src/cli/main.py (depends on T061, T062, T063, T064)
- [ ] T067 [US4] Create CLI display utilities (table formatting) in src/cli/display.py (depends on T065)
- [ ] T068 [P] [US4] Update CLI main menu to include sort option in src/cli/main.py (depends on T066, T067)
- [ ] T069 [US4] Write unit tests for all sort methods in tests/unit/test_task_manager.py (depends on T061, T062, T063, T064, T065)
- [ ] T070 [US4] Write unit tests for display utilities in tests/unit/test_display.py (depends on T067)
- [ ] T071 [US4] Write integration tests for CLI sort workflows in tests/integration/test_cli_workflows.py (depends on T066, T067)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final integration

- [ ] T072 Integrate JSONStorage with TaskManager for auto-save in src/services/task_manager.py (depends on T008, T009)
- [ ] T073 Integrate JSONStorage with TaskManager for auto-load on init in src/services/task_manager.py (depends on T010, T072)
- [ ] T074 Add StorageError handling in CLI operations in src/cli/main.py (depends on T072)
- [ ] T075 Create contract test for storage operations in tests/contract/test_storage_contract.py (depends on T010)
- [ ] T076 Write integration test for full workflow with persistence in tests/integration/test_cli_workflows.py (depends on T072, T073)
- [ ] T077 Run coverage check and achieve 100% coverage across all modules
- [ ] T078 Update existing unit tests to cover all edge cases (empty list, invalid inputs, etc.)
- [ ] T079 Update existing integration tests for error scenarios (corrupted JSON, permission errors)
- [ ] T080 Refactor any repeated code into shared utilities
- [ ] T081 Add help text and usage hints to CLI menu in src/cli/main.py
- [ ] T082 Performance test with 100 tasks (manual verification)
- [ ] T083 Run validation checklist from plan.md Phase 3
- [ ] T084 Run quickstart.md test scenarios (manual verification)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - no dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational - extends US1 but independently testable
- **User Story 3 (P3)**: Can start after Foundational - adds new features, independently testable
- **User Story 4 (P4)**: Can start after Foundational - adds new features, independently testable

### Within Each User Story

- Tests MUST be written and FAIL before implementation (constitution requirement)
- Models before services
- Services before endpoints/CLI
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

### Parallel Examples

**After Foundational phase completes, work on US2, US3, and US4 in parallel:**

```bash
# Developer A: User Story 2 (Task Organization)
Task: T026 [P] [US2] Write unit test for priority validation
Task: T029 [P] [US2] Create validate_priority() utility
Task: T035 [US2] Add CLI priority input validation

# Developer B: User Story 3 (Task Discovery)
Task: T040 [P] [US3] Write contract test for search_tasks()
Task: T043 [P] [US3] Create TaskFilter dataclass
Task: T051 [P] [US3] Add CLI search menu option

# Developer C: User Story 4 (Flexible Ordering)
Task: T059 [P] [US4] Write contract test for sort_tasks()
Task: T061 [P] [US4] Implement sort by due date
Task: T067 [P] [US4] Create CLI display utilities
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

**MVP delivers**: Core task management with priorities and tags - foundational enhanced Todo CLI

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Complete Polish phase
7. Final validation and deployment

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently
4. User Story 4 after (if needed)
5. Team completes Polish together

---

## Notes

- Constitution requires test-first development - write tests BEFORE implementation
- Each user story should be independently completable and testable
- Tasks follow strict checklist format with checkbox, ID, [P] marker, [Story] label, file path
- Stop at any checkpoint to validate story independently
- MVP = User Story 1 + Foundational phases (delivers core value)
- Total: 84 tasks organized across 7 phases
