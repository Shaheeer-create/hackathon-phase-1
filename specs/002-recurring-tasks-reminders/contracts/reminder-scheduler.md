# Contract: Reminder Scheduler

**Feature**: Recurring Tasks and Reminders
**Date**: 2026-01-01
**Status**: Complete

## Purpose

Define contract for reminder scheduler that monitors tasks with due times and dispatches notifications at scheduled times. This component is responsible for implementing requirements FR-008 ("System MUST display reminders at the scheduled time"), FR-009 ("System MUST display reminders at the scheduled time (24 hours before due date by default)"), FR-010 ("System MUST allow users to snooze or dismiss reminders"), and SC-004 ("Reminders display at the scheduled time 99% of the time").

---

## Interface

### Class: `ReminderScheduler`

```python
import threading
from typing import List, Callable
from datetime import datetime, timedelta
from .models.recurrence import Reminder

class ReminderScheduler:
    """Background scheduler that checks for due reminders and dispatches notifications.

    Attributes:
        reminders: List of active reminders to monitor
        timer: Background timer that triggers periodic checks
        dispatch_callback: Function called to send reminder (console or browser)
        check_interval_seconds: How often to check for due reminders (60 seconds default)
    """

    def __init__(
        self,
        check_interval_seconds: int = 60,
        dispatch_callback: Callable[[int, str], None] = None
    ) -> None:
        """Initialize reminder scheduler.

        Args:
            check_interval_seconds: Seconds between reminder checks (default: 60)
            dispatch_callback: Function to call when reminder fires (receives task_id, message)
        """
        self._reminders: List[Reminder] = []
        self._timer: Optional[threading.Timer] = None
        self._check_interval: int = check_interval_seconds
        self._dispatch_callback: Callable[[int, str], None] = dispatch_callback
        self._lock: threading.Lock = threading.Lock()
        self._running: bool = False

    def add_reminder(self, reminder: Reminder) -> None:
        """Add a reminder to monitor.

        Args:
            reminder: Reminder object to schedule
        """
        pass

    def check_reminders(self) -> List[Tuple[int, str]]:
        """Check all reminders and return due ones.

        Returns:
            List of (task_id, message) tuples for reminders due now
        """
        pass

    def start(self) -> None:
        """Start the background timer.

        Starts periodic reminder checks. Must be called after all reminders added.
        """
        pass

    def stop(self) -> None:
        """Stop the background timer.

        Cleans up resources and prevents new reminder dispatches.
        """
        pass
```

---

## Behavioral Contracts

### Reminder Addition

**Input**: New `Reminder` object with task_id=1, reminder_time=2025-01-15 14:00

**Expected Behavior**:
```python
scheduler.add_reminder(reminder)
# Reminder is stored in internal list
# Next check cycle will include this reminder
```

**Test Cases**:
1. **Given** no reminders exist, **When** adding a reminder, **Then** reminder is stored
2. **Given** 5 reminders exist, **When** adding a 6th reminder, **Then** all 6 reminders are stored
3. **Given** adding reminder with task_id=999 (doesn't exist), **When** add_reminder(), **Then** reminder is stored (validation at dispatch time)

### Reminder Checking

**Input**: Current time = 2025-01-15 14:01, Check interval = 60 seconds

**Expected Behavior**:
```python
due_reminders = scheduler.check_reminders()
# Returns list of reminders where reminder_time <= current_time
```

**Test Cases**:
1. **Given** reminder at 14:00, current_time=14:01, **When** check_reminders(), **Then** reminder is returned (due)
2. **Given** reminder at 14:00, current_time=13:59, **When** check_reminders(), **Then** reminder is NOT returned (not yet due)
3. **Given** reminder at 14:00, current_time=14:00, **When** check_reminders(), **Then** reminder is returned (exactly at due time)
4. **Given** 3 reminders at 14:00, current_time=14:00, **When** check_reminders(), **Then** all 3 reminders are returned

### Reminder Dispatching

**Input**: Due reminders = [(1, "Weekly report"), (2, "Team meeting")]

**Expected Behavior**:
```python
# For console CLI (primary implementation)
for task_id, message in due_reminders:
    print(f"\n⏰ REMINDER: Task '{message}' due at 14:00")
```

**Test Cases**:
1. **Given** 2 due reminders, **When** check triggers, **Then** both are displayed
2. **Given** 0 due reminders, **When** check triggers, **Then** no reminder message is shown
3. **Given** 1 due reminder, **When** check triggers, **Then** reminder is displayed once (not duplicate)

---

## Timer Behavior

### Periodic Callback

**Input**: Timer with 60-second interval, `check_reminders()` callback

**Expected Behavior**:
```python
# Timer fires every 60 seconds
timer = threading.Timer(60.0, scheduler.check_reminders)

# In check_reminders():
due_reminders = get_due_reminders()
if due_reminders:
    dispatch(due_reminders)

# Timer re-arms itself for continuous checking
```

**Test Cases**:
1. **Given** timer started at 00:00:01, **When** 60 seconds elapse, **Then** check_reminders() is called
2. **Given** timer started at 00:00:00, **When** 60 seconds elapse, **Then** next check happens at 00:01:00
3. **Given** timer running, **When** check_reminders() takes 0.5 seconds, **Then** next check occurs at 00:02:00 (60-second interval maintained)

### Timer Lifecycle

**Test Cases**:
1. **Given** scheduler not started, **When** start() is called, **Then** timer begins periodic checks
2. **Given** scheduler running, **When** stop() is called, **Then** timer is canceled and no new checks occur
3. **Given** scheduler running, **When** Ctrl+C is pressed, **Then** stop() is called and timer cleanly stops

---

## Threading Safety

### Concurrent Access Protection

**Scenario**: Main thread adds reminder while background timer is checking

**Expected Behavior**:
```python
with scheduler._lock:
    # Critical section for reminder list access
    due_reminders = scheduler.check_reminders()
```

**Test Cases**:
1. **Given** timer checking reminders, **When** main thread adds reminder, **Then** no data race occurs
2. **Given** main thread reading reminders, **When** timer dispatches notifications, **Then** consistent view of reminders
3. **Given** stop() called during check, **When** lock is held, **Then** cleanup completes before next check

---

## Edge Cases

### Task Completed Before Reminder

**Scenario**: Task completed at 13:30, reminder scheduled for 14:00

**Expected Behavior**:
```python
# At 14:00, check_reminders() finds reminder
# But task.completed == True, so reminder is NOT dispatched
```

**Test Case**: **Given** completed task with reminder, **When** reminder time arrives, **Then** no notification is shown (per FR requirement)

### Multiple Reminders at Same Time

**Scenario**: 3 reminders all due at 14:00

**Expected Behavior**:
```python
# check_reminders() returns all 3 reminders
# Dispatch callback groups them for non-intrusive display
print("\n⏰ 3 REMINDERS DUE NOW:")
for task_id, message in reminders:
    print(f"  {task_id}. {message}")
```

**Test Case**: **Given** 3 reminders due at same time, **When** check triggers, **Then** all 3 are displayed together (per spec requirement)

### Reminder Time in Past

**Scenario**: System starts at 10:00, reminder was due at 09:00 (already passed)

**Expected Behavior**:
```python
# Reminder is due (reminder_time < current_time)
# Skip dispatching but mark as handled (don't show stale reminder)
reminder.status = ReminderStatus.DISMISSED
```

**Test Case**: **Given** reminder due in past, **When** scheduler checks, **Then** reminder is not displayed to user

### System Time Changes

**Scenario**: User adjusts system time forward by 2 hours during running app

**Expected Behavior**:
```python
# Next check uses updated system time (datetime.now())
# Reminders that were due before time change are handled naturally
# Future reminders trigger at correct absolute time
```

**Test Case**: **Given** reminder for 14:00, system time advances to 14:01, **When** next check occurs, **Then** reminder is now considered "missed" (due in past)

---

## Performance Requirements

- **Check Frequency**: 60 seconds between checks (balances accuracy and CPU usage per research.md)
- **Dispatch Latency**: < 100ms from reminder_time to actual display (per SC-004 accuracy goal)
- **Memory Overhead**: < 1KB for timer thread and reminder list (minimal)

---

## Error Handling

| Error Condition | Exception Type | Error Message |
|----------------|------------------|---------------|
| Timer already running | RuntimeError | "Scheduler is already running" |
| Invalid interval | ValueError | "check_interval must be between 10 and 3600 seconds" |
| Timer not started | RuntimeError | "Cannot stop scheduler: not running" |

---

## Console Notification Format

**Format**:
```text
⏰ REMINDER: Task '{task_title}' due at {time}

For multiple reminders:
⏰ 3 REMINDERS DUE NOW:
    {task_id}. {task_title}
    {task_id}. {task_title}
    {task_id}. {task_title}
```

**Rationale**:
- Emoji (⏰) provides visual prominence in terminal
- Clear grouping for multiple reminders (non-intrusive)
- Task ID included for reference

---

## Testability Requirements

1. **Unit test for reminder checking logic** with mocked datetime
2. **Unit test for timer lifecycle** (start/stop behavior)
3. **Unit test for threading safety** with concurrent operations
4. **Integration test with TaskManager** (reminders linked to tasks)
5. **Manual timing test** (create reminder due in 30 seconds, verify display)

---

## Integration Notes

This contract is designed to integrate with `TaskManager`:

```python
class TaskManager:
    def __init__(self) -> None:
        self._reminder_scheduler = ReminderScheduler(
            check_interval_seconds=60,
            dispatch_callback=self._dispatch_reminder
        )

    def _dispatch_reminder(self, task_id: int, message: str) -> None:
        # Called by scheduler when reminder triggers
        task = self.get_task(task_id)
        print(f"\n⏰ REMINDER: Task '{task.title}' due at {task.due_time}")

    def start_reminder_checks(self) -> None:
        """Called when app starts to begin background monitoring."""
        self._reminder_scheduler.start()
```

This separation allows ReminderScheduler to be unit-tested independently and supports different dispatch mechanisms (console vs browser).
