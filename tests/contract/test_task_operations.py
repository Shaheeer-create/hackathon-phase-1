"""Contract tests for Todo CRUD operations."""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.services.task_manager import TaskManager
from src.models.task import Task
from src.exceptions import TaskNotFoundError


class TestTaskOperations(unittest.TestCase):
    """Contract tests for Task CRUD operations."""

    def setUp(self) -> None:
        """Set up a fresh TaskManager for each test."""
        self.manager = TaskManager()

    # Contract tests for add_task operation
    def test_add_task_creates_with_sequential_id(self) -> None:
        """Test that add_task creates task with sequential ID."""
        task1 = self.manager.add_task(title="Task 1")
        task2 = self.manager.add_task(title="Task 2")
        self.assertEqual(task1.id, 1)
        self.assertEqual(task2.id, 2)

    def test_add_task_with_all_fields(self) -> None:
        """Test that add_task creates task with all fields."""
        task = self.manager.add_task(
            title="Test Task",
            description="Test description",
            due_date="2025-01-05"
        )
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test description")
        self.assertEqual(task.due_date, "2025-01-05")

    def test_add_task_defaults_pending(self) -> None:
        """Test that add_task creates task as pending by default."""
        task = self.manager.add_task(title="Test")
        self.assertFalse(task.completed)

    # Contract tests for list_tasks operation
    def test_list_tasks_returns_all_tasks(self) -> None:
        """Test that list_tasks returns all tasks."""
        self.manager.add_task(title="Task 1")
        self.manager.add_task(title="Task 2")
        self.manager.add_task(title="Task 3")
        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 3)

    def test_list_tasks_returns_copy(self) -> None:
        """Test that list_tasks returns a copy (not the internal list)."""
        self.manager.add_task(title="Task 1")
        tasks = self.manager.list_tasks()
        tasks.append("modifying the list should not affect manager")
        # Verify internal list unchanged
        internal_tasks = self.manager.list_tasks()
        self.assertEqual(len(internal_tasks), 1)

    def test_list_tasks_empty_returns_empty_list(self) -> None:
        """Test that list_tasks returns empty list when no tasks."""
        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 0)


if __name__ == "__main__":
    unittest.main()
