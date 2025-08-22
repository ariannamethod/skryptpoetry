import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import skryptloger  # noqa: E402
from skryptrainer import SkryptTrainer  # noqa: E402


def _trainer(tmp_path, monkeypatch, **kwargs):
    monkeypatch.setattr(skryptloger, "DB_PATH", tmp_path / "db.sqlite3")
    return SkryptTrainer(datasets=[tmp_path], **kwargs)


def test_concurrent_scan_and_train(tmp_path, monkeypatch):
    trainer = _trainer(tmp_path, monkeypatch)
    (tmp_path / "file.txt").write_text("data")

    calls = []

    def fake_train(path):
        time.sleep(0.01)
        calls.append(path)

    monkeypatch.setattr(trainer, "_train_file", fake_train)

    threads = [
        threading.Thread(target=trainer.scan_and_train)
        for _ in range(5)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert calls == [tmp_path / "file.txt"]


def test_custom_filters(tmp_path, monkeypatch):
    trainer = _trainer(
        tmp_path,
        monkeypatch,
        allowed_extensions={".xyz"},
        excluded_parts={"skip"},
    )

    (tmp_path / "good.xyz").write_text("data")
    (tmp_path / "bad.txt").write_text("data")
    (tmp_path / "skip").mkdir()
    (tmp_path / "skip" / "also.xyz").write_text("data")

    calls = []

    def fake_train(path):
        calls.append(path)

    monkeypatch.setattr(trainer, "_train_file", fake_train)

    trainer.scan_and_train()

    assert calls == [tmp_path / "good.xyz"]


def test_scan_and_train_with_train_on_text(tmp_path, monkeypatch):
    trainer = _trainer(tmp_path, monkeypatch)
    (tmp_path / "file.txt").write_text("data")

    calls = []

    def fake_train(path):
        time.sleep(0.01)
        calls.append(path)

    monkeypatch.setattr(trainer, "_train_file", fake_train)

    def train_on_text():
        trainer.train_on_text("extra")

    threads = [
        threading.Thread(target=trainer.scan_and_train),
        threading.Thread(target=train_on_text),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert calls == [tmp_path / "file.txt"]
