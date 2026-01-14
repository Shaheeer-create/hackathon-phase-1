"""Unit tests for JSONStorage service."""

import os
import unittest
import tempfile
from src.services.storage import JSONStorage
from src.models.task import Task
from src.models.enums import Priority
from src.exceptions import StorageError


class TestJSONStorage(unittest.TestCase):
    """Test cases for JSONStorage service."""

    def setUp(self):
        """Create test storage instance with temp file."""
        self.temp_dir = tempfile.mkdtemp()
        self.filepath = os.path.join(self.temp_dir, "test_todo.json")

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.filepath):
            os.remove(self.filepath)
        if os.path.exists(f"{self.filepath}.bak"):
            os.remove(f"{self.filepath}.bak")
        os.rmdir(self.temp_dir)

    def _create_storage(self):
        """Helper to create storage instance."""
        return JSONStorage(self.filepath)

    def test_save_tasks_creates_new_file(self):
        """Test that saving tasks creates new file."""
        storage = self._create_storage()
        tasks = [
            Task(id=1, title="Task 1", completed=False),
            Task(id=2, title="Task 2", completed=False)
        ]
        storage.save_tasks(tasks)
        self.assertTrue(os.path.exists(self.filepath))
        loaded = storage.load_tasks()
        self.assertEqual(len(loaded), 2)

    def test_save_tasks_creates_backup_on_second_save(self):
        """Test that saving creates backup on subsequent save (overwriting)."""
        storage = self._create_storage()
        tasks = [Task(id=1, title="Task 1", completed=False)]
        storage.save_tasks(tasks)  # First save - no backup yet
        self.assertFalse(os.path.exists(f"{self.filepath}.bak"))

        # Second save - should create backup
        tasks[0] = Task(id=1, title="Task 1 Updated", completed=True)
        storage.save_tasks(tasks)
        self.assertTrue(os.path.exists(f"{self.filepath}.bak"))

    def test_save_tasks_overwrites_existing_file(self):
        """Test that saving overwrites existing file."""
        storage = self._create_storage()
        tasks1 = [Task(id=1, title="Task 1", completed=False)]
        storage.save_tasks(tasks1)

        tasks2 = [Task(id=1, title="Task 1 Updated", completed=True)]
        storage.save_tasks(tasks2)

        loaded = storage.load_tasks()
        self.assertEqual(loaded[0].completed, True)

    def test_save_tasks_with_empty_list(self):
        """Test that saving empty list works."""
        storage = self._create_storage()
        storage.save_tasks([])
        loaded = storage.load_tasks()
        self.assertEqual(len(loaded), 0)

    def test_load_tasks_returns_empty_list_if_file_not_exists(self):
        """Test that loading non-existent file returns empty list."""
        storage = self._create_storage()
        tasks = storage.load_tasks()
        self.assertEqual(tasks, [])

    def test_load_tasks_loads_existing_file(self):
        """Test that loading reads existing file."""
        storage = self._create_storage()
        original_tasks = [
            Task(id=1, title="Task 1", completed=False),
            Task(id=2, title="Task 2", completed=True)
        ]
        storage.save_tasks(original_tasks)
        loaded = storage.load_tasks()
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].title, "Task 1")
        self.assertEqual(loaded[1].title, "Task 2")

    def test_save_tasks_with_priority(self):
        """Test that tasks with priority are saved correctly."""
        storage = self._create_storage()
        tasks = [
            Task(id=1, title="Task", priority=Priority.HIGH),
            Task(id=2, title="Task", priority=Priority.MEDIUM)
        ]
        storage.save_tasks(tasks)
        loaded = storage.load_tasks()
        self.assertEqual(loaded[0].priority, Priority.HIGH)
        self.assertEqual(loaded[1].priority, Priority.MEDIUM)

    def test_save_tasks_with_tags(self):
        """Test that tasks with tags are saved correctly."""
        storage = self._create_storage()
        tasks = [
            Task(id=1, title="Task", tags=["Work", "Urgent"]),
            Task(id=2, title="Task", tags=["Home"])
        ]
        storage.save_tasks(tasks)
        loaded = storage.load_tasks()
        self.assertEqual(loaded[0].tags, ["Work", "Urgent"])
        self.assertEqual(loaded[1].tags, ["Home"])

    def test_save_tasks_with_due_date(self):
        """Test that tasks with due date are saved correctly."""
        storage = self._create_storage()
        tasks = [
            Task(id=1, title="Task", due_date="2025-01-05"),
            Task(id=2, title="Task", due_date=None)
        ]
        storage.save_tasks(tasks)
        loaded = storage.load_tasks()
        self.assertEqual(loaded[0].due_date, "2025-01-05")
        self.assertIsNone(loaded[1].due_date)

    def test_save_tasks_with_all_fields(self):
        """Test that tasks with all fields are saved correctly."""
        storage = self._create_storage()
        tasks = [
            Task(
                id=1,
                title="Complete task",
                description="Write documentation",
                completed=False,
                due_date="2025-01-10",
                priority=Priority.HIGH,
                tags=["Work", "Documentation"]
            )
        ]
        storage.save_tasks(tasks)
        loaded = storage.load_tasks()
        self.assertEqual(loaded[0].title, "Complete task")
        self.assertEqual(loaded[0].description, "Write documentation")
        self.assertEqual(loaded[0].due_date, "2025-01-10")
        self.assertEqual(loaded[0].priority, Priority.HIGH)
        self.assertEqual(loaded[0].tags, ["Work", "Documentation"])

    def test_load_tasks_handles_invalid_json(self):
        """Test that loading invalid JSON raises StorageError."""
        storage = self._create_storage()
        # Write invalid JSON
        with open(self.filepath, "w") as f:
            f.write("invalid json content")

        with self.assertRaises(StorageError) as context:
            storage.load_tasks()
        self.assertIn("Corrupted data file", str(context.exception))

    def test_load_tasks_handles_missing_tasks_key(self):
        """Test that loading JSON without tasks key raises StorageError."""
        storage = self._create_storage()
        # Write JSON without tasks key
        with open(self.filepath, "w") as f:
            f.write('{"other": "data"}')

        with self.assertRaises(StorageError) as context:
            storage.load_tasks()
        self.assertIn("Invalid file format", str(context.exception))

    def test_load_tasks_handles_tasks_not_array(self):
        """Test that loading JSON with non-array tasks raises StorageError."""
        storage = self._create_storage()
        # Write JSON with tasks as object
        with open(self.filepath, "w") as f:
            f.write('{"tasks": "not-an-array"}')

        with self.assertRaises(StorageError) as context:
            storage.load_tasks()
        self.assertIn("Invalid file format", str(context.exception))

    def test_save_tasks_creates_backup_before_write(self):
        """Test that backup is created before overwriting existing file."""
        storage = self._create_storage()
        tasks1 = [Task(id=1, title="Original", completed=False)]
        storage.save_tasks(tasks1)  # First save - no backup

        # Second save creates backup
        tasks2 = [Task(id=1, title="Updated", completed=True)]
        storage.save_tasks(tasks2)

        # Verify backup was created
        self.assertTrue(os.path.exists(f"{self.filepath}.bak"))

        # Verify backup contains original content
        backup_storage = JSONStorage(f"{self.filepath}.bak")
        backup_tasks = backup_storage.load_tasks()
        self.assertEqual(len(backup_tasks), 1)
        self.assertEqual(backup_tasks[0].title, "Original")
        self.assertFalse(backup_tasks[0].completed)

    def test_task_to_dict_includes_all_fields(self):
        """Test that task to dict conversion includes all fields."""
        storage = self._create_storage()
        task = Task(
            id=1,
            title="Test",
            description="Desc",
            completed=False,
            due_date="2025-01-01",
            priority=Priority.HIGH,
            tags=["Tag1", "Tag2"]
        )
        storage.save_tasks([task])
        loaded = storage.load_tasks()
        task_dict = storage._task_to_dict(task)

        self.assertIn("id", task_dict)
        self.assertIn("title", task_dict)
        self.assertIn("description", task_dict)
        self.assertIn("completed", task_dict)
        self.assertIn("due_date", task_dict)
        self.assertIn("priority", task_dict)
        self.assertIn("tags", task_dict)

    def test_dict_to_task_handles_all_fields(self):
        """Test that dict to task conversion handles all fields."""
        storage = self._create_storage()
        task_dict = {
            "id": 1,
            "title": "Test",
            "description": "Desc",
            "completed": False,
            "due_date": "2025-01-01",
            "priority": "High",
            "tags": ["Tag1", "Tag2"]
        }
        task = storage._dict_to_task(task_dict)

        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test")
        self.assertEqual(task.description, "Desc")
        self.assertFalse(task.completed)
        self.assertEqual(task.due_date, "2025-01-01")
        self.assertEqual(task.priority, Priority.HIGH)
        self.assertEqual(task.tags, ["Tag1", "Tag2"])

    def test_dict_to_task_handles_missing_optional_fields(self):
        """Test that dict to task conversion handles missing optional fields."""
        storage = self._create_storage()
        task_dict = {"id": 1, "title": "Test"}
        task = storage._dict_to_task(task_dict)

        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test")
        self.assertEqual(task.description, "")
        self.assertFalse(task.completed)
        self.assertIsNone(task.due_date)

    def test_dict_to_task_handles_none_values(self):
        """Test that dict to task conversion handles None values."""
        storage = self._create_storage()
        task_dict = {
            "id": 1,
            "title": "Test",
            "due_date": None
        }
        task = storage._dict_to_task(task_dict)

        self.assertEqual(task.title, "Test")
        self.assertEqual(task.description, "")
        self.assertIsNone(task.due_date)

    def test_dict_to_task_maps_priority_correctly(self):
        """Test that dict to task conversion maps priority strings to enums."""
        storage = self._create_storage()
        task_dict = {
            "id": 1,
            "title": "Test",
            "priority": "High"
        }
        task = storage._dict_to_task(task_dict)

        self.assertEqual(task.priority, Priority.HIGH)

        task_dict = {
            "id": 1,
            "title": "Test",
            "priority": "Medium"
        }
        task = storage._dict_to_task(task_dict)

        self.assertEqual(task.priority, Priority.MEDIUM)

        task_dict = {
            "id": 1,
            "title": "Test",
            "priority": "Low"
        }
        task = storage._dict_to_task(task_dict)

        self.assertEqual(task.priority, Priority.LOW)

    def test_dict_to_task_maps_tags_list_correctly(self):
        """Test that dict to task conversion handles tags as list."""
        storage = self._create_storage()
        task_dict = {
            "id": 1,
            "title": "Test",
            "tags": ["Work", "Home"]
        }
        task = storage._dict_to_task(task_dict)

        self.assertEqual(task.tags, ["Work", "Home"])

    def test_dict_to_task_handles_empty_tags(self):
        """Test that dict to task conversion handles empty tags array."""
        storage = self._create_storage()
        task_dict = {
            "id": 1,
            "title": "Test",
            "tags": []
        }
        task = storage._dict_to_task(task_dict)

        self.assertEqual(task.tags, [])

    def test_dict_to_task_handles_missing_tags(self):
        """Test that dict to task conversion handles missing tags field."""
        storage = self._create_storage()
        task_dict = {"id": 1, "title": "Test"}
        task = storage._dict_to_task(task_dict)

        self.assertEqual(task.tags, [])


if __name__ == "__main__":
    unittest.main()
