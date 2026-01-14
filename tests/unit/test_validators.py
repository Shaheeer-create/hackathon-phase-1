"""Unit tests for validation utilities."""

import unittest
from src.utils.validators import (
    validate_priority,
    validate_tags,
    is_valid_date,
    is_valid_time,
)

# Import Priority if available for test reference
try:
    from src.models.enums import Priority
except ImportError:
    Priority = None


class TestValidators(unittest.TestCase):
    """Test cases for validation utilities."""

    def test_validate_priority_high(self) -> None:
        """Test priority validation for HIGH."""
        if Priority:
            result = validate_priority("high")
            self.assertEqual(result, Priority.HIGH)
            result = validate_priority("High")
            self.assertEqual(result, Priority.HIGH)
            result = validate_priority("HIGH")
            self.assertEqual(result, Priority.HIGH)
            result = validate_priority("h")
            self.assertEqual(result, Priority.HIGH)

    def test_validate_priority_medium(self) -> None:
        """Test priority validation for MEDIUM."""
        if Priority:
            result = validate_priority("medium")
            self.assertEqual(result, Priority.MEDIUM)
            result = validate_priority("Medium")
            self.assertEqual(result, Priority.MEDIUM)
            result = validate_priority("M")
            self.assertEqual(result, Priority.MEDIUM)

    def test_validate_priority_low(self) -> None:
        """Test priority validation for LOW."""
        if Priority:
            result = validate_priority("low")
            self.assertEqual(result, Priority.LOW)
            result = validate_priority("Low")
            self.assertEqual(result, Priority.LOW)
            result = validate_priority("L")
            self.assertEqual(result, Priority.LOW)

    def test_validate_priority_empty_returns_medium(self) -> None:
        """Test that empty priority defaults to MEDIUM."""
        result = validate_priority("")
        if Priority:
            self.assertEqual(result, Priority.MEDIUM)
        else:
            # Fallback: return should be either Priority enum or string "Medium"
            if isinstance(result, str):
                self.assertEqual(result, "Medium")
            else:
                self.assertEqual(result, Priority.MEDIUM)
        result = validate_priority("   ")
        if Priority:
            self.assertEqual(result, Priority.MEDIUM)
        else:
            self.assertEqual(result, "Medium")

    def test_validate_priority_invalid(self) -> None:
        """Test that invalid priority returns None."""
        result = validate_priority("invalid")
        self.assertIsNone(result)
        result = validate_priority("xyz")
        self.assertIsNone(result)

    def test_validate_tags_single(self) -> None:
        """Test tags validation for single tag."""
        result = validate_tags("Work")
        self.assertEqual(result, ["Work"])

    def test_validate_tags_multiple(self) -> None:
        """Test tags validation for multiple tags."""
        result = validate_tags("Work, Home, Urgent")
        self.assertEqual(result, ["Work", "Home", "Urgent"])

    def test_validate_tags_deduplicates(self) -> None:
        """Test that tags are deduplicated."""
        result = validate_tags("Work, Work, Home, Work")
        self.assertEqual(result, ["Work", "Home"])
        result = validate_tags("A, B, C, A, B, A")
        self.assertEqual(result, ["A", "B", "C"])

    def test_validate_tags_empty_returns_empty(self) -> None:
        """Test that empty tags returns empty list."""
        result = validate_tags("")
        self.assertEqual(result, [])
        result = validate_tags("   ")
        self.assertEqual(result, [])

    def test_validate_tags_with_extra_commas(self) -> None:
        """Test tags with trailing/leading commas."""
        result = validate_tags(",Work,,Home,")
        self.assertEqual(result, ["Work", "Home"])

    def test_validate_tags_with_spaces(self) -> None:
        """Test tags with extra spaces."""
        result = validate_tags("  Work  ,  Home  ")
        self.assertEqual(result, ["Work", "Home"])

    def test_is_valid_date_valid_format(self) -> None:
        """Test valid date format."""
        self.assertTrue(is_valid_date("2025-01-05"))
        self.assertTrue(is_valid_date("1999-12-31"))
        self.assertTrue(is_valid_date("2020-01-01"))

    def test_is_valid_date_invalid_format(self) -> None:
        """Test invalid date formats."""
        self.assertFalse(is_valid_date("2025/01/05"))
        self.assertFalse(is_valid_date("01-05-2025"))
        self.assertFalse(is_valid_date("2025-01-05-"))
        self.assertFalse(is_valid_date("2025-1-5"))
        self.assertFalse(is_valid_date("2025-13-01"))
        self.assertFalse(is_valid_date("2025-00-01"))

    def test_is_valid_date_empty(self) -> None:
        """Test empty date string."""
        self.assertFalse(is_valid_date(""))
        self.assertFalse(is_valid_date("   "))

    # NEW: Time validation tests
    def test_is_valid_time_valid_format(self) -> None:
        """Test valid time format (HH:MM)."""
        self.assertTrue(is_valid_time("00:00"))
        self.assertTrue(is_valid_time("09:30"))
        self.assertTrue(is_valid_time("12:00"))
        self.assertTrue(is_valid_time("23:59"))

    def test_is_valid_time_invalid_hour(self) -> None:
        """Test invalid hour values."""
        self.assertFalse(is_valid_time("24:00"))
        self.assertFalse(is_valid_time("25:30"))
        self.assertFalse(is_valid_time("-1:00"))

    def test_is_valid_time_invalid_minute(self) -> None:
        """Test invalid minute values."""
        self.assertFalse(is_valid_time("09:60"))
        self.assertFalse(is_valid_time("12:99"))

    def test_is_valid_time_missing_leading_zero(self) -> None:
        """Test times without leading zeros."""
        self.assertFalse(is_valid_time("9:30"))
        self.assertFalse(is_valid_time("1:05"))

    def test_is_valid_time_wrong_format(self) -> None:
        """Test wrong time formats."""
        self.assertFalse(is_valid_time("09:30:00"))
        self.assertFalse(is_valid_time("09-30"))
        self.assertFalse(is_valid_time("09.30"))
        self.assertFalse(is_valid_time("9:30"))

    def test_is_valid_time_empty(self) -> None:
        """Test empty time string."""
        self.assertFalse(is_valid_time(""))
        self.assertFalse(is_valid_time("   "))


if __name__ == "__main__":
    unittest.main()
