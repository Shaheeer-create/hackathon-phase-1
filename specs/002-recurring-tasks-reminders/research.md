# Research: Recurring Tasks and Reminders

**Feature**: Recurring Tasks and Reminders (002-recurring-tasks-reminders)
**Date**: 2026-01-01
**Status**: Complete

## Research Summary

Investigated technical approaches for implementing recurring tasks with automatic rescheduling and time-based deadline reminders for CLI-based Todo application. Research focused on storage strategies, scheduling mechanisms, notification delivery, and edge case handling.

---

## Research Topic 1: Recurrence Rule Storage Strategy

### Question
Should recurrence rules be stored as task metadata or by generating all future task instances upfront?

### Investigation
Evaluated two approaches:

**Option A: Store Recurrence Rules per Task (RECOMMENDED)**
- Store `RecurrenceRule` object with each task containing: `pattern_type` (daily/weekly/monthly), `base_date`, `next_occurrence_date`, `max_instances`
- When task is completed, calculate `next_occurrence_date` and generate new task instance
- Existing completed tasks remain in memory for historical tracking
- **Pros**:
  - Storage efficient: Only one rule per task instead of hundreds of pre-generated instances
  - Flexible: Rules can be modified and propagate to all future instances
  - Aligns with spec requirement FR-002: "automatically generate new task instances when a recurring task is completed"
  - Prevents duplicates more reliably (FR-003)
- **Cons**:
  - Calculation overhead: Must calculate next date on each task completion
  - Complexity: Requires separate recurrence engine module

**Option B: Pre-generate Future Task Instances**
- Generate all task instances upfront (e.g., generate 52 weekly instances for a year)
- Store as individual tasks with pre-calculated due dates
- **Pros**:
  - Simple: No runtime calculation needed
  - Predictable: All future instances exist immediately
- **Cons**:
  - Storage inefficient: Hundreds of unnecessary task instances
  - Rigid: Rules cannot be modified without regenerating all future instances
  - Duplicate risk: Higher chance of creating duplicate instances if generation logic has bugs
  - Violates FR-007 requirement for easy pattern modification

### Decision
**Recommendation: Option A - Store Recurrence Rules per Task**

This approach aligns with spec requirements (FR-002 for auto-generation at completion, FR-007 for easy pattern modification), provides storage efficiency, and is more maintainable. The calculation overhead is negligible (single date addition per completion).

---

## Research Topic 2: Reminder Scheduling Mechanism

### Question
Should reminders use a system time polling loop or scheduled background timers?

### Investigation
Evaluated three Python timing approaches for CLI applications:

**Option A: `threading.Timer` with Periodic Callback (RECOMMENDED)**
- Create a background thread with `threading.Timer` that fires every N seconds
- Timer callback checks for due reminders and dispatches notifications
- **Pros**:
  - Accurate: Timer fires at exact intervals, minimal drift
  - Non-blocking: Main CLI loop remains responsive
  - Platform independent: Works on all platforms with Python standard library
  - Resource efficient: Thread sleeps between checks
- **Cons**:
  - Threading complexity: Requires thread-safe access to task list if concurrent modifications allowed
  - Shutdown complexity: Must cleanly stop timer on app exit

**Option B: `time.sleep` Polling Loop (NOT RECOMMENDED)**
- In main CLI loop, call `time.sleep(60)` to pause for 60 seconds
- Wake up and check for due reminders
- **Pros**:
  - Simple: No threading, sequential execution
  - Easy to reason about: No race conditions
- **Cons**:
  - Blocking: Cannot check reminders during long-running operations
  - Less accurate: Checks only at 60-second intervals, not exact trigger times
  - Poor UX: CLI feels unresponsive during sleep periods
  - Violates SC-004 (99% on-time accuracy)

**Option C: External Scheduler (APScheduler, schedule)**
- Use `schedule` library to define recurring reminder checks
- **Pros**:
  - Clean API: `schedule.every().day.at("14:00").do(check_reminders)`
  - Accurate: Library handles timing precisely
- **Cons**:
  - External dependency: Violates constitution "Python standard library only" rule
  - Over-engineered: For simple CLI use case

### Decision
**Recommendation: Option A - `threading.Timer` with Periodic Callback**

This approach meets SC-004 (99% on-time accuracy) by firing at exact intervals, provides non-blocking behavior for CLI, uses only Python standard library (constitution compliant), and is appropriate for CLI complexity. The threading complexity is manageable with proper locking or single-threaded CLI operations.

**Implementation Note**:
- Poll interval: 60 seconds (balances accuracy and CPU usage)
- Timer behavior: Re-arm timer after each check to maintain periodicity
- Shutdown: Store timer reference and cancel on app exit (Ctrl+C handling)

---

## Research Topic 3: Browser Notification Integration

### Question
How to trigger browser notifications from a Python CLI or simple web app?

### Investigation
Evaluated notification mechanisms for browser-based constraints:

**For CLI Environment (Primary)**
- **Reality**: Python CLI running in terminal cannot trigger browser notifications directly
- **Approach**: Display reminders as console text messages (e.g., "\n⏰ REMINDER: Task 'Meeting' due at 14:00")
- **Pros**:
  - Simple: No cross-process communication needed
  - Universal: Works on all platforms with terminal
- **Cons**:
  - Limited visibility: User must be looking at terminal to see reminder
  - No persistence: Missed reminders if user closed terminal

**For Web/Browser Environment (Optional/Secondary)**
If extending to web deployment later, browser notification options include:

**Option A: Notification API (RECOMMENDED for Web)**
- Use `Notification` API built into modern browsers
- `new Notification("Task Reminder", {body: "Meeting due at 14:00", icon: "/icon.png"})`
- **Pros**:
  - Standard API: Supported in Chrome, Firefox, Safari, Edge
  - Native feel: Uses OS notification system
  - Permission control: Browser manages notification preferences
- **Cons**:
  - Requires HTTPS for Notification API (not HTTP)
  - Requires user interaction to request permission first

**Option B: WebSocket/Server-Sent Events**
- Browser maintains WebSocket connection to server
- Server sends notification when reminder time arrives
- **Pros**:
  - Real-time: Can trigger at exact time
  - Flexible: Can handle complex notification logic server-side
- **Cons**:
  - Complex: Requires WebSocket server implementation
  - Over-engineered: For current CLI-only scope

### Decision
**For Current Scope**: Use CLI Console Notifications (SIMPLEST)**

Spec constraint "Platform Limitations: Browser notifications only" is interpreted as "browser notifications are the maximum capability, but CLI text notifications are acceptable baseline." Console notifications align with existing architecture and are sufficient for Phase 2 implementation.

**Implementation Note**:
- Format: Clear, prominent reminder messages with task ID and title
- Timing: Trigger at exact reminder time (based on `threading.Timer` research)
- UX: Flash terminal bell or visual marker (if platform supports) to draw attention

**Future Enhancement Path**: If web deployment is added, integrate Notification API per Option A.

---

## Research Topic 4: Date and Time Parsing

### Question
What's the best approach for parsing combined date-time strings (YYYY-MM-DD HH:MM)?

### Investigation
Evaluated Python `datetime` parsing strategies:

**Option A: `datetime.strptime()` with Format String (RECOMMENDED)**
- Use `datetime.strptime(date_str, "%Y-%m-%d %H:%M")` to parse combined format
- Extract date and time components separately
- **Pros**:
  - Precise: Exact format control, no ambiguity
  - Error handling: Raises `ValueError` for invalid formats immediately
  - Timezone aware: Can add timezone if needed later
- **Cons**:
  - Strict format: User must enter exactly YYYY-MM-DD HH:MM or parsing fails

**Option B: Parse Date and Time Separately**
- Prompt user for date and time in separate inputs
- Combine with `datetime.combine()`
- **Pros**:
  - Flexible: Can handle different input formats
  - Better UX: Can validate each field separately
- **Cons**:
  - Complex: Multiple prompts, more code paths
  - Violates spec requirement "Users MUST be able to specify due dates and times for tasks (format: YYYY-MM-DD HH:MM)" - this implies single string format

**Option C: `dateutil.parser`**
- Use `dateutil` library to parse natural language dates
- **Pros**:
  - Flexible: Parses "tomorrow at 2pm", "next Monday", etc.
- **Cons**:
  - External dependency: Violates constitution "standard library only"
  - Over-engineered: Spec clearly defines YYYY-MM-DD HH:MM format

### Decision
**Recommendation: Option A - `datetime.strptime()` with Format String**

Strict format parsing aligns with spec requirement FR-004, uses only Python standard library (constitution compliant), and provides immediate error feedback for invalid formats.

**Implementation Note**:
- Validation function: `is_valid_datetime(date_time_str: str) -> bool`
- Error message: "Invalid datetime format. Expected YYYY-MM-DD HH:MM (e.g., 2025-01-15 14:00)"
- Format validation: Regex `r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$"` for pre-check

---

## Research Topic 5: Recurrence Edge Case Handling

### Question
How to handle invalid dates in monthly recurrence (e.g., February 30th)?

### Investigation
Evaluated Python `datetime` calendar handling for invalid dates:

**Algorithm for Monthly Recurrence with Day-Target**

```python
import calendar
from datetime import datetime, timedelta

def calculate_next_monthly(current_date: datetime, target_day: int) -> datetime:
    # Calculate next month
    next_month = current_date.replace(day=1) + timedelta(days=32)  # Next month
    next_month = next_month.replace(day=1)  # First day of next month

    # Get last valid day of next month
    _, last_day = calendar.monthrange(next_month.year, next_month.month)

    # If target day exists, use it; otherwise use last day
    actual_day = min(target_day, last_day)

    return next_month.replace(day=actual_day)
```

**Edge Cases Covered**:
1. **February 30th**: Falls back to February 28th or 29th (leap year)
2. **February 31st**: Falls back to February 28th/29th
3. **April 31st**: Works (April has 31 days)
4. **Leap Year Handling**: `calendar.monthrange()` accounts for leap years automatically

**Pros**:
- Robust: Handles all invalid day combinations
- Simple: Uses only `calendar.monthrange()` from standard library
- Maintainable: Easy to understand and test
- **Aligns with spec**: Edge case explicitly mentioned in spec ("Use last valid day of month")

**Cons**:
- Calculation overhead: Slight performance cost vs simple `+ timedelta(days=30)`
- Edge case for January: If current is December, correctly wraps to next year

### Decision
**Recommendation: Calendar Month-Range Algorithm with Last-Day Fallback**

Use `calendar.monthrange()` approach to handle all invalid date scenarios. This is robust, uses only standard library, and directly addresses spec edge case requirement.

---

## Research Topic 6: Multi-Reminder Handling

### Question
What happens when multiple reminders trigger at the same time?

### Investigation
Evaluated notification strategies for concurrent reminders:

**Scenario**: 3 tasks with reminders all set for 14:00 - timer fires at 14:00:01

**Option A: Display All Together (RECOMMENDED)**
- Collect all due reminders in single check cycle
- Display as grouped message: "\n⏰ 3 REMINDERS DUE NOW:"
- List each task on separate line with indentation
- **Pros**:
  - Complete: User sees all reminders at once
  - Non-intrusive: Single notification burst instead of 3 separate notifications
  - Simple: Single code path for batch display
- **Cons**:
  - Terminal clutter: Multiple lines of output at once

**Option B: Sequential with Delay**
- Display first reminder, wait 2 seconds, display second, wait 2 seconds, display third
- **Pros**:
  - Less clutter: Easier to read each reminder
- **Cons**:
  - Long duration: Takes 6+ seconds to show all 3 reminders
  - Misses timeliness: Later reminders fire later than actual due time
  - Violates "non-intrusive" constraint

**Option C: Most Important First**
- Sort reminders by priority (High > Medium > Low)
- Display only highest priority, defer others until 60 seconds later
- **Pros**:
  - Minimal: Only shows what's most urgent
- **Cons**:
  - Misses deadlines: Low-priority reminders delayed
  - Violates "all reminders must be shown" requirement

### Decision
**Recommendation: Option A - Display All Together**

Grouped display aligns with spec requirements ("all due reminders are displayed together without overwhelming user"), is non-intrusive (single notification), and is simple to implement. Terminal clutter is acceptable for this edge case.

**Implementation Note**:
- Format: Use emoji + count + newline to group, then indent each task
- Example:
  ```
  ⏰ 3 REMINDERS DUE NOW:
    1. [HIGH] Weekly report
    2. [MEDIUM] Team meeting
    3. [LOW] Buy groceries
  ```

---

## Summary of Technical Decisions

| Decision Area | Chosen Approach | Rationale |
|----------------|---------------|----------|
| Recurrence Storage | Store rules per task, generate instances on completion | Storage efficient, supports rule modification, prevents duplicates |
| Reminder Scheduling | `threading.Timer` with 60-second polling | 99% accuracy, non-blocking, standard library only |
| Notifications (CLI) | Console text messages during CLI runtime | Simple, universal, sufficient for current scope |
| Date/Time Parsing | `datetime.strptime()` with strict format | Spec-compliant, immediate error feedback |
| Invalid Date Handling | `calendar.monthrange()` with last-day fallback | Robust for all invalid day combinations |
| Multi-Reminder Display | Grouped display in single notification | Non-intrusive, complete, aligns with spec |

## Implementation Notes

1. **Threading Safety**: If CLI allows concurrent task modifications (e.g., background reminder timer while user types command), implement `threading.Lock()` for task list access
2. **Performance**: Recurrence calculation is O(1) (simple date addition) - negligible overhead per completion
3. **Scalability**: With 100-instance limit, maximum active recurring tasks = manageable; memory impact minimal
4. **Testing Strategy**:
   - Unit tests for each recurrence pattern (daily, weekly, monthly)
   - Integration test for "create → complete → next instance appears" flow
   - Manual timer test: Create task due in 30 seconds, verify reminder triggers
5. **Constitution Compliance**:
   - All designs use Python standard library only (`datetime`, `calendar`, `threading`, `dataclasses`)
   - MVC architecture maintained (model: RecurrenceRule, controller: recurrence_engine)
   - Test-first approach emphasized (test each algorithm before use)

## Open Questions (Deferred to Planning)

None identified. All research topics have clear, documented recommendations aligned with spec requirements.
