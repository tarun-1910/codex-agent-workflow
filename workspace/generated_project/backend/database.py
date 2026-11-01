import os
import sqlite3
from pathlib import Path
from typing import Any

_DEFAULT_DATABASE = Path(__file__).resolve().parent / "taskflow.db"
DATABASE_PATH = Path(os.environ.get("TASKFLOW_DATABASE_PATH", str(_DEFAULT_DATABASE)))


def get_connection() -> sqlite3.Connection:
    """Open a SQLite connection configured to return rows by column name."""
    connection = sqlite3.connect(DATABASE_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    """Create the database directory and tasks table when needed."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'todo',
                priority TEXT NOT NULL DEFAULT 'medium',
                due_date TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        connection.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)")


def _to_task(row: sqlite3.Row | None) -> dict[str, Any] | None:
    if row is None:
        return None
    task = dict(row)
    if task.get("due_date") is not None:
        task["due_date"] = task["due_date"]
    return task


def create_task(
    *, title: str, description: str, task_status: str, priority: str,
    due_date: str | None, created_at: str, updated_at: str
) -> dict[str, Any]:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO tasks (title, description, status, priority, due_date, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (title, description, task_status, priority, due_date, created_at, updated_at),
        )
        row = connection.execute("SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,)).fetchone()
        result = _to_task(row)
        if result is None:
            raise RuntimeError("Created task could not be retrieved")
        return result


def list_tasks() -> list[dict[str, Any]]:
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM tasks ORDER BY created_at DESC, id DESC"
        ).fetchall()
    return [_to_task(row) for row in rows if row is not None]


def get_task(task_id: int) -> dict[str, Any] | None:
    with get_connection() as connection:
        row = connection.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return _to_task(row)


def update_task(
    *, task_id: int, title: str, description: str, task_status: str,
    priority: str, due_date: str | None, updated_at: str
) -> dict[str, Any] | None:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE tasks
            SET title = ?, description = ?, status = ?, priority = ?, due_date = ?, updated_at = ?
            WHERE id = ?
            """,
            (title, description, task_status, priority, due_date, updated_at, task_id),
        )
        if cursor.rowcount == 0:
            return None
        row = connection.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return _to_task(row)


def delete_task(task_id: int) -> bool:
    with get_connection() as connection:
        cursor = connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    return cursor.rowcount > 0
