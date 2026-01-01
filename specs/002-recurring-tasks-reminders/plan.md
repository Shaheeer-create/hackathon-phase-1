# Implementation Plan: Recurring Tasks and Reminders

**Branch**: `002-recurring-tasks-reminders` | **Date**: 2026-01-01 | **Spec**: [spec.md](spec.md)

**Note**: This template is filled in by `/sp.plan` command. See `.specify/templates/commands/plan.md` for execution workflow.

## Summary

Implement advanced-level intelligent features for the Todo CLI application, focusing on recurring tasks with automatic rescheduling and time-based deadline reminders. The solution will extend the existing in-memory task management system with minimal complexity while maintaining the MVC architecture and test-first approach specified in the project constitution.

**Primary Requirements**: Enable users to create daily/weekly/monthly recurring tasks that automatically generate new instances upon completion, assign specific due dates and times to tasks, and receive reminder notifications before deadlines.

**Technical Approach**: Research-concurrent implementation where recurrence rules are stored per task and evaluated at completion time to generate the next instance. Reminder scheduling will use a background timer or polling mechanism within the CLI runtime to check for due tasks at configured intervals. Browser notifications will be supported through a lightweight notification utility for web deployments, while CLI displays text-based alerts.

## Technical Context

**Language/Version**: Python 3.12+

**Primary Dependencies**: Python standard library only (`argparse`, `dataclasses`, `datetime`, `threading`, `json`)

**Storage**: In-memory list-based storage (existing `TaskManager` approach), extended with reminder metadata

**Testing**: `unittest` framework with 100% code coverage

**Target Platform**: CLI (primary), with optional web/browser notification support

**Project Type**: Single project (CLI application with modular architecture)

**Performance Goals**:
- Recurring task instance generation: < 1 second after task completion (per SC-002)
- Task listing with 100 tasks: < 5 seconds (per SC-003)
- Reminder trigger accuracy: 99% on-time display (per SC-004)
- System stability: Handles 10,000 recurring task instances without degradation (per SC-006)

**Constraints**:
- Browser notifications only (no mobile push or SMS) - requires cross-platform notification library or built-in browser API
- Recurrence patterns limited to daily, weekly, monthly - custom intervals excluded
- 100-instance maximum per recurring task to prevent excessive generation
- Reminder timing defaults to 24 hours before due date - not user-customizable initially

**Scale/Scope**:
- Single user, single session (no cross-device synchronization)
- In-memory storage persists only for current session
- Up to 10,000 task instances supported without performance degradation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Gates determined based on constitution file**

| Principle | Status | Notes |
|-----------|--------|--------|
| Test-First Accuracy | **PASS** | 100% coverage required, tests written before implementation |
| Clear CLI | **PASS** | Intuitive interface with argparse, follows standard conventions |
| Reproducible | **PASS** | Spec-driven development, 100% test coverage |
| MVC Architecture | **PASS** | Model (dataclasses), controller (services), view (CLI separation maintained |
| Immutability | **PASS** | Task models are immutable, state changes are explicit |
| Input Validation | **PASS** | All user inputs must be validated with clear error messages |

**Constitution Compliance**: All gates passed. No violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/002-recurring-tasks-reminders/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── recurrence-engine.md
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── models/
│   ├── __init__.py
│   ├── task.py                    # Existing - core Task dataclass
│   ├── enums.py                    # Existing - Priority enum
│   └── recurrence.py                # NEW - RecurrencePattern enum, RecurrenceRule dataclass
├── services/
│   ├── __init__.py
│   ├── task_manager.py              # Existing - core CRUD operations
│   ├── recurrence_engine.py          # NEW - Recurrence logic and next instance generation
│   ├── reminder_scheduler.py          # NEW - Background timer, reminder checking, notification dispatch
│   └── storage.py                  # Existing - JSON persistence (may extend for reminders)
├── cli/
│   ├── __init__.py
│   └── main.py                     # UPDATE - Add recurrence and reminder menu options
├── utils/
│   ├── __init__.py
│   └── validators.py               # UPDATE - Add time format validation (HH:MM)
└── exceptions/
    ├── __init__.py
    └── ...                           # Existing exception classes (may extend)

tests/
├── contract/
│   ├── test_task_operations.py      # Existing - CRUD tests
│   ├── test_recurrence_operations.py  # NEW - Recurrence pattern generation tests
│   └── test_reminder_operations.py   # NEW - Reminder scheduling and trigger tests
├── integration/
│   ├── test_cli_workflows.py         # UPDATE - Add recurrence and reminder workflow tests
│   └── test_recurring_tasks_flow.py # NEW - End-to-end recurring task lifecycle tests
└── unit/
    ├── test_task_manager.py         # UPDATE - Add recurring task method tests
    ├── test_recurrence_engine.py    # NEW - Unit tests for recurrence calculation logic
    ├── test_reminder_scheduler.py  # NEW - Unit tests for reminder timing and dispatch
    ├── test_reminder_model.py      # NEW - Unit tests for Reminder dataclass
    └── test_validators.py         # UPDATE - Add time format validation tests
```

**Structure Decision**: Selected single project structure (Option 1) with Option 1: Single project (DEFAULT) pattern. This aligns with existing `src/models`, `src/services`, `src/cli` directory organization. Recurrence and reminder modules will follow the same pattern as existing features like `search_tasks`, `filter_tasks`, and `sort_tasks`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|--------------------------------------|
| None | N/A | Constitution gates all passed, no violations identified |

## Phase 0: Research

### Research Goals

Investigate and validate technical approaches for recurring task logic and reminder scheduling while implementing features. This research-concurrent phase will inform design decisions and prevent architecture rework.

### Research Tasks

1. **Recurrence Rule Storage Strategy**
   - **Question**: Should recurrence rules be stored as task metadata or by generating all future task instances upfront?
   - **Investigation**: Compare storing recurrence rules per task vs pre-generating task instances. Evaluate tradeoffs between storage complexity and scheduling flexibility.
   - **Decision Point**: Document findings in `research.md` with recommendation aligned with spec (per FR-002, auto-generation at completion)

2. **Reminder Scheduling Mechanism**
   - **Question**: Should reminders use system time polling loop or scheduled background timers?
   - **Investigation**: Research Python threading/timer mechanisms for CLI. Compare `threading.Timer` vs `time.sleep` polling loop. Evaluate resource usage and accuracy tradeoffs.
   - **Decision Point**: Document findings in `research.md` with recommended approach meeting SC-004 (99% on-time accuracy)

3. **Browser Notification Integration**
   - **Question**: How to trigger browser notifications from a Python CLI or simple web app?
   - **Investigation**: Explore lightweight notification libraries (e.g., `plyer`, desktop notification APIs) or determine if web-based deployment requires browser notification API (Notification API). Validate platform compatibility.
   - **Decision Point**: Document findings in `research.md` with implementation path for constraint "browser notifications only"

4. **Date and Time Parsing**
   - **Question**: What's the best approach for parsing combined date-time strings (YYYY-MM-DD HH:MM)?
   - **Investigation**: Review Python `datetime` parsing capabilities. Validate timezone handling and error recovery for invalid formats.
   - **Decision Point**: Document recommended parsing approach with validation logic in `research.md`

5. **Reurrence Edge Case Handling**
   - **Question**: How to handle invalid dates in monthly recurrence (e.g., February 30th)?
   - **Investigation**: Research Python `datetime` calendar module for month-length calculations. Validate "last valid day of month" fallback logic.
   - **Decision Point**: Document algorithmic approach in `research.md`

### Research Output

- **File**: `specs/002-recurring-tasks-reminders/research.md`
- **Content**: Documented findings for each research task with recommendations, tradeoffs, and reference implementation approaches
- **Status**: Research complete, ready for Phase 1 design

## Phase 1: Design

### Design Goals

Create detailed technical design for recurrence engine and reminder scheduler integration with the existing TaskManager system. Ensure all design decisions are testable and align with success criteria.

### Phase 1 Deliverables

1. **Data Model** (`specs/002-recurring-tasks-reminders/data-model.md`)
   - Define `RecurrencePattern` enum (DAILY, WEEKLY, MONTHLY)
   - Define `RecurrenceRule` dataclass with fields: `pattern_type`, `next_occurrence_date`, `max_instances`
   - Extend `Task` model to include optional fields: `due_time` (HH:MM), `recurrence_rule` (RecurrenceRule)
   - Define `Reminder` dataclass with fields: `task_id`, `reminder_time`, `status` (SCHEDULED, SNOOZED, DISMISSED)
   - Document relationships: RecurrenceRule → Task, Reminder → Task
   - Specify immutability rules for new models

2. **Recurrence Engine Contract** (`specs/002-recurring-tasks-reminders/contracts/recurrence-engine.md`)
   - Define interface for `calculate_next_occurrence(current_date, pattern): next_date`
   - Define edge case handling: February 30th → last valid day, past dates → skip to next valid
   - Specify 100-instance limit enforcement logic
   - Document testability with unit-level assertions

3. **Reminder Scheduler Contract** (`specs/002-recurring-tasks-reminders/contracts/reminder-scheduler.md`)
   - Define interface for `check_reminders()` method called periodically
   - Define notification dispatch interface: `send_reminder(task_id, message)`
   - Specify timer/polling mechanism selection
   - Document error handling: task completed before reminder, multiple reminders at same time

4. **Quickstart Guide** (`specs/002-recurring-tasks-reminders/quickstart.md`)
   - Prerequisites: Python 3.12+, existing project setup
   - How to run the app with recurring tasks enabled
   - Example CLI usage for creating recurring tasks
   - Example CLI usage for setting reminders
   - How to verify reminders are working

### Design Validation

- **Constitution Re-Check**: Validate design against all principles (test-first, MVC, immutability)
- **Spec Compliance**: Ensure design supports all functional requirements (FR-001 through FR-015)
- **Testability**: Confirm design supports 100% coverage requirements
- **Performance**: Validate design meets performance goals (1-second instance generation, 5-second listing with 100 tasks)

## Phase 2: Implementation

### Implementation Strategy

Implement recurrence engine, reminder scheduler, and CLI integration following test-first development with iterative validation. Each component will be developed, tested, and integrated before moving to the next.

### Implementation Tasks (High-Level Overview)

Detailed task breakdown will be generated by `/sp.tasks` command. This section provides the strategic sequencing:

1. **Foundation Phase**
   - Create `RecurrencePattern` enum and `RecurrenceRule` dataclass in `models/recurrence.py`
   - Create `Reminder` dataclass in `models/recurrence.py` or separate file
   - Extend `Task` model with `due_time` and `recurrence_rule` optional fields
   - Add time format validation to `utils/validators.py` (HH:MM format)
   - Write unit tests for new models and validators

2. **Recurrence Engine Phase**
   - Implement `recurrence_engine.py` with `calculate_next_occurrence()` function
   - Implement logic for daily (+1 day), weekly (+7 days), monthly (+1 month with last-day fallback)
   - Implement 100-instance limit enforcement
   - Add duplicate task generation prevention (check if next instance already exists)
   - Write comprehensive unit tests for all recurrence patterns and edge cases

3. **Reminder Scheduler Phase**
   - Implement `reminder_scheduler.py` with background timer or polling loop
   - Implement `check_reminders()` method to scan tasks with due dates
   - Implement notification dispatch (CLI text output or browser notification)
   - Implement reminder status tracking (scheduled → snoozed/dismissed)
   - Write unit tests for reminder timing, status transitions, and edge cases

4. **Integration Phase**
   - Update `TaskManager` to support creating tasks with recurrence rules
   - Update `TaskManager` to auto-generate next instance on task completion
   - Update `TaskManager` to support adding reminders to tasks
   - Add reminder scheduler initialization to `TaskManager.__init__()`
   - Update CLI main menu to include "Create Recurring Task" and "Set Reminder" options
   - Add interactive prompts for recurrence pattern selection and reminder time
   - Update `display_tasks()` to show recurrence patterns and due times

5. **Contract Testing Phase**
   - Write recurrence operation tests in `tests/contract/test_recurrence_operations.py`
   - Write reminder operation tests in `tests/contract/test_reminder_operations.py`
   - Test recurrence pattern generation across daily/weekly/monthly
   - Test reminder scheduling and triggering at correct times
   - Test edge cases (invalid dates, completion before reminder, 100-instance limit)

6. **Integration Testing Phase**
   - Update existing CLI workflow tests to include recurring tasks
   - Write end-to-end test for recurring task lifecycle in `tests/integration/test_recurring_tasks_flow.py`
   - Test user journey: create recurring task → complete → verify next instance appears
   - Test user journey: set reminder → wait for due time → verify reminder appears
   - Test integration with existing search/filter/sort features

7. **Validation Phase**
   - Run all unit tests (target: 100% pass rate)
   - Run all contract tests (target: 100% pass rate)
   - Run all integration tests (target: 100% pass rate)
   - Validate performance metrics:
     - Recurring instance generation: < 1 second
     - Task listing (100 tasks): < 5 seconds
     - Reminder trigger accuracy: 99% (manual verification or automated tests)
   - Verify zero duplicate task instances in test scenarios

### Success Criteria Validation

After implementation, validate against spec-defined success criteria:

- **SC-001**: Create recurring task in < 60 seconds (CLI interaction timing test)
- **SC-002**: 95% of completions generate next instance in < 1 second (automated test)
- **SC-003**: View 100 tasks sorted correctly in < 5 seconds (performance test)
- **SC-004**: Reminders display at scheduled time 99% of time (automated timer test)
- **SC-005**: User can understand recurrence patterns and deadlines (user acceptance test or walkthrough)
- **SC-006**: System handles 10,000 instances without degradation (load test)
- **SC-007**: Zero duplicate instances in normal usage (test scenarios)
- **SC-008**: Modify/stop recurrence in < 30 seconds per task (CLI interaction test)

### Technical Risks and Mitigations

| Risk | Impact | Mitigation |
|-------|---------|-------------|
| Background timer consumes high CPU | Medium | Use efficient polling interval (e.g., check every 60 seconds) and sleep between checks |
| Browser notifications may not work in CLI-only mode | High | Clearly document that reminders are console-based for CLI; browser notifications require web deployment |
| Recurrence calculation errors for invalid dates | Medium | Comprehensive unit tests covering all edge cases (Feb 30th, past dates, leap years) |
| Reminder timing accuracy affected by system clock changes | Medium | Use `datetime.now()` consistently; document that reminders depend on system time |
| Complex recurrence patterns (custom intervals) requested later | Low | Document scope limitation in quickstart; design for future extensibility if needed |

## Next Steps

After this plan is reviewed and approved:

1. **Phase 0**: Execute research tasks and document findings in `research.md`
2. **Phase 1**: Create design artifacts (data-model.md, contracts/*.md, quickstart.md)
3. **Phase 2**: Run `/sp.tasks` to generate detailed, actionable implementation tasks
4. **Implementation**: Execute tasks in order, maintaining test-first development
5. **Validation**: Run tests and validate against success criteria before marking feature complete

**Suggested Next Command**: `/sp.tasks` (after Phase 0 research and Phase 1 design are complete)
