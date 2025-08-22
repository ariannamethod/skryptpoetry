import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().with_name('skrypt.sqlite3')


def init_db() -> None:
    """Initialize the sqlite database with required tables."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT,
                script TEXT,
                entropy REAL,
                perplexity REAL,
                resonance REAL,
                timestamp TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS used_scripts (
                script TEXT PRIMARY KEY
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS trained_files (
                path TEXT PRIMARY KEY,
                sha256 TEXT
            )
            """
        )


def log_interaction(
    message: str,
    script: str,
    entropy: float,
    perplexity: float,
    resonance: float,
) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO logs(
                message,
                script,
                entropy,
                perplexity,
                resonance,
                timestamp
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                message,
                script,
                entropy,
                perplexity,
                resonance,
                datetime.utcnow().isoformat(),
            ),
        )
        conn.execute(
            """
            INSERT OR IGNORE INTO used_scripts(script) VALUES (?)
            """,
            (script,),
        )


def script_used(script: str) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute(
            """
            SELECT 1 FROM used_scripts WHERE script=?
            """,
            (script,),
        ).fetchone()
    return result is not None


def log_trained_file(path: Path, sha256: str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO trained_files(path, sha256)
            VALUES (?, ?)
            """,
            (str(path), sha256),
        )


def was_trained(path: Path, sha256: str) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute(
            """
            SELECT 1 FROM trained_files WHERE path=? AND sha256=?
            """,
            (str(path), sha256),
        ).fetchone()
    return result is not None
