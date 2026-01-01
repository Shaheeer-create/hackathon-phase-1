# Contract: Recurrence Engine

**Feature**: Recurring Tasks and Reminders
**Date**: 2026-01-01
**Status**: Complete

## Purpose

Define contract for recurrence engine that calculates next occurrence dates for daily, weekly, and monthly recurring tasks. This component is responsible for implementing requirement FR-005 ("System MUST calculate next occurrence dates based on recurrence pattern") and FR-015 ("System MUST prevent generating more than 100 instances").

---

## Interface

### Function: `calculate_next_occurrence()`

```python
def calculate_next_occurrence(
    current_date: datetime,
    pattern: RecurrencePattern
    base_date: datetime
    max_instances: int,
    current_count: int
) -> datetime:
    """
    Calculate the next occurrence date based on recurrence pattern.

    Args:
        current_date: The due date of the just-completed task instance
        pattern: Recurrence pattern (daily/weekly/monthly)
        base_date: The original due date that anchors the recurrence cycle
        max_instances: Maximum number of instances allowed (from spec, FR-015)
        current_count: Number of instances already generated for this recurring task

    Returns:
        datetime: The due date for the next task instance

    Raises:
        ValueError: If next occurrence would exceed max_instances limit
        ValueError: If pattern is not recognized
    """
    pass
```

---

## Behavioral Contracts

### Daily Recurrence

**Input**: Current date = 2025-01-15 14:00, Pattern = DAILY

**Expected Output**:
```python
# Single day added to current date
next_occurrence = 2025-01-16 14:00
```

**Test Cases**:
1. **Given** current_date = 2025-01-15, **When** pattern = DAILY, **Then** next = 2025-01-16
2. **Given** current_date = 2025-12-31 23:59, **When** pattern = DAILY, **Then** next = 2026-01-01 00:00
3. **Given** current_date = leap year (2024-02-28), **When** pattern = DAILY, **Then** next = 2024-02-29

**Edge Cases**:
- Year boundary rollover: December 31st → January 1st correctly handles month/year increment
- Leap year handling: February 28th in non-leap → March 1st; February 28th in leap → February 29th

### Weekly Recurrence

**Input**: Current date = 2025-01-15 14:00, Pattern = WEEKLY

**Expected Output**:
```python
# Seven days added to current date
next_occurrence = 2025-01-22 14:00
```

**Test Cases**:
1. **Given** current_date = 2025-01-01 (Wednesday), **When** pattern = WEEKLY, **Then** next = 2025-01-08 (Wednesday)
2. **Given** current_date = 2025-01-06, **When** pattern = WEEKLY, **Then** next = 2025-01-13
3. **Given** current_date = 2025-12-29, **When** pattern = WEEKLY, **Then** next = 2026-01-05

**Edge Cases**:
- Month boundary rollover: January 28th → February 4th correctly handles month/year increment
- Day of week preservation: Maintains same weekday as `base_date`

### Monthly Recurrence

**Input**: Current date = 2025-01-15 14:00, Pattern = MONTHLY, Base Date = 2025-01-15

**Expected Output**:
```python
# One month added to current date, with last-day fallback for invalid days
next_occurrence = 2025-02-15 14:00
```

**Test Cases**:
1. **Given** current_date = 2025-01-15 (15th), **When** pattern = MONTHLY, **Then** next = 2025-02-15
2. **Given** current_date = 2025-01-30, **When** pattern = MONTHLY, **Then** next = 2025-02-28 (last valid day of February)
3. **Given** current_date = 2024-01-31, **When** pattern = MONTHLY, **Then** next = 2024-02-29 (leap year)
4. **Given** current_date = 2023-01-31, **When** pattern = MONTHLY, **Then** next = 2023-02-28 (non-leap year)

**Edge Cases** (per spec requirement):
- February 30th → Falls back to February 28th (non-leap) or 29th (leap)
- February 31st → Falls back to February 28th/29th
- April 31st → Remains April 31st (valid day)
- Year boundary rollover: December 15th → January 15th correctly handles month/year increment

---

## Max Instances Enforcement

**Requirement**: FR-015 ("System MUST prevent generating more than 100 instances")

**Behavior**:
```python
# Before calculating next occurrence
if current_count + 1 > max_instances:
    raise ValueError(
        f"Cannot create next instance: maximum {max_instances} instances reached"
    )
```

**Test Cases**:
1. **Given** current_count = 99, max_instances = 100, **When** calculating next, **Then** succeeds (returns next date)
2. **Given** current_count = 100, max_instances = 100, **When** calculating next, **Then** raises ValueError
3. **Given** current_count = 101, max_instances = 100, **When** calculating next, **Then** raises ValueError (should't reach this state)

---

## Algorithm Specification

### Daily Recurrence Algorithm

```python
def _next_daily(current_date: datetime) -> datetime:
    return current_date + timedelta(days=1)
```

**Complexity**: O(1) - simple timedelta addition

### Weekly Recurrence Algorithm

```python
def _next_weekly(current_date: datetime) -> datetime:
    return current_date + timedelta(weeks=1)
```

**Complexity**: O(1) - simple timedelta addition

### Monthly Recurrence Algorithm with Last-Day Fallback

```python
from datetime import datetime, timedelta
import calendar

def _next_monthly(current_date: datetime) -> datetime:
    # Move to first day of next month
    next_month = current_date.replace(day=1) + timedelta(days=32)
    next_month = next_month.replace(day=1)

    # Get last valid day of target month
    _, last_day = calendar.monthrange(next_month.year, next_month.month)

    # Use current day if valid, otherwise last day
    target_day = min(current_date.day, last_day)

    return next_month.replace(day=target_day)
```

**Complexity**: O(1) - `calendar.monthrange()` is O(1) lookup

**Rationale**: Uses `calendar.monthrange()` per research.md recommendation for robust invalid date handling.

---

## Error Handling

| Error Condition | Exception Type | Error Message |
|----------------|------------------|---------------|
| Invalid pattern | ValueError | "Invalid recurrence pattern. Expected: daily, weekly, or monthly" |
| Max instances exceeded | ValueError | "Cannot create next instance: maximum {max_instances} instances reached" |
| Negative max_instances | ValueError | "max_instances must be positive" |

---

## Performance Requirements

- **Calculation Time**: All recurrence calculations must complete in < 1ms (per performance goal SC-002)
- **Predictable Runtime**: O(1) for all pattern types (simple timedelta + calendar.monthrange lookup)

---

## Testability Requirements

Each function must be independently testable with unit tests:

1. **Test daily recurrence** across various dates (month boundaries, leap years)
2. **Test weekly recurrence** across month boundaries
3. **Test monthly recurrence** with valid and invalid target days (February 30th)
4. **Test max instances enforcement** at boundary values (99, 100, 101)
5. **Test all patterns** with time component preservation (14:00 → 14:00)

---

## Integration Notes

This contract is designed to integrate with `TaskManager` via:

```python
# In TaskManager.toggle_complete()
if task.recurrence_rule:
    try:
        next_date = calculate_next_occurrence(
            task.due_date_as_datetime,
            task.recurrence_rule.pattern,
            task.recurrence_rule.base_date,
            task.recurrence_rule.max_instances,
            current_count
        )
        # Create new task instance
        self.add_task(
            title=task.title,
            description=task.description,
            due_date=next_date.strftime("%Y-%m-%d"),
            due_time=task.due_time,
            priority=task.priority,
            tags=task.tags,
            recurrence_rule=task.recurrence_rule
        )
    except ValueError as e:
        print(f"Error: {e}")
```

This separation allows recurrence engine to be unit-tested independently from TaskManager logic.
