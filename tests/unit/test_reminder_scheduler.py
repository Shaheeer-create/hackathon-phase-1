"""Unit tests for ReminderScheduler class."""

import unittest
from datetime import datetime, timedelta
from time import sleep
from unittest.mock import patch

from src.models.recurrence import Reminder
from src.services.reminder_scheduler import ReminderScheduler


class MockReminder:
    """Mock reminder class for testing with past times."""

    def __init__(self, task_id: int, reminder_time: datetime, status: str = "scheduled"):
        self.task_id = task_id
        self.reminder_time = reminder_time
        self.status = status


class TestReminderScheduler(unittest.TestCase):
    """Test cases for ReminderScheduler class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.scheduler = ReminderScheduler(interval=0.1)  # Fast interval for testing

    def tearDown(self) -> None:
        """Clean up after tests."""
        if self.scheduler._running:
            self.scheduler.stop()

    def test_add_reminder(self) -> None:
        """Test adding a reminder to scheduler."""
        reminder = Reminder(
            task_id=1,
            reminder_time=datetime.now() + timedelta(seconds=1),
        )
        self.scheduler.add_reminder(reminder)

        self.assertEqual(len(self.scheduler.reminders), 1)
        self.assertEqual(self.scheduler.reminders[0].task_id, 1)

    def test_add_multiple_reminders(self) -> None:
        """Test adding multiple reminders."""
        reminder1 = Reminder(task_id=1, reminder_time=datetime.now() + timedelta(seconds=1))
        reminder2 = Reminder(task_id=2, reminder_time=datetime.now() + timedelta(seconds=2))
        reminder3 = Reminder(task_id=3, reminder_time=datetime.now() + timedelta(seconds=3))

        self.scheduler.add_reminder(reminder1)
        self.scheduler.add_reminder(reminder2)
        self.scheduler.add_reminder(reminder3)

        self.assertEqual(len(self.scheduler.reminders), 3)

    def test_check_reminders_no_due(self) -> None:
        """Test checking when no reminders are due."""
        # Add reminders for future
        reminder = Reminder(
            task_id=1,
            reminder_time=datetime.now() + timedelta(minutes=10),
        )
        self.scheduler.add_reminder(reminder)

        due = self.scheduler.check_reminders()
        self.assertEqual(len(due), 0)

    def test_check_reminders_due(self) -> None:
        """Test checking when reminders are due."""
        # Add reminders for past (due) - use mock to bypass validation
        reminder_due = MockReminder(
            task_id=1,
            reminder_time=datetime.now() - timedelta(seconds=1),
        )
        # Add reminder for future
        reminder_future = Reminder(
            task_id=2,
            reminder_time=datetime.now() + timedelta(minutes=10),
        )

        self.scheduler.add_reminder(reminder_due)
        self.scheduler.add_reminder(reminder_future)

        due = self.scheduler.check_reminders()
        self.assertEqual(len(due), 1)
        self.assertEqual(due[0].task_id, 1)

    def test_check_reminders_multiple_due(self) -> None:
        """Test checking when multiple reminders are due."""
        now = datetime.now()

        reminder1 = MockReminder(task_id=1, reminder_time=now - timedelta(seconds=5))
        reminder2 = MockReminder(task_id=2, reminder_time=now - timedelta(seconds=3))
        reminder3 = Reminder(task_id=3, reminder_time=now + timedelta(minutes=10))

        self.scheduler.add_reminder(reminder1)
        self.scheduler.add_reminder(reminder2)
        self.scheduler.add_reminder(reminder3)

        due = self.scheduler.check_reminders()
        self.assertEqual(len(due), 2)
        due_ids = [r.task_id for r in due]
        self.assertIn(1, due_ids)
        self.assertIn(2, due_ids)
        self.assertNotIn(3, due_ids)

    def test_start_stop_timer(self) -> None:
        """Test starting and stopping the background timer."""
        self.assertFalse(self.scheduler._running)

        self.scheduler.start()
        self.assertTrue(self.scheduler._running)

        self.scheduler.stop()
        self.assertFalse(self.scheduler._running)

    def test_start_already_running(self) -> None:
        """Test that starting when already running is safe."""
        self.scheduler.start()
        running_flag = self.scheduler._running
        timer_obj = self.scheduler._timer

        # Start again (should be no-op)
        self.scheduler.start()

        self.assertEqual(self.scheduler._running, running_flag)
        self.assertEqual(self.scheduler._timer, timer_obj)

    def test_stop_already_stopped(self) -> None:
        """Test that stopping when already stopped is safe."""
        self.assertFalse(self.scheduler._running)

        # Stop when not running (should be no-op)
        self.scheduler.stop()

        self.assertFalse(self.scheduler._running)

    def test_dispatch_reminder_prints_message(self) -> None:
        """Test that dispatch_reminder prints to console."""
        reminder = Reminder(
            task_id=1,
            reminder_time=datetime.now(),
        )

        # Use patch to capture print output
        with patch("builtins.print") as mock_print:
            self.scheduler._dispatch_reminder(reminder)

            # Verify print was called
            self.assertTrue(mock_print.called)
            output = str(mock_print.call_args)
            self.assertIn("REMINDER", output)
            self.assertIn("Task ID 1", output)

    @patch("builtins.print")
    def test_timer_dispatches_due_reminders(self, mock_print) -> None:
        """Test that timer triggers reminder dispatch."""
        # Add a due reminder (past time) - use mock to bypass validation
        reminder = MockReminder(
            task_id=1,
            reminder_time=datetime.now() - timedelta(seconds=1),
        )
        self.scheduler.add_reminder(reminder)

        # Start scheduler
        self.scheduler.start()

        # Wait for at least one check cycle
        sleep(0.2)

        # Stop scheduler
        self.scheduler.stop()

        # Verify dispatch was called
        self.assertTrue(mock_print.called)

    def test_clear_completed_reminders(self) -> None:
        """Test clearing reminders for completed tasks."""
        reminder1 = Reminder(
            task_id=1,
            reminder_time=datetime.now() + timedelta(minutes=10),
        )
        reminder2 = Reminder(
            task_id=2,
            reminder_time=datetime.now() + timedelta(minutes=10),
        )
        reminder3 = Reminder(
            task_id=3,
            reminder_time=datetime.now() + timedelta(minutes=10),
        )

        self.scheduler.add_reminder(reminder1)
        self.scheduler.add_reminder(reminder2)
        self.scheduler.add_reminder(reminder3)

        # Clear reminders for tasks 1 and 2
        self.scheduler.clear_completed_reminders([1, 2])

        self.assertEqual(len(self.scheduler.reminders), 1)
        self.assertEqual(self.scheduler.reminders[0].task_id, 3)

    def test_get_all_reminders(self) -> None:
        """Test getting all reminders."""
        reminder1 = Reminder(
            task_id=1,
            reminder_time=datetime.now() + timedelta(minutes=10),
        )
        reminder2 = Reminder(
            task_id=2,
            reminder_time=datetime.now() + timedelta(minutes=10),
        )

        self.scheduler.add_reminder(reminder1)
        self.scheduler.add_reminder(reminder2)

        all_reminders = self.scheduler.get_all_reminders()

        self.assertEqual(len(all_reminders), 2)
        self.assertEqual(all_reminders[0].task_id, 1)
        self.assertEqual(all_reminders[1].task_id, 2)

        # Verify it's a copy (modifying returned list doesn't affect scheduler)
        all_reminders.clear()
        self.assertEqual(len(self.scheduler.reminders), 2)

    def test_remove_reminder(self) -> None:
        """Test removing a specific reminder."""
        reminder = Reminder(
            task_id=1,
            reminder_time=datetime.now() + timedelta(minutes=10),
        )
        self.scheduler.add_reminder(reminder)

        # Remove reminder for task 1
        result = self.scheduler.remove_reminder(1)

        self.assertTrue(result)
        self.assertEqual(len(self.scheduler.reminders), 0)

    def test_remove_reminder_not_found(self) -> None:
        """Test removing a reminder that doesn't exist."""
        reminder = Reminder(
            task_id=1,
            reminder_time=datetime.now() + timedelta(minutes=10),
        )
        self.scheduler.add_reminder(reminder)

        # Try to remove reminder for task 999
        result = self.scheduler.remove_reminder(999)

        self.assertFalse(result)
        self.assertEqual(len(self.scheduler.reminders), 1)

    def test_thread_safety_add_reminder(self) -> None:
        """Test that adding reminders is thread-safe."""
        import threading

        def add_reminders(thread_id: int):
            for i in range(10):
                reminder = Reminder(
                    task_id=thread_id * 10 + i + 1,  # Ensure task_id >= 1
                    reminder_time=datetime.now() + timedelta(minutes=10),
                )
                self.scheduler.add_reminder(reminder)

        # Create multiple threads
        threads = [threading.Thread(target=add_reminders, args=(i,)) for i in range(5)]

        # Start all threads
        for t in threads:
            t.start()

        # Wait for all threads to finish
        for t in threads:
            t.join()

        # Should have exactly 50 reminders
        self.assertEqual(len(self.scheduler.reminders), 50)

    def test_custom_interval(self) -> None:
        """Test creating scheduler with custom interval."""
        scheduler = ReminderScheduler(interval=30)
        self.assertEqual(scheduler._interval, 30)

        scheduler.stop()


if __name__ == "__main__":
    unittest.main()
