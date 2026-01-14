---
id: 006
title: Implement search filter and sort features
stage: green
date: 2026-01-01
surface: agent
model: claude-sonnet-4.5-20250929
feature: 001-enhanced-todo-cli
branch: 001-enhanced-todo-cli
user: unknown
command: yes implement
labels: [feature-implementation, search, filter, sort]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - src/services/task_manager.py
  - src/cli/main.py
tests:
  - pytest (all 139 tests)
---

## Prompt

yes implement

## Response snapshot

Implemented three new features for the Todo CLI application: search, filter, and sort functionality.

**Changes to src/services/task_manager.py:**
1. Added `search_tasks(keyword)` method - searches tasks by keyword in title, description, or tags (case-insensitive)
2. Added `filter_tasks(status, priority, due_before)` method - filters tasks by status (completed/pending), priority, or due date
3. Added `sort_tasks(by)` method - sorts tasks by id, due_date, priority, or title

**Changes to src/cli/main.py:**
1. Updated menu from 6 to 9 options to include:
   - Option 6: Search Tasks
   - Option 7: Filter Tasks
   - Option 8: Sort Tasks
   - Option 9: Exit (was 6)
2. Added `display_tasks(tasks)` helper function for consistent task display formatting
3. Added `search_tasks_interactive(manager)` function for interactive search
4. Added `filter_tasks_interactive(manager)` function for interactive filtering with multiple criteria
5. Added `sort_tasks_interactive(manager)` function with menu for sort field selection
6. Updated `get_menu_choice()` to accept options 1-9
7. Updated `main()` to wire up new menu options
8. Added `from typing import List` import

**Testing:**
- All 139 existing tests pass
- No new test files were added (implementation only)

## Outcome

- ✅ Impact: Added three major features (search, filter, sort) that were missing from the original implementation
- 🧪 Tests: All 139 existing tests pass
- 📁 Files: Modified 2 files (task_manager.py +118 lines, main.py +147 lines)
- 🔁 Next prompts: Could add unit tests for new search/filter/sort methods if needed
- 🧠 Reflection: Features implemented cleanly following existing code patterns and architecture

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All 139 tests pass
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): Could add unit tests for the three new TaskManager methods (search_tasks, filter_tasks, sort_tasks)
