# Quickstart Guide: Todo CLI Application

**Version**: 1.0.0
**Last Updated**: 2025-12-31

## Overview

Todo CLI is a Python 3.12+ command-line application for managing tasks with in-memory storage. Supports add, list, update, delete, and complete operations with sequential task IDs.

## Prerequisites

- Python 3.12 or higher
- Standard library only (no external dependencies)
- Basic familiarity with command-line interfaces

## Installation

```bash
# Clone repository
git clone <repository-url>
cd <repository-directory>

# Verify Python version
python --version  # Should be 3.12+

# No pip install required - standard library only
```

## Quick Start

### Add Your First Task

```bash
# Basic task
python -m src.cli.main add --title "Buy groceries"

# Task with description
python -m src.cli.main add --title "Meeting" --desc "Team standup at 10am"

# Task with due date
python -m src.cli.main add --title "Review code" --due "2025-01-10"

# Complete task
python -m src.cli.main add --title "Complete project" --desc "Finish MVP" --due "2025-01-15"
```

### View All Tasks

```bash
# List all tasks
python -m src.cli.main list

# Output example:
# Tasks (3 total):
#
# [ ] 1: Buy groceries
#     Due: 2025-01-05
#
# [✓] 2: Complete Python project
#     Due: 2025-01-10
#
# [ ] 3: Call mom
```

### Complete a Task

```bash
# Mark task 1 as completed
python -m src.cli.main complete 1

# Toggle task back to pending
python -m src.cli.main complete 1
```

### Update a Task

```bash
# Update title
python -m src.cli.main update 1 --title "Buy almond milk"

# Add description
python -m src.cli.main update 1 --desc "Unsweetened, vanilla"

# Change due date
python -m src.cli.main update 1 --due "2025-01-15"

# Update multiple fields
python -m src.cli.main update 1 --title "Buy groceries" --desc "Weekly shopping" --due "2025-01-20"
```

### Delete a Task

```bash
# Delete task 3
python -m src.cli.main delete 3
```

### Get Help

```bash
# General help
python -m src.cli.main help

# Help for specific command
python -m src.cli.main help add
python -m src.cli.main help update
python -m src.cli.main help list
```

## Common Workflows

### Daily Task Management

```bash
# Morning: Add today's tasks
python -m src.cli.main add --title "Review emails"
python -m src.cli.main add --title "Team standup" --due "2025-01-05"
python -m src.cli.main add --title "Code review" --due "2025-01-05"

# Mid-day: Check progress
python -m src.cli.main list

# Afternoon: Complete finished tasks
python -m src.cli.main complete 1
python -m src.cli.main complete 2

# Evening: Review and update
python -m src.cli.main list
python -m src.cli.main update 3 --desc "Review PR #123"
python -m src.cli.main complete 3
```

### Batch Task Entry

```bash
# Add multiple tasks at once
python -m src.cli.main add --title "Task 1" --desc "Description 1"
python -m src.cli.main add --title "Task 2" --desc "Description 2"
python -m src.cli.main add --title "Task 3" --desc "Description 3"

# View all
python -m src.cli.main list
```

### Task Cleanup

```bash
# View all tasks
python -m src.cli.main list

# Delete completed or unwanted tasks
python -m src.cli.main delete 2
python -m src.cli.main delete 5

# View updated list (IDs re-indexed)
python -m src.cli.main list
```

## Testing

```bash
# Run all tests
python -m unittest discover tests

# Run specific test suite
python -m unittest tests.unit.test_task_model
python -m unittest tests.integration.test_cli_workflows
python -m unittest tests.contract.test_task_operations

# Run with verbose output
python -m unittest discover -v tests

# Check coverage (if coverage.py is installed)
coverage run -m unittest discover tests
coverage report
coverage html
```

## Data Persistence

**Important**: This application uses in-memory storage. All tasks are lost when the application exits.

```bash
# Tasks persist only during application session
python -m src.cli.main add --title "Session task"
python -m src.cli.main list

# Restart: tasks are gone
python -m src.cli.main list
# Output: No tasks found. Add a task with `todo add --title "your task"`
```

This is intentional design for the MVP. Future versions (Intermediate level) will add file persistence.

## Troubleshooting

### Task ID Not Found

```bash
# Error: Task with ID 10 not found
# Solution: Run `python -m src.cli.main list` to see valid task IDs
```

### Invalid Date Format

```bash
# Error: Invalid date format. Expected YYYY-MM-DD
# Solution: Use YYYY-MM-DD format (e.g., 2025-01-05)
python -m src.cli.main add --title "Meeting" --due "2025-01-05"
```

### Empty Task Title

```bash
# Error: Task title cannot be empty
# Solution: Provide a non-empty title
python -m src.cli.main add --title "Valid task title"
```

### Python Version Too Old

```bash
# Error: Python version < 3.12 required
# Solution: Upgrade Python
# Visit https://www.python.org/downloads/
```

## Architecture Overview

```
src/
├── models/
│   └── task.py              # Task dataclass (immutable)
├── services/
│   └── task_manager.py       # TaskList and CRUD operations
└── cli/
    └── main.py               # CLI entry point with argparse

tests/
├── contract/
│   └── test_task_operations.py  # Contract tests
├── integration/
│   └── test_cli_workflows.py     # End-to-end tests
└── unit/
    ├── test_task_model.py         # Task model tests
    └── test_task_manager.py      # TaskList service tests
```

## Next Steps

1. **Explore**: Try all commands with `python -m src.cli.main help`
2. **Manage tasks**: Add your daily tasks and practice CRUD operations
3. **Run tests**: Execute `python -m unittest discover tests` to verify functionality
4. **Extend**: Consider adding features from spec (priorities, tags, search - Intermediate level)

## Limitations

- In-memory storage only (no persistence across sessions)
- Single-user application (no multi-user support)
- Basic CRUD operations (no priorities, tags, search/filter - coming in Intermediate level)
- No notifications or reminders (coming in Advanced level)
- Maximum 100+ tasks supported (performance degrades beyond this)

## Support

For issues, questions, or feature requests:
- Review [spec.md](spec.md) for detailed requirements
- Check [research.md](research.md) for architectural decisions
- Consult [data-model.md](data-model.md) for entity definitions
