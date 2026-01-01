"""Unit tests for recurrence models."""

import unittest
from datetime import datetime, timedelta

from src.models.recurrence import RecurrencePattern, RecurrenceRule, Reminder


class TestRecurrencePattern(unittest.TestCase):
    """Test cases for RecurrencePattern enum."""

    def test_pattern_values(self) -> None:
        """Test that all pattern values are correctly defined."""
        self.assertEqual(RecurrencePattern.DAILY.value, "daily")
        self.assertEqual(RecurrencePattern.WEEKLY.value, "weekly")
        self.assertEqual(RecurrencePattern.MONTHLY.value, "monthly")

    def test_pattern_str(self) -> None:
        """Test string representation of patterns."""
        self.assertEqual(str(RecurrencePattern.DAILY), "daily")
        self.assertEqual(str(RecurrencePattern.WEEKLY), "weekly")
        self.assertEqual(str(RecurrencePattern.MONTHLY), "monthly")


class TestRecurrenceRule(unittest.TestCase):
    """Test cases for RecurrenceRule dataclass."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.now = datetime.now()
        self.tomorrow = self.now + timedelta(days=1)

    def test_create_valid_rule(self) -> None:
        """Test creating a valid recurrence rule."""
        rule = RecurrenceRule(
            pattern=RecurrencePattern.DAILY,
            base_date=self.now,
            next_occurrence_date=self.tomorrow,
            max_instances=100,
        )
        self.assertEqual(rule.pattern, RecurrencePattern.DAILY)
        self.assertEqual(rule.base_date, self.now)
        self.assertEqual(rule.next_occurrence_date, self.tomorrow)
        self.assertEqual(rule.max_instances, 100)

    def test_default_max_instances(self) -> None:
        """Test that max_instances defaults to 100."""
        rule = RecurrenceRule(
            pattern=RecurrencePattern.WEEKLY,
            base_date=self.now,
            next_occurrence_date=self.tomorrow,
        )
        self.assertEqual(rule.max_instances, 100)

    def test_invalid_max_instances_too_low(self) -> None:
        """Test that max_instances < 1 raises ValueError."""
        with self.assertRaises(ValueError) as cm:
            RecurrenceRule(
                pattern=RecurrencePattern.DAILY,
                base_date=self.now,
                next_occurrence_date=self.tomorrow,
                max_instances=0,
            )
        self.assertIn("max_instances must be at least 1", str(cm.exception))

    def test_invalid_max_instances_too_high(self) -> None:
        """Test that max_instances > 100 raises ValueError."""
        with self.assertRaises(ValueError) as cm:
            RecurrenceRule(
                pattern=RecurrencePattern.DAILY,
                base_date=self.now,
                next_occurrence_date=self.tomorrow,
                max_instances=101,
            )
        self.assertIn("max_instances cannot exceed 100", str(cm.exception))

    def test_invalid_next_occurrence_in_past(self) -> None:
        """Test that next_occurrence_date in the past raises ValueError."""
        past_date = self.now - timedelta(days=1)
        with self.assertRaises(ValueError) as cm:
            RecurrenceRule(
                pattern=RecurrencePattern.DAILY,
                base_date=self.now,
                next_occurrence_date=past_date,
            )
        self.assertIn("next_occurrence_date cannot be in the past", str(cm.exception))

    def test_all_patterns_valid(self) -> None:
        """Test that all patterns can be used in a rule."""
        for pattern in RecurrencePattern:
            rule = RecurrenceRule(
                pattern=pattern,
                base_date=self.now,
                next_occurrence_date=self.tomorrow,
            )
            self.assertEqual(rule.pattern, pattern)

    def test_rule_immutability(self) -> None:
        """Test that RecurrenceRule is immutable (frozen dataclass)."""
        from dataclasses import FrozenInstanceError

        rule = RecurrenceRule(
            pattern=RecurrencePattern.DAILY,
            base_date=self.now,
            next_occurrence_date=self.tomorrow,
        )
        with self.assertRaises(FrozenInstanceError):  # frozen=True prevents assignment
            rule.max_instances = 50


class TestReminder(unittest.TestCase):
    """Test cases for Reminder dataclass."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.now = datetime.now()
        self.tomorrow = self.now + timedelta(days=1)

    def test_create_valid_reminder(self) -> None:
        """Test creating a valid reminder."""
        reminder = Reminder(
            task_id=1,
            reminder_time=self.tomorrow,
            status="scheduled",
            offset_hours=24,
        )
        self.assertEqual(reminder.task_id, 1)
        self.assertEqual(reminder.reminder_time, self.tomorrow)
        self.assertEqual(reminder.status, "scheduled")
        self.assertEqual(reminder.offset_hours, 24)

    def test_default_status(self) -> None:
        """Test that status defaults to 'scheduled'."""
        reminder = Reminder(
            task_id=1,
            reminder_time=self.tomorrow,
        )
        self.assertEqual(reminder.status, "scheduled")

    def test_default_offset_hours(self) -> None:
        """Test that offset_hours defaults to 24."""
        reminder = Reminder(
            task_id=1,
            reminder_time=self.tomorrow,
        )
        self.assertEqual(reminder.offset_hours, 24)

    def test_invalid_task_id_negative(self) -> None:
        """Test that negative task_id raises ValueError."""
        with self.assertRaises(ValueError) as cm:
            Reminder(
                task_id=-1,
                reminder_time=self.tomorrow,
            )
        self.assertIn("task_id must be positive", str(cm.exception))

    def test_invalid_task_id_zero(self) -> None:
        """Test that task_id=0 raises ValueError."""
        with self.assertRaises(ValueError) as cm:
            Reminder(
                task_id=0,
                reminder_time=self.tomorrow,
            )
        self.assertIn("task_id must be positive", str(cm.exception))

    def test_invalid_reminder_time_in_past(self) -> None:
        """Test that reminder_time in the past raises ValueError."""
        past_date = self.now - timedelta(hours=1)
        with self.assertRaises(ValueError) as cm:
            Reminder(
                task_id=1,
                reminder_time=past_date,
            )
        self.assertIn("reminder_time cannot be in the past", str(cm.exception))

    def test_invalid_offset_hours_negative(self) -> None:
        """Test that negative offset_hours raises ValueError."""
        with self.assertRaises(ValueError) as cm:
            Reminder(
                task_id=1,
                reminder_time=self.tomorrow,
                offset_hours=-1,
            )
        self.assertIn("offset_hours must be between 0 and 168", str(cm.exception))

    def test_invalid_offset_hours_too_high(self) -> None:
        """Test that offset_hours > 168 (7 days) raises ValueError."""
        with self.assertRaises(ValueError) as cm:
            Reminder(
                task_id=1,
                reminder_time=self.tomorrow,
                offset_hours=169,
            )
        self.assertIn("offset_hours must be between 0 and 168", str(cm.exception))

    def test_valid_offset_boundary_values(self) -> None:
        """Test that boundary offset values are accepted."""
        # 0 hours (immediate reminder)
        reminder_zero = Reminder(
            task_id=1,
            reminder_time=self.tomorrow,
            offset_hours=0,
        )
        self.assertEqual(reminder_zero.offset_hours, 0)

        # 168 hours (7 days)
        reminder_max = Reminder(
            task_id=1,
            reminder_time=self.tomorrow,
            offset_hours=168,
        )
        self.assertEqual(reminder_max.offset_hours, 168)

    def test_different_status_values(self) -> None:
        """Test different status values."""
        statuses = ["scheduled", "snoozed", "dismissed"]
        for status in statuses:
            reminder = Reminder(
                task_id=1,
                reminder_time=self.tomorrow,
                status=status,
            )
            self.assertEqual(reminder.status, status)

    def test_reminder_immutability(self) -> None:
        """Test that Reminder is immutable (frozen dataclass)."""
        from dataclasses import FrozenInstanceError

        reminder = Reminder(
            task_id=1,
            reminder_time=self.tomorrow,
        )
        with self.assertRaises(FrozenInstanceError):  # frozen=True prevents assignment
            reminder.status = "dismissed"


if __name__ == "__main__":
    unittest.main()
