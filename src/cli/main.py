"""Todo CLI - Interactive menu-based application for Windows Console."""

import sys
import os

# Support running as a module (preferred) or as a script.
# When executed as a script, relative imports fail because there's no
# parent package; in that case add the package root (`src`) to `sys.path`
# and import sibling packages directly.
try:
    from ..services.task_manager import TaskManager
    from ..exceptions import TaskNotFoundError, InvalidTaskError
except (ImportError, ValueError):
    # When running as script, we're in the project root
    # Add src/ to sys.path and use absolute imports
    import sys
    script_dir = os.path.dirname(os.path.abspath(__file__))
    src_root = os.path.join(script_dir, "..")
    if src_root not in sys.path:
        sys.path.insert(0, src_root)
    from services.task_manager import TaskManager
    from exceptions import TaskNotFoundError, InvalidTaskError


def show_menu() -> None:
    """Display the main menu."""
    print("\n" + "=" * 50)
    print("Todo Application - Basic Task Management")
    print("=" * 50)
    print()
    print("Main Menu:")
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Update Task")
    print("6. Exit")
    print("=" * 50)
    print()


def get_menu_choice() -> str:
    """Get menu choice from user input.

    Returns:
        User's menu choice as string (1-6)
    """
    while True:
        choice = input("Enter choice (1-6): ").strip()
        if choice in ["1", "2", "3", "4", "5", "6"]:
            return choice
        print("Invalid choice. Please enter a number between 1 and 6.")


def add_task_interactive(manager: TaskManager) -> None:
    """Handle adding a task interactively.

    Args:
        manager: TaskManager instance
    """
    print("\n" + "-" * 40)
    print("Add Task")
    print("-" * 40)

    # Get title
    while True:
        title = input("Task title: ").strip()
        if title:
            break
        print("Task title cannot be empty.")

    # Get description (optional)
    description = input("Description (optional, press Enter to skip): ").strip()

    # Get due date (optional)
    due_date = None
    date_input = input("Due date (YYYY-MM-DD, optional, press Enter to skip): ").strip()
    if date_input:
        due_date = date_input

    try:
        task = manager.add_task(title=title, description=description, due_date=due_date)
        print(f"\nTask added: [{task.id}] {task.title}")
        if task.description:
            print(f"  Description: {task.description}")
        if task.due_date:
            print(f"  Due: {task.due_date}")
    except ValueError as e:
        print(f"\nError: {str(e)}")


def list_tasks_interactive(manager: TaskManager) -> None:
    """Handle listing tasks interactively.

    Args:
        manager: TaskManager instance
    """
    print("\n" + "-" * 40)
    print("List Tasks")
    print("-" * 40)

    tasks = manager.list_tasks()

    if not tasks:
        print("\nNo tasks found. Add a task from the main menu.")
        return

    print(f"\nTasks ({len(tasks)} total):")
    print()

    for task in tasks:
        # Status indicator
        status = "[✓]" if task.completed else "[ ]"

        # Title line
        print(f"{status} {task.id}: {task.title}")

        # Description (if present)
        if task.description:
            print(f"    Description: {task.description}")

        # Due date (if present)
        if task.due_date:
            print(f"    Due: {task.due_date}")

        print()


def complete_task_interactive(manager: TaskManager) -> None:
    """Handle completing a task interactively.

    Args:
        manager: TaskManager instance
    """
    print("\n" + "-" * 40)
    print("Complete Task")
    print("-" * 40)

    tasks = manager.list_tasks()

    if not tasks:
        print("\nNo tasks found. Add a task from the main menu.")
        return

    # Show tasks first
    print("\nCurrent tasks:")
    for task in tasks:
        status = "[✓]" if task.completed else "[ ]"
        print(f"  {status} {task.id}: {task.title}")
    print()

    # Get task ID
    while True:
        task_id_input = input("Enter task ID to toggle: ").strip()
        if not task_id_input:
            print("Task ID cannot be empty.")
            continue

        try:
            task_id = int(task_id_input)
            updated_task = manager.toggle_complete(task_id=task_id)
            status = "completed" if updated_task.completed else "pending"
            print(f"\nTask {task_id} marked as {status}")
            print(f"  {updated_task.title}")
            break
        except ValueError:
            print("Please enter a valid number.")
        except TaskNotFoundError as e:
            print(f"\nError: {str(e)}")


def delete_task_interactive(manager: TaskManager) -> None:
    """Handle deleting a task interactively.

    Args:
        manager: TaskManager instance
    """
    print("\n" + "-" * 40)
    print("Delete Task")
    print("-" * 40)

    tasks = manager.list_tasks()

    if not tasks:
        print("\nNo tasks found. Add a task from the main menu.")
        return

    # Show tasks first
    print("\nCurrent tasks:")
    for task in tasks:
        status = "[✓]" if task.completed else "[ ]"
        print(f"  {status} {task.id}: {task.title}")
    print()

    # Get task ID
    while True:
        task_id_input = input("Enter task ID to delete: ").strip()
        if not task_id_input:
            print("Task ID cannot be empty.")
            continue

        try:
            task_id = int(task_id_input)
            manager.delete_task(task_id=task_id)
            tasks = manager.list_tasks()
            print(f"\nTask {task_id} deleted successfully")
            print(f"Remaining tasks: {len(tasks)}")
            break
        except ValueError:
            print("Please enter a valid number.")
        except TaskNotFoundError as e:
            print(f"\nError: {str(e)}")


def update_task_interactive(manager: TaskManager) -> None:
    """Handle updating a task interactively.

    Args:
        manager: TaskManager instance
    """
    print("\n" + "-" * 40)
    print("Update Task")
    print("-" * 40)

    tasks = manager.list_tasks()

    if not tasks:
        print("\nNo tasks found. Add a task from the main menu.")
        return

    # Get task ID first
    while True:
        task_id_input = input("Enter task ID to update: ").strip()
        if not task_id_input:
            print("Task ID cannot be empty.")
            continue

        try:
            task_id = int(task_id_input)
            # Show current task details
            current_task = manager.get_task(task_id=task_id)
            print(f"\nCurrent task: {current_task.title}")
            if current_task.description:
                print(f"  Description: {current_task.description}")
            if current_task.due_date:
                print(f"  Due: {current_task.due_date}")
            print()

            # Get new values (all optional)
            print("Enter new values (press Enter to keep current):")

            new_title = input(f"Title [{current_task.title}]: ").strip()
            new_desc = input(f"Description [{current_task.description}]: ").strip()
            new_due = input(f"Due date [{current_task.due_date or 'none'}]: ").strip()
            if new_due.lower() == "none" or new_due == "":
                new_due = None

            # Build kwargs
            kwargs = {}
            if new_title:
                kwargs["title"] = new_title
            if new_desc:
                kwargs["description"] = new_desc
            if new_due:
                kwargs["due_date"] = new_due

            if not kwargs:
                print("\nNo changes provided. Task not updated.")
                return

            updated_task = manager.update_task(task_id=task_id, **kwargs)
            print(f"\nTask {task_id} updated: {updated_task.title}")
            if updated_task.description:
                print(f"  Description: {updated_task.description}")
            if updated_task.due_date:
                print(f"  Due: {updated_task.due_date}")
            break
        except ValueError:
            print("Please enter a valid number.")
        except TaskNotFoundError as e:
            print(f"\nError: {str(e)}")
        except ValueError as e:
            print(f"\nError: {str(e)}")


def main() -> int:
    """Main entry point for Todo CLI application with interactive menu."""
    # Global TaskManager instance
    manager = TaskManager()

    while True:
        # Show menu
        show_menu()

        # Get choice
        choice = get_menu_choice()

        # Execute action
        if choice == "1":
            add_task_interactive(manager)
        elif choice == "2":
            list_tasks_interactive(manager)
        elif choice == "3":
            complete_task_interactive(manager)
        elif choice == "4":
            delete_task_interactive(manager)
        elif choice == "5":
            update_task_interactive(manager)
        elif choice == "6":
            print("\nGoodbye!")
            return 0

        # Prompt to continue
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    sys.exit(main())
