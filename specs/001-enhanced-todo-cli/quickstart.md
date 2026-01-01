# Quickstart: Enhanced Todo CLI

## Installation

```bash
# Clone repository
git clone <repo-url>
cd phase-1

# Run application
python -m src.cli.main
```

**Requirements**:
- Python 3.12 or higher
- No external dependencies needed (standard library only)

## Basic Usage

### Main Menu

```
==================================================
Todo Application - Enhanced Task Management
==================================================

Main Menu:
1. Add Task
2. List Tasks
3. Complete Task
4. Delete Task
5. Update Task
6. Search Tasks         [NEW]
7. Filter Tasks         [NEW]
8. Sort Tasks           [NEW]
9. Exit
==================================================

Enter choice (1-9):
```

### 1. Add Task

Create a new task with title, description, due date, priority, and tags.

```
Enter choice (1-9): 1

----------------------------------------
Add Task
----------------------------------------
Task title: Complete project documentation
Description (optional, press Enter to skip): Write detailed docs for each feature
Due date (YYYY-MM-DD, optional, press Enter to skip): 2025-01-05
Priority (High/Medium/Low) [Medium]: High
Tags (comma-separated, optional): Work, Documentation

Task added: [1] Complete project documentation
  Description: Write detailed docs for each feature
  Due: 2025-01-05
  Priority: High
  Tags: Work, Documentation
```

**Options**:
- **Title**: Required, cannot be empty
- **Description**: Optional, press Enter to skip
- **Due Date**: Optional, format YYYY-MM-DD
- **Priority**: High/Medium/Low (default: Medium)
- **Tags**: Comma-separated, optional (e.g., Work, Home, Study)

---

### 2. List Tasks

View all tasks in a formatted table.

```
Enter choice (1-9): 2

----------------------------------------
List Tasks
----------------------------------------

Tasks (3 total):

ID  | Status | Priority | Tags       | Title                          | Due Date
----+---------+-----------+------------+--------------------------------+------------
1   | [ ]     | High      | Work, Doc  | Complete project documentation    | 2025-01-05
2   | [✓]     | Medium    | Home       | Buy groceries                  | 2025-01-03
3   | [ ]     | Low       | Personal   | Read book                      | None
```

**Table Columns**:
- **ID**: Task number (for reference in other operations)
- **Status**: `[ ]` = Pending, `[✓]` = Completed
- **Priority**: High, Medium, or Low
- **Tags**: Comma-separated list (or blank if none)
- **Title**: Task name (truncated if too long)
- **Due Date**: YYYY-MM-DD format or "None"

---

### 3. Complete Task

Toggle task completion status between pending and completed.

```
Enter choice (1-9): 3

----------------------------------------
Complete Task
----------------------------------------

Current tasks:
  [ ] 1: Complete project documentation
  [✓] 2: Buy groceries
  [ ] 3: Read book

Enter task ID to toggle: 1

Task 1 marked as completed
  Complete project documentation
```

**Notes**:
- Shows current tasks with status indicators
- Enter task ID to toggle (pending → completed or completed → pending)
- Invalid IDs show error message

---

### 4. Delete Task

Permanently remove a task from the list.

```
Enter choice (1-9): 4

----------------------------------------
Delete Task
----------------------------------------

Current tasks:
  [ ] 1: Complete project documentation
  [✓] 2: Buy groceries
  [ ] 3: Read book

Enter task ID to delete: 2

Task 2 deleted successfully
Remaining tasks: 2
```

**Notes**:
- Shows current tasks with status indicators
- Deleting reindexes remaining tasks (IDs shift down)
- Cannot undo deletion

---

### 5. Update Task

Modify any attribute of an existing task.

```
Enter choice (1-9): 5

----------------------------------------
Update Task
----------------------------------------

Enter task ID to update: 1

Current task: Complete project documentation
  Description: Write detailed docs for each feature
  Due: 2025-01-05
  Priority: High
  Tags: Work, Documentation

Enter new values (press Enter to keep current):

Title [Complete project documentation]: Complete API documentation
Description [Write detailed docs for each feature]:
Due date [2025-01-05]: 2025-01-07
Priority [High]: Medium
Tags [Work, Documentation]: Work, API, Important

Task 1 updated: Complete API documentation
  Description: Write detailed docs for each feature
  Due: 2025-01-07
  Priority: Medium
  Tags: Work, API, Important
```

**Notes**:
- Shows current task details
- Press Enter to keep each field unchanged
- Enter "none" for due date to remove it
- New tags replace existing tags (not appended)
- Can update multiple fields at once

---

### 6. Search Tasks [NEW]

Find tasks by keyword in title or description.

```
Enter choice (1-9): 6

----------------------------------------
Search Tasks
----------------------------------------
Enter keyword: documentation

Found 2 tasks:

ID  | Status | Priority | Tags       | Title                          | Due Date
----+---------+-----------+------------+--------------------------------+------------
1   | [ ]     | Medium    | Work, API  | Complete API documentation       | 2025-01-07
4   | [✓]     | High      | Work, Doc  | Write user documentation        | 2025-01-02
```

**Notes**:
- Case-insensitive search
- Matches keyword in title OR description
- Empty keyword returns all tasks with hint
- Shows matching tasks in table format

---

### 7. Filter Tasks [NEW]

Narrow down task list by status, priority, and due date.

```
Enter choice (1-9): 7

----------------------------------------
Filter Tasks
----------------------------------------
Status filter (All/Completed/Pending) [All]: Pending
Priority filter (All/High/Medium/Low) [All]: High
Due date filter (All/Today/Upcoming/Overdue) [All]: Upcoming

Filtered tasks (3 total):

ID  | Status | Priority | Tags       | Title                    | Due Date
----+---------+-----------+------------+--------------------------+------------
1   | [ ]     | High      | Work       | Fix critical bug         | 2025-01-07
3   | [ ]     | High      | Urgent     | Complete feature X       | 2025-01-10
5   | [ ]     | High      | Work       | Prepare presentation    | 2025-01-15
```

**Filter Options**:

**Status**:
- `All`: Show both pending and completed tasks (default)
- `Completed`: Show only completed tasks
- `Pending`: Show only pending tasks

**Priority**:
- `All`: Show all priority levels (default)
- `High`: Show only High priority tasks
- `Medium`: Show only Medium priority tasks
- `Low`: Show only Low priority tasks

**Due Date**:
- `All`: Show all tasks, including those without due date (default)
- `Today`: Show tasks due today
- `Upcoming`: Show tasks due in the future
- `Overdue`: Show past-due tasks that are not completed

**Notes**:
- Press Enter to keep "All" for any filter
- All filters apply together (AND logic)
- Tasks without due date are excluded from date filters
- Empty results show message: "No tasks match the current filters"

---

### 8. Sort Tasks [NEW]

Change display order of tasks (temporary view, doesn't affect stored order).

```
Enter choice (1-9): 8

----------------------------------------
Sort Tasks
----------------------------------------
Sort by (1: Due Date, 2: Priority, 3: Alphabetical, 4: Default) [1]: 2

Tasks (5 total), sorted by Priority:

ID  | Status | Priority | Tags       | Title                    | Due Date
----+---------+-----------+------------+--------------------------+------------
1   | [ ]     | High      | Work       | Fix critical bug         | 2025-01-07
3   | [ ]     | High      | Urgent     | Complete feature X       | 2025-01-10
2   | [✓]     | Medium    | Home       | Buy groceries            | 2025-01-03
4   | [ ]     | Medium    | Personal   | Read book                | None
5   | [ ]     | Low       | Study      | Review notes             | 2025-01-20
```

**Sort Options**:

**1: Due Date**
- Tasks with due date shown first (earliest first)
- Tasks without due date shown last
- Good for planning what to work on soonest

**2: Priority** (shown above)
- High priority tasks first, then Medium, then Low
- Good for focusing on most urgent tasks

**3: Alphabetical**
- Tasks sorted by title (A-Z)
- Case-insensitive
- Good for finding specific tasks quickly

**4: Default**
- Tasks shown in stored order (no sorting)
- Good for returning to original view

**Notes**:
- Sorting is temporary (view-only)
- Stored order is preserved
- Use "4: Default" to exit sort view

---

### 9. Exit

Quit the application. All changes are automatically saved.

```
Enter choice (1-9): 9

Goodbye!
```

**Notes**:
- Tasks are saved automatically after each operation
- No manual save needed
- Application saves to `todo.json` in current directory

---

## Data Persistence

### File Storage

Tasks are automatically saved to `todo.json` after each operation.

**File Location**: Current working directory

**Backup**: Before overwriting, `todo.json.bak` is created

### First Run

If `todo.json` doesn't exist, it's created automatically when you add your first task.

### Data Recovery

If `todo.json` becomes corrupted, restore from backup:

```bash
# Restore from backup
mv todo.json.bak todo.json
```

Or manually edit the JSON file (it's human-readable):

```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Example task",
      "description": "",
      "completed": false,
      "due_date": "2025-01-05",
      "priority": "High",
      "tags": ["Work"]
    }
  ]
}
```

---

## Common Workflows

### Workflow 1: Daily Planning

```
1. Add new tasks for the day
2. Sort by Due Date to see schedule
3. Filter by Priority "High" to focus on urgent tasks
4. Mark tasks complete as you finish them
```

### Workflow 2: Task Organization

```
1. List all tasks to see current state
2. Add new task with appropriate priority and tags
3. Search by keyword to find related tasks
4. Update existing tasks to adjust priorities/tags
```

### Workflow 3: Review and Cleanup

```
1. Filter by "Completed" to see finished tasks
2. Delete completed tasks you no longer need
3. Filter by "Overdue" to see past-due pending tasks
4. Update priorities/tags for overdue tasks
```

### Workflow 4: Category Focus

```
1. Search by keyword (e.g., "Work") to see work tasks
2. Sort by Priority to tackle most urgent work tasks
3. Mark tasks complete as you finish
4. Repeat for other categories (e.g., "Home", "Study")
```

---

## Error Messages

### Invalid Input

```
Task title:     (empty)
Task title cannot be empty.
```

### Invalid Date Format

```
Due date (YYYY-MM-DD, optional): 01/05/2025
Invalid date format. Expected YYYY-MM-DD
```

### Invalid Priority

```
Priority (High/Medium/Low) [Medium]: Critical
Invalid priority: "Critical". Valid options: High, Medium, Low
```

### Task Not Found

```
Enter task ID to delete: 10
Error: Task with ID 10 not found
```

### Storage Error

```
Error: Cannot write file: Permission denied
```

---

## Tips and Best Practices

1. **Use Descriptive Titles**: Clear titles help with search
2. **Set Priorities**: Helps focus on what matters most
3. **Use Tags**: Organize by category (Work, Home, Study)
4. **Set Due Dates**: Filter by today/upcoming/overdue
5. **Search Before Adding**: Avoid duplicate tasks
6. **Review Regularly**: Filter by "Overdue" to catch past-due tasks
7. **Sort Contextually**: Use different sort views for different purposes
8. **Backup Regularly**: `todo.json.bak` contains previous version

---

## Keyboard Shortcuts

Not applicable (this is a menu-driven CLI, not a TUI)

---

## Troubleshooting

### Issue: Tasks not saving

**Solution**: Check write permissions in current directory

### Issue: "Corrupted data file" error

**Solution**: Restore from `todo.json.bak` backup

### Issue: Table formatting looks broken

**Solution**: Ensure terminal width is at least 80 columns

### Issue: Special characters not displaying correctly

**Solution**: Check terminal encoding (should be UTF-8)

---

## Advanced Features

### Complex Filtering

Combine multiple filters for precise results:

```
Status filter: Pending
Priority filter: High
Due date filter: Overdue
```

Result: Past-due, pending, High priority tasks only

### Multi-Tag Organization

Use multiple tags to categorize tasks:

```
Tags: Work, Urgent, Project-X
```

Then search for "Work" or "Project-X" to find related tasks.

### Priority Evolution

Update task priorities as circumstances change:

```
1. Add task with Medium priority
2. Later: Update task priority to High if urgent
3. Or: Update task priority to Low if no longer important
```

---

## Getting Help

For more information:

1. **Review specification**: `specs/001-enhanced-todo-cli/spec.md`
2. **Check contracts**: `specs/001-enhanced-todo-cli/contracts/`
3. **View source code**: `src/cli/main.py`, `src/services/task_manager.py`

---

**Last Updated**: 2025-12-31
**Application Version**: Enhanced CLI Todo v1.0
