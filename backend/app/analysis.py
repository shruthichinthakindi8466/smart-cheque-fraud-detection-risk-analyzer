import json
import os
import sqlite3
from typing import Any, Dict, List

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "analysis_results.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS analysis_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            payload TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def save_result(payload: Dict[str, Any]) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT INTO analysis_results (created_at, payload) VALUES (datetime('now'), ?)",
        (json.dumps(payload),),
    )
    conn.commit()
    conn.close()


def fetch_recent_results(limit: int = 10) -> List[Dict[str, Any]]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT payload FROM analysis_results ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return [json.loads(row["payload"]) for row in rows]
