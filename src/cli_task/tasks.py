from .db import get_db, init_db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def create_task(title, description=None, due_date=None, priority=None):
	"""
	Insert a new task into the database.

    Args:
        title (str): Task title (required, non-empty).
        description (str): Optional description.
        due_date (str): Optional due date in YYYY-MM-DD.
        priority (int): Optional priority level.

    Returns:
        int: ID of the newly created task.

    Raises:
        ValueError: If title is empty.
        sqlite3.Error: If insertion fails.
    """
	if not title.strip():
		logger.error("Attempted to create task with empty title")
		raise ValueError("Title cannot be empty.")
	conn = get_db()
	cur = conn.cursor()
	cur.execute("""
		INSERT INTO tasks (title, description, due_date, priority)
		VALUES (?, ?, ?, ?)
	""", (title, description, due_date, priority))
	task_id = cur.lastrowid
	conn.commit()
	conn.close()
	logger.info(f"Created task {task_id}: {title}")
	return task_id

def get_task(task_id):
	"""
    Retrieve a single task by ID.

    Args:
        task_id (int): ID of the task.

    Returns:
        tuple or None: The task row or None if not found.
    """
	conn = get_db()
	cur = conn.cursor()
	cur.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
	task = cur.fetchone()
	conn.close()
	logger.info(f"Retrieved task {task_id}: {task}")
	return task

def list_tasks():
	"""
    Fetch all tasks ordered by creation time.

    Returns:
        list of tuples: [(id, title, due_date, priority, status), ...]
    """
	conn = get_db()
	cur = conn.cursor()
	cur.execute("""
		SELECT id, title, due_date, priority, status
		FROM tasks
		ORDER BY created_at ASC
		""")
	rows = cur.fetchall()
	conn.close()
	logger.info(f"Fetched {len(rows)} tasks")
	return rows

def update_task(task_id, **fields):
	"""
    Update fields of an existing task.

    Args:
        task_id (int): ID of the task to update.
        **fields: Key/value pairs of columns to update.

    Raises:
        ValueError: If no fields provided or task does not exist.
        sqlite3.Error: If update fails.
    """
	if not fields:
		logger.error("No fields provided for update")
		raise ValueError("No fields to update.")
	columns = ", ".join(f"{k}=?" for k in fields)
	values = list(fields.values()) + [task_id]
	sql = f"UPDATE tasks SET {columns}, updated_at=CURRENT_TIMESTAMP WHERE id=?"
	conn = get_db()
	cur = conn.cursor()
	cur.execute(sql, values)
	if cur.rowcount == 0:
		raise ValueError(f"No task with id {task_id}.")
	conn.commit()
	conn.close()
	logger.info(f"Updated task {task_id} with {fields}")

def delete_task(task_id):
	"""
    Delete a task by ID.

    Args:
        task_id (int): ID of the task to delete.

    Raises:
        ValueError: If task does not exist.
        sqlite3.Error: If deletion fails.
    """
	conn = get_db()
	cur = conn.cursor()
	cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
	if cur.rowcount == 0:
		logger.error(f"No task found with id {task_id} for deletion")
		raise ValueError(f"No task with id {task_id}.")
	conn.commit()
	conn.close()
	logger.info(f"Deleted task {task_id}")