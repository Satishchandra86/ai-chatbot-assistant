
import os
import sqlite3
from pathlib import Path

DB_PATH = (
    Path("/tmp/chat_history.db")
    if os.getenv("VERCEL")
    else Path(__file__).with_name("chat_history.db")
)


def connect():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with connect() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL
                    CHECK(role IN ('user', 'assistant')),
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
                    DEFAULT (datetime('now', 'localtime'))
            )
        """)


def save_message(role, content):
    with connect() as connection:
        connection.execute(
            """
            INSERT INTO messages (role, content)
            VALUES (?, ?)
            """,
            (role, content)
        )


def get_history(limit=100):
    with connect() as connection:
        rows = connection.execute(
            """
            SELECT role, content, created_at
            FROM messages
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        ).fetchall()

    return [dict(row) for row in reversed(rows)]


def clear_history():
    with connect() as connection:
        connection.execute("DELETE FROM messages")
