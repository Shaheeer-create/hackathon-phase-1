"""Reminder scheduler for time-based task notifications."""

import threading
from datetime import datetime
from typing import List, Optional

from ..models.recurrence import Reminder


class ReminderScheduler:
    """Manages reminder scheduling and dispatch with background timer.

    Attributes:
        reminders: Internal list of active reminders
        _lock: Thread-safe lock for accessing reminders list
        _timer: Background timer for periodic reminder checking
        _running: Flag to control timer loop
        _interval: Check interval in seconds (default 60)
    """

    def __init__(self, interval: int = 60) -> None:
        """Initialize reminder scheduler.

        Args:
            interval: Check interval in seconds (default 60 seconds)
        """
        self.reminders: List[Reminder] = []
        self._lock = threading.Lock()
        self._timer: Optional[threading.Timer] = None
        self._running = False
        self._interval = interval

    def add_reminder(self, reminder: Reminder) -> None:
        """Add a reminder to the scheduler.

        Args:
            reminder: Reminder object to schedule
        """
        with self._lock:
            self.reminders.append(reminder)

    def check_reminders(self) -> List[Reminder]:
        """Check for due reminders and return them.

        Returns:
            List of reminders that are due (reminder_time <= now).

        Notes:
            This method does not modify the reminders list. Callers should
            handle reminder dispatch and cleanup as needed.
        """
        now = datetime.now()
        due_reminders = []

        with self._lock:
            for reminder in self.reminders:
                if reminder.reminder_time <= now:
                    due_reminders.append(reminder)

        return due_reminders

    def _schedule_next_check(self) -> None:
        """Schedule next reminder check."""
        if self._running:
            self._timer = threading.Timer(self._interval, self._check_and_reschedule)
            self._timer.daemon = True
            self._timer.start()

    def _check_and_reschedule(self) -> None:
        """Check reminders and reschedule next check."""
        due_reminders = self.check_reminders()

        # Dispatch notifications for due reminders
        for reminder in due_reminders:
            self._dispatch_reminder(reminder)

        # Schedule next check
        self._schedule_next_check()

    def _dispatch_reminder(self, reminder: Reminder) -> None:
        """Dispatch a reminder notification to console.

        Args:
            reminder: Reminder to dispatch
        """
        message = (
            f"\n[REMINDER] Task ID {reminder.task_id} is due!\n"
            f"Scheduled for: {reminder.reminder_time.strftime('%Y-%m-%d %H:%M')}\n"
        )
        print(message)

    def start(self) -> None:
        """Start the background reminder checking timer."""
        if self._running:
            return  # Already running

        self._running = True
        self._schedule_next_check()

    def stop(self) -> None:
        """Stop the background timer and cleanup."""
        if not self._running:
            return  # Already stopped

        self._running = False

        if self._timer is not None:
            self._timer.cancel()
            self._timer = None

    def clear_completed_reminders(
        self,
        completed_task_ids: List[int],
    ) -> None:
        """Remove reminders for completed tasks.

        Args:
            completed_task_ids: List of task IDs that were completed
        """
        with self._lock:
            self.reminders = [
                r
                for r in self.reminders
                if r.task_id not in completed_task_ids
            ]

    def get_all_reminders(self) -> List[Reminder]:
        """Get all reminders (thread-safe copy).

        Returns:
            Copy of the reminders list
        """
        with self._lock:
            return self.reminders.copy()

    def remove_reminder(self, task_id: int) -> bool:
        """Remove a reminder for a specific task.

        Args:
            task_id: ID of task whose reminder to remove

        Returns:
            True if reminder was removed, False if not found
        """
        with self._lock:
            for i, reminder in enumerate(self.reminders):
                if reminder.task_id == task_id:
                    self.reminders.pop(i)
                    return True
            return False
