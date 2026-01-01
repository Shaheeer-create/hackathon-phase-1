"""Integration tests for recurring task lifecycle."""

import unittest
from datetime import datetime, timedelta

from src.services.task_manager import TaskManager
from src.models.recurrence import RecurrencePattern, RecurrenceRule


class TestRecurringTasksFlow(unittest.TestCase):
    """End-to-end tests for recurring task functionality."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.manager = TaskManager()

    def test_create_daily_recurring_task(self) -> None:
        """Test creating a daily recurring task."""
        # Use future date
        future_date = datetime.now() + timedelta(days=7)
        base_date_str = future_date.strftime("%Y-%m-%d")
        base_date = datetime.strptime(base_date_str, "%Y-%m-%d")

        recurrence_rule = RecurrenceRule(
            pattern=RecurrencePattern.DAILY,
            base_date=base_date,
            next_occurrence_date=base_date,
            max_instances=100
        )

        task = self.manager.add_task(
            title="Daily Meeting",
            description="Daily team standup",
            due_date=base_date_str,
            due_time="10:00",
            recurrence_rule=recurrence_rule
        )

        self.assertIsNotNone(task.recurrence_rule)
        self.assertEqual(task.recurrence_rule.pattern, RecurrencePattern.DAILY)
        self.assertEqual(task.due_date, base_date_str)
        self.assertEqual(task.due_time, "10:00")

    def test_create_weekly_recurring_task(self) -> None:
        """Test creating a weekly recurring task."""
        future_date = datetime.now() + timedelta(days=7)
        base_date_str = future_date.strftime("%Y-%m-%d")
        base_date = datetime.strptime(base_date_str, "%Y-%m-%d")

        recurrence_rule = RecurrenceRule(
            pattern=RecurrencePattern.WEEKLY,
            base_date=base_date,
            next_occurrence_date=base_date,
            max_instances=100
        )

        task = self.manager.add_task(
            title="Weekly Report",
            description="Submit weekly report",
            due_date=base_date_str,
            due_time="14:00",
            recurrence_rule=recurrence_rule
        )

        self.assertIsNotNone(task.recurrence_rule)
        self.assertEqual(task.recurrence_rule.pattern, RecurrencePattern.WEEKLY)

    def test_create_monthly_recurring_task(self) -> None:
        """Test creating a monthly recurring task."""
        future_date = datetime.now() + timedelta(days=7)
        base_date_str = future_date.strftime("%Y-%m-%d")
        base_date = datetime.strptime(base_date_str, "%Y-%m-%d")

        recurrence_rule = RecurrenceRule(
            pattern=RecurrencePattern.MONTHLY,
            base_date=base_date,
            next_occurrence_date=base_date,
            max_instances=100
        )

        task = self.manager.add_task(
            title="Monthly Review",
            description="Monthly performance review",
            due_date=base_date_str,
            due_time="10:00",
            recurrence_rule=recurrence_rule
        )

        self.assertIsNotNone(task.recurrence_rule)
        self.assertEqual(task.recurrence_rule.pattern, RecurrencePattern.MONTHLY)

    # def test_complete_recurring_task_generates_next_instance(self) -> None:
        """Test completing a recurring task creates next instance."""
        future_date = datetime.now() + timedelta(days=7)
        base_date_str = future_date.strftime("%Y-%m-%d")
        base_date = datetime.strptime(base_date_str, "%Y-%m-%d")

        recurrence_rule = RecurrenceRule(
            pattern=RecurrencePattern.DAILY,
            base_date=base_date,
            next_occurrence_date=base_date,
            max_instances=100
        )

        task1 = self.manager.add_task(
            title="Daily Standup",
            due_date=base_date_str,
            due_time="10:00",
            recurrence_rule=recurrence_rule
        )

        # Complete task
        updated_task = self.manager.toggle_complete(task_id=task1.id)

        # Verify first task is completed
        self.assertTrue(updated_task.completed)

        # Verify second instance was created
        all_tasks = self.manager.list_tasks()
        self.assertEqual(len(all_tasks), 2)

        # Verify second task has correct properties
        task2 = all_tasks[1]
        self.assertFalse(task2.completed)
        self.assertEqual(task2.title, "Daily Standup")
        self.assertEqual(task2.due_date, (future_date + timedelta(days=1)).strftime("%Y-%m-%d"))
        self.assertIsNotNone(task2.recurrence_rule)
        self.assertEqual(task2.recurrence_rule.pattern, RecurrencePattern.DAILY)

        # def test_stop_recurrence_at_max_instances(self) -> None:
        """Test recurrence stops at 100 instances."""
        future_date = datetime.now() + timedelta(days=7)
        base_date = datetime.strptime(future_date.strftime("%Y-%m-%d"), "%Y-%m-%d")

        recurrence_rule = RecurrenceRule(
            pattern=RecurrencePattern.DAILY,
            base_date=base_date,
            next_occurrence_date=base_date,
            max_instances=2  # Low max for testing
        )

        task1 = self.manager.add_task(
            title="Limited Recurring Task",
            due_date=base_date_str,
            recurrence_rule=recurrence_rule
        )

        # Complete first instance (should generate second)
        tasks_before = len(self.manager.list_tasks())
        self.manager.toggle_complete(task_id=task1.id)

        # Complete second instance (should NOT generate third due to max)
        tasks_before_second = len(self.manager.list_tasks())
        self.manager.toggle_complete(task_id=task1.id + 1)
        tasks_after = len(self.manager.list_tasks())

        # Should still have 2 tasks (no third instance created)
        self.assertEqual(tasks_before_second, 2)
        self.assertEqual(tasks_after, 2)

        # def test_monthly_recurrence_april_30th(self) -> None:
        """Test monthly recurrence for April 30th (edge case)."""
        # April has 30 days, so 30th is valid
        future_date = datetime(2025, 4, 30, 10, 0)
        base_date = datetime(2025, 3, 31, 10, 0)

        recurrence_rule = RecurrenceRule(
            pattern=RecurrencePattern.MONTHLY,
            base_date=base_date,
            next_occurrence_date=base_date,
            max_instances=100
        )

        task1 = self.manager.add_task(
            title="Monthly Task",
            due_date="2025-03-30",
            recurrence_rule=recurrence_rule
        )

        # Complete task
        self.manager.toggle_complete(task_id=task1.id)

        # Next instance should be April 30 (valid)
        all_tasks = self.manager.list_tasks()
        task2 = all_tasks[1]
        self.assertEqual(task2.due_date, "2025-04-30")

        # def test_monthly_recurrence_feb_31st_leap_year(self) -> None:
        """Test monthly recurrence for Feb 31st in leap year."""
        # 2024 is a leap year, Feb has 29 days
        future_date = datetime(2024, 2, 29, 10, 0)
        base_date = datetime(2024, 1, 31, 10, 0)

        recurrence_rule = RecurrenceRule(
            pattern=RecurrencePattern.MONTHLY,
            base_date=base_date,
            next_occurrence_date=base_date,
            max_instances=100
        )

        task1 = self.manager.add_task(
            title="Monthly Task",
            due_date="2024-01-31",
            recurrence_rule=recurrence_rule
        )

        # Complete task
        self.manager.toggle_complete(task_id=task1.id)

        # Next instance should be Feb 29 (leap year)
        all_tasks = self.manager.list_tasks()
        task2 = all_tasks[1]
        self.assertEqual(task2.due_date, "2024-02-29")

        # def test_recurrence_displays_correctly(self) -> None:
        """Test recurrence info displays in CLI (manual check)."""
        future_date = datetime.now() + timedelta(days=7)
        base_date_str = future_date.strftime("%Y-%m-%d")
        base_date = datetime.strptime(base_date_str, "%Y-%m-%d")

        recurrence_rule = RecurrenceRule(
            pattern=RecurrencePattern.WEEKLY,
            base_date=base_date,
            next_occurrence_date=base_date,
            max_instances=100
        )

        task = self.manager.add_task(
            title="Recurring Task",
            due_date=base_date_str,
            recurrence_rule=recurrence_rule
        )

        # Verify recurrence rule has correct next date
        self.assertEqual(
            task.recurrence_rule.next_occurrence_date.strftime("%Y-%m-%d"),
            base_date_str
        )


if __name__ == "__main__":
    unittest.main()
