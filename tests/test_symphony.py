import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import skryptloger  # noqa: E402
from symphony import Symphony, retrieve  # noqa: E402


def test_retrieve_picks_highest_resonance():
    docs = [
        "alpha beta gamma",
        "alpha beta",
        "beta gamma",
    ]
    assert retrieve("alpha beta", docs) == "alpha beta"


def test_respond_selects_script_and_logs(tmp_path, monkeypatch):
    dataset = tmp_path / "data.md"
    dataset.write_text("hello world dataset")
    scripts = tmp_path / "scripts.md"
    scripts.write_text("hello script\nother line\n")

    monkeypatch.setattr(skryptloger, "DB_PATH", tmp_path / "db.sqlite3")

    class DummyTrainer:
        def train_async(self):
            pass

        def scan_and_train(self):
            pass

        def train_on_text_async(self, text):
            pass

    monkeypatch.setattr(
        sys.modules["symphony"],
        "SkryptTrainer",
        lambda *a, **k: DummyTrainer(),
    )

    bot = Symphony(
        dataset_path=str(dataset),
        scripts_path=str(scripts),
    )

    message = "hello world"
    script = bot.respond(message)
    assert script == "hello script"

    with sqlite3.connect(skryptloger.DB_PATH) as conn:
        rows = conn.execute(
            "SELECT message, script FROM logs"
        ).fetchall()
    assert rows == [(message, script)]
