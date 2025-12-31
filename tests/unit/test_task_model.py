"""Unit tests for Task model."""

import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime
from src.models.task import Task
from src.exceptions import InvalidTaskError


class TestTaskModel(unittest.TestCase):
    """Test cases for Task dataclass model."""

    def test_task_creation_with_all_fields(self) -> None:
        """Test task creation with all fields provided."""
        task = Task(
            id=1,
            title="Test Task",
            description="Test description",
            completed=False,
            due_date="2025-01-05"
        )
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test description")
        self.assertFalse(task.completed)
        self.assertEqual(task.due_date, "2025-01-05")

    def test_task_creation_with_defaults(self) -> None:
        """Test task creation with optional fields defaulted."""
        task = Task(id=1, title="Test Task")
        self.assertEqual(task.description, "")
        self.assertFalse(task.completed)
        self.assertIsNone(task.due_date)

    def test_task_immutability(self) -> None:
        """Test that Task is immutable (frozen dataclass)."""
        task = Task(id=1, title="Test Task")
        with self.assertRaises(FrozenInstanceError):
            task.title = "New Title"

    def test_task_positive_id(self) -> None:
        """Test that task ID must be positive."""
        task = Task(id=1, title="Test")
        self.assertGreater(task.id, 0)

    def test_task_description_accepts_special_characters(self) -> None:
        """Test that description accepts special characters."""
        task = Task(
            id=1,
            title="Test",
            description="Special: @#$%^&*()_+-={}[]|\\:\";'<>?,./"
        )
        self.assertEqual(
            task.description, "Special: @#$%^&*()_+-={}[]|\\:\";'<>?,./"
        )

    def test_task_completed_false_default(self) -> None:
        """Test that completed defaults to False (pending state)."""
        task = Task(id=1, title="Test")
        self.assertFalse(task.completed)

    def test_task_completed_true(self) -> None:
        """Test that completed can be set to True."""
        task = Task(id=1, title="Test", completed=True)
        self.assertTrue(task.completed)

    def test_task_due_date_validation_format_only(self) -> None:
        """Test that due_date stores YYYY-MM-DD string (no calendar validation)."""
        # Valid format
        task = Task(id=1, title="Test", due_date="2025-01-05")
        self.assertEqual(task.due_date, "2025-01-05")
        # Invalid format still stored (validation in TaskManager)
        task_invalid = Task(id=2, title="Test", due_date="not-a-date")
        self.assertEqual(task_invalid.due_date, "not-a-date")

    def test_task_equality(self) -> None:
        """Test that two tasks with same values are equal."""
        task1 = Task(id=1, title="Test")
        task2 = Task(id=1, title="Test")
        self.assertEqual(task1, task2)

    def test_task_repr(self) -> None:
        """Test task string representation."""
        task = Task(id=1, title="Test", description="Desc")
        repr_str = repr(task)
        self.assertIn("Task", repr_str)
        self.assertIn("id=1", repr_str)
        self.assertIn("title='Test'", repr_str)
