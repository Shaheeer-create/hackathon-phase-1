"""Recurrence engine for calculating next occurrence dates."""

import calendar
from datetime import datetime, timedelta
from typing import Optional

from ..models.recurrence import RecurrencePattern
from ..models.task import Task


def calculate_next_occurrence(
    current_date: datetime,
    pattern: RecurrencePattern,
    base_date: datetime,
    max_instances: int,
    current_count: int
) -> datetime:
    """
    Calculate next occurrence date based on recurrence pattern.

    Args:
        current_date: The due date of just-completed task instance
        pattern: Recurrence pattern (daily/weekly/monthly)
        base_date: The original due date that anchors recurrence cycle
        max_instances: Maximum number of instances allowed (from spec, FR-015)
        current_count: Number of instances already generated for this recurring task

    Returns:
        datetime: The due date for next task instance

    Raises:
        ValueError: If next occurrence would exceed max_instances limit
        ValueError: If pattern is not recognized
    """
    # Check max instances limit before calculating
    if current_count + 1 > max_instances:
        raise ValueError(
            f"Cannot create next instance: maximum {max_instances} instances reached"
        )

    # Calculate based on pattern
    if pattern == RecurrencePattern.DAILY:
        next_date = _next_daily(current_date)
    elif pattern == RecurrencePattern.WEEKLY:
        next_date = _next_weekly(current_date)
    elif pattern == RecurrencePattern.MONTHLY:
        next_date = _next_monthly(current_date, base_date)
    else:
        raise ValueError(
            f"Invalid recurrence pattern. Expected: daily, weekly, or monthly"
        )

    return next_date


def _next_daily(current_date: datetime) -> datetime:
    """Calculate next occurrence for daily recurrence (current_date + 1 day)."""
    return current_date + timedelta(days=1)


def _next_weekly(current_date: datetime) -> datetime:
    """Calculate next occurrence for weekly recurrence (current_date + 7 days)."""
    return current_date + timedelta(weeks=1)


def _next_monthly(current_date: datetime, base_date: datetime) -> datetime:
    """
    Calculate next occurrence for monthly recurrence.

    Handles edge case where target day doesn't exist in month
    (e.g., February 30th → falls back to February 28th/29th).
    """
    # Move to first day of next month
    next_month = current_date.replace(day=1) + timedelta(days=32)
    next_month = next_month.replace(day=1)

    # Get last valid day of target month
    _, last_day = calendar.monthrange(next_month.year, next_month.month)

    # Use current day if valid, otherwise use last day
    target_day = min(base_date.day, last_day)

    return next_month.replace(day=target_day)
