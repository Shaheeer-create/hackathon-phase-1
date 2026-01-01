# Quickstart Guide: Recurring Tasks and Reminders

**Feature**: Recurring Tasks and Reminders (002-recurring-tasks-reminders)
**Date**: 2026-01-01
**Status**: Complete

## Prerequisites

- Python 3.12+ installed
- Project repository cloned
- Existing `001-enhanced-todo-cli` feature complete (base tasks, search, filter, sort)

---

## Installation

```bash
# Already cloned from Phase 1
cd E:\quarter4\hacakthon-2\phase-1

# Switch to feature branch
git checkout 002-recurring-tasks-reminders
```

---

## How to Run

### Running the CLI Application

```bash
# From project root
python src/cli/main.py
```

The application will start with the main menu, including new options for recurring tasks and reminders.

---

## New Menu Options

When you run the application, you'll see updated menu:

```
==================================================
Todo Application - Basic Task Management
==================================================

Main Menu:
1. Add Task
2. List Tasks
3. Complete Task
4. Delete Task
5. Update Task
6. Add Recurring Task         ← NEW
7. Set Reminder               ← NEW
8. Search Tasks
9. Filter Tasks
10. Sort Tasks
11. Exit
==================================================
```

---

## Creating a Recurring Task

### Example: Daily Recurring Task

```
1. Add Recurring Task

Task title: Daily standup meeting
Description (optional): Team sync to review progress
Due date (YYYY-MM-DD HH:MM, optional): 2025-01-15 09:00
Priority (High/Medium/Low, press Enter for Medium): High
Tags (comma-separated, optional): work, team

Recurrence pattern:
1. Daily
2. Weekly
3. Monthly
Enter choice (1-3): 1

Task added: [1] Daily standup meeting [High]
  Due: 2025-01-15 09:00
  Recurrence: Daily
  Next: 2025-01-16 09:00
```

### Example: Weekly Recurring Task

```
1. Add Recurring Task

Task title: Weekly report
Description (optional): Submit status updates to manager
Due date (YYYY-MM-DD HH:MM, optional): 2025-01-15 17:00
Priority (High/Medium/Low, press Enter for Medium): Medium
Tags (comma-separated, optional): work

Recurrence pattern:
1. Daily
2. Weekly
3. Monthly
Enter choice (1-3): 2

Task added: [2] Weekly report [Medium]
  Due: 2025-01-15 17:00
  Recurrence: Weekly
  Next: 2025-01-22 17:00
```

### Example: Monthly Recurring Task

```
1. Add Recurring Task

Task title: Monthly invoice review
Description (optional): Review and process all invoices
Due date (YYYY-MM-DD HH:MM, optional): 2025-01-31 10:00
Priority (High/Medium/Low, press Enter for Medium): High
Tags (comma-separated, optional): finance, billing

Recurrence pattern:
1. Daily
2. Weekly
3. Monthly
Enter choice (1-3): 3

Task added: [3] Monthly invoice review [High]
  Due: 2025-01-31 10:00
  Recurrence: Monthly
  Next: 2025-02-28 10:00
```

---

## Setting a Reminder

### Adding a Reminder to a Task

```
7. Set Reminder

Current tasks:
  [ ] 1: Daily standup meeting [High]
    Due: 2025-01-15 09:00
    Recurrence: Daily
  [ ] 2: Weekly report [Medium]
    Due: 2025-01-15 17:00
    Recurrence: Weekly
  [ ] 3: Monthly invoice review [High]
    Due: 2025-01-31 10:00

Enter task ID to set reminder: 1

Reminder time (HH:MM) [default: due time - 24h]: 09:00

Reminder set for task 1: Daily standup meeting
  Will trigger at: 2025-01-14 09:00 (24 hours before due)
```

### Example Reminder Output

When reminder time arrives, you'll see:

```
⏰ REMINDER: Task 'Daily standup meeting' due at 09:00
```

If multiple reminders are due at the same time:

```
⏰ 3 REMINDERS DUE NOW:
    1. Daily standup meeting
    2. Weekly report
    3. Monthly invoice review
```

---

## Viewing Recurring Tasks

### Listing Tasks Shows Recurrence Patterns

```
2. List Tasks

Tasks (3 total):

  [ ] 1: Daily standup meeting [High]
    Due: 2025-01-15 09:00
    Recurrence: Daily
    Next: 2025-01-16 09:00

  [ ] 2: Weekly report [Medium]
    Due: 2025-01-15 17:00
    Recurrence: Weekly
    Next: 2025-01-22 17:00

  [ ] 3: Monthly invoice review [High]
    Due: 2025-01-31 10:00
    Recurrence: Monthly
    Next: 2025-02-28 10:00
```

---

## Recurring Task Lifecycle

### Step-by-Step Workflow

1. **Create Recurring Task**
   - Enter task details (title, description, due date/time, priority, tags)
   - Select recurrence pattern (Daily/Weekly/Monthly)
   - System calculates "Next" occurrence date
   - Task appears in list with recurrence pattern displayed

2. **Task Becomes Due**
   - Wait until task's due date/time arrives
   - Reminder triggers 24 hours before due (if reminder set)

3. **Complete Task**
   - Mark task as completed via option 3 (Complete Task)
   - System automatically generates **new instance** of recurring task
   - New instance has updated due date based on recurrence pattern

4. **Repeat**
   - Process continues: new instance can be completed → generates another
   - Continue until recurrence is stopped or 100-instance limit reached

---

## Stopping Recurrence

### Changing a Recurring Task to Non-Recurring

```
5. Update Task

Enter task ID to update: 1
Current task: Daily standup meeting [High]
    Due: 2025-01-15 09:00
    Recurrence: Daily

Enter new values (press Enter to keep current):
Title [Daily standup meeting]:
Description [Team sync to review progress]:
Due date [2025-01-15 09:00]:
Due time [09:00]:
Priority [High]:
Tags [work, team]:
Recurrence pattern (Daily/None): None
Press Enter to skip: [Press Enter]

Task 1 updated: Daily standup meeting [High]
  Due: 2025-01-15 09:00
  Recurrence: None
```

After changing recurrence to `None`, completing the task will NOT generate a new instance.

---

## Edge Cases

### Invalid Monthly Date (February 30th)

```
1. Add Recurring Task

Task title: February review
Due date: 2025-01-30 10:00
Recurrence pattern: Monthly

Task added: [4] February review [Medium]
  Due: 2025-01-30 10:00
  Recurrence: Monthly
  Next: 2025-02-28 10:00
```

Notice the system automatically adjusted from February 30th to February 28th (last valid day).

---

## Testing Reminders

### Quick Manual Test

1. **Create a task due in 1 minute:**
   ```
   1. Add Recurring Task
   Task title: Test reminder
   Due date/time: [CURRENT_TIME + 1 minute]
   ```

2. **Set a reminder:**
   ```
   7. Set Reminder
   Task ID: [task ID from above]
   Reminder time: [CURRENT_TIME]
   ```

3. **Wait and verify:**
   - Wait 60 seconds (or app check interval)
   - You should see: `⏰ REMINDER: Task 'Test reminder' due at {time}`

---

## Troubleshooting

### Reminders Not Appearing

**Problem**: Reminder time passed but no notification shown

**Possible Causes**:
1. **App not running**: CLI must be active for background timer to check
   - Solution: Keep CLI application open
2. **Incorrect time**: System time may differ from expected
   - Solution: Check `datetime.now()` values
3. **Task already completed**: Reminders don't trigger for completed tasks
   - Solution: Verify task status via "List Tasks"

### Recurrence Not Working

**Problem**: Completed task didn't generate next instance

**Possible Causes**:
1. **No recurrence pattern set**: Task was created without recurrence
   - Solution: Update task and set recurrence pattern
2. **100-instance limit reached**: Maximum instances generated for this task
   - Solution: Stop recurrence and create new recurring task
3. **Next occurrence is in past**: Date calculation error
   - Solution: Verify date format and recurrence pattern

---

## Tips

1. **Set reminders at least 1 hour before due** to avoid missing notification during short tasks
2. **Review recurring tasks periodically** to stop patterns you no longer need
3. **Use tags for organization** (e.g., "work", "personal", "finance") - works with existing filter feature
4. **Check "Next" field** when listing tasks to see when recurring task will appear next
5. **Test recurrence pattern** by completing a task once to verify next instance is created correctly

---

## Next Steps

After completing this quickstart guide:
1. Explore advanced features via the CLI menu
2. Read detailed specifications in `specs/002-recurring-tasks-reminders/` for technical details
3. Run tests to verify functionality: `python -m pytest tests/ -v`
4. Provide feedback on implementation to improve future iterations
