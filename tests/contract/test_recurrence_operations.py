"""Contract tests for recurrence engine operations."""

import unittest
from datetime import datetime, timedelta

from src.models.recurrence import RecurrencePattern, RecurrenceRule
from src.services.recurrence_engine import calculate_next_occurrence


class TestRecurrenceOperations(unittest.TestCase):
    """Contract tests validating recurrence engine behavior."""

    def test_calculate_next_daily(self) -> None:
        """Test daily recurrence across year boundaries."""
        base_date = datetime(2024, 12, 31, 10, 0)
        current_date = datetime(2025, 1, 1, 10, 0)

        next_date = calculate_next_occurrence(
            current_date=current_date,
            pattern=RecurrencePattern.DAILY,
            base_date=base_date,
            max_instances=100,
            current_count=1
        )

        # Should be Jan 2, 2025 (current_date + 1 day)
        self.assertEqual(next_date, datetime(2025, 1, 2, 10, 0))

    def test_calculate_next_weekly(self) -> None:
        """Test weekly recurrence across month boundaries."""
        base_date = datetime(2025, 1, 21, 10, 0)
        current_date = datetime(2025, 1, 28, 10, 0)

        next_date = calculate_next_occurrence(
            current_date=current_date,
            pattern=RecurrencePattern.WEEKLY,
            base_date=base_date,
            max_instances=100,
            current_count=1
        )

        # Should be Feb 4, 2025 (current_date + 7 days)
        self.assertEqual(next_date, datetime(2025, 2, 4, 10, 0))

    def test_calculate_next_monthly_valid_day(self) -> None:
        """Test monthly recurrence with valid target days."""
        base_date = datetime(2025, 1, 15, 10, 0)
        current_date = datetime(2025, 1, 15, 10, 0)

        next_date = calculate_next_occurrence(
            current_date=current_date,
            pattern=RecurrencePattern.MONTHLY,
            base_date=base_date,
            max_instances=100,
            current_count=1
        )

        # Should be Feb 15, 2025
        self.assertEqual(next_date, datetime(2025, 2, 15, 10, 0))

    def test_calculate_next_monthly_31st_to_30th(self) -> None:
        """Test monthly recurrence for 31st in 30-day month."""
        base_date = datetime(2025, 1, 31, 10, 0)
        current_date = datetime(2025, 1, 31, 10, 0)

        next_date = calculate_next_occurrence(
            current_date=current_date,
            pattern=RecurrencePattern.MONTHLY,
            base_date=base_date,
            max_instances=100,
            current_count=1
        )

        # Should be Feb 28, 2025 (last day of February)
        self.assertEqual(next_date, datetime(2025, 2, 28, 10, 0))

    def test_calculate_next_monthly_invalid_day_feb_30th(self) -> None:
        """Test monthly recurrence for February 30th/31st edge case."""
        base_date = datetime(2025, 1, 30, 10, 0)
        current_date = datetime(2025, 1, 30, 10, 0)

        next_date = calculate_next_occurrence(
            current_date=current_date,
            pattern=RecurrencePattern.MONTHLY,
            base_date=base_date,
            max_instances=100,
            current_count=1
        )

        # Should be Feb 28, 2025 (last day of February)
        self.assertEqual(next_date, datetime(2025, 2, 28, 10, 0))

    def test_max_instances_enforcement(self) -> None:
        """Test that max_instances limit is enforced."""
        base_date = datetime(2025, 1, 1, 10, 0)
        current_date = datetime(2025, 1, 1, 10, 0)

        # 100th instance should succeed
        calculate_next_occurrence(
            current_date=current_date,
            pattern=RecurrencePattern.DAILY,
            base_date=base_date,
            max_instances=100,
            current_count=99
        )

        # 101st instance should raise ValueError
        with self.assertRaises(ValueError) as cm:
            calculate_next_occurrence(
                current_date=current_date,
                pattern=RecurrencePattern.DAILY,
                base_date=base_date,
                max_instances=100,
                current_count=100
            )

        self.assertIn("maximum 100 instances reached", str(cm.exception))

    def test_leap_year_handling(self) -> None:
        """Test leap year handling for February."""
        # 2024 is a leap year (Feb has 29 days)
        base_date = datetime(2024, 1, 31, 10, 0)
        current_date = datetime(2024, 1, 31, 10, 0)

        next_date = calculate_next_occurrence(
            current_date=current_date,
            pattern=RecurrencePattern.MONTHLY,
            base_date=base_date,
            max_instances=100,
            current_count=1
        )

        # Should be Feb 29, 2024 (leap year)
        self.assertEqual(next_date, datetime(2024, 2, 29, 10, 0))

    def test_non_leap_year_handling(self) -> None:
        """Test non-leap year handling for February."""
        # 2025 is NOT a leap year (Feb has 28 days)
        base_date = datetime(2025, 1, 31, 10, 0)
        current_date = datetime(2025, 1, 31, 10, 0)

        next_date = calculate_next_occurrence(
            current_date=current_date,
            pattern=RecurrencePattern.MONTHLY,
            base_date=base_date,
            max_instances=100,
            current_count=1
        )

        # Should be Feb 28, 2025 (non-leap year)
        self.assertEqual(next_date, datetime(2025, 2, 28, 10, 0))

    def test_monthly_april_30th(self) -> None:
        """Test monthly recurrence for April 30th (April has 30 days)."""
        base_date = datetime(2025, 4, 30, 10, 0)
        current_date = datetime(2025, 4, 30, 10, 0)

        next_date = calculate_next_occurrence(
            current_date=current_date,
            pattern=RecurrencePattern.MONTHLY,
            base_date=base_date,
            max_instances=100,
            current_count=1
        )

        # Should be May 30, 2025
        self.assertEqual(next_date, datetime(2025, 5, 30, 10, 0))


if __name__ == "__main__":
    unittest.main()
