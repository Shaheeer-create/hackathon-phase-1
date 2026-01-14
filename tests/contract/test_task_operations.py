"""Contract tests for Todo CRUD operations."""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.services.task_manager import TaskManager
from src.models.task import Task
from src.models.enums import Priority
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

    # Contract tests for add_task with priority and tags (T013)
    def test_add_task_with_priority(self) -> None:
        """Test that add_task creates task with priority."""
        task = self.manager.add_task(
            title="Urgent Task",
            priority=Priority.HIGH
        )
        self.assertEqual(task.priority, Priority.HIGH)

    def test_add_task_with_single_tag(self) -> None:
        """Test that add_task creates task with single tag."""
        task = self.manager.add_task(
            title="Tagged Task",
            tags=["Work"]
        )
        self.assertEqual(task.tags, ["Work"])

    def test_add_task_with_multiple_tags(self) -> None:
        """Test that add_task creates task with multiple tags."""
        task = self.manager.add_task(
            title="Multi-tag Task",
            tags=["Work", "Urgent", "Project"]
        )
        self.assertEqual(task.tags, ["Work", "Urgent", "Project"])

    def test_add_task_with_duplicate_tags_deduplicates(self) -> None:
        """Test that add_task deduplicates duplicate tags."""
        task = self.manager.add_task(
            title="Duplicate Tags",
            tags=["Work", "Work", "Urgent", "Work"]
        )
        self.assertEqual(task.tags, ["Work", "Urgent"])

    def test_add_task_with_empty_tags_list(self) -> None:
        """Test that add_task handles empty tags list."""
        task = self.manager.add_task(
            title="No Tags",
            tags=[]
        )
        self.assertEqual(task.tags, [])

    def test_add_task_with_all_enhanced_fields(self) -> None:
        """Test that add_task creates task with all fields including priority and tags."""
        task = self.manager.add_task(
            title="Complete Task",
            description="Full description",
            due_date="2025-01-10",
            priority=Priority.HIGH,
            tags=["Work", "Documentation"]
        )
        self.assertEqual(task.title, "Complete Task")
        self.assertEqual(task.description, "Full description")
        self.assertEqual(task.due_date, "2025-01-10")
        self.assertEqual(task.priority, Priority.HIGH)
        self.assertEqual(task.tags, ["Work", "Documentation"])

    # Contract tests for update_task with priority and tags (T014)
    def test_update_task_with_priority(self) -> None:
        """Test that update_task can change priority."""
        task = self.manager.add_task(title="Task", priority=Priority.LOW)
        updated = self.manager.update_task(
            task_id=1,
            priority=Priority.HIGH
        )
        self.assertEqual(updated.priority, Priority.HIGH)

    def test_update_task_with_single_tag(self) -> None:
        """Test that update_task can set single tag."""
        self.manager.add_task(title="Task")
        updated = self.manager.update_task(
            task_id=1,
            tags=["Work"]
        )
        self.assertEqual(updated.tags, ["Work"])

    def test_update_task_with_multiple_tags(self) -> None:
        """Test that update_task can set multiple tags."""
        self.manager.add_task(title="Task")
        updated = self.manager.update_task(
            task_id=1,
            tags=["Home", "Shopping"]
        )
        self.assertEqual(updated.tags, ["Home", "Shopping"])

    def test_update_task_with_duplicate_tags_deduplicates(self) -> None:
        """Test that update_task deduplicates tags on update."""
        self.manager.add_task(title="Task", tags=["Existing"])
        updated = self.manager.update_task(
            task_id=1,
            tags=["Work", "Work", "Existing", "New"]
        )
        self.assertEqual(updated.tags, ["Work", "Existing", "New"])

    def test_update_task_preserves_existing_fields(self) -> None:
        """Test that update_task preserves unchanged fields."""
        task = self.manager.add_task(
            title="Original",
            description="Original Desc",
            due_date="2025-01-05",
            priority=Priority.MEDIUM,
            tags=["Tag1"]
        )
        updated = self.manager.update_task(
            task_id=1,
            priority=Priority.HIGH
        )
        # Only priority should change
        self.assertEqual(updated.title, "Original")
        self.assertEqual(updated.description, "Original Desc")
        self.assertEqual(updated.due_date, "2025-01-05")
        self.assertEqual(updated.priority, Priority.HIGH)
        self.assertEqual(updated.tags, ["Tag1"])

    def test_update_task_with_all_fields(self) -> None:
        """Test that update_task can update all fields including priority and tags."""
        self.manager.add_task(title="Task")
        updated = self.manager.update_task(
            task_id=1,
            title="Updated Title",
            description="Updated Description",
            due_date="2025-01-15",
            priority=Priority.LOW,
            tags=["New", "Tags"]
        )
        self.assertEqual(updated.title, "Updated Title")
        self.assertEqual(updated.description, "Updated Description")
        self.assertEqual(updated.due_date, "2025-01-15")
        self.assertEqual(updated.priority, Priority.LOW)
        self.assertEqual(updated.tags, ["New", "Tags"])


if __name__ == "__main__":
    unittest.main()
