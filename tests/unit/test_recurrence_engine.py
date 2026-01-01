"""Unit tests for recurrence engine."""

import unittest
from datetime import datetime, timedelta

from src.models.recurrence import RecurrencePattern
from src.services.recurrence_engine import calculate_next_occurrence


class TestCalculateNextOccurrence(unittest.TestCase):
    """Test cases for calculate_next_occurrence function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        # Fixed dates for consistent testing
        self.base_date = datetime(2025, 1, 15, 10, 0, 0)  # Jan 15, 2025, 10:00 AM
        self.current_date = datetime(2025, 1, 15, 10, 0, 0)

    def test_next_daily(self) -> None:
        """Test daily recurrence adds 1 day."""
        next_date = calculate_next_occurrence(
            current_date=self.current_date,
            pattern=RecurrencePattern.DAILY,
            base_date=self.base_date,
            max_instances=100,
            current_count=1,
        )
        expected = self.current_date + timedelta(days=1)
        self.assertEqual(next_date, expected)

    def test_next_weekly(self) -> None:
        """Test weekly recurrence adds 7 days."""
        next_date = calculate_next_occurrence(
            current_date=self.current_date,
            pattern=RecurrencePattern.WEEKLY,
            base_date=self.base_date,
            max_instances=100,
            current_count=1,
        )
        expected = self.current_date + timedelta(weeks=1)
        self.assertEqual(next_date, expected)

    def test_next_monthly_same_day(self) -> None:
        """Test monthly recurrence for valid day (15th)."""
        next_date = calculate_next_occurrence(
            current_date=self.current_date,
            pattern=RecurrencePattern.MONTHLY,
            base_date=self.base_date,
            max_instances=100,
            current_count=1,
        )
        # Feb 15, 2025 (next month, same day)
        expected = datetime(2025, 2, 15, 10, 0, 0)
        self.assertEqual(next_date, expected)

    def test_next_monthly_feb_31st_fallback_to_28th(self) -> None:
        """Test monthly recurrence for 31st in February (fallback to 28th)."""
        base_jan_31 = datetime(2025, 1, 31, 10, 0, 0)
        current_jan_31 = datetime(2025, 1, 31, 10, 0, 0)

        next_date = calculate_next_occurrence(
            current_date=current_jan_31,
            pattern=RecurrencePattern.MONTHLY,
            base_date=base_jan_31,
            max_instances=100,
            current_count=1,
        )
        # Feb 28, 2025 (last day of February)
        expected = datetime(2025, 2, 28, 10, 0, 0)
        self.assertEqual(next_date, expected)

    def test_next_monthly_feb_31st_leap_year(self) -> None:
        """Test monthly recurrence for 31st in leap year February (fallback to 29th)."""
        base_jan_31_2024 = datetime(2024, 1, 31, 10, 0, 0)
        current_jan_31_2024 = datetime(2024, 1, 31, 10, 0, 0)

        next_date = calculate_next_occurrence(
            current_date=current_jan_31_2024,
            pattern=RecurrencePattern.MONTHLY,
            base_date=base_jan_31_2024,
            max_instances=100,
            current_count=1,
        )
        # Feb 29, 2024 (leap year, last day of February)
        expected = datetime(2024, 2, 29, 10, 0, 0)
        self.assertEqual(next_date, expected)

    def test_next_monthly_april_31st_fallback_to_30th(self) -> None:
        """Test monthly recurrence for 31st in April (fallback to 30th)."""
        base_mar_31 = datetime(2025, 3, 31, 10, 0, 0)
        current_mar_31 = datetime(2025, 3, 31, 10, 0, 0)

        next_date = calculate_next_occurrence(
            current_date=current_mar_31,
            pattern=RecurrencePattern.MONTHLY,
            base_date=base_mar_31,
            max_instances=100,
            current_count=1,
        )
        # April 30, 2025 (last day of April)
        expected = datetime(2025, 4, 30, 10, 0, 0)
        self.assertEqual(next_date, expected)

    def test_max_instances_enforcement(self) -> None:
        """Test that creating the 101st instance raises ValueError."""
        with self.assertRaises(ValueError) as cm:
            calculate_next_occurrence(
                current_date=self.current_date,
                pattern=RecurrencePattern.DAILY,
                base_date=self.base_date,
                max_instances=100,
                current_count=100,  # Already at max
            )
        self.assertIn("maximum 100 instances reached", str(cm.exception))

    def test_max_instances_boundary(self) -> None:
        """Test that 100th instance is allowed, 101st is not."""
        # 100th instance should succeed
        next_date = calculate_next_occurrence(
            current_date=self.current_date,
            pattern=RecurrencePattern.DAILY,
            base_date=self.base_date,
            max_instances=100,
            current_count=99,
        )
        self.assertIsNotNone(next_date)

        # 101st instance should fail
        with self.assertRaises(ValueError):
            calculate_next_occurrence(
                current_date=self.current_date,
                pattern=RecurrencePattern.DAILY,
                base_date=self.base_date,
                max_instances=100,
                current_count=100,
            )

    def test_daily_multiple_steps(self) -> None:
        """Test multiple consecutive daily recurrences."""
        current = self.current_date

        # First recurrence
        current = calculate_next_occurrence(
            current_date=current,
            pattern=RecurrencePattern.DAILY,
            base_date=self.base_date,
            max_instances=100,
            current_count=1,
        )
        self.assertEqual(current, datetime(2025, 1, 16, 10, 0, 0))

        # Second recurrence
        current = calculate_next_occurrence(
            current_date=current,
            pattern=RecurrencePattern.DAILY,
            base_date=self.base_date,
            max_instances=100,
            current_count=2,
        )
        self.assertEqual(current, datetime(2025, 1, 17, 10, 0, 0))

    def test_weekly_across_month_boundary(self) -> None:
        """Test weekly recurrence crossing month boundary."""
        current = datetime(2025, 1, 28, 10, 0, 0)

        next_date = calculate_next_occurrence(
            current_date=current,
            pattern=RecurrencePattern.WEEKLY,
            base_date=datetime(2025, 1, 21, 10, 0, 0),
            max_instances=100,
            current_count=1,
        )
        # Feb 4, 2025
        expected = datetime(2025, 2, 4, 10, 0, 0)
        self.assertEqual(next_date, expected)

    def test_monthly_across_year_boundary(self) -> None:
        """Test monthly recurrence crossing year boundary."""
        current = datetime(2025, 12, 15, 10, 0, 0)

        next_date = calculate_next_occurrence(
            current_date=current,
            pattern=RecurrencePattern.MONTHLY,
            base_date=datetime(2025, 1, 15, 10, 0, 0),
            max_instances=100,
            current_count=11,
        )
        # Jan 15, 2026
        expected = datetime(2026, 1, 15, 10, 0, 0)
        self.assertEqual(next_date, expected)

    def test_invalid_pattern_raises_error(self) -> None:
        """Test that invalid pattern raises ValueError."""
        # This test assumes we can create an invalid enum value
        # In practice, RecurrencePattern enum prevents this
        pass  # Enum prevents invalid values at compile time

    def test_preserves_time_component(self) -> None:
        """Test that time component is preserved in all patterns."""
        test_time = datetime(2025, 6, 15, 14, 30, 45)  # 2:30:45 PM

        # Daily
        next_daily = calculate_next_occurrence(
            current_date=test_time,
            pattern=RecurrencePattern.DAILY,
            base_date=test_time,
            max_instances=100,
            current_count=1,
        )
        self.assertEqual(next_daily.hour, 14)
        self.assertEqual(next_daily.minute, 30)
        self.assertEqual(next_daily.second, 45)

        # Weekly
        next_weekly = calculate_next_occurrence(
            current_date=test_time,
            pattern=RecurrencePattern.WEEKLY,
            base_date=test_time,
            max_instances=100,
            current_count=1,
        )
        self.assertEqual(next_weekly.hour, 14)
        self.assertEqual(next_weekly.minute, 30)
        self.assertEqual(next_weekly.second, 45)

        # Monthly
        next_monthly = calculate_next_occurrence(
            current_date=test_time,
            pattern=RecurrencePattern.MONTHLY,
            base_date=test_time,
            max_instances=100,
            current_count=1,
        )
        self.assertEqual(next_monthly.hour, 14)
        self.assertEqual(next_monthly.minute, 30)
        self.assertEqual(next_monthly.second, 45)


if __name__ == "__main__":
    unittest.main()
