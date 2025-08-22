import sys
import sqlite3
from pathlib import Path

import pytest

# Ensure root project directory is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import skryptloger  # noqa: E402


@pytest.fixture
def temp_db(monkeypatch, tmp_path):
    """Provide a temporary database for tests."""
    db_path = tmp_path / "test.sqlite3"
    monkeypatch.setattr(skryptloger, "DB_PATH", db_path)
    skryptloger.init_db()
    return db_path


def test_log_interaction_and_script_used(temp_db):
    skryptloger.log_interaction("hello", "script.py", 0.1, 0.2, 0.3)
    with sqlite3.connect(temp_db) as conn:
        row = conn.execute("SELECT message, script FROM logs").fetchone()
    assert row == ("hello", "script.py")
    assert skryptloger.script_used("script.py")
    assert not skryptloger.script_used("other.py")


def test_log_trained_file_and_was_trained(temp_db, tmp_path):
    file_path = tmp_path / "model.txt"
    sha256 = "abc123"
    skryptloger.log_trained_file(file_path, sha256)
    assert skryptloger.was_trained(file_path, sha256)
    assert not skryptloger.was_trained(file_path, "wrong")
