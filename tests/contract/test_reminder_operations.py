"""Contract tests for reminder operations."""

import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, Mock

from src.models.recurrence import Reminder
from src.services.reminder_scheduler import ReminderScheduler


class MockReminder:
    """Mock reminder class for testing with past times."""

    def __init__(self, task_id: int, reminder_time: datetime, status: str = "scheduled"):
        self.task_id = task_id
        self.reminder_time = reminder_time
        self.status = status


class TestReminderOperations(unittest.TestCase):
    """Contract tests validating reminder scheduler behavior."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.scheduler = ReminderScheduler(interval=0.1)

    def tearDown(self) -> None:
        """Clean up after tests."""
        if self.scheduler._running:
            self.scheduler.stop()

    def test_add_reminder(self) -> None:
        """Test storing reminders in scheduler."""
        future_time = datetime.now() + timedelta(minutes=5)
        reminder = MockReminder(
            task_id=1,
            reminder_time=future_time,
            status="scheduled"
        )

        self.scheduler.add_reminder(reminder)
        self.assertEqual(len(self.scheduler.reminders), 1)
        self.assertEqual(self.scheduler.reminders[0].task_id, 1)

    def test_check_reminders_due(self) -> None:
        """Test finding due reminders."""
        now = datetime.now()

        # Add due reminder (1 minute in past - use mock
        reminder_due = MockReminder(
            task_id=1,
            reminder_time=now - timedelta(minutes=1),
            status="scheduled"
        )

        # Add future reminder
        reminder_future = MockReminder(
            task_id=2,
            reminder_time=now + timedelta(minutes=5),
            status="scheduled"
        )

        self.scheduler.add_reminder(reminder_due)
        self.scheduler.add_reminder(reminder_future)

        # Check for due reminders
        due = self.scheduler.check_reminders()

        self.assertEqual(len(due), 1)
        self.assertEqual(due[0].task_id, 1)

    def test_check_reminders_not_due(self) -> None:
        """Test checking when no reminders are due."""
        now = datetime.now()

        # Add future reminders only
        reminder1 = MockReminder(
            task_id=1,
            reminder_time=now + timedelta(minutes=5),
            status="scheduled"
        )
        reminder2 = MockReminder(
            task_id=2,
            reminder_time=now + timedelta(minutes=10),
            status="scheduled"
        )

        self.scheduler.add_reminder(reminder1)
        self.scheduler.add_reminder(reminder2)

        # Check for due reminders
        due = self.scheduler.check_reminders()

        self.assertEqual(len(due), 0)

    @patch("builtins.print")
    def test_dispatch_notification(self, mock_print) -> None:
        """Test console output format for notifications."""
        reminder = MockReminder(
            task_id=1,
            reminder_time=datetime(2025, 1, 15, 10, 0),
            status="scheduled"
        )

        self.scheduler._dispatch_reminder(reminder)

        # Verify print was called
        self.assertTrue(mock_print.called)
        output = str(mock_print.call_args)
        self.assertIn("REMINDER", output)
        self.assertIn("Task ID 1", output)

    def test_timer_lifecycle(self) -> None:
        """Test start and stop behavior."""
        self.assertFalse(self.scheduler._running)

        self.scheduler.start()
        self.assertTrue(self.scheduler._running)

        self.scheduler.stop()
        self.assertFalse(self.scheduler._running)

    def test_multiple_reminders_same_time(self) -> None:
        """Test multiple reminders triggering simultaneously."""
        now = datetime.now()

        # Add 3 reminders all due now - use mock
        for i in range(1, 4):
            reminder = MockReminder(
                task_id=i,
                reminder_time=now - timedelta(seconds=10),
                status="scheduled"
            )
            self.scheduler.add_reminder(reminder)

        # Check for due reminders
        due = self.scheduler.check_reminders()

        self.assertEqual(len(due), 3)
        due_ids = [r.task_id for r in due]
        self.assertEqual(due_ids, [1, 2, 3])

    def test_clear_completed_reminders(self) -> None:
        """Test clearing reminders for completed tasks."""
        now = datetime.now()

        # Add reminders for tasks 1, 2, 3
        for i in range(1, 4):
            reminder = MockReminder(
                task_id=i,
                reminder_time=now + timedelta(minutes=5),
                status="scheduled"
            )
            self.scheduler.add_reminder(reminder)

        # Clear reminders for tasks 1 and 2
        self.scheduler.clear_completed_reminders([1, 2])

        # Should only have reminder for task 3
        self.assertEqual(len(self.scheduler.reminders), 1)
        self.assertEqual(self.scheduler.reminders[0].task_id, 3)

    def test_get_all_reminders(self) -> None:
        """Test getting all reminders returns copy."""
        now = datetime.now()

        reminder = MockReminder(
            task_id=1,
            reminder_time=now + timedelta(minutes=5),
            status="scheduled"
        )

        self.scheduler.add_reminder(reminder)

        # Get all reminders
        all_reminders = self.scheduler.get_all_reminders()

        # Verify it's a copy
        self.assertEqual(len(all_reminders), 1)
        self.assertEqual(all_reminders[0].task_id, 1)

        # Modify returned list
        all_reminders.clear()

        # Original should be unaffected
        self.assertEqual(len(self.scheduler.reminders), 1)

    def test_remove_reminder(self) -> None:
        """Test removing a specific reminder."""
        now = datetime.now()

        reminder1 = MockReminder(
            task_id=1,
            reminder_time=now + timedelta(minutes=5),
            status="scheduled"
        )
        reminder2 = MockReminder(
            task_id=2,
            reminder_time=now + timedelta(minutes=10),
            status="scheduled"
        )

        self.scheduler.add_reminder(reminder1)
        self.scheduler.add_reminder(reminder2)

        # Remove reminder for task 1
        result = self.scheduler.remove_reminder(1)

        self.assertTrue(result)
        self.assertEqual(len(self.scheduler.reminders), 1)
        self.assertEqual(self.scheduler.reminders[0].task_id, 2)

    def test_remove_reminder_not_found(self) -> None:
        """Test removing reminder that doesn't exist."""
        now = datetime.now()

        reminder = MockReminder(
            task_id=1,
            reminder_time=now + timedelta(minutes=5),
            status="scheduled"
        )

        self.scheduler.add_reminder(reminder)

        # Try to remove non-existent reminder
        result = self.scheduler.remove_reminder(999)

        self.assertFalse(result)
        self.assertEqual(len(self.scheduler.reminders), 1)

    def test_custom_interval(self) -> None:
        """Test creating scheduler with custom interval."""
        scheduler = ReminderScheduler(interval=30)
        self.assertEqual(scheduler._interval, 30)
        scheduler.stop()


if __name__ == "__main__":
    unittest.main()
