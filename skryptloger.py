import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().with_name('skrypt.sqlite3')

def init_db() -> None:
    """Initialize the sqlite database with required tables."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
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
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS used_scripts (
            script TEXT PRIMARY KEY
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS trained_files (
            path TEXT PRIMARY KEY,
            sha256 TEXT
        )
        """
    )
    conn.commit()
    conn.close()

def log_interaction(message: str, script: str, entropy: float, perplexity: float, resonance: float) -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO logs(message, script, entropy, perplexity, resonance, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
        (message, script, entropy, perplexity, resonance, datetime.utcnow().isoformat()),
    )
    cur.execute("INSERT OR IGNORE INTO used_scripts(script) VALUES (?)", (script,))
    conn.commit()
    conn.close()

def script_used(script: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM used_scripts WHERE script=?", (script,))
    result = cur.fetchone()
    conn.close()
    return result is not None

def log_trained_file(path: Path, sha256: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO trained_files(path, sha256) VALUES (?, ?)",
        (str(path), sha256),
    )
    conn.commit()
    conn.close()

def was_trained(path: Path, sha256: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM trained_files WHERE path=? AND sha256=?",
        (str(path), sha256),
    )
    result = cur.fetchone()
    conn.close()
    return result is not None
