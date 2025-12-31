"""Integration tests for CLI workflows."""

import unittest
import sys
import os
import io
from contextlib import redirect_stdout, redirect_stderr

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.services.task_manager import TaskManager
from src.exceptions import TaskNotFoundError


class TestCLIWorkflows(unittest.TestCase):
    """Integration tests for end-to-end CLI workflows."""

    def setUp(self) -> None:
        """Set up a fresh TaskManager for each test."""
        self.manager = TaskManager()

    # User Story 1 workflows
    def test_add_then_list_workflow(self) -> None:
        """Test add task followed by list to verify appearance."""
        # Add task
        task = self.manager.add_task(title="Buy groceries")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Buy groceries")

        # List tasks
        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Buy groceries")

    def test_add_task_with_description_then_list(self) -> None:
        """Test add task with description and list."""
        task = self.manager.add_task(
            title="Meeting",
            description="Team standup at 10am"
        )

        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Meeting")
        self.assertEqual(tasks[0].description, "Team standup at 10am")

    def test_add_task_with_due_date_then_list(self) -> None:
        """Test add task with due date and list."""
        task = self.manager.add_task(title="Review code", due_date="2025-01-10")

        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Review code")
        self.assertEqual(tasks[0].due_date, "2025-01-10")

    def test_add_multiple_tasks_then_list(self) -> None:
        """Test add multiple tasks then list all."""
        self.manager.add_task(title="Task 1")
        self.manager.add_task(title="Task 2")
        self.manager.add_task(title="Task 3")

        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0].title, "Task 1")
        self.assertEqual(tasks[1].title, "Task 2")
        self.assertEqual(tasks[2].title, "Task 3")

    def test_add_task_with_all_fields_then_list(self) -> None:
        """Test add task with all fields and list."""
        task = self.manager.add_task(
            title="Complete project",
            description="Finish MVP",
            due_date="2025-01-15"
        )

        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Complete project")
        self.assertEqual(tasks[0].description, "Finish MVP")
        self.assertEqual(tasks[0].due_date, "2025-01-15")

    def test_empty_list_shows_no_tasks(self) -> None:
        """Test that empty list returns no tasks."""
        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 0)

    # Error case tests
    def test_add_empty_title_raises_error(self) -> None:
        """Test that adding task with empty title raises error."""
        with self.assertRaises(ValueError):
            self.manager.add_task(title="")
        with self.assertRaises(ValueError):
            self.manager.add_task(title="   ")

    def test_add_invalid_date_raises_error(self) -> None:
        """Test that adding task with invalid date format raises error."""
        with self.assertRaises(ValueError):
            self.manager.add_task(title="Task", due_date="invalid")
        with self.assertRaises(ValueError):
            self.manager.add_task(title="Task", due_date="2025/01/05")

    # User Story 2 workflows
    def test_complete_task_then_list(self) -> None:
        """Test complete task followed by list to verify [✓] indicator."""
        self.manager.add_task(title="Task 1")
        # Complete the task
        updated = self.manager.toggle_complete(task_id=1)
        self.assertTrue(updated.completed)

        # Verify in list
        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertTrue(tasks[0].completed)

    def test_toggle_complete_back_to_pending(self) -> None:
        """Test toggle complete task back to pending."""
        self.manager.add_task(title="Task 1")
        # Complete first
        self.manager.toggle_complete(task_id=1)
        self.assertTrue(self.manager.get_task(task_id=1).completed)

        # Toggle back
        updated = self.manager.toggle_complete(task_id=1)
        self.assertFalse(updated.completed)

    def test_delete_task_then_list(self) -> None:
        """Test delete task followed by list to verify removal."""
        self.manager.add_task(title="Task 1")
        self.manager.add_task(title="Task 2")
        self.manager.add_task(title="Task 3")

        # Delete task ID 2
        self.manager.delete_task(task_id=2)

        # Verify removal and re-indexing
        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].title, "Task 1")
        self.assertEqual(tasks[1].title, "Task 3")
        # Verify re-indexing
        self.assertEqual(tasks[0].id, 1)
        self.assertEqual(tasks[1].id, 2)

    def test_delete_multiple_tasks(self) -> None:
        """Test deleting multiple tasks and verify re-indexing."""
        self.manager.add_task(title="Task 1")
        self.manager.add_task(title="Task 2")
        self.manager.add_task(title="Task 3")
        self.manager.add_task(title="Task 4")
        self.manager.add_task(title="Task 5")

        # Delete task ID 3
        self.manager.delete_task(task_id=3)
        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 4)
        self.assertEqual(tasks[0].id, 1)
        self.assertEqual(tasks[1].id, 2)
        self.assertEqual(tasks[2].id, 3)
        self.assertEqual(tasks[3].id, 4)

        # Delete task ID 1 (now has new ID 1, but was Task 2)
        self.manager.delete_task(task_id=1)
        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0].id, 1)  # Original Task 2
        self.assertEqual(tasks[1].id, 2)  # Original Task 4
        self.assertEqual(tasks[2].id, 3)  # Original Task 5

    def test_complete_nonexistent_raises_error(self) -> None:
        """Test completing non-existent task ID raises error."""
        with self.assertRaises(TaskNotFoundError):
            self.manager.toggle_complete(task_id=99)

    def test_delete_nonexistent_raises_error(self) -> None:
        """Test deleting non-existent task ID raises error."""
        with self.assertRaises(TaskNotFoundError):
            self.manager.delete_task(task_id=99)

    # User Story 3 workflows
    def test_update_title_then_list(self) -> None:
        """Test update task title followed by list."""
        self.manager.add_task(title="Original Title")
        self.manager.update_task(task_id=1, title="Updated Title")

        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Updated Title")

    def test_update_description_then_list(self) -> None:
        """Test update task description followed by list."""
        self.manager.add_task(title="Task")
        self.manager.update_task(task_id=1, description="New description")

        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].description, "New description")

    def test_update_due_date_then_list(self) -> None:
        """Test update task due date followed by list."""
        self.manager.add_task(title="Task", due_date="2025-01-01")
        self.manager.update_task(task_id=1, due_date="2025-01-15")

        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].due_date, "2025-01-15")

    def test_update_multiple_fields_then_list(self) -> None:
        """Test update multiple task fields followed by list."""
        self.manager.add_task(title="Task", description="Desc", due_date="2025-01-01")
        self.manager.update_task(
            task_id=1, title="New Task", description="New Desc", due_date="2025-01-15"
        )

        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "New Task")
        self.assertEqual(tasks[0].description, "New Desc")
        self.assertEqual(tasks[0].due_date, "2025-01-15")

    def test_update_nonexistent_raises_error(self) -> None:
        """Test updating non-existent task ID raises error."""
        self.manager.add_task(title="Task")
        with self.assertRaises(TaskNotFoundError):
            self.manager.update_task(task_id=99, title="New Title")

    def test_update_empty_title_raises_error(self) -> None:
        """Test updating with empty title raises error."""
        self.manager.add_task(title="Task")
        with self.assertRaises(ValueError):
            self.manager.update_task(task_id=1, title="")

    def test_update_invalid_date_raises_error(self) -> None:
        """Test updating with invalid date format raises error."""
        self.manager.add_task(title="Task")
        with self.assertRaises(ValueError):
            self.manager.update_task(task_id=1, due_date="invalid-date")


if __name__ == "__main__":
    unittest.main()
