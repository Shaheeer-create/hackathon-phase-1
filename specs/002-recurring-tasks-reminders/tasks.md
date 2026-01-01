# Implementation Tasks: Recurring Tasks and Reminders

**Feature**: Recurring Tasks and Reminders
**Date**: 2026-01-01
**Branch**: `002-recurring-tasks-reminders`
**Plan**: [plan.md](plan.md)

## Overview

This document contains actionable implementation tasks for the Recurring Tasks and Reminders feature. Tasks are organized by user story priority and implementation phase to enable independent development and testing.

**Total Tasks**: 21

---

## Phase 1: Setup

**Goal**: Initialize project structure and create base models for recurrence and reminder support.

- [ ] T001 [P] Create RecurrencePattern enum and RecurrenceRule dataclass in src/models/recurrence.py
- [ ] T002 [P] Create Reminder dataclass in src/models/recurrence.py or separate file
- [ ] T003 [P] Extend Task model with due_time and recurrence_rule optional fields in src/models/task.py
- [ ] T004 [P] Add time format validation (HH:MM) to src/utils/validators.py
- [ ] T005 Write unit tests for new models and validators

---

## Phase 2: Recurrence Engine Foundation

**Goal**: Implement core recurrence logic for calculating next occurrence dates.

- [ ] T006 [P] Implement calculate_next_occurrence() function in src/services/recurrence_engine.py
- [ ] T007 [P] Implement _next_daily() algorithm (current_date + 1 day)
- [ ] T008 [P] Implement _next_weekly() algorithm (current_date + 7 days)
- [ ] T009 [P] Implement _next_monthly() algorithm with calendar.monthrange() and last-day fallback
- [ ] T010 [P] Implement max_instances enforcement logic (raises ValueError at 101st instance)
- [ ] T011 Write unit tests for all recurrence patterns in tests/unit/test_recurrence_engine.py

---

## Phase 3: Reminder Scheduler Foundation

**Goal**: Implement background timer and reminder checking logic.

- [ ] T012 [P] Create ReminderScheduler class with threading.Timer in src/services/reminder_scheduler.py
- [ ] T013 [P] Implement add_reminder() method to store reminders in internal list
- [ ] T014 [P] Implement check_reminders() method to find due reminders using datetime.now()
- [ ] T015 [P] Implement start() method with periodic timer (60-second interval)
- [ ] T016 [P] Implement stop() method to cancel timer and cleanup
- [ ] T017 [P] Implement threading.Lock for thread-safe reminder list access
- [ ] T018 Write unit tests for ReminderScheduler in tests/unit/test_reminder_scheduler.py

---

## Phase 4: TaskManager Integration - Recurrence

**Goal**: Integrate recurrence engine with existing TaskManager for recurring task support.

- [ ] T019 [P] Add add_recurrence_rule() method to TaskManager to manage RecurrenceRule objects
- [ ] T020 [P] Update add_task() to accept optional recurrence_rule parameter
- [ ] T021 [P] Implement auto-generation of next instance on task completion (toggle_complete)
- [ ] T022 [P] Update toggle_complete() to call recurrence engine and create new task
- [ ] T023 [P] Ensure recurrence_rule is copied to new task instance (reminders preserved)
- [ ] T024 [P] Track instance count per recurring task to enforce 100-instance limit
- [ ] T025 Write contract test in tests/contract/test_recurrence_operations.py
- [ ] T026 [P] Write unit tests for recurrence integration in tests/unit/test_task_manager.py

---

## Phase 5: TaskManager Integration - Reminders

**Goal**: Integrate reminder scheduler with TaskManager for time-based notifications.

- [ ] T027 [P] Initialize ReminderScheduler in TaskManager.__init__()
- [ ] T028 [P] Add add_reminder_to_task() method to TaskManager
- [ ] T029 [P] Update add_task() to create and associate Reminder object
- [ ] T030 [P] Update toggle_complete() to handle completed task reminders (skip dispatch)
- [ ] T031 [P] Add start_reminder_checks() method to TaskManager
- [ ] T032 [P] Update TaskManager shutdown to stop ReminderScheduler
- [ ] T033 Write contract test for reminder operations in tests/contract/test_reminder_operations.py
- [ ] T034 Write unit tests for reminder integration in tests/unit/test_task_manager.py

---

## Phase 6: CLI Integration - Recurrence

**Goal**: Add user interface for creating recurring tasks.

- [ ] T035 [P] Add "Add Recurring Task" option to CLI menu (option 6)
- [ ] T036 [P] Implement add_recurring_task_interactive() function in src/cli/main.py
- [ ] T037 [P] Add interactive prompt for recurrence pattern selection (1-3: Daily/Weekly/Monthly)
- [ ] T038 [P] Pass selected recurrence pattern to create_recurrence_rule() and add_task()
- [ ] T039 [P] Update display_tasks() to show recurrence pattern and next occurrence date
- [ ] T040 [P] Add validation for empty pattern selection
- [ ] T041 Write integration test in tests/integration/test_cli_workflows.py

---

## Phase 7: CLI Integration - Reminders

**Goal**: Add user interface for setting reminders on tasks.

- [ ] T042 [P] Add "Set Reminder" option to CLI menu (option 7)
- [ ] T043 [P] Implement set_reminder_interactive() function in src/cli/main.py
- [ ] T044 [P] Display tasks with reminders and prompt for task ID selection
- [ ] T045 [P] Add interactive prompt for reminder time (HH:MM format, 24h default)
- [ ] T046 [P] Call add_reminder_to_task() to associate reminder with task
- [ ] T047 [P] Display confirmation with scheduled reminder time
- [ ] T048 [P] Add validation for invalid reminder time format
- [ ] T049 Write integration test in tests/integration/test_cli_workflows.py

---

## Phase 8: Update Task Display

**Goal**: Update task list view to display recurrence patterns and due times.

- [ ] T050 [P] Update list_tasks_interactive() to display recurrence pattern (if set)
- [ ] T051 [P] Update task display to show due_time field (if set)
- [ ] T052 [P] Add "Next occurrence" field to recurring task display
- [ ] T053 [P] Add visual indicator for tasks with reminders (e.g., [🔔] icon)
- [ ] T054 [P] Update "View Upcoming Deadlines" to sort by combined due_date + due_time
- [ ] T055 [P] Test updated display with sample recurring tasks

---

## Phase 9: Recurrence Contract Tests

**Goal**: Validate recurrence engine behavior through contract tests.

- [ ] T056 [P] Write test_calculate_next_daily() for daily recurrence across year boundaries
- [ ] T057 [P] Write test_calculate_next_weekly() for weekly recurrence across month boundaries
- [ ] T058 [P] Write test_calculate_next_monthly() with valid target days (15th, 31st)
- [ ] T059 [P] Write test_calculate_next_monthly_invalid_day() for February 30th/31st edge cases
- [ ] T060 [P] Write test_max_instances_enforcement() for 100-instance limit
- [ ] T061 [P] Write test_leap_year_handling() for February 28th/29th in different years
- [ ] T062 [P] Create tests/contract/test_recurrence_operations.py file
- [ ] T063 [P] Run all recurrence tests and verify 100% pass rate

---

## Phase 10: Reminder Contract Tests

**Goal**: Validate reminder scheduler behavior through contract tests.

- [ ] T064 [P] Write test_add_reminder() for storing reminders
- [ ] T065 [P] Write test_check_reminders_due() for finding due reminders
- [ ] T066 [P] Write test_check_reminders_not_due() for past reminders
- [ ] T067 [P] Write test_dispatch_notification() for console output format
- [ ] T068 [P] Write test_timer_lifecycle() for start/stop behavior
- [ ] T069 [P] Write test_multiple_reminders_same_time() for grouped display
- [ ] T070 [P] Write test_task_completed_before_reminder() for completed tasks
- [ ] T071 [P] Create tests/contract/test_reminder_operations.py file
- [ ] T072 [P] Run all reminder tests and verify 100% pass rate

---

## Phase 11: Recurring Task Integration Tests

**Goal**: End-to-end testing of recurring task lifecycle.

- [ ] T073 [P] Write test_create_daily_recurring_task() for daily pattern
- [ ] T074 [P] Write test_create_weekly_recurring_task() for weekly pattern
- [ ] T075 [P] Write test_create_monthly_recurring_task() for monthly pattern
- [ ] T076 [P] Write test_complete_recurring_task_generates_next_instance() for auto-generation
- [ ] T077 [P] Write test_stop_recurrence_stops_future_generation() for pattern modification
- [ ] T078 [P] Write test_delete_single_instance_preserves_recurrence() for individual deletion
- [ ] T079 [P] Write test_recurrence_displays_correctly() for pattern and next date display
- [ ] T080 [P] Create tests/integration/test_recurring_tasks_flow.py file
- [ ] T081 [P] Run all integration tests and verify 100% pass rate

---

## Phase 12: Reminder Integration Tests

**Goal**: End-to-end testing of reminder functionality.

- [ ] T082 [P] Write test_set_reminder_triggers_at_correct_time() for 24h before due
- [ ] T083 [P] Write test_reminder_displays_for_task_due_soon() for near-term tasks
- [ ] T084 [P] Write test_completed_task_skips_reminder() for completed task handling
- [ ] T085 [P] Write test_multiple_reminders_displayed_together() for concurrent notifications
- [ ] T086 [P] Write test_snooze_and_dismiss_reminder() (UI if implemented later)
- [ ] T087 [P] Update existing test_cli_workflows.py with reminder tests
- [ ] T088 [P] Run all reminder integration tests and verify 100% pass rate

---

## Phase 13: Performance Validation

**Goal**: Verify system meets performance goals from spec.

- [ ] T089 [P] Create performance test: create_recurring_task() < 60 seconds
- [ ] T090 [P] Create performance test: complete_task_generates_next_instance() < 1 second
- [ ] T091 [P] Create performance test: list_tasks_with_100_tasks() < 5 seconds
- [ ] T092 [P] Create performance test: reminder_triggers_at_exact_time() with 99% accuracy
- [ ] T093 [P] Create performance test: handle_10000_recurring_instances() without degradation
- [ ] T094 [P] Run all performance tests and verify all SC-001 through SC-007 pass

---

## Phase 14: Final Validation

**Goal**: Complete test suite and validate against all success criteria.

- [ ] T095 [P] Run complete test suite: python -m pytest tests/ -v
- [ ] T096 [P] Verify 100% test coverage achieved
- [ ] T097 [P] Validate all functional requirements FR-001 through FR-015 are tested
- [ ] T098 [P] Validate all success criteria SC-001 through SC-008 are met
- [ ] T099 [P] Verify zero duplicate task instances in test scenarios (SC-007)
- [ ] T100 [P] Manual walkthrough test of complete user journey (SC-005)

---

## Phase 15: Polish and Documentation

**Goal**: Finalize implementation with code quality and user documentation.

- [ ] T101 [P] Run pylint or similar linter and fix any code quality issues
- [ ] T102 [P] Run mypy type checker and ensure all type hints are valid
- [ ] T103 [P] Verify PEP 8 compliance for all new code
- [ ] T104 [P] Update quickstart.md with working CLI examples
- [ ] T105 [P] Verify research.md reflects actual implementation decisions
- [ ] T106 [P] Update README.md if project-level documentation exists
- [ ] T107 [P] Add docstrings to all new public functions and classes
- [ ] T108 [P] Final code review and cleanup

---

## Success Criteria Validation

Track completion of spec-defined success criteria:

- **SC-001**: Create recurring task in under 60 seconds - Validated in Phase 13
- **SC-002**: 95% of completions generate next instance in < 1 second - Validated in Phase 13
- **SC-003**: View 100 tasks sorted correctly in < 5 seconds - Validated in Phase 13
- **SC-004**: Reminders display at scheduled time 99% of time - Validated in Phase 13
- **SC-005**: 90% of users report understanding recurrence patterns - Validated in Phase 14
- **SC-006**: System handles 10,000 instances without degradation - Validated in Phase 13
- **SC-007**: Zero duplicate task instances - Validated in Phase 11
- **SC-008**: Modify/stop recurrence in < 30 seconds - Validated in Phase 8

---

## Dependencies

Task completion dependencies ensure prerequisites are met before starting later phases.

**Phase 1 (Setup)** depends on: None
**Phase 2-9** depends on: T001, T002, T003, T004, T005
**Phase 10-12** depends on: Previous phase completion
**Phase 13-14** depends on: T019-T034
**Phase 15** depends on: T081-T100

---

## MVP Scope

For rapid delivery, complete these phases first:

**MVP Tasks**: T001, T006-T011, T012-T018, T019-T026 (Phases 1-5)

This provides:
- Recurrence rule storage and calculation
- Background reminder scheduler
- Integration with TaskManager for automatic next instance generation
- Basic CLI interface for creating recurring tasks and setting reminders

**Estimated MVP Duration**: 3-4 days

---

## Parallel Execution Opportunities

These task groups can be executed in parallel without blocking dependencies:

- **Group A**: T019-T026 (TaskManager Recurrence) AND T035-T040 (CLI Recurrence) → Can develop in parallel
- **Group B**: T027-T034 (TaskManager Reminders) AND T042-T049 (CLI Reminders) → Can develop in parallel
- **Group C**: T056-T063 (Recurrence Tests) AND T064-T072 (Reminder Tests) → Can develop in parallel
- **Group D**: T073-T081 (Recurring Integration Tests) AND T082-T088 (Reminder Integration Tests) → Can develop in parallel

**Parallel Strategy**: Execute Group A first, then Groups B, C, D for maximum efficiency.

---

## Testing Strategy

- **Unit Tests**: T005, T011, T018, T026, T034, T063-T072
- **Contract Tests**: T025, T033, T056-T063, T064-T072
- **Integration Tests**: T041, T049, T080, T087
- **Performance Tests**: T089-T094

---

## Notes

- All tasks follow strict checklist format: `- [ ] TaskID [P?] [Story?] Description with file path`
- File paths assume feature directory structure: `src/`, `tests/`, etc.
- Tests use existing `unittest` framework per constitution
- All code must maintain immutability and type hints
