"""Unit tests for TaskManager service."""

import unittest
from src.services.task_manager import TaskManager
from src.models.task import Task
from src.models.enums import Priority
from src.exceptions import TaskNotFoundError, InvalidTaskError


class TestTaskManager(unittest.TestCase):
    """Test cases for TaskManager service."""

    def setUp(self) -> None:
        """Set up a fresh TaskManager for each test."""
        self.manager = TaskManager()

    def test_add_task_with_title_only(self) -> None:
        """Test adding a task with only title."""
        task = self.manager.add_task(title="Test Task")
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "")
        self.assertFalse(task.completed)
        self.assertIsNone(task.due_date)
        self.assertEqual(task.id, 1)

    def test_add_task_with_all_fields(self) -> None:
        """Test adding a task with all fields."""
        task = self.manager.add_task(
            title="Test Task",
            description="Test description",
            due_date="2025-01-05"
        )
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test description")
        self.assertFalse(task.completed)
        self.assertEqual(task.due_date, "2025-01-05")
        self.assertEqual(task.id, 1)

    def test_add_task_increments_next_id(self) -> None:
        """Test that each new task gets sequential ID."""
        task1 = self.manager.add_task(title="Task 1")
        task2 = self.manager.add_task(title="Task 2")
        task3 = self.manager.add_task(title="Task 3")
        self.assertEqual(task1.id, 1)
        self.assertEqual(task2.id, 2)
        self.assertEqual(task3.id, 3)

    def test_add_task_validates_empty_title(self) -> None:
        """Test that add_task raises error for empty title."""
        with self.assertRaises(ValueError):
            self.manager.add_task(title="")
        with self.assertRaises(ValueError):
            self.manager.add_task(title="   ")

    def test_add_task_validates_date_format(self) -> None:
        """Test that add_task validates date format YYYY-MM-DD."""
        with self.assertRaises(ValueError):
            self.manager.add_task(title="Test", due_date="invalid")
        with self.assertRaises(ValueError):
            self.manager.add_task(title="Test", due_date="2025/01/05")

    def test_get_task_valid_id(self) -> None:
        """Test getting a task by valid ID."""
        self.manager.add_task(title="Test Task")
        task = self.manager.get_task(task_id=1)
        self.assertIsNotNone(task)
        self.assertEqual(task.title, "Test Task")

    def test_get_task_invalid_id_raises_error(self) -> None:
        """Test that get_task raises TaskNotFoundError for invalid ID."""
        with self.assertRaises(TaskNotFoundError) as cm:
            self.manager.get_task(task_id=99)
        self.assertIn("99", str(cm.exception))

    def test_list_tasks_empty(self) -> None:
        """Test listing tasks when empty."""
        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 0)

    def test_list_tasks_with_tasks(self) -> None:
        """Test listing tasks when tasks exist."""
        self.manager.add_task(title="Task 1")
        self.manager.add_task(title="Task 2")
        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].title, "Task 1")
        self.assertEqual(tasks[1].title, "Task 2")

    def test_update_task_title(self) -> None:
        """Test updating task title."""
        self.manager.add_task(title="Original Title")
        updated = self.manager.update_task(task_id=1, title="Updated Title")
        self.assertEqual(updated.title, "Updated Title")

    def test_update_task_description(self) -> None:
        """Test updating task description."""
        self.manager.add_task(title="Task")
        updated = self.manager.update_task(task_id=1, description="New description")
        self.assertEqual(updated.description, "New description")

    def test_update_task_due_date(self) -> None:
        """Test updating task due date."""
        self.manager.add_task(title="Task")
        updated = self.manager.update_task(task_id=1, due_date="2025-01-15")
        self.assertEqual(updated.due_date, "2025-01-15")

    def test_update_task_multiple_fields(self) -> None:
        """Test updating multiple task fields."""
        self.manager.add_task(title="Task", description="Desc", due_date="2025-01-01")
        updated = self.manager.update_task(
            task_id=1, title="New Task", description="New Desc", due_date="2025-01-15"
        )
        self.assertEqual(updated.title, "New Task")
        self.assertEqual(updated.description, "New Desc")
        self.assertEqual(updated.due_date, "2025-01-15")

    def test_update_task_invalid_id_raises_error(self) -> None:
        """Test that update_task raises TaskNotFoundError for invalid ID."""
        self.manager.add_task(title="Task")
        with self.assertRaises(TaskNotFoundError):
            self.manager.update_task(task_id=99, title="New Title")

    def test_update_task_empty_title_raises_error(self) -> None:
        """Test that update_task raises error for empty title."""
        self.manager.add_task(title="Task")
        with self.assertRaises(ValueError):
            self.manager.update_task(task_id=1, title="")

    def test_update_task_invalid_date_raises_error(self) -> None:
        """Test that update_task validates date format."""
        self.manager.add_task(title="Task")
        with self.assertRaises(ValueError):
            self.manager.update_task(task_id=1, due_date="invalid-date")

    def test_delete_task(self) -> None:
        """Test deleting a task."""
        self.manager.add_task(title="Task 1")
        self.manager.add_task(title="Task 2")
        self.manager.delete_task(task_id=1)
        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Task 2")

    def test_delete_task_re_indexes_remaining(self) -> None:
        """Test that remaining tasks are re-indexed after deletion."""
        self.manager.add_task(title="Task 1")
        self.manager.add_task(title="Task 2")
        self.manager.add_task(title="Task 3")
        self.manager.add_task(title="Task 4")
        self.manager.add_task(title="Task 5")
        # Delete task ID 3
        self.manager.delete_task(task_id=3)
        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 4)
        # Verify re-indexing: [1, 2, 4, 5] → [1, 2, 3, 4]
        self.assertEqual(tasks[0].id, 1)
        self.assertEqual(tasks[1].id, 2)
        self.assertEqual(tasks[2].id, 3)
        self.assertEqual(tasks[3].id, 4)

    def test_delete_task_invalid_id_raises_error(self) -> None:
        """Test that delete_task raises TaskNotFoundError for invalid ID."""
        self.manager.add_task(title="Task")
        with self.assertRaises(TaskNotFoundError):
            self.manager.delete_task(task_id=99)

    def test_toggle_complete_pending_to_completed(self) -> None:
        """Test toggling task from pending to completed."""
        self.manager.add_task(title="Task")
        self.assertFalse(self.manager.get_task(task_id=1).completed)
        updated = self.manager.toggle_complete(task_id=1)
        self.assertTrue(updated.completed)

    def test_toggle_complete_completed_to_pending(self) -> None:
        """Test toggling task from completed to pending."""
        self.manager.add_task(title="Task")
        # First toggle to completed
        self.manager.toggle_complete(task_id=1)
        self.assertTrue(self.manager.get_task(task_id=1).completed)
        # Then toggle back to pending
        updated = self.manager.toggle_complete(task_id=1)
        self.assertFalse(updated.completed)

    def test_toggle_complete_invalid_id_raises_error(self) -> None:
        """Test that toggle_complete raises TaskNotFoundError for invalid ID."""
        self.manager.add_task(title="Task")
        with self.assertRaises(TaskNotFoundError):
            self.manager.toggle_complete(task_id=99)

    # Tests for priority support (T024)
    def test_add_task_with_priority(self) -> None:
        """Test adding a task with priority."""
        task = self.manager.add_task(title="Task", priority=Priority.HIGH)
        self.assertEqual(task.priority, Priority.HIGH)

    def test_add_task_priority_defaults_to_medium(self) -> None:
        """Test that priority defaults to MEDIUM when not specified."""
        task = self.manager.add_task(title="Task")
        self.assertEqual(task.priority, Priority.MEDIUM)

    def test_add_task_with_single_tag(self) -> None:
        """Test adding a task with single tag."""
        task = self.manager.add_task(title="Task", tags=["Work"])
        self.assertEqual(task.tags, ["Work"])

    def test_add_task_with_multiple_tags(self) -> None:
        """Test adding a task with multiple tags."""
        task = self.manager.add_task(title="Task", tags=["Work", "Urgent", "Project"])
        self.assertEqual(task.tags, ["Work", "Urgent", "Project"])

    def test_add_task_deduplicates_tags(self) -> None:
        """Test that duplicate tags are deduplicated."""
        task = self.manager.add_task(title="Task", tags=["Work", "Work", "Urgent", "Work"])
        self.assertEqual(task.tags, ["Work", "Urgent"])

    def test_add_task_with_all_enhanced_fields(self) -> None:
        """Test adding task with all enhanced fields."""
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

    def test_update_task_priority(self) -> None:
        """Test updating task priority."""
        self.manager.add_task(title="Task", priority=Priority.LOW)
        updated = self.manager.update_task(task_id=1, priority=Priority.HIGH)
        self.assertEqual(updated.priority, Priority.HIGH)

    def test_update_task_single_tag(self) -> None:
        """Test updating task with single tag."""
        self.manager.add_task(title="Task")
        updated = self.manager.update_task(task_id=1, tags=["Work"])
        self.assertEqual(updated.tags, ["Work"])

    def test_update_task_multiple_tags(self) -> None:
        """Test updating task with multiple tags."""
        self.manager.add_task(title="Task")
        updated = self.manager.update_task(task_id=1, tags=["Home", "Shopping"])
        self.assertEqual(updated.tags, ["Home", "Shopping"])

    def test_update_task_deduplicates_tags(self) -> None:
        """Test that update deduplicates tags."""
        self.manager.add_task(title="Task", tags=["Existing"])
        updated = self.manager.update_task(
            task_id=1, tags=["Work", "Work", "Existing", "New"]
        )
        self.assertEqual(updated.tags, ["Work", "Existing", "New"])

    def test_update_task_with_all_enhanced_fields(self) -> None:
        """Test updating all enhanced fields."""
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

    def test_delete_task_preserves_priority_and_tags(self) -> None:
        """Test that delete reindexing preserves priority and tags."""
        self.manager.add_task(
            title="Task 1",
            priority=Priority.HIGH,
            tags=["Tag1", "Tag2"]
        )
        self.manager.add_task(title="Task 2", priority=Priority.LOW, tags=["Tag3"])
        self.manager.add_task(title="Task 3")
        # Delete task 1
        self.manager.delete_task(task_id=1)
        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 2)
        # Verify priority and tags are preserved on remaining tasks
        self.assertEqual(tasks[0].id, 1)
        self.assertEqual(tasks[0].title, "Task 2")
        self.assertEqual(tasks[0].priority, Priority.LOW)
        self.assertEqual(tasks[0].tags, ["Tag3"])

    def test_toggle_complete_preserves_priority_and_tags(self) -> None:
        """Test that toggle_complete preserves priority and tags."""
        self.manager.add_task(
            title="Task",
            priority=Priority.HIGH,
            tags=["Work", "Urgent"]
        )
        self.assertFalse(self.manager.get_task(task_id=1).completed)
        updated = self.manager.toggle_complete(task_id=1)
        self.assertTrue(updated.completed)
        self.assertEqual(updated.priority, Priority.HIGH)
        self.assertEqual(updated.tags, ["Work", "Urgent"])


if __name__ == "__main__":
    unittest.main()
