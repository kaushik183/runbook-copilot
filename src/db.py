"""
SQLite audit log (data/audit.db).

This is NOT the conversation memory. Memory lives in data/langgraph_memory.sqlite and
is managed by LangGraph (see src/self_rag.py). This file is a plain log of every
question/answer, so you can review what the copilot said later via GET /api/audits.

SQLite basics used here:
  * A database is a single file. sqlite3.connect(path) opens it (creating it if missing).
  * `with sqlite3.connect(...) as conn:` wraps the block in a transaction; commit() saves it.
  * `?` placeholders pass values safely (never build SQL with f-strings -> SQL injection).
"""

import json
import sqlite3
from datetime import datetime, timezone
from src.config import get_settings


# Called once at startup (app.py). CREATE TABLE IF NOT EXISTS is safe to run repeatedly.
def init_db() -> None:
    path = get_settings().database_file
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS rag_audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            route TEXT,
            used_web INTEGER DEFAULT 0,
            support_status TEXT,
            usefulness TEXT,
            trace_json TEXT,
            sources_json TEXT
        )
        """)
        conn.commit()


# Insert one row per chat answer. Lists (trace, sources) are stored as JSON text,
# because SQLite has no list column type.
def save_audit(question: str, result: dict) -> None:
    path = get_settings().database_file
    with sqlite3.connect(path) as conn:
        conn.execute(
            """INSERT INTO rag_audit
            (created_at, question, answer, route, used_web, support_status, usefulness, trace_json, sources_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                datetime.now(timezone.utc).isoformat(),
                question,
                result.get("answer", ""),
                result.get("route", ""),
                int(bool(result.get("used_web_search"))),  # SQLite stores booleans as 0/1
                result.get("support_status", ""),
                result.get("usefulness", ""),
                json.dumps(result.get("trace", []), ensure_ascii=False),
                json.dumps(result.get("sources", []), ensure_ascii=False),
            ),
        )
        conn.commit()


# Newest rows first. row_factory=sqlite3.Row lets us turn each row into a dict,
# which FastAPI can return as JSON directly.
def latest_audits(limit: int = 25):
    path = get_settings().database_file
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM rag_audit ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]
