import sqlite3
import sys
from concurrent.futures import ThreadPoolExecutor
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


def test_load_file_thread_safety(tmp_path):
    from symphony import _CACHE, _load_file

    _CACHE.clear()
    path = tmp_path / "file.txt"
    path.write_text("a")

    def call_load():
        return _load_file(path)

    with ThreadPoolExecutor(max_workers=8) as exe:
        results = list(exe.map(lambda _: call_load(), range(100)))
    assert all(r == "a" for r in results)
    assert _CACHE[path][1] == "a"
    assert len(_CACHE) == 1

    path.write_text("b")
    with ThreadPoolExecutor(max_workers=8) as exe:
        results = list(exe.map(lambda _: call_load(), range(100)))
    assert all(r == "b" for r in results)
    assert _CACHE[path][1] == "b"
    assert len(_CACHE) == 1
