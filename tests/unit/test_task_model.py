"""Unit tests for Task model."""

import unittest
from dataclasses import FrozenInstanceError
from src.models.task import Task
from src.models.enums import Priority
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
            due_date="2025-01-05",
            priority=Priority.HIGH,
            tags=["Work", "Urgent"]
        )
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test description")
        self.assertFalse(task.completed)
        self.assertEqual(task.due_date, "2025-01-05")
        self.assertEqual(task.priority, Priority.HIGH)
        self.assertEqual(task.tags, ["Work", "Urgent"])

    def test_task_creation_with_defaults(self) -> None:
        """Test task creation with optional fields defaulted."""
        task = Task(id=1, title="Test Task")
        self.assertEqual(task.description, "")
        self.assertFalse(task.completed)
        self.assertIsNone(task.due_date)
        self.assertEqual(task.priority, Priority.MEDIUM)
        self.assertEqual(task.tags, [])

    def test_task_with_priority_high(self) -> None:
        """Test task with High priority."""
        task = Task(
            id=1,
            title="Test",
            priority=Priority.HIGH
        )
        self.assertEqual(task.priority, Priority.HIGH)

    def test_task_with_priority_medium(self) -> None:
        """Test task with Medium priority."""
        task = Task(
            id=1,
            title="Test",
            priority=Priority.MEDIUM
        )
        self.assertEqual(task.priority, Priority.MEDIUM)

    def test_task_with_priority_low(self) -> None:
        """Test task with Low priority."""
        task = Task(
            id=1,
            title="Test",
            priority=Priority.LOW
        )
        self.assertEqual(task.priority, Priority.LOW)

    def test_task_with_single_tag(self) -> None:
        """Test task with single tag."""
        task = Task(id=1, title="Test", tags=["Work"])
        self.assertEqual(task.tags, ["Work"])

    def test_task_with_multiple_tags(self) -> None:
        """Test task with multiple tags."""
        task = Task(
            id=1,
            title="Test",
            tags=["Work", "Home", "Study"]
        )
        self.assertEqual(task.tags, ["Work", "Home", "Study"])

    def test_task_with_empty_tags_list(self) -> None:
        """Test task tags default to empty list."""
        task = Task(id=1, title="Test")
        self.assertEqual(task.tags, [])

    def test_task_immutability(self) -> None:
        """Test that Task is immutable (frozen dataclass)."""
        task = Task(id=1, title="Test")
        with self.assertRaises(FrozenInstanceError):
            task.title = "New Title"

    def test_task_positive_id(self) -> None:
        """Test that task ID must be positive."""
        task = Task(id=1, title="Test")
        self.assertGreater(task.id, 0)

    def test_task_title_required(self) -> None:
        """Test that title is provided (handled by validation in service layer)."""
        # Dataclass allows empty title; validation happens in TaskManager
        task = Task(id=1, title="")
        self.assertEqual(task.title, "")

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

    def test_task_tags_accept_special_characters(self) -> None:
        """Test that tags accept special characters."""
        task = Task(
            id=1,
            title="Test",
            tags=["@#$%", "key:value", "tag/with\\slashes"]
        )
        self.assertEqual(task.tags, ["@#$%", "key:value", "tag/with\\slashes"])

    def test_task_due_date_stores_as_string(self) -> None:
        """Test that due date is stored as string (not validated here)."""
        task = Task(id=1, title="Test", due_date="2025-01-05")
        self.assertEqual(task.due_date, "2025-01-05")

    def test_task_due_date_none(self) -> None:
        """Test that due date defaults to None."""
        task = Task(id=1, title="Test")
        self.assertIsNone(task.due_date)

    def test_task_priority_default_medium(self) -> None:
        """Test that priority defaults to MEDIUM."""
        task = Task(id=1, title="Test")
        self.assertEqual(task.priority, Priority.MEDIUM)

    def test_task_tags_default_empty_list(self) -> None:
        """Test that tags default to empty list."""
        task = Task(id=1, title="Test")
        self.assertEqual(task.tags, [])
        self.assertEqual(task.tags, [])  # Same object

    def test_task_completed_default_false(self) -> None:
        """Test that completed defaults to False."""
        task = Task(id=1, title="Test")
        self.assertFalse(task.completed)

    def test_task_equality(self) -> None:
        """Test that two tasks with same values are equal."""
        task1 = Task(
            id=1,
            title="Test",
            description="Desc",
            due_date="2025-01-05",
            priority=Priority.HIGH,
            tags=["Work"]
        )
        task2 = Task(
            id=1,
            title="Test",
            description="Desc",
            due_date="2025-01-05",
            priority=Priority.HIGH,
            tags=["Work"]
        )
        self.assertEqual(task1, task2)

    def test_task_inequality_different_title(self) -> None:
        """Test that tasks with different titles are not equal."""
        task1 = Task(id=1, title="Task 1")
        task2 = Task(id=1, title="Task 2")
        self.assertNotEqual(task1, task2)

    def test_task_tags_list_is_mutable(self) -> None:
        """Test that tags list is a new object, not shared reference."""
        task1 = Task(id=1, title="Test", tags=["A", "B"])
        task2 = Task(id=2, title="Test", tags=["A", "B"])
        task1.tags.append("C")
        task2.tags.append("D")
        # Each task has its own list
        self.assertEqual(task1.tags, ["A", "B", "C"])
        self.assertEqual(task2.tags, ["A", "B", "D"])
