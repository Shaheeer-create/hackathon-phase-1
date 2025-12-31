# CLI Command Contract: Todo Application

**Date**: 2025-12-31
**Purpose**: Define CLI command interface contract for Todo application

## Overview

The Todo application exposes a command-line interface using argparse with subcommands. All commands follow standard CLI conventions with clear help text.

## Command Structure

### General Format
```bash
todo <command> [arguments] [options]
```

### Global Options

| Option | Alias | Type | Description |
|--------|--------|--------|-------------|
| --help | -h | flag | Display help for command or application |

### Commands

## Command: add

Add a new task to the task list.

**Syntax**:
```bash
todo add --title TITLE [--desc DESCRIPTION] [--due YYYY-MM-DD]
```

**Arguments**:

| Argument | Type | Required | Description | Validation |
|----------|--------|-----------|-------------|
| --title | string | Yes | Task title | Must not be empty or whitespace-only |
| --desc | string | No | Task description | Can be empty, accepts any characters |
| --due | string | No | Due date in YYYY-MM-DD format | Must match YYYY-MM-DD regex |

**Success Output**:
```
Task added: [1] Buy groceries
```

**Error Output**:
```
Error: Task title cannot be empty
Error: Invalid date format. Expected YYYY-MM-DD
```

**Examples**:
```bash
todo add --title "Buy groceries"
todo add --title "Meeting" --desc "Team standup at 10am" --due "2025-01-05"
todo add --title "Review code" --due "2025-01-10"
```

---

## Command: list

Display all tasks in the task list.

**Syntax**:
```bash
todo list
```

**Arguments**: None

**Success Output (with tasks)**:
```
Tasks (3 total):

[ ] 1: Buy groceries
    Due: 2025-01-05

[✓] 2: Complete Python project
    Due: 2025-01-10

[ ] 3: Call mom
```

**Success Output (empty)**:
```
No tasks found. Add a task with `todo add --title "your task"`
```

**Examples**:
```bash
todo list
```

---

## Command: complete

Toggle task completion status between pending and completed.

**Syntax**:
```bash
todo complete <task_id>
```

**Arguments**:

| Argument | Type | Required | Description | Validation |
|----------|--------|-----------|-------------|
| task_id | int | Yes | Sequential task ID | Must be valid task ID (exists in list) |

**Success Output (pending → completed)**:
```
Task 1 marked as completed: [✓] Buy groceries
```

**Success Output (completed → pending)**:
```
Task 1 marked as pending: [ ] Buy groceries
```

**Error Output**:
```
Error: Task with ID 10 not found
Error: Task ID must be a positive integer
```

**Examples**:
```bash
todo complete 1
todo complete 5
```

---

## Command: delete

Remove a task from the task list and re-index remaining tasks.

**Syntax**:
```bash
todo delete <task_id>
```

**Arguments**:

| Argument | Type | Required | Description | Validation |
|----------|--------|-----------|-------------|
| task_id | int | Yes | Sequential task ID | Must be valid task ID (exists in list) |

**Success Output**:
```
Task 3 deleted successfully
Remaining tasks: 4
```

**Error Output**:
```
Error: Task with ID 99 not found
Error: Task ID must be a positive integer
```

**Examples**:
```bash
todo delete 3
todo delete 1
```

---

## Command: update

Update task details (title, description, or due date).

**Syntax**:
```bash
todo update <task_id> [--title TITLE] [--desc DESCRIPTION] [--due YYYY-MM-DD]
```

**Arguments**:

| Argument | Type | Required | Description | Validation |
|----------|--------|-----------|-------------|
| task_id | int | Yes | Sequential task ID | Must be valid task ID (exists in list) |
| --title | string | No | New task title | Must not be empty or whitespace-only if provided |
| --desc | string | No | New task description | Can be empty or any characters |
| --due | string | No | New due date | Must match YYYY-MM-DD format if provided |

**Success Output**:
```
Task 1 updated: Buy almond milk
    Due: 2025-01-15
```

**Error Output**:
```
Error: Task with ID 5 not found
Error: Task title cannot be empty
Error: Invalid date format. Expected YYYY-MM-DD
```

**Examples**:
```bash
todo update 1 --title "Buy almond milk"
todo update 1 --desc "Unsweetened"
todo update 1 --due "2025-01-15"
todo update 1 --title "Meeting" --desc "Team standup" --due "2025-01-20"
```

---

## Command: help

Display help text for application or specific command.

**Syntax**:
```bash
todo help [command]
```

**Arguments**:

| Argument | Type | Required | Description |
|----------|--------|-----------|-------------|
| command | string | No | Command to show help for |

**Success Output (general)**:
```
Todo Application - Basic Task Management

Commands:
  add       Add a new task
  list       List all tasks
  complete   Toggle task completion
  delete     Delete a task
  update     Update task details
  help       Show help for commands

Use 'todo help <command>' for more information on a command.
```

**Success Output (specific)**:
```
add - Add a new task

Usage: todo add --title TITLE [--desc DESCRIPTION] [--due YYYY-MM-DD]

Options:
  --title TITLE  Task title (required)
  --desc TEXT    Task description (optional)
  --due DATE     Due date in YYYY-MM-DD format (optional)

Examples:
  todo add --title "Buy groceries"
  todo add --title "Meeting" --desc "Team standup" --due "2025-01-05"
```

**Examples**:
```bash
todo help
todo help add
todo help update
```

---

## Error Handling

### Error Response Format

All errors follow this format:
```
Error: <error message>
```

### Common Error Messages

| Error | Cause |
|--------|--------|
| Task with ID {n} not found | Task ID does not exist in task list |
| Task title cannot be empty | Title is empty or whitespace-only |
| Invalid date format. Expected YYYY-MM-DD | Due date does not match YYYY-MM-DD regex |
| Task ID must be a positive integer | Task ID is not a valid positive integer |
| Unrecognized command | Invalid subcommand provided |

### Exit Codes

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success |
| 1 | Error (validation, not found, etc.) |
| 2 | Invalid arguments/usage |

---

## Display Format

### Task Display Format

**Pending Task**:
```
[ ] {id}: {title}
    Description: {description}  (if provided)
    Due: {YYYY-MM-DD}  (if provided)
```

**Completed Task**:
```
[✓] {id}: {title}
    Description: {description}  (if provided)
    Due: {YYYY-MM-DD}  (if provided)
```

### Task List Header

```
Tasks ({count} total):

{task 1}
{task 2}
...
```

### Empty List Message

```
No tasks found. Add a task with `todo add --title "your task"`
```

---

## Input Validation

### Title Validation
- Must not be empty
- Must not be whitespace-only
- Accepts special characters (quotes, emojis, etc.)

### Description Validation
- Can be empty
- Accepts any characters including special characters
- No length limit (display truncated for readability)

### Due Date Validation
- Format: YYYY-MM-DD
- Regex: `^\d{4}-\d{2}-\d{2}$`
- Not validated as actual calendar date (format-only check)

### Task ID Validation
- Must be positive integer (>= 1)
- Must exist in current task list
